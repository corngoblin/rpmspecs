Name:           duckstation
Version:        0.1.9226
Release:        1%{?dist}
Summary:        Fast PlayStation 1 emulator

License:        CC-BY-NC-ND-4.0
URL:            https://github.com/stenzek/duckstation

# pinned Discord-RPC commit for reproducibility
%global discord_rpc_ver   cc59d26d1d628fbd6527aac0ac1d6301f4978b92
%global discord_rpc_file  %{discord_rpc_ver}.tar.gz

# the real upstream tag (contains a dash)
%global upstream_tag      0.1-9226

Source0:        https://github.com/stenzek/duckstation/archive/refs/tags/v%{upstream_tag}.tar.gz
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
DuckStation is a fast and accurate PlayStation 1 emulator, focused on speed, playability, and long-term maintainability.

%prep
# Unpack the main tarball (folder is duckstation-0.1-9226)
%setup -q -n duckstation-%{upstream_tag}

# Embed and unpack Discord-RPC into ./discord-rpc
mkdir -p discord-rpc
pushd discord-rpc
%setup -q -T -D -a 1
popd

%build
# Build & install static Discord-RPC
pushd discord
