Name:           ghostty
Version:        1.1.3
Release:        1%{?dist}
Summary:        Fast, feature-rich modern terminal

License:        MPL-2.0
URL:            https://github.com/wasamasa/ghostty
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  git-core
BuildRequires:  zig
BuildRequires:  libxkbcommon-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libinput-devel
BuildRequires:  systemd-rpm-macros

%description
Ghostty is a modern, fast and GPU-accelerated terminal emulator.

%prep
%autosetup -n %{name}-v%{version}

# Patch build.zig.zon so that zig can fetch required packages.
# This assumes you're using zig's package manager for dependencies.
sed -i '1s/^\.{/{ fingerprint = 0x64407a2a5ee614e9; /' build.zig.zon
sed -i 's/\.name = "ghostty"/.name = .ghostty/' build.zig.zon

%build
zig build \
  --summary all \
  --prefix %{_prefix} \
  -Dversion-string=%{version}-%{release} \
  -Doptimize=ReleaseSafe \
  -Dcpu=baseline \
  -Dpie=true \
  -Demit-docs

%install
rm -rf %{buildroot}
install -d %{buildroot}%{_bindir}
install -m 0755 zig-out/bin/ghostty %{buildroot}%{_bindir}/ghostty

%files
%license LICENSE
%doc README.md
%{_bindir}/ghostty

%changelog
* Mon Jul 29 2025 Your Name <you@example.com> - 1.1.3-1
- Initial package for ghostty
