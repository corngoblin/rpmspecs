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
%{summary}

%prep
%setup -q

%build
zig build \
    --prefix "%{_prefix}" \
    -Dversion-string=%{version}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Demit-docs

%install
rm -rf %{buildroot}
zig build install --prefix "%{buildroot}%{_prefix}"

# Remove ghostty terminfo on Fedora 42 due to packaging conflict
%if 0%{?fedora} == 42
    rm -f %{buildroot}%{_datadir}/terminfo/g/ghostty
%endif

%files
%license LICENSE
%{_bindir}/ghostty
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_datadir}/bash-completion/completions/ghostty.bash
%{_datadir}/bat/syntaxes/ghostty.sublime-syntax
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/ghostty
%{_datadir}/icons/hicolor/*/apps/com.mitchellh.ghostty.png
%{_datadir}/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_mandir}/man1/ghostty.1*
%{_mandir}/man5/ghostty.5*
%{_datadir}/nautilus-python/extensions/ghostty.py
%{_datadir}/nvim/site/**/ghostty.vim
%{_datadir}/vim/vimfiles/**/ghostty.vim
%{_datadir}/zsh/site-functions/_ghostty
%{_datadir}/terminfo/x/xterm-ghostty
%if 0%{?fedora} != 42
    %{_datadir}/terminfo/g/ghostty
%endif

%changelog
%autochangelog
