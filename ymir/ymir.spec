%global debug_package %{nil}

Name:           ymir
Version:        0.1.7
Release:        1%{?dist}
Summary:        A Sega Saturn emulator

License:        GPLv3
URL:            https://github.com/StrikerX3/Ymir
# Source0:        https://github.com/StrikerX3/Ymir/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  git
BuildRequires:  make

# SDL3 dependencies
BuildRequires:  alsa-lib-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  nas-devel
BuildRequires:  pipewire-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXi-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  dbus-devel
BuildRequires:  ibus-devel
BuildRequires:  systemd-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  vulkan-devel
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libdrm-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libusb1-devel
BuildRequires:  libdecor-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  liburing-devel

%description
Ymir is an open-source Sega Saturn emulator.

%prep
# Clone the repository with submodules
git clone --recursive https://github.com/StrikerX3/Ymir.git
cd Ymir

# Checkout the specific version tag
git checkout v%{version}

# Remove the .git directory to create a clean source tree
rm -rf .git

%build
# Set the compiler to Clang as recommended
export CC=clang
export CXX=clang++

# Move into the source directory created by git clone
cd Ymir

# Configure a release build with optimizations
cmake -S . -B build \
  -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_INSTALL_PREFIX=%{_prefix} \
  -DYmir_AVX2=ON \
  -DYmir_ENABLE_DEVLOG=OFF \
  -DYmir_ENABLE_IMGUI_DEMO=OFF \
  -DYmir_EXTRA_INLINING=ON

# Build the project
cmake --build build --parallel

%install
# Move into the source directory before running install commands
cd Ymir

# Let CMake handle the installation to the correct prefix, using DESTDIR
cmake --install build --prefix /usr --install-destdir %{buildroot}

# Move and rename the executable to /usr/bin
mv %{buildroot}%{_bindir}/ymir-sdl3 %{buildroot}%{_bindir}/ymir

# Install the desktop file
install -Dm0644 apps/ymir-sdl3/res/io.github.strikerx3.ymir.desktop %{buildroot}%{_datadir}/applications/io.github.strikerx3.ymir.desktop

# Install the icon file with the generic name "ymir.png" so the desktop file can find it
install -Dm0644 apps/ymir-sdl3/res/ymir.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/ymir.png


%files
%doc
%{_bindir}/ymir
%{_datadir}/applications/io.github.strikerx3.ymir.desktop
%{_datadir}/icons/hicolor/256x256/apps/ymir.png

%changelog
