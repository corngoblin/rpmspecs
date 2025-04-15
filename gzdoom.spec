Name:           gzdoom
Version:        4.14.1
Release:        0
Summary:        A DOOM source port with graphic and modding extensions
License:        GPL-3.0-only
Group:          Amusements/Games/3D/Shoot
URL:            https://zdoom.org/

#Git-Clone:     https://github.com/zdoom/gzdoom
Source:         https://github.com/zdoom/gzdoom/archive/g%version.tar.gz
BuildRequires:  g++
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  libsdl2-dev
BuildRequires:  git
BuildRequires:  zlib1g-dev
BuildRequires:  libbz2-dev
BuildRequires:  libjpeg-dev
BuildRequires:  libfluidsynth-dev
BuildRequires:  libgme-dev
BuildRequires:  libopenal-dev
BuildRequires:  libmpg123-dev
BuildRequires:  libsndfile1-dev
BuildRequires:  libgtk-3-dev
BuildRequires:  timidity 
BuildRequires:  nasm
BuildRequires:  libgl1-mesa-dev
BuildRequires:  tar
BuildRequires:  libsdl1.2-dev
BuildRequires:  libglew-dev
BuildRequires:  libvpx-dev


%description
GZDoom is a port (a modification) of the original Doom source code, featuring:
* an OpenGL renderer, HQnX/xBRZ rescaling, 3D floor and model support
* Truecolor software rendering, extending the classic 8-bit palette
* Heretic, Hexen and Strife game modes and support for a lot of
  additional IWADs.
* Boom and Hexen map extension support, scriptability with ACS and
  ZScript, and various modding features regarding actors and scenery.
* Demo record/playback of classic and Boom demos is not supported.

%ifarch %ix86
SSE2 is a hard requirement even on 32-bit x86.
%endif

%prep
%autosetup -n %name-g%version -p1
%if 0%{?suse_version} < 1600
# system lzma-sdk too old, use bundled copy
%patch -P 5 -R -p1
%endif
# osc/rpm always has the version identifier (only has an effect when snapshots are used via _service files)
pushd tools/updaterevision/
savedate=$(stat -c "%y" UpdateRevision.cmake)
perl -i -pe "s{<unknown version>}{%version}g" UpdateRevision.cmake
touch -d "$savedate" UpdateRevision.cmake
popd

%build
# Disable LTO, which does not like seeing handcrafted assembler
%define _lto_cflags %nil

export CXXFLAGS="$CXXFLAGS -DSHARE_DIR=\\\"%_datadir/doom\\\""
%cmake -DNO_STRIP=1 \
	-DCMAKE_SHARED_LINKER_FLAGS="" \
	-DCMAKE_EXE_LINKER_FLAGS="" -DCMAKE_MODULE_LINKER_FLAGS="" \
	-DINSTALL_DOCS_PATH="%_defaultdocdir/%name" \
	-DINSTALL_PK3_PATH="%_datadir/doom" \
	-DINSTALL_SOUNDFONT_PATH="%_datadir/doom" \
	-DDYN_OPENAL=OFF -DINSTALL_RPATH:STRING="NO"
%cmake_build

%install
%cmake_install

%post
echo "INFO: %name: The global IWAD directory is %_datadir/doom."

%files
%_bindir/%name
%_defaultdocdir/%name
%_datadir/doom/

%changelog


%changelog

