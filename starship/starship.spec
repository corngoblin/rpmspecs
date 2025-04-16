%global debug_package %{nil}
%undefine _package_note_file

Name: starship
Version: 1.22.0
Release: 1%{?dist}
Summary: â˜„ðŸŒŒï¸ The minimal, blazing-fast, and infinitely customizable prompt for any shell!

License: ISC
URL: https://github.com/starship/starship
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: cargo >= 1.80
BuildRequires: cmake3
BuildRequires: gcc
BuildRequires: rust >= 1.80

BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(zlib)

%description
The minimal, blazing-fast, and infinitely customizable prompt for any shell!

  - Fast: it's fast â€“ really really fast! ðŸš€
  - Customizable: configure every aspect of your prompt.
  - Universal: works on any shell, on any operating system.
  - Intelligent: shows relevant information at a glance.
  - Feature rich: support for all your favorite tools.
  - Easy: quick to install â€“ start using it in minutes.


%prep
%autosetup


%install
export CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_OPT_LEVEL=3
export CMAKE=cmake3
RUSTFLAGS='-C strip=symbols' cargo install --root=%{buildroot}%{_prefix} --path=.
rm -f %{buildroot}%{_prefix}/.crates.toml \
    %{buildroot}%{_prefix}/.crates2.json


%files
%license LICENSE
%doc README.md CONTRIBUTING.md
%{_bindir}/%{name}


