Name:           copyparty
Version:        1.19.1
Release:        1%{?dist}
Summary:        A standalone, multi-threaded, c-extensible web server.
License:        MIT
URL:            https://github.com/9001/copyparty
Source0:        https://github.com/9001/copyparty/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-jinja2
BuildRequires:  python3-build
# python3-strip-hints is not a system package, so we'll install it with pip.
# BuildRequires:  python3-strip-hints
BuildRequires:  python3-requests
BuildRequires:  python3-certifi

%description
Copyparty is a fast, standalone, c-extensible web server with a built-in UI for serving static files, archives, and directories.

%prep
%autosetup -p1 -n copyparty-%{version}

%build
# Install the build dependency 'strip-hints' using pip.
python3 -m pip install --user -U strip-hints

# Navigate to the scripts directory to run the build commands.
pushd scripts
# Download web dependencies from the latest GitHub release.
./make-sfx.sh fast dl-wd
# Build the copyparty-sfx.py standalone executable.
./make-sfx.sh gz fast
popd

%install
# Create the destination directory.
mkdir -p %{buildroot}/usr/local/bin

# The script is in the source directory after being built.
install -m 0755 copyparty-sfx.py %{buildroot}/usr/local/bin/copyparty-sfx.py

%files
/usr/local/bin/copyparty-sfx.py

%changelog
* Mon Aug 14 2025 monkeygold - 1.19.1-1
- Initial package using the correct build process.
