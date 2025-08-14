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
# The python3-strip-hints RPM does not exist, so it will be installed via pip.
# BuildRequires:  python3-strip-hints

%description
Copyparty is a fast, standalone, c-extensible web server with a built-in UI for serving static files, archives, and directories.

%prep
%autosetup -p1 -n copyparty-%{version}

%build
# Install the build dependencies from PyPI that are not available as RPMs.
python3 -m pip install --user -U strip-hints
# Use python3-pip to install the other necessary build dependencies
python3 -m pip install --user -U build setuptools wheel jinja2

# Run the build process
python3 -m build

%install
# Create the destination directory
mkdir -p %{buildroot}/usr/local/bin

# The built file is located in the dist/ directory
# Let's verify it exists and then move it.
install -m 0755 dist/copyparty-sfx.py %{buildroot}/usr/local/bin/copyparty-sfx.py

%files
/usr/local/bin/copyparty-sfx.py

%changelog
* Mon Aug 14 2025 monkeygold - 1.19.1-1
- Initial package using the latest tag
