Name:           duckstation
Version:        0.1.9226
Release:        1%{?dist}
Summary:        Fast PlayStation 1 emulator

License:        CC-BY-NC-ND-4.0
URL:            https://github.com/stenzek/duckstation
Source0:        https://github.com/stenzek/duckstation/archive/refs/tags/v0.1-9226.tar.gz#/duckstation-%{version}.tar.gz
Patch0:         duckstation-find_appropriate_shaderc.patch
Patch1:         duckstation-stop_nagging.patch

BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc-c++
BuildRequires:  clang-devel
BuildRequires:  lld
BuildRequires:  extra-cmake-modules
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtmultimedia-devel
BuildRequires:  qt6-qtshadertools-devel
BuildRequires:  qt6-qtx11extras-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  qt6-qtdeclarative-devel
BuildRequires:  qt6-qt5compat-devel
BuildRequires:  SDL2-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  vulkan-devel
BuildRequires:  minizip-compat-devel
BuildRequires:  zlib-devel
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  pkgconfig
BuildRequires:  glslang-devel
BuildRequires:  imgui-devel

ExclusiveArch:  x86_64 aarch64

%description
DuckStation is a fast and accurate PlayStation 1 emulator,
focused on speed, playability, and long-term maintainability.

%prep
%autosetup -p1 -n duckstation-%{version}
# Fix patches similar to openSUSE spec
sed -i -e '/ENABLE_DISCORD_PRESENCE 1/d' src/core/system.cpp || :
sed -i '/DiscordRPC/d' CMakeModules/DuckStationDependencies.cmake || :

%build
ulimit -Sn 4000

# Use clang and lld if available (fallback to gcc/g++)
%ifarch x86_64 aarch64
export CC=clang
export CXX=clang++
export LD=ld.lld
export LDFLAGS="-fuse-ld=lld -Wl,--gc-sections -Wl,-O1 -Wl,--icf=safe"
export CFLAGS="%{optflags} -fPIC -O3"
export CXXFLAGS="%{optflags} -fPIC -O3"
%else
export CC=gcc
export CXX=g++
export LD=ld.gold
export LDFLAGS="-fuse-ld=gold -Wl,--gc-sections -Wl,-O1"
export CFLAGS="%{optflags} -fPIC -O3"
export CXXFLAGS="%{optflags} -fPIC -O3"
%endif

%cmake .. \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DUSE_PCH=OFF \
  -DENABLE_PCH=OFF \
  -DENABLE_PRECOMPILED_HEADERS=OFF \
  -DSKIP_PRECOMPILE_HEADERS=ON \
  -DUSE_PRECOMPILED_HEADERS=OFF \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DCMAKE_C_COMPILER=${CC} \
  -DCMAKE_CXX_COMPILER=${CXX} \
  -DCMAKE_LINKER=${LD} \
  -DCMAKE_C_FLAGS="${CFLAGS}" \
  -DCMAKE_CXX_FLAGS="${CXXFLAGS}" \
  -DCMAKE_EXE_LINKER_FLAGS="${LDFLAGS}" \
  -DENABLE_DISCORD_PRESENCE=OFF \
  -DUSE_FBDEV=ON \
  -DBUILD_SHARED_LIBS=OFF \
  -DBUILD_STATIC_LIBS=ON

%ninja_build

%install
mkdir -p %{buildroot}%{_libexecdir}/%{name}
mv %{_builddir}/duckstation-%{version}/build/bin/* %{buildroot}%{_libexecdir}/%{name}/

mkdir -p %{buildroot}%{_bindir}
ln -s %{_libexecdir}/%{name}/%{name}-qt %{buildroot}%{_bindir}/

install -d -m 0755 %{buildroot}%{_datadir}/pixmaps
ln -s %{_libexecdir}/%{name}/resources/images/duck.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=DuckStation
Comment=%{summary}
Exec=%{_bindir}/%{name}-qt
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=Game;Emulator;
EOF

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}-qt
%{_libexecdir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop

%changelog
* Thu Jul 01 2025 Monkeygold <you@example.com> - 0.1.9226-1
- Improved Fedora spec with clang/lld support and patches from openSUSE spec
- Disabled Discord presence, added explicit install layout
