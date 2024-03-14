#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	5.27.11
%define		qtver		5.15.2
%define		kpname		drkonqi
Summary:	drkonqi
Name:		kp5-%{kpname}
Version:	5.27.11
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	b2f7ba7f396e08b94b43b46ff94e3ce5
URL:		http://www.kde.org/
BuildRequires:	Qt5Core-devel >= %{qtver}
BuildRequires:	Qt5DBus-devel
BuildRequires:	Qt5Gui-devel
BuildRequires:	Qt5Widgets-devel
BuildRequires:	Qt5X11Extras-devel
BuildRequires:	Qt5Xml-devel
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-devel
BuildRequires:	hardlink >= 1.0-3
BuildRequires:	kf5-attica-devel
BuildRequires:	kf5-extra-cmake-modules >= 1.4.0
BuildRequires:	kf5-frameworkintegration-devel
BuildRequires:	kf5-kauth-devel
BuildRequires:	kf5-kcmutils-devel
BuildRequires:	kf5-kcodecs-devel
BuildRequires:	kf5-kconfig-devel
BuildRequires:	kf5-kconfigwidgets-devel
BuildRequires:	kf5-kcoreaddons-devel
BuildRequires:	kf5-kcrash-devel
BuildRequires:	kf5-kguiaddons-devel
BuildRequires:	kf5-ki18n-devel
BuildRequires:	kf5-kiconthemes-devel
BuildRequires:	kf5-kservice-devel
BuildRequires:	kf5-kwidgetsaddons-devel
BuildRequires:	kf5-kwindowsystem-devel
BuildRequires:	kf5-syntax-highlighting-devel
BuildRequires:	kp5-kdecoration-devel
BuildRequires:	kuserfeedback-devel >= 1.2.0
BuildRequires:	libstdc++-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt5-build >= %{qtver}
BuildRequires:	qt5-qmake
BuildRequires:	rpmbuild(macros) >= 1.596
BuildRequires:	systemd
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Plasma crash handler, gives the user feedback if a program crashed.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DHTML_INSTALL_DIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_iconsdir}/{breeze-dark,breeze}
install -d $RPM_BUILD_ROOT%{systemdunitdir}

%ninja_install -C build

mv $RPM_BUILD_ROOT%{_prefix}%{systemdunitdir}/drkonqi-coredump-processor@.service $RPM_BUILD_ROOT%{systemdunitdir}/

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{kpname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/drkonqi
%{_datadir}/drkonqi
%{_desktopdir}/org.kde.drkonqi.desktop
%{_datadir}/qlogging-categories5/drkonqi.categories
%{systemdunitdir}/drkonqi-coredump-processor@.service
%{systemduserunitdir}/drkonqi-coredump-cleanup.service
%{systemduserunitdir}/drkonqi-coredump-cleanup.timer
%{systemduserunitdir}/drkonqi-coredump-launcher.socket
%{systemduserunitdir}/drkonqi-coredump-launcher@.service
%dir %{_libdir}/qt5/plugins/drkonqi
%{_libdir}/qt5/plugins/drkonqi/KDECoredumpNotifierTruck.so
%attr(755,root,root) %{_prefix}/libexec/drkonqi-coredump-cleanup
%attr(755,root,root) %{_prefix}/libexec/drkonqi-coredump-launcher
%attr(755,root,root) %{_prefix}/libexec/drkonqi-coredump-processor
%attr(755,root,root) %{_bindir}/drkonqi-coredump-gui
%{_desktopdir}/org.kde.drkonqi.coredump.gui.desktop
