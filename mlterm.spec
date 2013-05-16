%define majorkik       10
%define libnamekik     %mklibname kik %{majorkik}
%define libnamedevkik  %mklibname -d kik %{majorkik}

%define majormkf       13
%define libnamemkf     %mklibname mkf %{majormkf}
%define libnamedevmkf  %mklibname -d mkf %{majormkf}

Summary:     Multi Lingual TERMinal emulator for X
Name:        mlterm
Version:     3.0.11
Release:     3
License:     BSD style
Group:       Terminals
URL:         http://mlterm.sourceforge.net/
Source0:     http://prdownloads.sourceforge.net/mlterm/mlterm-%{version}.tar.gz
Patch0:      mlterm_font_config.diff
Patch1:      mlterm_main_config.diff
Patch2:      mlterm-2.9.4-mdv-fix-str-fmt.patch
Patch3:		mlterm-3.0.0-linkage.patch
# we need to versionate the two following requires b/c of missing major changes:
Requires:       %libnamekik = %{version}
Requires:       %libnamemkf = %{version}
Requires:       ncurses-extraterms
BuildRequires:  fribidi-devel
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  imagemagick
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)

%description
mlterm is a multi-lingual terminal emulator written from
scratch, which supports various character sets and encodings
in the world.  It also supports various unique feature such as
anti-alias using FreeType, multiple windows, scrollbar API,
scroll by mouse wheel, automatic selection of encoding,
and so on. Multiple xims are also supported.
You can dynamically change various xims.
NOTE: mlterm has good config tools.
Press Ctrl + right click or Ctrl + left click to run them.


%package -n	%libnamekik
Group:		System/Libraries
Summary:	Uitlity Library for Multi Lingual TERMinal

%description -n %libnamekik
This library is necessary for Multi Lingual TERMinal. It contains
various utility functions for mlterm.

%package -n	%libnamemkf
Group:		System/Libraries
Summary:	Mlterm Library for Handling Various Character Encodings

%description -n %libnamemkf
This library is necessary for Multi Lingual TERMinal. It contains
routines for handling various character sets.


%prep
%setup -q -n %name-%version
%patch0 -p0
%patch1 -p0
%patch2 -p1 -b .strfmt
#%patch3 -p0 -b .link

%build
%define _disable_ld_no_undefined 1
export CFLAGS="%optflags %ldflags"
%configure2_5x \
	--disable-static \
	--enable-fribidi \
	--with-imagelib=gdk-pixbuf \
	--enable-anti-alias \
	--with-scrollbars=sample,extra,pixmap_engine \
	--enable-optimize-redrawing \
	--with-tools \
	--disable-rpath

%make

%install
%makeinstall_std

# install terminfo
tic -o $RPM_BUILD_ROOT/%{_datadir}/terminfo/ doc/term/mlterm.ti

# install menu entry.
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop <<EOF
[Desktop Entry]
Name=Mlterm
Comment=A multi-lingual terminal emulator
Exec=%{_bindir}/%{name}
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=false
Categories=System;TerminalEmulator;
EOF

#install icons.
mkdir -p $RPM_BUILD_ROOT%{_liconsdir} \
         $RPM_BUILD_ROOT%{_iconsdir} \
         $RPM_BUILD_ROOT%{_miconsdir} \

convert doc/icon/mlterm_16x16.xpm $RPM_BUILD_ROOT/%{_miconsdir}/mlterm.png
convert doc/icon/mlterm_32x32.xpm $RPM_BUILD_ROOT/%{_iconsdir}/mlterm.png
convert doc/icon/mlterm_48x48.xpm $RPM_BUILD_ROOT/%{_liconsdir}/mlterm.png

# remove unnecessary files
rm -f $RPM_BUILD_ROOT%{_libdir}/libkik.{so,la,a} \
      $RPM_BUILD_ROOT%{_libdir}/libmkf.{so,la,a} \
      $RPM_BUILD_ROOT%{_libexecdir}/%{name}/lib*.a \
      $RPM_BUILD_ROOT%{_libexecdir}/%{name}/lib*.la

%find_lang mlconfig
rm -fr $RPM_BUILD_ROOT%{_datadir}/terminfo/m/mlterm

%files -f mlconfig.lang
%doc ChangeLog LICENCE README doc/{en,ja}
%config(noreplace) %{_sysconfdir}/mlterm/
%{_bindir}/mlcc
%{_bindir}/mlclient
%{_bindir}/mlterm
%{_bindir}/mlclientx
%{_libdir}/mkf
%{_libdir}/libmlterm_core.so
%{_libdir}/mlimgloader
%{_libexecdir}/mlconfig
%{_libexecdir}/mlterm-menu
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png

%files -n %libnamekik
%_libdir/libkik*.so.*

%files -n %libnamemkf
%_libdir/libmkf*.so.*


%changelog
* Thu Apr 19 2012 Alexander Khrukin <akhrukin@mandriva.org> 3.0.11-1
+ Revision: 791996
- version update 3.0.11

* Mon Dec 06 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.0-2mdv2011.0
+ Revision: 612872
- the mass rebuild of 2010.1 packages

* Sun Apr 25 2010 Funda Wang <fwang@mandriva.org> 3.0.0-1mdv2010.1
+ Revision: 538658
- New version 3.0.0
- fix linkage

  + Jérôme Brenier <incubusss@mandriva.org>
    - use %%configure2_5x
    - fix str fmt (P2)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Nov 11 2008 Funda Wang <fwang@mandriva.org> 2.9.4-3mdv2009.1
+ Revision: 302071
- revert to configure as 2_5x breaks x86_64 build
- use configure2_5x

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 2.9.4-3mdv2009.0
+ Revision: 252611
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Thu Dec 13 2007 Jérôme Soyer <saispo@mandriva.org> 2.9.4-1mdv2008.1
+ Revision: 119233
- New release 2.9.4

* Mon Oct 01 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.9.3-3mdv2008.0
+ Revision: 94090
- Rebuild for fixed package changelog.

* Mon Oct 01 2007 Herton Ronaldo Krzesinski <herton@mandriva.com.br> 2.9.3-2mdv2008.0
+ Revision: 94081
- Rebuild (#34355).
- Bunzip patches.
- Install binaries at /usr/bin, not /usr/X11R6/bin (#34324).
- Switch to xdg menu.

  + Jérôme Soyer <saispo@mandriva.org>
    - import mlterm

