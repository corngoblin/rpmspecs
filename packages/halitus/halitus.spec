%global debug_package %{nil}

Name:           halitus
Version:        0.1.0
Release:        0.1.beta1
Summary:        Map the 2026 Steam Controller to a gamepad, mouse and keyboard
License:        GPL-3.0-or-later
URL:            https://github.com/corngoblin/halitus

# The source tarball is built from the tagged commit with `git archive`, so the prefix is halitus-0.1.0/.
# It is a local Source rather than a URL on purpose: the upstream repository is private while the project is in
# beta, so COPR cannot fetch it, and the SRPM carries the tarball instead. When the repository opens, replace
# Source0 with the archive URL for the release tag.
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  rust cargo
BuildRequires:  pkgconfig
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  gtk-update-icon-cache

%description
Halitus reads the 2026 Steam Controller directly over HID, maps its buttons, sticks, trackpads, triggers,
paddles and gyroscope with its own engine, and presents the result to games as a standard virtual gamepad,
pointer and keyboard.

Because everything is translated into inputs a game already understands, mappings work with XInput-only games
under Proton, native Linux games and emulators alike: a rear paddle can become a keyboard key, gyro can steer a
thumbstick, and a trackpad can act as a stick.

This package installs the graphical application, the background service, the command-line diagnostics and the
udev rules that let a normal user read the controller.

%prep
%autosetup -n %{name}-%{version}

%build
# The library crates are dependency-free, but the GUI is built on the gtk4 and libadwaita crates, so the build
# needs the registry. COPR has network enabled for this project, and --locked pins every crate to the version in
# Cargo.lock, so a build cannot drift silently. Vendoring for a fully offline build is the next step for a stable
# release; it trades source size for not depending on crates.io being reachable.
cargo build --release --workspace --locked

%install
install -Dpm0755 target/release/halitus %{buildroot}%{_bindir}/halitus
install -Dpm0755 target/release/halitus-service %{buildroot}%{_bindir}/halitus-service
install -Dpm0755 target/release/halitusctl %{buildroot}%{_bindir}/halitusctl

install -Dpm0644 data/org.corngoblin.Halitus.desktop %{buildroot}%{_datadir}/applications/org.corngoblin.Halitus.desktop
install -Dpm0644 data/org.corngoblin.Halitus.metainfo.xml %{buildroot}%{_metainfodir}/org.corngoblin.Halitus.metainfo.xml
install -Dpm0644 data/org.corngoblin.Halitus.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/org.corngoblin.Halitus.svg

install -Dpm0644 packaging/systemd/halitus.service %{buildroot}%{_userunitdir}/halitus.service
install -Dpm0644 packaging/rpm/dev-rules/99-halitus-dev.rules %{buildroot}%{_udevrulesdir}/99-halitus.rules

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.corngoblin.Halitus.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.corngoblin.Halitus.metainfo.xml

%post
%udev_rules_update
%desktop_database_post
%icon_theme_cache_post

%postun
%udev_rules_update
%desktop_database_postun
%icon_theme_cache_postun

%files
%license LICENSE
%doc README.md
%{_bindir}/halitus
%{_bindir}/halitus-service
%{_bindir}/halitusctl
%{_datadir}/applications/org.corngoblin.Halitus.desktop
%{_metainfodir}/org.corngoblin.Halitus.metainfo.xml
%{_datadir}/icons/hicolor/scalable/apps/org.corngoblin.Halitus.svg
%{_userunitdir}/halitus.service
%{_udevrulesdir}/99-halitus.rules

%changelog
* Tue Nov 17 2026 corngoblin <corngoblin@users.noreply.github.com> - 0.1.0-0.1.beta1
- First beta: 2026 Steam Controller support, native mapping engine, virtual gamepad with force feedback,
  keyboard and mouse output, and a graphical binding editor.
