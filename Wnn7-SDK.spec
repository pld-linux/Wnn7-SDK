Summary:	Wnn6 Client Library
Summary(pl.UTF-8):	Biblioteka kliencka Wnn6
Name:		Wnn7-SDK
Version:	1.0
Release:	2
License:	OMRON Corporation (distributable, see README)
Group:		Libraries
#Source0Download: http://www.omronsoft.co.jp/SP/pcunix/sdk/
Source0:	http://www.omronsoft.co.jp/SP/pcunix/sdk/wnn/Wnn7SDK.tgz
# Source0-md5:	19b41bf2ef86d7f4cb889c7f689602fb
Patch0:		%{name}-config.patch
Patch1:		%{name}-incl.patch
Patch2:		%{name}-shared.patch
Patch3:		%{name}-nonroot.patch
Patch4:		%{name}-header.patch
BuildRequires:	xorg-util-imake
BuildRequires:	xorg-util-makedepend
URL:		http://www.omronsoft.co.jp/SP/pcunix/sdk/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Runtime Wnn6 client library necessary to run Wnn6 clients.

%description -l pl.UTF-8
Biblioteka kliencka Wnn6 potrzebna do uruchamiania klientów Wnn6.

%package devel
Summary:	Header files for Wnn6
Summary(pl.UTF-8):	Pliki nagłówkowe Wnn6
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains header files for Wnn6 client developments.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia klientów Wnn6.

%package static
Summary:	Static Wnn6 client library
Summary(pl.UTF-8):	Statyczna biblioteka kliencka Wnn6
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Wnn6 client library.

%description static -l pl.UTF-8
Statyczna biblioteka kliencka Wnn6.

%prep
%setup -q -c
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

cd src
%{__sed} -i -e 's|/usr/lib64/X11|%{_libdir}/X11|g' \
	config/X11.tmpl config/Project.tmpl Makefile.ini

%build
%{__make} -C src -f Makefile.ini World \
	WNNLIBDIR=%{_libdir} \
	CC="%{__cc}" \
	CDEBUGFLAGS="%{rpmcflags} -fPIC" \
	REQUIREDLIBS="-lcrypt" \

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc src/README
%attr(755,root,root) %{_libdir}/libwnn7.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libwnn7.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libwnn7.so
%{_includedir}/wnn7

%files static
%defattr(644,root,root,755)
%{_libdir}/libwnn7.a
