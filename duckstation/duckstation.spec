Name:           duckstation
Version:        0.1.9226
Release:        8%{?dist}
Summary:        Fast PlayStation 1 emulator

License:        CC-BY-NC-ND-4.0
URL:            https://github.com/stenzek/duckstation

# pinned Discord-RPC commit for reproducible builds
%global discord_rpc_ver   cc59d26d1d628fbd6527aac0ac1d6301f4978b92
%global discord_rpc_file  %{discord_rpc_ver}.tar.gz

# real upstream tag (contains a dash)
%global upstream_tag      0.1-9226

Source0:        https://github.com/stenzek/duckstation/archive/refs/tags/v%{upstream_tag}.tar.gz
Source1:        https://github.com/stenzek/discord-rpc/archive/%{discord_rpc_file}

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  ninja-build
BuildRequires:  pkgconfig

# system Shaderc – headers, .so symlink, shaderc.pc
BuildRequires:  libshaderc-devel

# Core deps
BuildRequires:  SDL3-devel SDL3_image-devel SDL3_ttf-devel
BuildRequires:  qt6-qtbase-devel qt6-qttools-devel qt6-qtsvg-devel
BuildRequires:  qt6-qtmultimedia-devel qt6-qtshadertools-devel
BuildRequires:  qt6-qtwayland-devel qt6-qtdeclarative-devel qt6-qt5compat-devel

# Multimedia & graphics
BuildRequires:  mesa-libGL-devel mesa-libEGL-devel vulkan-devel
BuildRequires:  libavcodec-free-devel libavformat-free-devel
BuildRequires:  libavutil-free-devel libswresample-free-devel libswscale-free-devel

# Networking & compression
BuildRequires:  libcurl-devel openssl-devel zlib-devel
BuildRequires:  brotli-devel minizip-compat-devel

# Fonts & images
BuildRequires:  fontconfig-devel libjpeg-turbo-devel libpng-devel

# Audio & input
BuildRequires:  pulseaudio-libs-devel pipewire-devel
BuildRequires:  alsa-lib-devel libevdev-devel libinput-devel

# Windowing (Wayland, X11, etc.)
BuildRequires:  egl-wayland-devel gtk3-devel dbus-devel systemd-devel
BuildRequires:  wayland-devel libdecor-devel libSM-devel libICE-devel
BuildRequires:  libX11-devel libXau-devel libxcb-devel libXcomposite-devel
BuildRequires:  libXcursor-devel libXext-devel libXfixes-devel libXft-devel
BuildRequires:  libXi-devel libXpresent-devel libXrandr-devel libXrender-devel
BuildRequires:  xcb-util-cursor-devel xcb-util-devel xcb-util-errors-devel
BuildRequires:  xcb-util-image-devel xcb-util-keysyms-devel
BuildRequires:  xcb-util-renderutil-devel xcb-util-wm-devel xcb-util-xrm-devel
BuildRequires:  libxkbcommon-devel libxkbcommon-x11-devel

# CPU features & extras
BuildRequires:  cpuinfo-devel libzip-devel soundtouch-devel

ExclusiveArch:  x86_64 aarch64

%description
DuckStation is a fast and accurate PlayStation 1 emulator, focused on speed, playability, and long-term maintainability.

%prep
%autosetup -n duckstation-%{upstream_tag} -p1

# Vendor Discord-RPC
mkdir -p discord-rpc
tar xf %{_sourcedir}/%{discord_rpc_file} \
    --strip-components=1 -C discord-rpc

# Vendor SPIRV-Cross C-API (shared)
git clone --depth=1 https://github.com/KhronosGroup/SPIRV-Cross.git spirv-cross
pushd spirv-cross
mkdir build-spirv && cd build-spirv
cmake .. \
  -DBUILD_SHARED_LIBS=ON \
  -DSPIRV_CROSS_C_API=ON \
  -DBUILD_TESTING=OFF \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON
# build everything
cmake --build .
popd

# patch out the broken spirv-cross target queries in DuckStationDependencies
# (lines that do get_target_property / get_filename_component on spirv-cross-c-shared)
sed -i '/find_package(spirv_cross_c_shared REQUIRED)/,/^endif()/ { 
  /get_target_property/ s/^/#/; 
  /get_filename_component/ s/^/#/ 
}' CMakeModules/DuckStationDependencies.cmake

# Custom CMake find-modules
mkdir -p CMakeModules

# … your other Find*.cmake here (FindDiscordRPC, FindShaderc, etc.) …

%build
# Build Discord-RPC
pushd discord-rpc
mkdir build && cd build
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON
cmake --build . --target discord-rpc
popd

# Configure & build DuckStation
%cmake -S . -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DUSE_QT6=ON \
  -DDUCKSTATION_QT_UI=ON \
  -DDISCORDRPC_SUPPORT=ON \
  -DCMAKE_MODULE_PATH=CMakeModules \
  -DECM_DIR=%{_libdir}/cmake/ECM

ninja -C build

%install
ninja -C build install DESTDIR=%{buildroot}

#desktop file & icon install omitted for brevity

%files
# … your file list …

%changelog
* Fri Aug  1 2025 You <you@example.com> — 0.1.9226-8
- Patched out spirv-cross-c-shared target queries to avoid missing-target errors  
