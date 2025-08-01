Name:           duckstation
Version:        0.1.9226
Release:        10%{?dist}
Summary:        Fast PlayStation 1 emulator

License:        CC-BY-NC-ND-4.0
URL:            https://github.com/stenzek/duckstation

%global discord_rpc_ver   cc59d26d1d628fbd6527aac0ac1d6301f4978b92
%global discord_rpc_file  %{discord_rpc_ver}.tar.gz
%global upstream_tag      0.1-9226

Source0:        https://github.com/stenzek/duckstation/archive/refs/tags/v%{upstream_tag}.tar.gz
Source1:        https://github.com/stenzek/discord-rpc/archive/%{discord_rpc_file}

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  git
BuildRequires:  ninja-build
BuildRequires:  pkgconfig

# Qt6
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qtshadertools-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qt5compat-devel

# Graphics / Vulkan / OpenGL
BuildRequires:  SDL3-devel SDL3_image-devel SDL3_ttf-devel
BuildRequires:  mesa-libGL-devel mesa-libEGL-devel vulkan-devel
BuildRequires:  glslang-devel imgui-devel

# Codec / multimedia
BuildRequires:  libavcodec-free-devel libavformat-free-devel \
                libavutil-free-devel libswresample-free-devel libswscale-free-devel
BuildRequires:  libshaderc-devel

# Audio
BuildRequires:  libcurl-devel openssl-devel zlib-devel \
                brotli-devel minizip-compat-devel
BuildRequires:  pulseaudio-libs-devel pipewire-devel \
                alsa-lib-devel libevdev-devel libinput-devel

# Fonts & images
BuildRequires:  fontconfig-devel libjpeg-turbo-devel libpng-devel

# X / Wayland / Misc
BuildRequires:  gtk3-devel dbus-devel systemd-devel
BuildRequires:  wayland-devel egl-wayland-devel libdecor-devel
BuildRequires:  libSM-devel libICE-devel libX11-devel libXau-devel \
                libxcb-devel libXcomposite-devel libXcursor-devel \
                libXext-devel libXfixes-devel libXft-devel libXi-devel \
                libXpresent-devel libXrandr-devel libXrender-devel \
                xcb-util-cursor-devel xcb-util-devel xcb-util-errors-devel \
                xcb-util-image-devel xcb-util-keysyms-devel \
                xcb-util-renderutil-devel xcb-util-wm-devel \
                xcb-util-xrm-devel libxkbcommon-devel libxkbcommon-x11-devel

BuildRequires:  cpuinfo-devel libzip-devel soundtouch-devel
BuildRequires:  libbacktrace-devel python3-devel

ExclusiveArch:  x86_64 aarch64

%description
DuckStation is a fast and accurate PlayStation 1 emulator, focused on speed, playability, and long-term maintainability.

%prep
%autosetup -n duckstation-%{upstream_tag} -p1

# Vendor Discord-RPC
mkdir -p discord-rpc
tar xf %{_sourcedir}/%{discord_rpc_file} \
    --strip-components=1 -C discord-rpc

# Vendor and build SPIRV-Cross C API (shared)
git clone --depth=1 https://github.com/KhronosGroup/SPIRV-Cross.git spirv-cross
pushd spirv-cross
  mkdir build-spirv && cd build-spirv
  cmake .. \
    -DBUILD_SHARED_LIBS=ON \
    -DSPIRV_CROSS_C_API=ON \
    -DBUILD_TESTING=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON
  cmake --build .
popd

# Create our CMakeModules dir
mkdir -p CMakeModules

# 1) DiscordRPC finder
cat > CMakeModules/FindDiscordRPC.cmake << 'EOF'
find_path(DiscordRPC_INCLUDE_DIR discord_rpc.h
  PATHS ${CMAKE_SOURCE_DIR}/discord-rpc/include
)
find_library(DiscordRPC_LIBRARY
  NAMES discord-rpc libdiscord-rpc
  PATHS ${CMAKE_SOURCE_DIR}/discord-rpc/build
)
if (DiscordRPC_INCLUDE_DIR AND DiscordRPC_LIBRARY)
  set(DiscordRPC_FOUND       TRUE)
  set(DiscordRPC_INCLUDE_DIRS ${DiscordRPC_INCLUDE_DIR})
  set(DiscordRPC_LIBRARIES   ${DiscordRPC_LIBRARY})

  add_library(DiscordRPC::DiscordRPC STATIC IMPORTED GLOBAL)
  set_target_properties(DiscordRPC::DiscordRPC PROPERTIES
    IMPORTED_LOCATION "${DiscordRPC_LIBRARY}"
    INTERFACE_INCLUDE_DIRECTORIES "${DiscordRPC_INCLUDE_DIR}"
  )
