Name:          duckstation
Version:       0.1.9483
Release:       1%{?dist}
Summary:       A fast PlayStation 1 emulator
License:       CC-BY-NC-ND-4.0
URL:           https://github.com/stenzek/duckstation

# Main source tarball from the release tag
Source0:       https://github.com/stenzek/duckstation/archive/refs/tags/v0.1-9483.tar.gz

# Cheat and patch databases
Source1:       https://github.com/duckstation/chtdb/releases/download/latest/cheats.zip
Source2:       https://github.com/duckstation/chtdb/releases/download/latest/patches.zip

# Don't want extra flags producing a slower build than our other formats.
%undefine _hardened_build
%undefine _annotated_build
%undefine _fortify_level
%undefine _include_frame_pointers

# Defines -O2, -flto, and others. We manage LTO ourselves.
%global _general_options "-O3" "-pipe"
%global _preprocessor_defines ""

# We include debug information in the main package for user backtrace reporting.
%global debug_package %{nil}

# BuildRequires for dependencies handled by the build script have been removed.
BuildRequires: alsa-lib-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: brotli-devel
BuildRequires: clang
BuildRequires: cmake
BuildRequires: curl
BuildRequires: dbus-devel
BuildRequires: egl-wayland-devel
BuildRequires: extra-cmake-modules
BuildRequires: gcc-c++
BuildRequires: git
BuildRequires: libavcodec-free-devel
BuildRequires: libavformat-free-devel
BuildRequires: libavutil-free-devel
BuildRequires: libcurl-devel
BuildRequires: libdecor-devel
BuildRequires: libevdev-devel
BuildRequires: libICE-devel
BuildRequires: libinput-devel
BuildRequires: libSM-devel
BuildRequires: libswresample-free-devel
BuildRequires: libswscale-free-devel
BuildRequires: libX11-devel
BuildRequires: libXau-devel
BuildRequires: libxcb-devel
BuildRequires: libXcomposite-devel
BuildRequires: libXcursor-devel
BuildRequires: libXext-devel
BuildRequires: libXfixes-devel
BuildRequires: libXft-devel
BuildRequires: libXi-devel
BuildRequires: libxkbcommon-devel
BuildRequires: libxkbcommon-x11-devel
BuildRequires: libXpresent-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libtool
BuildRequires: lld
BuildRequires: llvm
BuildRequires: make
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGL-devel
BuildRequires: nasm
BuildRequires: ninja-build
BuildRequires: openssl-devel
BuildRequires: patch
BuildRequires: pcre2-devel
BuildRequires: perl-Digest-SHA
BuildRequires: pipewire-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: systemd-devel
BuildRequires: wayland-devel
BuildRequires: xcb-util-cursor-devel
BuildRequires: xcb-util-devel
BuildRequires: xcb-util-errors-devel
BuildRequires: xcb-util-image-devel
BuildRequires: xcb-util-keysyms-devel
BuildRequires: xcb-util-renderutil-devel
BuildRequires: xcb-util-wm-devel
BuildRequires: xcb-util-xrm-devel
BuildRequires: zlib-devel
BuildRequires: qt6-qtbase-devel
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt6-qttools
BuildRequires: qt6-qttools-devel

# The 'Requires' section should still list the dependencies for the final packaged application.
Requires: bash
Requires: curl
Requires: dbus
Requires: freetype
Requires: libpng
Requires: libwebp
Requires: libzip
Requires: libzstd
Requires: qt6-qtbase
Requires: qt6-qtbase-gui
Requires: qt6-qtimageformats
Requires: qt6-qtsvg

%description
DuckStation is an simulator/emulator of the Sony PlayStation(TM) console, focusing on playability, speed, and long-term maintainability. The goal is to be as accurate as possible while maintaining performance suitable for low-end devices.
"Hack" options are discouraged, the default configuration should support all playable games with only some of the enhancements having compatibility issues.
"PlayStation" and "PSX" are registered trademarks of Sony Interactive Entertainment Europe Limited. This project is not affiliated in any way with Sony Interactive Entertainment.

%prep
%setup -q -n duckstation-0.1-9483

# Use sed to fix the SDL3 version requirement
sed -i 's/find_package(SDL3 3.2.18/find_package(SDL3 3.2.16/' CMakeModules/DuckStationDependencies.cmake

mkdir -p data/resources/
cp %{SOURCE1} data/resources/cheats.zip
cp %{SOURCE2} data/resources/patches.zip

%build
# Run the dependency build script, installing into a temporary directory
scripts/packaging/build-dependencies-linux.sh "%{_builddir}/%{name}-%{version}/deps"

# Now, build the main project, and explicitly tell it where to find all built dependencies.
cmake -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_PREFIX_PATH="%{_builddir}/%{name}-%{version}/deps;/usr" \
    -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_EXE_LINKER_FLAGS_INIT="-fuse-ld=lld" \
    -DCMAKE_MODULE_LINKER_FLAGS_INIT="-fuse-ld=lld" \
    -DCMAKE_SHARED_LINKER_FLAGS_INIT="-fuse-ld=lld" \
    -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON \
    -DALLOW_INSTALL=ON -DINSTALL_SELF_CONTAINED=ON \
    -DCMAKE_INSTALL_PREFIX=%{buildroot}/opt/%{name}

ninja -C build %{?_smp_mflags}

%install
rm -fr %{buildroot}
ninja -C build install

# Create necessary directories
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/icons/hicolor/512x512/apps

# Symlink the binary
ln -s /opt/%{name}/duckstation-qt %{buildroot}/usr/bin/duckstation-qt

# Install desktop files and icons
install -Dm644 scripts/packaging/org.duckstation.DuckStation.png %{buildroot}/usr/share/icons/hicolor/512x512/apps/org.duckstation.DuckStation.png
install -Dm644 scripts/packaging/org.duckstation.DuckStation.desktop %{buildroot}/usr/share/applications/org.duckstation.DuckStation.desktop


%files
%license LICENSE
/opt/duckstation
/usr/bin/duckstation-qt
/usr/share/icons/hicolor/512x512/apps/org.duckstation.DuckStation.png
/usr/share/applications/org.duckstation.DuckStation.desktop
