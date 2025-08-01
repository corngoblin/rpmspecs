Name:           duckstation
Version:        0.1.9226
Release:        1%{?dist}
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
BuildRequires:  ninja-build
BuildRequires:  gcc-c++

# DuckStation dependencies
BuildRequires:  SDL3-devel
BuildRequires:  SDL3_image-devel
BuildRequires:  SDL3_ttf-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qtshadertools-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qt5compat-devel

# Multimedia and graphics
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  vulkan-devel
BuildRequires:  libavcodec-free-devel
BuildRequires:  libavformat-free-devel
BuildRequires:  libavutil-free-devel
BuildRequires:  libswresample-free-devel
BuildRequires:  libswscale-free-devel

# Networking and compression
BuildRequires:  libcurl-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  brotli-devel
BuildRequires:  minizip-compat-devel

# Fonts and images
BuildRequires:  fontconfig-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel

# Audio and input
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  pipewire-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libevdev-devel
BuildRequires:  libinput-devel

# Wayland/X11/windowing
BuildRequires:  egl-wayland-devel
BuildRequires:  gtk3-devel
BuildRequires:  dbus-devel
BuildRequires:  systemd-devel
BuildRequires:  wayland-devel
BuildRequires:  libdecor-devel

# X11-specific
BuildRequires:  libSM-devel
BuildRequires:  libICE-devel
BuildRequires:  libX11-devel
BuildRequires:  libXau-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXext-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXft-devel
BuildRequires:  libXi-devel
BuildRequires:  libXpresent-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  xcb-util-cursor-devel
BuildRequires:  xcb-util-devel
BuildRequires:  xcb-util-errors-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-xrm-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  libxkbcommon-x11-devel

# CPU features
BuildRequires:  cpuinfo-devel

# << NEW >> SoundTouch is required by DuckStationDependencies.cmake
BuildRequires:  soundtouch-devel

ExclusiveArch:  x86_64 aarch64

%description
DuckStation is a fast and accurate PlayStation 1 emulator, focused on speed, playability, and long-term maintainability.

%prep
# 1) Unpack DuckStation (creates duckstation-0.1-9226/)
%setup -q -n duckstation-%{upstream_tag}

# 2) Vendor in Discord-RPC, stripping its top folder
mkdir -p discord-rpc
tar -xzf %{_sourcedir}/%{discord_rpc_file} \
    --strip-components=1 -C discord-rpc

# 3) Inject custom FindDiscordRPC.cmake so find_package(DiscordRPC) works
mkdir -p CMakeModules
cat > CMakeModules/FindDiscordRPC.cmake << 'EOF'
# FindDiscordRPC.cmake — locate our vendored static Discord-RPC
find_path(DiscordRPC_INCLUDE_DIR discord_rpc.h
  PATHS ${CMAKE_SOURCE_DIR}/discord-rpc/include
        ENV DISCORDRPC_INCLUDE_DIR
)
find_library(DiscordRPC_LIBRARY
  NAMES discord-rpc libdiscord-rpc
  PATHS ${CMAKE_SOURCE_DIR}/discord-rpc/build
        ENV DISCORDRPC_LIBRARY
)
if(DiscordRPC_INCLUDE_DIR AND DiscordRPC_LIBRARY)
  set(DiscordRPC_FOUND TRUE)
  set(DiscordRPC_INCLUDE_DIR ${DiscordRPC_INCLUDE_DIR})
  set(DiscordRPC_LIBRARY     ${DiscordRPC_LIBRARY})
endif()
mark_as_advanced(DiscordRPC_INCLUDE_DIR DiscordRPC_LIBRARY)
EOF

%build
# Build static Discord-RPC in-place
pushd discord-rpc
mkdir build && cd build
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON
cmake --build . --target discord-rpc
popd

# Configure DuckStation to pick up vendored RPC and system SoundTouch
%cmake -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DUSE_QT6=ON \
  -DDUCKSTATION_QT_UI=ON \
  -DDISCORDRPC_SUPPORT=ON \
  -DCMAKE_MODULE_PATH=$PWD/CMakeModules

# Compile DuckStation
ninja -C build

%install
# Stage into %{buildroot}
ninja -C build install DESTDIR=%{buildroot}

# Install desktop file & icon (no error if already present)
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/org.duckstation.DuckStation.desktop 2>/dev/null || :

install -Dm644 \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/org.duckstation.DuckStation.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/org.duckstation.DuckStation.png

%files
%license LICENSE
%doc README.md
%{_bindir}/duckstation-qt
%{_datadir}/applications/org.duckstation.DuckStation.desktop
%{_datadir}/icons/hicolor/128x128/apps/org.duckstation.DuckStation.png

%changelog
* Fri Aug  1 2025 Monkegold <you@example.com> - 0.1.9226-1
- Added soundtouch-devel to satisfy find_package(SoundTouch)
- Vendored Discord-RPC with custom FindDiscordRPC.cmake
- Retained dash-free Version; actual tag in %{upstream_tag}
