Name:          duckstation
Version:       0.1.9384
Release:       1%{?dist}
Summary:       A fast PlayStation 1 emulator
License:       CC-BY-NC-ND-4.0
URL:           https://github.com/stenzek/duckstation
Source0:       https://github.com/stenzek/duckstation/archive/refs/tags/v0.1-9384.tar.gz

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
BuildRequires: git
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

%build
./scripts/deps/build-dependencies-linux.sh deps

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

ninja -C build-release

%install
# The -Dinstall flag from cmake is used to install files to the buildroot
# with a prefix path, so a dedicated install step isn't needed here.
# Instead, we will directly move the files to their final destination from
# the default installation location.

# Create the standard directories for desktop files and icons
mkdir -p %{buildroot}/%{_datadir}/applications/
mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/512x512/apps/

# Install the desktop file and icon
install -Dm644 scripts/packaging/org.duckstation.DuckStation.desktop %{buildroot}%{_datadir}/applications/org.duckstation.DuckStation.desktop
install -Dm644 scripts/packaging/org.duckstation.DuckStation.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/org.duckstation.DuckStation.png

# Create the final destination directory for the binary and link it to /usr/bin
mkdir -p %{buildroot}/opt/duckstation
cp build-release/bin/duckstation-qt %{buildroot}/opt/duckstation/
ln -s /opt/duckstation/duckstation-qt %{buildroot}/%{_bindir}/duckstation

%files
%license LICENSE
/opt/duckstation
%{_bindir}/duckstation
%{_datadir}/icons/hicolor/512x512/apps/org.duckstation.DuckStation.png
%{_datadir}/applications/org.duckstation.DuckStation.desktop

%changelog
* Fri Aug 15 2025 Your Name <you@example.com> - 0.1.9384-1
- Initial COPR package for Duckstation release v0.1-9384.
- Added git to BuildRequires.
- Adjusted installation paths for desktop file and icons.
