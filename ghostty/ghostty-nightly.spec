Name:           ghostty-nightly
%global tipcommit %(curl -sL https://api.github.com/repos/ghostty-org/ghostty/git/ref/tags/tip | grep '"sha"' | head -1 | cut -d '"' -f 4)
%global shortcommit %(echo %{tipcommit} | cut -c1-7)
Version:        0.0~git%{shortcommit}
Release:        1%{?dist}
Summary:        Nightly build of Ghostty terminal emulator

License:        MIT
URL:            https://github.com/ghostty-org/ghostty
Source0:        https://github.com/ghostty-org/ghostty/archive/refs/tags/tip.tar.gz

ExclusiveArch:  x86_64 aarch64

BuildRequires:  blueprint-compiler
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk4-devel
BuildRequires:  gtk4-layer-shell-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  libadwaita-devel
BuildRequires:  libpng-devel
BuildRequires:  oniguruma-devel
BuildRequires:  pandoc-cli
BuildRequires:  pixman-devel
BuildRequires:  pkg-config
BuildRequires:  wayland-protocols-devel
BuildRequires:  zlib-ng-devel
# Remove Fedora zig package — we’ll use the official one instead

Requires:       fontconfig
Requires:       freetype
Requires:       glib2
Requires:       gtk4
Requires:       harfbuzz
Requires:       libadwaita
Requires:       libpng
Requires:       oniguruma
Requires:       pixman
Requires:       zlib-ng

%description
Nightly (tip) build of Ghostty terminal emulator.
Automatically includes the latest upstream commit hash for COPR versioning.

%prep
%setup -q -n ghostty-tip

%build
# Download and use the latest Zig development binary (needed for .zon import)
ZIG_VERSION=0.14.0-dev
ZIG_URL="https://ziglang.org/builds/zig-linux-x86_64-${ZIG_VERSION}.tar.xz"
curl -sSL "$ZIG_URL" -o zig.tar.xz
tar -xf zig.tar.xz
ZIGDIR=$(find . -maxdepth 1 -type d -name "zig-linux-*")
export PATH="$PWD/$ZIGDIR:$PATH"

# Verify zig version for logging
zig version

DESTDIR=%{buildroot} zig build \
    --summary all \
    --prefix "%{_prefix}" \
    -Dversion-string=nightly-%{shortcommit}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Demit-docs

%if 0%{?fedora} >= 42
    rm -f "%{buildroot}%{_prefix}/share/terminfo/g/ghostty"
%endif

%files
%license LICENSE
%{_bindir}/ghostty
%{_prefix}/share/**

%changelog
* Thu Oct 24 2025 corngoblin - nightly
