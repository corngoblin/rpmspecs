Name:           duckstation
Version:        0.1.9226
Release:        1%{?dist}
Summary:        Fast PlayStation 1 emulator

License:        CC-BY-NC-ND-4.0
URL:            https://github.com/stenzek/duckstation
Source0:        https://github.com/stenzek/duckstation/archive/refs/tags/v0.1-9226.tar.gz#/duckstation-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  SDL3-devel
BuildRequires:  SDL3_image-devel
BuildRequires:  SDL3_ttf-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qtshadertools-devel
# qt6-qtx11extras-devel removed (not in Fedora 42)
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qt5compat-devel
BuildRequires:  SDL2-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  vulkan-devel
BuildRequires:  libavcodec-free-devel
BuildRequires:  libavformat-free-devel
BuildRequires:  libavutil-free-devel
BuildRequires:  libswresample-free-devel
BuildRequires:  libswscale-free-devel
BuildRequires:  libcurl-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel
BuildRequires:  brotli-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  minizip-compat-devel
BuildRequires:  gtk3-devel
BuildRequires:  egl-wayland-devel
BuildRequires:  dbus-devel
BuildRequires:  systemd-devel
BuildRequires:  wayland-devel
BuildRequires:  pipewire-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libdecor-devel
BuildRequires:  libevdev-devel
BuildRequires:  libinput-devel
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
BuildRequires:  libxkbcommon-devel
BuildRequires:  libxkbcommon-x11-devel
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

ExclusiveArch:  x86_64 aarch64

%description
DuckStation is a fast and accurate PlayStation 1 emulator, focused on speed, playability, and long‑term maintainability.

%prep
%autosetup -n duckstation-0.1-9226

%build
%cmake -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DUSE_QT6=ON \
  -DDUCKSTATION_QT_UI=ON
%ninja_build -C build

%install
%ninja_install -C build

# Optional desktop files/icons if present
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/org.duckstation.DuckStation.desktop 2>/dev/null || :
install -Dm644 %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/org.duckstation.DuckStation.png \
  %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/org.duckstation.DuckStation.png || :

%files
%license LICENSE
%doc README.md
%{_bindir}/duckstation-qt
%{_datadir}/applications/org.duckstation.DuckStation.desktop
%{_datadir}/icons/hicolor/128x128/apps/org.duckstation.DuckStation.png

%changelog
* Thu Jul 31 2025 Monkegold <o53cbexp0@mozmail.com> - 0.1.9226-1
- Included SDL3 devel packages to satisfy find_package(SDL3)
- Removed qt6‑qtx11extras-devel (unavailable in Fedora 42)
