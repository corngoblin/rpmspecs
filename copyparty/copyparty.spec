Name:           copyparty
Version:        0.0.0
Release:        1%{?dist}
Summary:        A standalone, multi-threaded, c-extensible web server.
License:        MIT
URL:            https://github.com/9001/copyparty
Source0:        %{url}/archive/main/copyparty-main.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  python3-jinja2

%description
Copyparty is a fast, standalone, c-extensible web server with a built-in UI for serving static files, archives, and directories.

%prep
%autosetup -p1 -n copyparty-main

%build
# Use python3-pip to install the necessary build dependencies
python3 -m pip install --user -U build setuptools wheel jinja2 strip_hints

# Run the build process
python3 -m build

%install
# Create the destination directory
mkdir -p %{buildroot}/usr/local/bin

# Move the built copyparty-sfx.py file to the buildroot
# The built file is typically located in dist/
install -m 0755 dist/copyparty-sfx.py %{buildroot}/usr/local/bin/copyparty-sfx.py

%files
/usr/local/bin/copyparty-sfx.py

%changelog
* Mon Aug 12 2024 Your Name <your.email@example.com> - 0.0.0-1
- Initial package
