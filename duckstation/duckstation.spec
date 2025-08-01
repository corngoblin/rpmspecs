Name:           duckstation
Version:        0.1.9226
Release:        6%{?dist}
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

# spirv_cross C shared – headers, .so, pkg-config
BuildRequires:  libspirv-cross-c-shared-devel

# Core deps
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

# Windowing (Wayland, X11, etc.)
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

# CPU features
BuildRequires:  cpuinfo-devel

# satisfy find_package(libzip) & find_package(SoundTouch)
BuildRequires:  libzip-devel
BuildRequires:  soundtouch-devel

ExclusiveArch:  x86_64 aarch64

%description
DuckStation is a fast and accurate PlayStation 1 emulator, focused on speed, playability, and long-term maintainability.

%prep
%autosetup -n duckstation-%{upstream_tag} -p1

# Vendor Discord-RPC
mkdir -p discord-rpc
tar xf %{_sourcedir}/%{discord_rpc_file} \
    --strip-components=1 -C discord-rpc

# Prepare our custom CMake find-modules
mkdir -p CMakeModules

# FindDiscordRPC.cmake
cat > CMakeModules/FindDiscordRPC.cmake << 'EOF'
find_path(DiscordRPC_INCLUDE_DIR discord_rpc.h
  PATHS ${CMAKE_SOURCE_DIR}/discord-rpc/include
)
find_library(DiscordRPC_LIBRARY
  NAMES discord-rpc libdiscord-rpc
  PATHS ${CMAKE_SOURCE_DIR}/discord-rpc/build
)
if (DiscordRPC_INCLUDE_DIR AND DiscordRPC_LIBRARY)
  set(DiscordRPC_FOUND      TRUE)
  set(DiscordRPC_INCLUDE_DIRS ${DiscordRPC_INCLUDE_DIR})
  set(DiscordRPC_LIBRARIES   ${DiscordRPC_LIBRARY})
endif()
mark_as_advanced(DiscordRPC_INCLUDE_DIR DiscordRPC_LIBRARY)
EOF

# Findlibzip.cmake
cat > CMakeModules/Findlibzip.cmake << 'EOF'
find_path(libzip_INCLUDE_DIR zip.h
  PATHS %{_includedir}
)
find_library(libzip_LIBRARY
  NAMES zip libzip
  PATHS %{_libdir}
)
if (libzip_INCLUDE_DIR AND libzip_LIBRARY)
  set(libzip_FOUND       TRUE)
  set(libzip_INCLUDE_DIRS ${libzip_INCLUDE_DIR})
  set(libzip_LIBRARIES   ${libzip_LIBRARY})
endif()
mark_as_advanced(libzip_INCLUDE_DIR libzip_LIBRARY)
EOF

# FindSoundTouch.cmake
cat > CMakeModules/FindSoundTouch.cmake << 'EOF'
find_path(SoundTouch_INCLUDE_DIR SoundTouch.h
  PATHS %{_includedir}
)
find_library(SoundTouch_LIBRARY
  NAMES SoundTouch
  PATHS %{_libdir}
)
if (SoundTouch_INCLUDE_DIR AND SoundTouch_LIBRARY)
  set(SoundTouch_FOUND       TRUE)
  set(SoundTouch_INCLUDE_DIRS ${SoundTouch_INCLUDE_DIR})
  set(SoundTouch_LIBRARIES   ${SoundTouch_LIBRARY})
endif()
mark_as_advanced(SoundTouch_INCLUDE_DIR SoundTouch_LIBRARY)
EOF

# FindShaderc.cmake
cat > CMakeModules/FindShaderc.cmake << 'EOF'
find_package(PkgConfig REQUIRED)
pkg_check_modules(Shaderc REQUIRED shaderc)
set(Shaderc_FOUND        TRUE)
set(Shaderc_INCLUDE_DIRS ${Shaderc_INCLUDEDIR})
set(Shaderc_LIBRARIES   ${Shaderc_LIBRARIES})
mark_as_advanced(Shaderc_INCLUDE_DIRS Shaderc_LIBRARIES)
EOF

# Findspirv_cross_c_shared.cmake
cat > CMakeModules/Findspirv_cross_c_shared.cmake << 'EOF'
find_package(PkgConfig REQUIRED)
pkg_check_modules(spirv_cross_c_shared REQUIRED spirv-cross-c-shared)
set(spirv_cross_c_shared_FOUND        TRUE)
set(spirv_cross_c_shared_INCLUDE_DIRS ${spirv_cross_c_shared_INCLUDEDIR})
set(spirv_cross_c_shared_LIBRARIES    ${spirv_cross_c_shared_LIBRARIES})
mark_as_advanced(spirv_cross_c_shared_INCLUDE_DIRS spirv_cross_c_shared_LIBRARIES)
EOF

%build
# Build vendored Discord-RPC
pushd discord-rpc
mkdir build && cd build
cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DBUILD_SHARED_LIBS=OFF \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON
cmake --build . --target discord-rpc
popd

# Configure DuckStation
%cmake -S . -B build \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DUSE_QT6=ON \
  -DDUCKSTATION_QT_UI=ON \
  -DDISCORDRPC_SUPPORT=ON \
  -DCMAKE_MODULE_PATH=%{_sourcedir}/CMakeModules \
  -DECM_DIR=%{_libdir}/cmake/ECM

ninja -C build

%install
ninja -C build install DESTDIR=%{buildroot}

# desktop file & icon
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
* Fri Aug  1 2025 You <you@example.com> — 0.1.9226-6
- Removed vendored Shaderc clone & build
- Switched to system libshaderc-devel
- Added FindShaderc.cmake (pkg-config-based)
- Added libspirv-cross-c-shared-devel & Findspirv_cross_c_shared.cmake
