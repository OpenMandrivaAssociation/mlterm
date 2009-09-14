%define name    mlterm
%define version 2.9.4
%define release	%mkrel 4

%define majorkik       10
%define libnamekik     %mklibname kik %{majorkik}
%define libnamedevkik  %mklibname -d kik %{majorkik}

%define majormkf       13
%define libnamemkf     %mklibname mkf %{majormkf}
%define libnamedevmkf  %mklibname -d mkf %{majormkf}

Summary:     Multi Lingual TERMinal emulator for X
Name:        %{name}
Version:     %{version}
Release:     %{release}
License:     BSD style
Group:       Terminals
URL:         http://mlterm.sourceforge.net/
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source0:     http://prdownloads.sourceforge.net/mlterm/mlterm-%{version}.tar.bz2
Patch0:      mlterm_font_config.diff
Patch1:      mlterm_main_config.diff
# we need to versionate the two following requires b/c of missing major changes:
Requires:       %libnamekik = %{version}
Requires:       %libnamemkf = %{version}
Requires:       ncurses-extraterms
BuildRequires:  fribidi-devel gtk2-devel
BuildRequires:  imagemagick

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

find -name CVS -type d | xargs -r rm -rf

%build
%configure \
	--enable-fribidi \
	--with-imagelib=gdk-pixbuf \
	--enable-anti-alias \
	--with-scrollbars=sample,extra,pixmap_engine \
	--enable-optimize-redrawing \
	--with-tools \
	--disable-rpath

# temporary hack until xft cflags is fixed
find -name 'Makefile' -type f | xargs grep '/usr/X11R6/include/freetype2' | cut -d: -f1 | xargs -r perl -pi -e 's#/usr/X11R6/include/freetype2#/usr/include/freetype2#g'

%make

%install
rm -rf $RPM_BUILD_ROOT
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

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%update_menus
%endif

%if %mdkversion < 200900
%post -n %libnamekik -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libnamekik -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %libnamemkf -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %libnamemkf -p /sbin/ldconfig
%endif


%files -f mlconfig.lang
%defattr(-,root,root)
%doc ChangeLog LICENCE README doc/{en,ja}
%config(noreplace) %{_sysconfdir}/mlterm/
%{_bindir}/mlcc
%{_bindir}/mlclient
%{_bindir}/mlterm
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
%defattr(-,root,root)
%_libdir/libkik*.so.*

%files -n %libnamemkf
%defattr(-,root,root)
%_libdir/libmkf*.so.*


