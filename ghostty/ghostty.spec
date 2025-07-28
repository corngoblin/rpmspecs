Name:           ghostty
Version:        1.1.3
Release:        1%{?dist}
Summary:        A fast, feature-rich modern terminal emulator

License:        MPL-2.0
URL:            https://github.com/ghostty-org/ghostty
Source0:        https://github.com/ghostty-org/ghostty/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  git
BuildRequires:  zig >= 0.12.0
BuildRequires:  which

ExclusiveArch:  x86_64 aarch64

%description
Ghostty is a modern terminal emulator with GPU-accelerated rendering, fast startup,
and native configuration using Lua. This package builds Ghostty using Zig.

%prep
%autosetup -n %{name}-%{version}

# Patch build.zig.zon for Zig 0.12 compatibility:
# - Fix deprecated `.name` format
# - Add required `.fingerprint` field
sed -i 's/\.name = "ghostty"/.name = .ghostty/' build.zig.zon
sed -i '1i.fingerprint = 0x64407a2a0b4147e5,' build.zig.zon

%build
export ZIG_LOCAL_CACHE_DIR=$PWD/.zig-cache
export ZIG_GLOBAL_CACHE_DIR=$PWD/.zig-cache
export ZIG_TELEMETRY_DISABLED=1

zig build -Drelease-safe

%install
install -Dm755 zig-out/bin/ghostty -t %{buildroot}%{_bindir}

%files
%license LICENSE
%doc README.md
%{_bindir}/ghostty

%changelog
* Mon Jul 29 2025 Rob <you@example.com> - 1.1.3-1
- Initial build for Fedora with Zig 0.12 patch and ghostty-org repo URL
