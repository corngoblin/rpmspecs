Name:           ghostty
Version:        1.1.3
Release:        1%{?dist}
Summary:        Fast, GPU-accelerated, and cross-platform terminal emulator

License:        MIT
URL:            https://github.com/ghostty-org/ghostty
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

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
Ghostty is a modern terminal emulator that is GPU-accelerated, cross-platform, and leverages native system UI components.

%prep
%autosetup -n ghostty-%{version}

# Fix .zon enum formatting (Zig requires bare enum identifiers)
sed -i 's/\.name = "ghostty"/.name = .ghostty/' build.zig.zon

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
install -Dm0755 zig-out/bin/ghostty %{buildroot}%{_bindir}/ghostty

%files
%license LICENSE
%doc README.md
%{_bindir}/ghostty

%changelog
* Mon Jul 29 2025 Monkeygold <monkeygold@example.com> - 1.1.3-1
- Initial COPR package