endif()
mark_as_advanced(DiscordRPC_INCLUDE_DIR DiscordRPC_LIBRARY)
EOF

# 2) SPIRV-Cross C shared API finder
#     NOTE filename uses underscores to match find_package(spirv_cross_c_shared)
cat > CMakeModules/Findspirv_cross_c_shared.cmake << 'EOF'
find_path(spirv_cross_c_shared_INCLUDE_DIR
  NAMES spirv_cross_c.h
  PATHS ${CMAKE_SOURCE_DIR}/spirv-cross
)
find_library(spirv_cross_c_shared_LIBRARY
  NAMES spirv_cross_c_shared spirv-cross-c-shared
  PATHS ${CMAKE_SOURCE_DIR}/spirv-cross/build-spirv
)
if (spirv_cross_c_shared_INCLUDE_DIR AND spirv_cross_c_shared_LIBRARY)
  set(spirv_cross_c_shared_FOUND        TRUE)
  set(spirv_cross_c_shared_INCLUDE_DIRS ${spirv_cross_c_shared_INCLUDE_DIR})
  set(spirv_cross_c_shared_LIBRARIES    ${spirv_cross_c_shared_LIBRARY})

  add_library(spirv-cross-c-shared UNKNOWN IMPORTED GLOBAL)
  set_target_properties(spirv-cross-c-shared PROPERTIES
    IMPORTED_LOCATION        "${spirv_cross_c_shared_LIBRARY}"
    INTERFACE_INCLUDE_DIRECTORIES "${spirv_cross_c_shared_INCLUDE_DIR}"
  )
endif()
mark_as_advanced(spirv_cross_c_shared_INCLUDE_DIR spirv_cross_c_shared_LIBRARY)
EOF

# 3) Shaderc finder (in case CMake’s built-in or pkgconfig is broken)
cat > CMakeModules/FindShaderc.cmake << 'EOF'
find_package(PkgConfig REQUIRED)
pkg_check_modules(Shaderc REQUIRED shaderc)
set(Shaderc_FOUND        TRUE)
set(Shaderc_INCLUDE_DIRS ${Shaderc_INCLUDEDIR})
set(Shaderc_LIBRARIES    ${Shaderc_LIBRARIES})

get_filename_component(_shlib_dir ${Shaderc_LIBRARIES} PATH)
set(_shlib "${_shlib_dir}/libshaderc_shared.so")
add_library(Shaderc::shaderc_shared UNKNOWN IMPORTED GLOBAL)
set_target_properties(Shaderc::shaderc_shared PROPERTIES
  IMPORTED_LOCATION "${_shlib}"
  INTERFACE_INCLUDE_DIRECTORIES "${Shaderc_INCLUDEDIR}"
)
mark_as_advanced(Shaderc_INCLUDE_DIRS Shaderc_LIBRARIES)
EOF

%build
# Build Discord-RPC
pushd discord-rpc
  mkdir -p build && cd build
  cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_POSITION_INDEPENDENT_CODE=ON
  cmake --build . --target discord-rpc
popd

# SPIRV-Cross C API was built in %prep already

# Configure and build DuckStation itself
%cmake -S . -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DUSE_QT6=ON \
  -DDUCKSTATION_QT_UI=ON \
  -DDISCORDRPC_SUPPORT=ON \
  -DCMAKE_MESSAGE_LOG_LEVEL=DEBUG \
  -DCMAKE_MODULE_PATH=\${CMAKE_SOURCE_DIR}/CMakeModules \
  -DECM_DIR=%{_libdir}/cmake/ECM \
  -DUSE_PCH=OFF -DENABLE_PCH=OFF \
  -DENABLE_PRECOMPILED_HEADERS=OFF \
  -DSKIP_PRECOMPILE_HEADERS=ON \
  -DUSE_PRECOMPILED_HEADERS=OFF \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="" \
  -DCMAKE_BUILD_WITH_INSTALL_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=ON

ninja -C build

%install
ninja -C build install DESTDIR=%{buildroot}

# Desktop integration
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
* Sat Aug  2 2025 Your Name <you@example.com> — 0.1.9226-10
- Renamed Findspirv_cross_c_shared.cmake to match find_package(spirv_cross_c_shared)  
- Added glslang-devel, imgui-devel, libbacktrace-devel, python3-devel BuildRequires  
- Disabled PCH and cleaned up RPATH flags  
