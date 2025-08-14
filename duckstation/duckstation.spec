Name:          duckstation
Version:       0.1.9384
Release:       1%{?dist}
Summary:       A fast PlayStation 1 emulator
License:       CC-BY-NC-ND-4.0
URL:           https://github.com/stenzek/duckstation
Source0:       https://github.com/stenzek/duckstation/archive/refs/tags/v0.1-9384.tar.gz
# We use the tagged release as the source instead of a git clone.
# This makes the build more reproducible.
BuildRequires: alsa-lib-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: brotli-devel
BuildRequires: clang
BuildRequires: cmake
BuildRequires: dbus-devel
BuildRequires: egl-wayland-devel
BuildRequires: extra-cmake-modules
BuildRequires: fontconfig-devel
BuildRequires: gcc-c++
BuildRequires: gtk3-devel
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

%description
Duckstation is an open-source, multi-platform PlayStation 1 emulator. It focuses on
playability, speed, and long-term maintainability. The emulator uses a JIT
recompiler and has a robust user interface with features like save states,
rewind, and various graphical enhancements.

%prep
%setup -q -n duckstation-0.1-9384
# The -n flag specifies the source directory name after extraction

%build
# Build dependencies using the provided script
./scripts/deps/build-dependencies-linux.sh deps

# Use CMake to configure the build. The -B build-release flag creates a build directory
# and the options specify clang and lld as the compiler and linker.
# We also link to the locally built dependencies.
cmake -B build-release \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON \
      -DCMAKE_C_COMPILER=clang \
      -DCMAKE_CXX_COMPILER=clang++ \
      -DCMAKE_EXE_LINKER_FLAGS_INIT="-fuse-ld=lld" \
      -DCMAKE_MODULE_LINKER_FLAGS_INIT="-fuse-ld=lld" \
      -DCMAKE_SHARED_LINKER_FLAGS_INIT="-fuse-ld=lld" \
      -DCMAKE_PREFIX_PATH="%{_builddir}/duckstation-0.1-9384/deps" \
      -G Ninja

# Use Ninja to compile the source code.
ninja -C build-release

%install
# Create a destination directory for the installation
mkdir -p %{buildroot}%{_bindir}
# Copy the compiled binary to the system's binary directory
cp build-release/bin/duckstation-qt %{buildroot}%{_bindir}/duckstation
# Copy the required license file
mkdir -p %{buildroot}%{_docdir}/duckstation
cp LICENSE %{buildroot}%{_docdir}/duckstation/

%files
%{_bindir}/duckstation
%{_docdir}/duckstation/LICENSE

%changelog
* Fri Aug 15 2025 Your Name <you@example.com> - 0.1.9384-1
- Initial COPR package for Duckstation release v0.1-9384.
