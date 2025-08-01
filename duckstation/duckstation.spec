Name:           duckstation
Version:        0.1.9226
Release:        1%{?dist}
Summary:        Fast PlayStation 1 emulator

License:        CC-BY-NC-ND-4.0
URL:            https://github.com/stenzek/duckstation

# Pin to the discord-rpc commit hash from the build script for reproducibility
%global discord_rpc_ver cc59d26d1d628fbd6527aac0ac1d6301f4978b92
%global discord_rpc_file %{discord_rpc_ver}.tar.gz

# Define builddir macro for extracted source directory
%global builddir %{_builddir}/%{name}-%{version}

Source0:        https://github.com/stenzek/duckstation/archive/refs/tags/v0.1-9226.tar.gz
Source1:        https://github.com/stenzek/discord-rpc/archive/%{discord_rpc_file}

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++

# Core dependencies
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

# Fonts and image support
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

# X11-specific deps
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

# CPU detection
BuildRequires:  cpuinfo-devel

ExclusiveArch:  x86_64 aarch64

%description
DuckStation is a fast and accurate PlayStation 1 emulator, focused on speed, playability, and long‑term maintainability.

%prep
%autosetup -n duckstation-0.1-9226

mkdir -p discord-rpc
pushd discord-rpc
%setup -q -T -D -a 1
popd

%build
cd discord-rpc
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON
cmake --build . --target discord-rpc
cd ../..

%cmake -B build -G Ninja \
  -DCMAKE_BUILD_TYPE=RelWithDebInfo \
  -DUSE_QT6=ON \
  -DDUCKSTATION_QT_UI=ON \
  -DDISCORDRPC_SUPPORT=ON \
  -DDiscordRPC_INCLUDE_DIR=%{_builddir}/duckstation-0.1-9226/discord-rpc/include \
  -DDiscordRPC_LIBRARY=%{_builddir}/duckstation-0.1-9226/discord-rpc/build/libdiscord-rpc.a \
  -DDiscordRPC_FOUND=TRUE

%ninja_build -C build

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
- Updated to tag v0.1-9226
- Switched to SDL3
- Enabled DiscordRPC support with embedded build
- Ensured compatibility with Fedora 42 and Rawhide
