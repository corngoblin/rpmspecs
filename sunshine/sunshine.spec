The mv: cannot stat 'rpmspecs/sunshine': No such file or directory error is the key. It shows that your manual directory manipulation in the %prep section is incorrect for how the COPR build system sets up the Git repository.

To fix this, we need to adapt the %prep section to the correct directory structure that COPR uses. The simplest and most reliable way is to let the rpmbuild environment handle the directories for you and avoid manual mv and cd commands.

Here is the corrected spec file with a simplified and more robust %prep section:

%global build_timestamp %(date +"%Y%m%d")

# Define the GitHub repository owner and name
%global github_owner LizardByte
%global github_repo Sunshine

Name: Sunshine
# Set a placeholder version that will be updated later.
# We will use the git tag for the version and a date for the release.
Version: 0.1
Release: %{build_timestamp}%{?dist}
Summary: Self-hosted game stream host for Moonlight.
License: GPLv3-only
URL: https://github.com/LizardByte/Sunshine

# Add jq as a build dependency so it's available when we need it.
BuildRequires: jq
BuildRequires: appstream
BuildRequires: cmake >= 3.25.0
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: libayatana-appindicator3-devel
BuildRequires: libcap-devel
BuildRequires: libcurl-devel
BuildRequires: libdrm-devel
BuildRequires: libevdev-devel
BuildRequires: libgudev
BuildRequires: libnotify-devel
BuildRequires: libva-devel
BuildRequires: libX11-devel
BuildRequires: libxcb-devel
BuildRequires: libXcursor-devel
BuildRequires: libXfixes-devel
BuildRequires: libXi-devel
BuildRequires: libXinerama-devel
BuildRequires: libXrandr-devel
BuildRequires: libXtst-devel
BuildRequires: git
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libgbm-devel
BuildRequires: miniupnpc-devel
BuildRequires: npm
BuildRequires: numactl-devel
BuildRequires: openssl-devel
BuildRequires: opus-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: rpm-build
BuildRequires: systemd-udev
BuildRequires: systemd-rpm-macros
%{?sysusers_requires_compat}
BuildRequires: wget
BuildRequires: which

# for unit tests
BuildRequires: xorg-x11-server-Xvfb

# Conditional BuildRequires for cuda-gcc based on Fedora version
%if 0%{?fedora} <= 41
BuildRequires: gcc13
BuildRequires: gcc13-c++
%global gcc_version 13
%global cuda_version 12.9.1
%global cuda_build 575.57.08
%elif %{?fedora} >= 42
BuildRequires: gcc14
BuildRequires: gcc14-c++
%global gcc_version 14
%global cuda_version 12.9.1
%global cuda_build 575.57.08
%endif

%global cuda_dir %{_builddir}/cuda

Requires: libcap >= 2.22
Requires: libcurl >= 7.0
Requires: libdrm > 2.4.97
Requires: libevdev >= 1.5.6
Requires: libopusenc >= 0.2.1
Requires: libva >= 2.14.0
Requires: libwayland-client >= 1.20.0
Requires: libX11 >= 1.7.3.1
Requires: miniupnpc >= 2.2.4
Requires: numactl-libs >= 2.0.14
Requires: openssl >= 3.0.2
Requires: pulseaudio-libs >= 10.0
Requires: libayatana-appindicator3 >= 0.5.3

%description
Self-hosted game stream host for Moonlight.

%prep
# Exit on error.
set -e

