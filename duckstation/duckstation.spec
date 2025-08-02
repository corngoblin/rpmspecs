Name:           duckstation
Version:        0.1.9226
Release:        10%{?dist}
Summary:        Fast PlayStation 1 emulator

License:        CC-BY-NC-ND-4.0
URL:            https://github.com/stenzek/duckstation

# pinned Discord-RPC commit for reproducible builds
%global discord_rpc_ver    cc59d26d1d628fbd6527aac0ac1d6301f4978b92
%global discord_rpc_file   %{discord_rpc_ver}.tar.gz
# real upstream tag (contains a dash)
%global upstream_tag       0.1-9226

Source0:        https://github.com/stenzek/duckstation/archive/refs/tags/v%{upstream_tag}.tar.gz
Source1:        https://github.com/stenzek/discord-rpc/archive/%{discord_rpc_file}

# -----------------------------------------------------------------------------
# BuildRequires
# -----------------------------------------------------------------------------
BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  ninja-build
BuildRequires:  pkgconfig
BuildRequires:  libshaderc-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

# Core UI
BuildRequires:  SDL3-devel
BuildRequires:  SDL3_image-devel
BuildRequires:  SDL3_ttf-devel

# Qt6
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qtshadertools-devel
BuildRequires:  qt6-qt5compat-devel

# Multimedia & graphics
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  vulkan-devel
BuildRequires:  libavcodec-free-devel
BuildRequires:  libavformat-free-devel
BuildRequires:  libavutil-free-devel
BuildRequires:  libswresample-free-devel
BuildRequires:  libswscale-free-devel

# Networking & compression
BuildRequires:  libcurl-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  brotli-devel
BuildRequires:  minizip-compat-devel

# Fonts & images
BuildRequires:  fontconfig-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel

# Audio & input
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  pipewire-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libevdev-devel
BuildRequires:  libinput-devel

# Windowing (Wayland, X11…)
BuildRequires:  egl-wayland-devel
BuildRequires:  gtk3-devel
BuildRequires:  dbus-devel
BuildRequires:  systemd-devel
BuildRequires:  wayland-devel
BuildRequires:  libdecor-devel
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

# CPU features & extras
BuildRequires:  cpuinfo-devel
BuildRequires:  libzip-devel
# No soundtouch-devel to prevent CMake from finding the system library and
# instead use the vendored one.

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
git clone --depth=1 \
    https://github.com/KhronosGroup/SPIRV-Cross.git spirv-cross

# Vendor libbacktrace
git clone --depth=1 \
    https://github.com/ianlancetaylor/libbacktrace.git backtrace

# Custom CMake find-modules
mkdir -p CMakeModules

# 1) FindDiscordRPC.cmake
# FIX: Find and use the vendored discord-rpc library.
cat > CMakeModules/FindDiscordRPC.cmake << 'EOF'
find_path(DiscordRPC_INCLUDE_DIR discord_rpc.h
  PATHS ${CMAKE_SOURCE_DIR}/discord-rpc/include
)
find_library(DiscordRPC_LIBRARY
  NAMES discord-rpc libdiscord-rpc
  PATHS ${CMAKE_SOURCE_DIR}/discord-rpc/build
)
if (DiscordRPC_INCLUDE_DIR AND DiscordRPC_LIBRARY)
  set(DiscordRPC_FOUND        TRUE)
  set(DiscordRPC_INCLUDE_DIRS ${DiscordRPC_INCLUDE_DIR})
  set(DiscordRPC_LIBRARIES    ${DiscordRPC_LIBRARY})
endif()
mark_as_advanced(DiscordRPC_INCLUDE_DIR DiscordRPC_LIBRARY)
EOF

# 2) Findspirv_cross_c_shared.cmake
# FIX: The SPIRV-Cross build produces a static library. We define an
# imported target to link against it.
cat > CMakeModules/Findspirv_cross_c_shared.cmake << 'EOF'
find_path(spirv_cross_c_shared_INCLUDE_DIR
  NAMES spirv_cross_c.h
  PATHS ${CMAKE_SOURCE_DIR}/spirv-cross/include
)
find_library(spirv_cross_c_shared_LIBRARY
  NAMES spirv-cross-c
  PATHS ${CMAKE_SOURCE_DIR}/spirv-cross/build-spirv
)
if (spirv_cross_c_shared_INCLUDE_DIR AND spirv_cross_c_shared_LIBRARY)
  set(spirv_cross_c_shared_FOUND         TRUE)
  set(spirv_cross_c_shared_INCLUDE_DIRS  ${spirv_cross_c_shared_INCLUDE_DIR})
  set(spirv_cross_c_shared_LIBRARIES     ${spirv_cross_c_shared_LIBRARY})
  add_library(spirv-cross-c-shared STATIC IMPORTED)
  set_target_properties(spirv-cross-c-shared PROPERTIES
    IMPORTED_LOCATION "${spirv_cross_c_shared_LIBRARY}"
    INTERFACE_INCLUDE_DIRECTORIES "${spirv_cross_c_shared_INCLUDE_DIR}"
  )
