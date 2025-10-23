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

# --- Build Dependencies ---
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
# Use official Zig v0.15.2 instead of Fedora package

# --- Runtime Dependencies ---
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
# ------------------------------------------------------------
# Download and use the Zig binary required by Ghostty
# ------------------------------------------------------------
ZIG_VERSION="0.15.2"
ZIG_URL="https://ziglang.org/download/0.15.2/zig-x86_64-linux-0.15.2.tar.xz"
echo "Downloading Zig from $ZIG_URL"
curl -sSL "$ZIG_URL" -o zig.tar.xz

echo "Extracting Zig..."
tar -xf zig.tar.xz
ZIGDIR=$(find . -maxdepth 1 -type d -name "zig-*")
export PATH="$PWD/$ZIGDIR:$PATH"

echo "Using Zig version:"
zig version

# ------------------------------------------------------------
# Build Ghostty using Zig
# ------------------------------------------------------------
DESTDIR=%{buildroot} zig build \
    --summary all \
    --prefix "%{_prefix}" \
    -Dversion-string=nightly-%{shortcommit}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Demit-docs

%if 0%{?fedora} >= 42
# Remove terminfo conflict on newer Fedora builds
rm -f "%{buildroot}%{_prefix}/share/terminfo/g/ghostty"
%endif

%install
# Zig installs directly into %{buildroot} via --prefix
# Nothing extra needed here

%files
%license LICENSE
%{_bindir}/ghostty
%{_prefix}/share/applications/com.mitchellh.ghostty.desktop
%{_prefix}/share/bash-completion/completions/ghostty.bash
%{_prefix}/share/bat/syntaxes/ghostty.sublime-syntax
%{_prefix}/share/fish/vendor_completions.d/ghostty.fish
%{_prefix}/share/ghostty
%{_prefix}/share/icons/hicolor/1024x1024/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/128x128/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/128x128@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/16x16/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/16x16@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/256x256/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/256x256@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/32x32/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/32x32@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/512x512/apps/com.mitchellh.ghostty.png
%{_prefix}/share/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_prefix}/share/man/man1/ghostty.1
%{_prefix}/share/man/man5/ghostty.5
%{_prefix}/share/nautilus-python/extensions/ghostty.py
%{_prefix}/share/nvim/site/compiler/ghostty.vim
%{_prefix}/share/nvim/site/ftdetect/ghostty.vim
%{_prefix}/share/nvim/site/ftplugin/ghostty.vim
%{_prefix}/share/nvim/site/syntax/ghostty.vim
%{_prefix}/share/vim/vimfiles/compiler/ghostty.vim
%{_prefix}/share/vim/vimfiles/ftdetect/ghostty.vim
%{_prefix}/share/vim/vimfiles/ftplugin/ghostty.vim
%{_prefix}/share/vim/vimfiles/syntax/ghostty.vim
%{_prefix}/share/zsh/site-functions/_ghostty
%{_prefix}/share/dbus-1/services/com.mitchellh.ghostty.service
%{_prefix}/share/locale/*/LC_MESSAGES/com.mitchellh.ghostty.mo
%{_prefix}/share/metainfo/com.mitchellh.ghostty.metainfo.xml
%{_prefix}/share/systemd/user/app-com.mitchellh.ghostty.service
%{_prefix}/share/terminfo/x/xterm-ghostty
%if 0%{?fedora} < 42
    %{_prefix}/share/terminfo/g/ghostty
%endif

%changelog
* Thu Oct 23 2025 Corngoblin <none@none> - 0.0~git%{shortcommit}-1
- Nightly snapshot build from latest tip commit
- Updated to Zig 0.15.2