# Fetch the latest release tag from GitHub using curl and jq.
# Since this is done in the %prep section, jq is guaranteed to be available.
release_tag=$(curl -s https://api.github.com/repos/%{github_owner}/%{github_repo}/releases/latest | jq -r '.tag_name')
if [ -z "$release_tag" ]; then
    echo "Error: Could not retrieve latest release tag." >&2
    exit 1
fi

# The COPR build system automatically clones the repository.
# We just need to ensure the correct version is used for building.
# The following commands will update the version and prepare the source for the build.
git clone https://github.com/%{github_owner}/%{github_repo}.git Sunshine
cd Sunshine
git checkout $release_tag
git submodule update --init --recursive
rm -rf .git*
# Now, the source directory is ready for the build.
# We also create a tarball to satisfy the rpmbuild's requirement for a source tarball.
tar -czf ../Sunshine-$release_tag.tar.gz .

%setup -q -n Sunshine-$release_tag


%build
# exit on error
set -e

# Detect the architecture and Fedora version
architecture=$(uname -m)

cuda_supported_architectures=("x86_64" "aarch64")

# prepare CMAKE args
cmake_args=(
  "-B=build"
  "-G=Unix Makefiles"
  "-S=."
  "-DBUILD_DOCS=OFF"
  "-DBUILD_WERROR=ON"
  "-DCMAKE_BUILD_TYPE=Release"
  "-DCMAKE_INSTALL_PREFIX=%{_prefix}"
  "-DSUNSHINE_ASSETS_DIR=%{_datadir}/sunshine"
  "-DSUNSHINE_EXECUTABLE_PATH=%{_bindir}/sunshine"
  "-DSUNSHINE_ENABLE_WAYLAND=ON"
  "-DSUNSHINE_ENABLE_X11=ON"
  "-DSUNSHINE_ENABLE_DRM=ON"
  "-DSUNSHINE_PUBLISHER_NAME=LizardByte"
  "-DSUNSHINE_PUBLISHER_WEBSITE=https://app.lizardbyte.dev"
  "-DSUNSHINE_PUBLISHER_ISSUE_URL=https://app.lizardbyte.dev/support"
)

export CC=gcc-%{gcc_version}
export CXX=g++-%{gcc_version}

function install_cuda() {
  # check if we need to install cuda
  if [ -f "%{cuda_dir}/bin/nvcc" ]; then
    echo "cuda already installed"
    return
  fi

  local cuda_prefix="https://developer.download.nvidia.com/compute/cuda/"
  local cuda_suffix=""
  if [ "$architecture" == "aarch64" ]; then
    local cuda_suffix="_sbsa"
  fi

  local url="${cuda_prefix}%{cuda_version}/local_installers/cuda_%{cuda_version}_%{cuda_build}_linux${cuda_suffix}.run"
  echo "cuda url: ${url}"
  wget \
    "$url" \
    --progress=bar:force:noscroll \
    --retry-connrefused \
    --tries=3 \
    -q -O "%{_builddir}/cuda.run"
  chmod a+x "%{_builddir}/cuda.run"
  "%{_builddir}/cuda.run" \
    --no-drm \
    --no-man-page \
    --no-opengl-libs \
    --override \
    --silent \
    --toolkit \
    --toolkitpath="%{cuda_dir}"
  rm "%{_builddir}/cuda.run"

  # we need to patch math_functions.h on fedora 42
  # see https://forums.developer.nvidia.com/t/error-exception-specification-is-incompatible-for-cospi-sinpi-cospif-sinpif-with-glibc-2-41/323591/3
  if [ "%{?fedora}" -eq 42 ]; then
    echo "Original math_functions.h:"
    find "%{cuda_dir}" -name math_functions.h -exec cat {} \;

    # Apply the patch
    patch -p2 \
      --backup \
      --directory="%{cuda_dir}" \
      --verbose \
      < "%{_builddir}/Sunshine/packaging/linux/patches/${architecture}/01-math_functions.patch"
  fi
}

if [ -n "%{cuda_version}" ] && [[ " ${cuda_supported_architectures[@]} " =~ " ${architecture} " ]]; then
  install_cuda
  cmake_args+=("-DSUNSHINE_ENABLE_CUDA=ON")
  cmake_args+=("-DCMAKE_CUDA_COMPILER:PATH=%{cuda_dir}/bin/nvcc")
  cmake_args+=("-DCMAKE_CUDA_HOST_COMPILER=gcc-%{gcc_version}")
else
  cmake_args+=("-DSUNSHINE_ENABLE_CUDA=OFF")
fi

# setup the version
export BUILD_VERSION=v%{release_tag}

# cmake
echo "cmake args:"
echo "${cmake_args[@]}"
cmake "${cmake_args[@]}"
make -j$(nproc) -C "build"

%check
# validate the metainfo file
appstreamcli validate %{buildroot}%{_metainfodir}/*.metainfo.xml
appstream-util validate %{buildroot}%{_metainfodir}/*.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

# run tests
cd build
xvfb-run ./tests/test_sunshine

%install
cd build
%make_install

# Add modules-load configuration
# load the uhid module in initramfs even if it doesn't detect the module as being used during dracut
# which must be run every time a new kernel is installed
install -D -m 0644 /dev/stdin %{buildroot}/usr/lib/modules-load.d/uhid.conf <<EOF
uhid
EOF

%post
# Note: this is copied from the postinst script
# Check if we're in an rpm-ostree environment
if [ ! -x "$(command -v rpm-ostree)" ]; then
  echo "Not in an rpm-ostree environment, proceeding with post install steps."

  # Trigger udev rule reload for /dev/uinput and /dev/uhid
  path_to_udevadm=$(which udevadm)
  if [ -x "$path_to_udevadm" ]; then
    echo "Reloading udev rules."
    $path_to_udevadm control --reload-rules
    $path_to_udevadm trigger --property-match=DEVNAME=/dev/uinput
    $path_to_udevadm trigger --property-match=DEVNAME=/dev/uhid
    echo "Udev rules reloaded successfully."
  else
    echo "error: udevadm not found or not executable."
  fi
else
  echo "rpm-ostree environment detected, skipping post install steps. Restart to apply the changes."
fi

%preun
# Remove modules-load configuration
rm -f /usr/lib/modules-load.d/uhid.conf

%files
# Executables
%caps(cap_sys_admin+p) %{_bindir}/sunshine
%caps(cap_sys_admin+p) %{_bindir}/sunshine-*

# Systemd unit file for user services
%{_userunitdir}/sunshine.service

# Udev rules
%{_udevrulesdir}/*-sunshine.rules

# Modules-load configuration
%{_modulesloaddir}/uhid.conf

# Desktop entries
%{_datadir}/applications/*.desktop

# Icons
%{_datadir}/icons/hicolor/scalable/apps/sunshine.svg
%{_datadir}/icons/hicolor/scalable/status/sunshine*.svg

# Metainfo
%{_datadir}/metainfo/*.metainfo.xml

# Assets
%{_datadir}/sunshine/**

%changelog
* Fri Aug 15 2025 Monkeygold
