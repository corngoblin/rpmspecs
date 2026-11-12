Name:           ghostty
Version:        1.4.0
Release:        1%{?dist}
Summary:        Fast, feature-rich, and cross-platform terminal emulator that uses platform-native UI and GPU acceleration


License:        MIT
URL:            https://ghostty.org
Source0:        https://github.com/ghostty-org/ghostty/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz

# Ghostty pins the exact Zig release it is developed against (minimum_zig_version
# in build.zig.zon) and refuses to build with anything older. Fedora 44 and 45
# ship Zig 0.16, so the official upstream toolchain release is used instead of
# the distribution package. Bump this together with Version.
%global zigver 0.17.0
%ifarch x86_64
Source1:        https://ziglang.org/download/%{zigver}/zig-x86_64-linux-%{zigver}.tar.xz
%endif
%ifarch aarch64
Source2:        https://ziglang.org/download/%{zigver}/zig-aarch64-linux-%{zigver}.tar.xz
%endif


ExclusiveArch: x86_64 aarch64

# Single definition of the build invocation, used for both compiling and for the
# DESTDIR install pass in %%install.
%global zig_build zig build --summary all --prefix "%{_prefix}" -Dversion-string=%{version}-%{release} -Doptimize=ReleaseFast -Dcpu=baseline -Dpie=true -Demit-docs


BuildRequires: blueprint-compiler
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
BuildRequires: glib2-devel
BuildRequires: gtk4-devel
BuildRequires: gtk4-layer-shell-devel
BuildRequires: harfbuzz-devel
BuildRequires: libadwaita-devel
BuildRequires: libpng-devel
BuildRequires: oniguruma-devel
BuildRequires: pandoc-cli
BuildRequires: pixman-devel
BuildRequires: pkg-config
BuildRequires: wayland-protocols-devel
BuildRequires: zlib-ng-devel
BuildRequires: desktop-file-utils
BuildRequires: xz


Requires: fontconfig
Requires: freetype
Requires: glib2
Requires: gtk4
Requires: harfbuzz
Requires: libadwaita
Requires: libpng
Requires: oniguruma
Requires: pixman
Requires: zlib-ng


%description
%{summary}.

Ghostty is a terminal emulator that differentiates itself by being fast,
feature-rich, and native. While there are many excellent terminal emulators
available, Ghostty aims to leverage native platform features and modern
tooling to create a fast, feature-rich, and native terminal emulator.


%prep
%setup -q -n %{name}-%{version}

%ifarch x86_64
tar xf %{SOURCE1}
mv zig-x86_64-linux-%{zigver} zig-toolchain
%endif
%ifarch aarch64
tar xf %{SOURCE2}
mv zig-aarch64-linux-%{zigver} zig-toolchain
%endif


%build
export PATH="%{_builddir}/%{name}-%{version}/zig-toolchain:$PATH"
zig version

# The Zig dependencies listed in build.zig.zon are the hash-verified tarballs
# published by upstream on deps.files.ghostty.org; they are fetched during the
# build, which is why the COPR project keeps network access enabled for builds.
%zig_build

%install
export PATH="%{_builddir}/%{name}-%{version}/zig-toolchain:$PATH"
DESTDIR=%{buildroot} %zig_build

# Fedora provides the terminfo entry for xterm-ghostty in ncurses-base from
# Fedora 42 onwards; do not ship a second copy of the same name.
rm -f "%{buildroot}%{_prefix}/share/terminfo/g/ghostty"

desktop-file-validate \
    "%{buildroot}%{_prefix}/share/applications/com.mitchellh.ghostty.desktop"

%files
%license LICENSE
%{_bindir}/ghostty
%{_prefix}/share/applications/com.mitchellh.ghostty.desktop
%{_prefix}/share/bash-completion/completions/ghostty.bash
%{_prefix}/share/bat/syntaxes/ghostty.sublime-syntax
%{_prefix}/share/fish/vendor_completions.d/ghostty.fish
%{_prefix}/share/ghostty
%{_prefix}/share/icons/hicolor/1024x1024/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/128x128/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/128x128@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/16x16/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/16x16@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/256x256/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/256x256@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/32x32/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/32x32@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/512x512/apps/com.mitchellh.ghostty.png
%{_prefix}/share/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_prefix}/share/man/man1/ghostty.1
%{_prefix}/share/man/man5/ghostty.5
%{_prefix}/share/nautilus-python/extensions/ghostty.py
%{_prefix}/share/nvim/site/compiler/ghostty.vim
%{_prefix}/share/nvim/site/ftdetect/ghostty.vim
%{_prefix}/share/nvim/site/ftplugin/ghostty.vim
%{_prefix}/share/nvim/site/syntax/ghostty.vim
%{_prefix}/share/vim/vimfiles/compiler/ghostty.vim
%{_prefix}/share/vim/vimfiles/ftdetect/ghostty.vim
%{_prefix}/share/vim/vimfiles/ftplugin/ghostty.vim
%{_prefix}/share/vim/vimfiles/syntax/ghostty.vim
%{_prefix}/share/zsh/site-functions/_ghostty
%{_prefix}/share/dbus-1/services/com.mitchellh.ghostty.service
%{_prefix}/share/locale/*/LC_MESSAGES/com.mitchellh.ghostty.mo
%{_prefix}/share/metainfo/com.mitchellh.ghostty.metainfo.xml
%{_prefix}/share/systemd/user/app-com.mitchellh.ghostty.service
%{_prefix}/share/terminfo/x/xterm-ghostty

%changelog
* Thu Nov 12 2026 Ferah <ferah@localhost> - 1.4.0-1
- Update to 1.4.0
- Build with the upstream-pinned Zig 0.17.0 toolchain (Fedora ships Zig 0.16)
- Keep the Zig package cache outside the source tree
- Validate the desktop entry during the build

* Thu Oct 23 2025 Ferah <ferah@localhost> - 1.2.2-1
- Update to 1.2.2
