Name:           duckstation
Version:        0.1.9226
Release:        10%{?dist}
Summary:        Fast PlayStation 1 emulator

License:        GPLv2+
URL:            https://github.com/stenzek/duckstation
Source0:        https://github.com/stenzek/duckstation/archive/%{version}.tar.gz

# -----------------------------------------------------------------------------
# Build-time dependencies
# -----------------------------------------------------------------------------
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  extra-cmake-modules
BuildRequires:  pkgconfig

# C++ toolchain
BuildRequires:  gcc-c++

# Qt6
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qt5compat-devel

# Graphics / rendering
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  vulkan-headers
BuildRequires:  shaderc-devel
BuildRequires:  zstd-devel
BuildRequires:  libwebp-devel
BuildRequires:  libpng-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  freetype-devel
BuildRequires:  soundtouch-devel

# Networking, compression
BuildRequires:  libcurl-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  brotli-devel
BuildRequires:  minizip-compat-devel

# X11 / Wayland
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  wayland-devel
BuildRequires:  egl-wayland-devel

# -----------------------------------------------------------------------------
# No official spirv_cross_c_shared on F42, use our shipped CMake module
# -----------------------------------------------------------------------------
# BuildRequires:  spirv-cross-c-shared-devel

ExclusiveArch:  x86_64 aarch64

%description
DuckStation is a fast, accurate emulator for the original Sony PlayStation 1.  
It focuses on performance, playability, and long-term code maintainability.

%prep
%autosetup -p1

# Rename upstream’s CMake finder so `find_package(spirv_cross_c_shared)` works
mv CMakeModules/Findspirv-cross-c-shared.cmake \
   CMakeModules/Findspirv_cross_c_shared.cmake

%build
cmake -S . -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DUSE_QT6=ON \
    -DDUCKSTATION_QT_UI=ON \
    -DDISCORDRPC_SUPPORT=ON \
    -DCMAKE_VERBOSE_MAKEFILE=ON \
    -DCMAKE_MODULE_PATH=%{_sourcedir}/CMakeModules

cmake --build build

%install
cmake --install build --prefix %{_prefix} --strip

%files
%license LICENSE*
%doc README.md
%{_bindir}/duckstation*
%{_datadir}/duckstation
%{_libdir}/libduckstation*

%changelog
* Fri Aug 01 2025 Your Name <you@example.com> - 0.1.9226-10
- Added extra-cmake-modules BuildRequires
- Renamed Findspirv-cross-c-shared.cmake → Findspirv_cross_c_shared.cmake
- Added missing Qt6, Vulkan, shaderc, zstd, webp, png, jpeg-turbo, freetype, soundtouch BuildRequires