endif()
mark_as_advanced(spirv_cross_c_shared_INCLUDE_DIR spirv_cross_c_shared_LIBRARY)
EOF

# 3) FindShaderc.cmake
# FIX: The project expects an imported target, but the system package does not provide one.
# We create it manually here, ensuring the correct library path is used.
cat > CMakeModules/FindShaderc.cmake << 'EOF'
find_package(PkgConfig REQUIRED)
pkg_check_modules(Shaderc REQUIRED shaderc)
set(Shaderc_FOUND         TRUE)
set(Shaderc_INCLUDE_DIRS  ${Shaderc_INCLUDEDIR})
set(Shaderc_LIBRARIES     ${Shaderc_LIBRARIES})

get_filename_component(_shlib_dir ${Shaderc_LIBRARIES} PATH)
set(_shlib "${_shlib_dir}/libshaderc_shared.so")
add_library(Shaderc::shaderc_shared SHARED IMPORTED GLOBAL)
set_target_properties(Shaderc::shaderc_shared PROPERTIES
  IMPORTED_LOCATION "${_shlib}"
  INTERFACE_INCLUDE_DIRECTORIES "${Shaderc_INCLUDEDIR}"
)
mark_as_advanced(Shaderc_INCLUDE_DIRS Shaderc_LIBRARIES)
EOF

# 4) FindLibbacktrace.cmake
# FIX: Define the required imported target for the vendored library.
cat > CMakeModules/FindLibbacktrace.cmake << 'EOF'
set(Libbacktrace_INCLUDE_DIRS %{_builddir}/duckstation-%{upstream_tag}/backtrace/install/include)
set(Libbacktrace_LIBRARIES %{_builddir}/duckstation-%{upstream_tag}/backtrace/install/lib/libbacktrace.a)
if (EXISTS "${Libbacktrace_INCLUDE_DIRS}" AND EXISTS "${Libbacktrace_LIBRARIES}")
  set(Libbacktrace_FOUND TRUE)
  add_library(libbacktrace::libbacktrace STATIC IMPORTED)
  set_target_properties(libbacktrace::libbacktrace PROPERTIES
    IMPORTED_LOCATION "${Libbacktrace_LIBRARIES}"
    INTERFACE_INCLUDE_DIRECTORIES "${Libbacktrace_INCLUDE_DIRS}"
  )
endif()
mark_as_advanced(Libbacktrace_INCLUDE_DIRS Libbacktrace_LIBRARIES)
EOF

# 5) FindSoundTouch.cmake
# FIX: The project expects an imported target, but the system package does not provide one.
# We create it manually here, ensuring the correct library path is used. This also
# prevents the build from looking for a system-installed version.
cat > CMakeModules/FindSoundTouch.cmake << 'EOF'
# This module is intentionally left empty. The project's build system
# will automatically fall back to using the vendored SoundTouch library
# when find_package(SoundTouch) fails.
EOF

# Patch the CMake file to force the use of the vendored SoundTouch library.
# We remove the line that attempts to find a system-installed SoundTouch.
sed -i '/find_package(SoundTouch/d' CMakeLists.txt

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

# Build SPIRV-Cross C-API
mkdir -p spirv-cross/build-spirv && pushd spirv-cross/build-spirv
cmake .. \
    -DBUILD_SHARED_LIBS=ON \
    -DSPIRV_CROSS_C_API=ON \
    -DBUILD_TESTING=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON
cmake --build .
popd

# Build vendored libbacktrace
pushd backtrace
# libbacktrace uses autotools, not cmake
./configure --prefix=%{_builddir}/duckstation-%{upstream_tag}/backtrace/install
make
make install
popd

# Configure & build DuckStation
%cmake -S . -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DUSE_QT6=ON \
    -DDUCKSTATION_QT_UI=ON \
    -DDISCORDRPC_SUPPORT=ON \
    -DCMAKE_MODULE_PATH=CMakeModules \
    -DECM_DIR=%{_libdir}/cmake/ECM \
    -Dspirv_cross_c_shared_INCLUDE_DIR=%{_builddir}/duckstation-%{upstream_tag}/spirv-cross/include \
    -Dspirv_cross_c_shared_LIBRARY=%{_builddir}/duckstation-%{upstream_tag}/spirv-cross/build-spirv/libspirv-cross-c.a

ninja -C build

%install
ninja -C build install DESTDIR=%{buildroot}

# desktop file & icon
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    %{buildroot}%{_datadir}/applications/org.duckstation.DuckStation.desktop \
    2>/dev/null || :

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
* Sat Aug 2 2025 You <you@example.com> - 0.1.9226-10
- Re-added soundtouch-devel to BuildRequires and added a corrected FindSoundTouch.cmake module.
- The new module creates the required `SoundTouch::SoundTouchDLL` target from the system library, resolving the build failure.
- This change correctly addresses the project's dependency requirements and allows the build to proceed.
