Name:           ghostty-nightly
%global tipcommit %(curl -sL https://api.github.com/repos/ghostty-org/ghostty/commits/main | grep '"sha"' | head -1 | cut -d '"' -f 4)
%global shortcommit %(echo %{tipcommit} | cut -c1-7)
Version:        0.0~git%{shortcommit}
Release:        1%{?dist}
Summary:        Nightly build of Ghostty terminal emulator

License:        MIT
URL:            https://github.com/ghostty-org/ghostty
Source0:        https://github.com/ghostty-org/ghostty/archive/%{tipcommit}.tar.gz

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
%setup -q -n ghostty-%{tipcommit}

%build
ZIG_VERSION="0.15.2"
ZIG_URL="https://ziglang.org/download/0.15.2/zig-x86_64-linux-${ZIG_VERSION}.tar.xz"

curl -sSL "$ZIG_URL" -o zig.tar.xz
tar -xf zig.tar.xz
ZIGDIR=$(find . -maxdepth 1 -type d -name "zig-*")
export PATH="$PWD/$ZIGDIR:$PATH"

DESTDIR=%{buildroot} zig build \
    --summary all \
    --prefix "%{_prefix}" \
    -Dversion-string=0.0.0-nightly.%{shortcommit}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Demit-docs

%if 0%{?fedora} >= 42
rm -f "%{buildroot}%{_prefix}/share/terminfo/g/ghostty"
%endif

%install
rm -rf %{buildroot}

# --- Binary ---
mkdir -p %{buildroot}%{_bindir}
cp zig-out/bin/ghostty %{buildroot}%{_bindir}/ghostty

# --- Desktop files ---
mkdir -p %{buildroot}%{_prefix}/share/applications
cp desktop/com.mitchellh.ghostty.desktop %{buildroot}%{_prefix}/share/applications/

# --- Shell completions ---
mkdir -p %{buildroot}%{_prefix}/share/bash-completion/completions
cp completions/ghostty.bash %{buildroot}%{_prefix}/share/bash-completion/completions/

mkdir -p %{buildroot}%{_prefix}/share/fish/vendor_completions.d
cp completions/ghostty.fish %{buildroot}%{_prefix}/share/fish/vendor_completions.d/

# --- Syntax highlighting ---
mkdir -p %{buildroot}%{_prefix}/share/bat/syntaxes
cp syntax/ghostty.sublime-syntax %{buildroot}%{_prefix}/share/bat/syntaxes/

# --- Ghostty assets directory ---
cp -r assets/ghostty %{buildroot}%{_prefix}/share/ghostty

# --- Icons ---
mkdir -p %{buildroot}%{_prefix}/share/icons/hicolor
cp -r assets/icons/* %{buildroot}%{_prefix}/share/icons/hicolor/

# --- KIO, Nautilus, Vim, Neovim, Zsh files ---
mkdir -p %{buildroot}%{_prefix}/share/kio/servicemenus
cp desktop/com.mitchellh.ghostty.desktop %{buildroot}%{_prefix}/share/kio/servicemenus/

mkdir -p %{buildroot}%{_prefix}/share/nautilus-python/extensions
cp extensions/ghostty.py %{buildroot}%{_prefix}/share/nautilus-python/extensions/

mkdir -p %{buildroot}%{_prefix}/share/nvim/site/{compiler,ftdetect,ftplugin,syntax}
cp nvim/*.vim %{buildroot}%{_prefix}/share/nvim/site/

mkdir -p %{buildroot}%{_prefix}/share/vim/vimfiles/{compiler,ftdetect,ftplugin,syntax}
cp vim/*.vim %{buildroot}%{_prefix}/share/vim/vimfiles/

mkdir -p %{buildroot}%{_prefix}/share/zsh/site-functions
cp completions/_ghostty %{buildroot}%{_prefix}/share/zsh/site-functions/

# --- D-Bus, systemd, locale, metainfo ---
mkdir -p %{buildroot}%{_prefix}/share/dbus-1/services
cp dbus/com.mitchellh.ghostty.service %{buildroot}%{_prefix}/share/dbus-1/services/

mkdir -p %{buildroot}%{_prefix}/share/systemd/user
cp systemd/app-com.mitchellh.ghostty.service %{buildroot}%{_prefix}/share/systemd/user/

mkdir -p %{buildroot}%{_prefix}/share/metainfo
cp metainfo/com.mitchellh.ghostty.metainfo.xml %{buildroot}%{_prefix}/share/metainfo/

mkdir -p %{buildroot}%{_prefix}/share/locale
cp -r locale/* %{buildroot}%{_prefix}/share/locale/

# --- Terminfo ---
mkdir -p %{buildroot}%{_prefix}/share/terminfo/x
cp terminfo/xterm-ghostty %{buildroot}%{_prefix}/share/terminfo/x/

%if 0%{?fedora} < 42
mkdir -p %{buildroot}%{_prefix}/share/terminfo/g
cp terminfo/ghostty %{buildroot}%{_prefix}/share/terminfo/g/
%endif

%files
%license LICENSE
%{_bindir}/ghostty
%{_prefix}/share/applications/com.mitchellh.ghostty.desktop
%{_prefix}/share/bash-completion/completions/ghostty.bash
%{_prefix}/share/bat/syntaxes/ghostty.sublime-syntax
%{_prefix}/share/fish/vendor_completions.d/ghostty.fish
%{_prefix}/share/ghostty
%{_prefix}/share/icons/hicolor
%{_prefix}/share/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_prefix}/share/man/man1/ghostty.1
%{_prefix}/share/man/man5/ghostty.5
%{_prefix}/share/nautilus-python/extensions/ghostty.py
%{_prefix}/share/nvim/site
%{_prefix}/share/vim/vimfiles
%{_prefix}/share/zsh/site-functions/_ghostty
%{_prefix}/share/dbus-1/services/com.mitchellh.ghostty.service
%{_prefix}/share/locale
%{_prefix}/share/metainfo/com.mitchellh.ghostty.metainfo.xml
%{_prefix}/share/systemd/user/app-com.mitchellh.ghostty.service
%{_prefix}/share/terminfo/x/xterm-ghostty
%if 0%{?fedora} < 42
%{_prefix}/share/terminfo/g/ghostty
%endif

%changelog
- Nightly snapshot build from latest tip commit
- Updated to Zig 0.15.2
