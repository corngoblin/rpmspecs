Name:           ghostty
Version:        1.1.3
Release:        1%{?dist}
Summary:        A minimal, fast, and keyboard-centric terminal emulator

License:        MIT
URL:            https://github.com/ghostty-org/ghostty
Source0:        https://github.com/ghostty-org/ghostty/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  zig
BuildRequires:  scdoc
BuildRequires:  fontconfig-devel
BuildRequires:  wayland-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  libGL-devel

%description
Ghostty is a modern terminal emulator focused on performance and a minimalist keyboard-centric interface.

%prep
%setup -q
# Fix .zon file to include fingerprint in TOML format
sed -i '1ifingerprint = "0x64407a2a0b4147e5"' build.zig.zon

%build
export ZIG_LOCAL_CACHE_DIR=$PWD/.zig-cache
export ZIG_GLOBAL_CACHE_DIR=$PWD/.zig-cache
export ZIG_TELEMETRY_DISABLED=1

zig build -Drelease-safe

%install
mkdir -p %{buildroot}%{_bindir}
install -m 0755 zig-out/bin/ghostty %{buildroot}%{_bindir}/ghostty

mkdir -p %{buildroot}%{_mandir}/man1
install -m 0644 man/ghostty.1 %{buildroot}%{_mandir}/man1/

%files
%license LICENSE
%doc README.md
%{_bindir}/ghostty
%{_mandir}/man1/ghostty.1*

%changelog
* 
- Initial RPM package for Ghostty terminal emulator
