Name:           duckstation
Version:        0.1.9226
Release:        1%{?dist}
Summary:        Fast PlayStation 1 emulator

License:        GPL-3.0-only
URL:            https://github.com/stenzek/duckstation
Source0:        https://github.com/stenzek/duckstation/archive/refs/tags/v0.1-9226.tar.gz#/duckstation-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qt5compat-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qtshadertools-devel
BuildRequires:  zlib-devel
BuildRequires:  libpng-devel
BuildRequires:  SDL2-devel
BuildRequires:  minizip-compat-devel

ExclusiveArch:  x86_64 aarch64

%description
DuckStation is a fast and accurate PlayStation 1 emulator, focused on speed,
playability, and long-term maintainability.

%prep
%autosetup -n duckstation-0.1-9226

%build
%cmake -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DUSE_QT6=ON \
    -DDUCKSTATION_QT_UI=ON

%ninja_build -C build

%install
%ninja_install -C build

# Desktop integration (if provided)
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    %{buildroot}%{_datadir}/applications/org.duckstation.DuckStation.desktop || :

%files
%license LICENSE
%doc README.md
%{_bindir}/duckstation-qt
%{_datadir}/applications/org.duckstation.DuckStation.desktop
%{_datadir}/icons/hicolor/*/apps/org.duckstation.DuckStation.png

%changelog
* Thu Jul 031 2025 Monkeygold - 0.1.9226-1
- Update to latest tag v0.1-9226
