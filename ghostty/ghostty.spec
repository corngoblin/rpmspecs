Name:           ghostty
Version:        1.1.3
Release:        1%{?dist}
Summary:        Fast, feature-rich, cross-platform terminal emulator with native UI and GPU acceleration

License:        MIT
URL:            https://github.com/ghostty-org/ghostty
Source0:        https://github.com/ghostty-org/ghostty/archive/refs/tags/v%{version}.tar.gz

ExclusiveArch:  x86_64 aarch64

BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk4-devel
BuildRequires:  harfbuzz-devel
BuildRequires:  libadwaita-devel
BuildRequires:  libpng-devel
BuildRequires:  oniguruma-devel
BuildRequires:  pandoc-cli
BuildRequires:  pixman-devel
BuildRequires:  pkg-config
BuildRequires:  wayland-protocols-devel
BuildRequires:  zig
BuildRequires:  zlib-ng-devel

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
%{summary}.

%prep
%setup -q -n ghostty-%{version}

# Fix Zig enum literal in build.zig.zon (Zig enums do not accept quoted strings)
sed -i 's/\.name = "ghostty"/.name = ghostty/' build.zig.zon

%build
zig build \
    --summary all \
    --prefix "%{_prefix}" \
    -Dversion-string=%{version}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Demit-docs

%install
rm -rf %{buildroot}

# Install the compiled binary
install -Dm755 zig-out/bin/ghostty %{buildroot}%{_bindir}/ghostty

# Install data files - adjust paths if needed
install -Dm644 data/com.mitchellh.ghostty.desktop %{buildroot}%{_datadir}/applications/com.mitchellh.ghostty.desktop
install -Dm644 data/com.mitchellh.ghostty.kio.desktop %{buildroot}%{_datadir}/kio/servicemenus/com.mitchellh.ghostty.desktop

install -Dm644 data/icons/ghostty-1024.png %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps/com.mitchellh.ghostty.png
install -Dm644 data/icons/ghostty-128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/com.mitchellh.ghostty.png
install -Dm644 data/icons/ghostty-16.png %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/com.mitchellh.ghostty.png
install -Dm644 data/icons/ghostty-256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/com.mitchellh.ghostty.png
install -Dm644 data/icons/ghostty-32.png %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/com.mitchellh.ghostty.png
install -Dm644 data/icons/ghostty-512.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/com.mitchellh.ghostty.png

# Install completion scripts
install -Dm644 completions/ghostty.bash %{buildroot}%{_datadir}/bash-completion/completions/ghostty
install -Dm644 completions/ghostty.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/ghostty.fish

# Install syntax files
cp -a syntax %{buildroot}%{_datadir}/ghostty

# Install man pages
install -Dm644 man/ghostty.1 %{buildroot}%{_mandir}/man1/ghostty.1
install -Dm644 man/ghostty.5 %{buildroot}%{_mandir}/man5/ghostty.5

# Install nautilus extension
install -Dm644 nautilus/ghostty.py %{buildroot}%{_datadir}/nautilus-python/extensions/ghostty.py

# Install vim, nvim, zsh files
cp -a vim %{buildroot}%{_datadir}/vim/vimfiles
cp -a nvim %{buildroot}%{_datadir}/nvim/site
install -Dm644 completions/_ghostty %{buildroot}%{_datadir}/zsh/site-functions/_ghostty

# Install terminfo files
install -Dm644 terminfo/x/xterm-ghostty %{buildroot}%{_datadir}/terminfo/x/xterm-ghostty
%if 0%{?fedora} != 42
install -Dm644 terminfo/g/ghostty %{buildroot}%{_datadir}/terminfo/g/ghostty
%endif

%files
%license LICENSE
%{_bindir}/ghostty
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_datadir}/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_datadir}/icons/hicolor/*/apps/com.mitchellh.ghostty.png
%{_datadir}/bash-completion/completions/ghostty
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/ghostty
%{_mandir}/man1/ghostty.1
%{_mandir}/man5/ghostty.5
%{_datadir}/nautilus-python/extensions/ghostty.py
%{_datadir}/vim/vimfiles
%{_datadir}/nvim/site
%{_datadir}/zsh/site-functions/_ghostty
%{_datadir}/terminfo/x/xterm-ghostty
%if 0%{?fedora} != 42
%{_datadir}/terminfo/g/ghostty
%endif

%changelog
%autochangelog
