Name:           ghostty
Version:        1.1.3
Release:        1%{?dist}
Summary:        Fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration

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

# Fix Zig enum literal: replace `.name = "ghostty"` with `.name = .ghostty`
sed -i 's/\.name = "ghostty"/.name = .ghostty/' build.zig.zon

%build
zig build \
    --summary all \
    --prefix "%{buildroot}%{_prefix}" \
    -Dversion-string=%{version}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Demit-docs

%if 0%{?fedora} == 42
rm -f "%{buildroot}%{_prefix}/share/terminfo/g/ghostty"
%endif

%files
%license LICENSE
%{_bindir}/ghostty
%{_prefix}/share/applications/com.mitchellh.ghostty.desktop
%{_prefix}/share/bash-completion/completions/ghostty.bash
%{_prefix}/share/bat/syntaxes/ghostty.sublime-syntax
%{_prefix}/share/fish/vendor_completions.d/ghostty.fish
%{_prefix}/share/ghostty
%{_prefix}/share/icons/hicolor/*/apps/com.mitchellh.ghostty.png
%{_prefix}/share/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_prefix}/share/man/man1/ghostty.1
%{_prefix}/share/man/man5/ghostty.5
%{_prefix}/share/nautilus-python/extensions/ghostty.py
%{_prefix}/share/nvim/site/**/*ghostty.vim
%{_prefix}/share/vim/vimfiles/**/*ghostty.vim
%{_prefix}/share/zsh/site-functions/_ghostty
%{_prefix}/share/terminfo/x/xterm-ghostty
%if 0%{?fedora} != 42
%{_prefix}/share/terminfo/g/ghostty
%endif

%changelog
%autochangelog
