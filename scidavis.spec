%global pluginversion 1.0.0

Name:           scidavis
Version:        1.21
Release:        4%{?dist}
Summary:        Application for Scientific Data Analysis and Visualization

License:        GPLv2+ and GPLv3+
URL:            http://scidavis.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# To be removed after 1.22 release
Source1:        %{name}.appdata.xml
# Patches by Miquel Garriga <gbmiquel.at.gmail.com>
# https://sourceforge.net/p/scidavis/scidavis-bugs/313/
# https://sourceforge.net/p/scidavis/scidavis-bugs/317/
Patch0:         scidavis-armv7hl-build.patch
# enable after liborigin-3.0.0 release
#Patch1:         fedora-rpm-with-system-liborigin3.patch
Patch2:         scidavis-set_python_path.patch
# To be removed after 1.22 release
Patch3:         scidavis-fix_bug_316.patch

BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  gsl-devel
# enable after liborigin-3.0.0 release
#BuildRequires:  liborigin3-devel
BuildRequires:  muParser-devel
BuildRequires:  qt-assistant-adp-devel
BuildRequires:  qt-devel
BuildRequires:  qwt5-qt4-devel
BuildRequires:  qwtplot3d-qt4-devel
BuildRequires:  sip-devel
BuildRequires:  zlib-devel
BuildRequires:  libappstream-glib
# required for the tests, enable when building locally
#BuildRequires:  xorg-x11-server-Xvfb

Requires:       PyQt4
Requires:       hicolor-icon-theme

Recommends:     python2-%{name}


%description
SciDAVis is a free interactive application aimed at data analysis and
publication-quality plotting. It combines a shallow learning curve and
an intuitive, easy-to-use graphical user interface with powerful
features such as scriptability and extensibility.



%package -n python2-%{name}
BuildRequires:  python2-devel
BuildRequires:  PyQt4-devel
Requires:       python2-scipy

Summary:        Python 2 bindings for SciDAVis
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-%{name}}


%description -n python2-%{name}
This module provides SciDAVis bindings to the Python2 programming language.



%prep
%setup -q -n %{name}-%{version}
%ifarch armv7hl
%patch0 -p1
%endif
# enable after liborigin-3.0.0 release
#%patch1 -p1
#rm -rf 3rdparty/liborigin
%patch2 -p0
# To be removed after 1.22 release
%patch3 -p1


%build
%if 0%{?__isa_bits} == 64
%qmake_qt4 PRESET=linux_package libsuff="64" CONFIG+=aegis CONFIG+=python
%else
%qmake_qt4 PRESET=linux_package CONFIG+=aegis CONFIG+=python
%endif
%make_build


%install
make INSTALL_ROOT="%{buildroot}" install
install -pm 644 CHANGES %{buildroot}%{_docdir}/%{name}/

mkdir -p %{buildroot}%{_datadir}/{%{name}/translations,applications,mime/packages,appdata}
cp -p %{name}/translations/*.qm %{buildroot}%{_datadir}/%{name}/translations/

# To be removed after 1.22 release
cp -p %{SOURCE1} %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

# KDE3 remnant - upstream is aware
rm -rf %{buildroot}%{_datadir}/mimelnk/

# man page gets installed under scidavis.1/ subdirectory - fixed upstream, nextrelease
rm -rf %{buildroot}%{_mandir}/man1/%{name}.1
cp -p %{name}/%{name}.1 %{buildroot}%{_mandir}/man1/

# gpl.txt is copied over by the license macro
rm -f %{buildroot}%{_docdir}/%{name}/gpl.txt


# Plugins are unversioned .so files
cd %{buildroot}%{_libdir}/%{name}/plugins
for plugin in `ls *.so`
do
    mv ${plugin}.%{pluginversion} ${plugin}
    rm -f ${plugin}.*
done


%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/*.appdata.xml
# Enable when building locally
#cd test && xvfb-run -a ./unittests


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%license gpl.txt LICENSE license.rtf
%{_mandir}/man1/%{name}.1*
%{_docdir}/%{name}/
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/icons/locolor/*/apps/%{name}.*


%files -n python2-%{name}
%{python2_sitearch}/%{name}/


%changelog
* Thu Sep 14 2017 Alexander Ploumistos <alexpl@fedoraproject.org> - 1.21-4
- Fix another armv7hl issue - patches by Robert-André Mauchin and Miquel Garriga
- Patch for setting Python paths by Antonio Trande
- Backport patch for https://sourceforge.net/p/scidavis/scidavis-bugs/316/
- Enable all build options (CONFIG+=aegis)
- Include AppData file from next release
- More code cleanup

* Tue Sep 12 2017 Alexander Ploumistos <alexpl@fedoraproject.org> - 1.21-3
- Enable Python scripting
- Remove more redundant code

* Mon Sep 11 2017 Alexander Ploumistos <alexpl@fedoraproject.org> - 1.21-2
- Hold off unbundling until liborigin-3.0.0 official release
- Remove x-sciprj.desktop and /usr/share/mimelnk/application/
- Fix manpage location
- Remove redundant code from the spec file

* Sat Aug 19 2017 Alexander Ploumistos <alexpl@fedoraproject.org> - 1.21-1
- New version

* Tue Aug 01 2017 Alexander Ploumistos <alexpl@fedoraproject.org> - 1.19-2
- Enable ARM builds - patch by Miquel Garriga <gbmiquel.at.gmail.com>
- Clean up spec file

* Thu Jul 20 2017 Alexander Ploumistos <alexpl@fedoraproject.org> - 1.19-1
- New version

* Wed Jun 28 2017 Alexander Ploumistos <alexpl@fedoraproject.org> - 1.18-2.20170628git7c6e07df
- Unbundle liborigin - patch by Miquel Garriga <gbmiquel.at.gmail.com>

* Fri Jun 23 2017 Alexander Ploumistos <alexpl@fedoraproject.org> - 1.18-1
- new version

* Mon Jun 12 2017 Alexander Ploumistos <alexpl@fedoraproject.org> - 1.17-2
- Enabled bundled patched liborigin

* Mon Jun 12 2017 Alexander Ploumistos <alexpl@fedoraproject.org> - 1.17-1
- new version

* Mon Jul 11 2016 Alexander Ploumistos <alexpl@fedoraproject.org> - 1.D13-1
- new version

* Tue Nov 24 2015 Christian Dersch <lupinix@mailbox.org> - 1.D9-1
- new version

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.D8-12
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1.D8-11
- rebuild for Boost 1.58

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.D8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.D8-9
- Rebuilt for GCC 5 C++11 ABI change

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 1.D8-8
- Rebuild for boost 1.57.0

* Fri Jan 02 2015 Christian Dersch <lupinix@fedoraproject.org> - 1.D8-7
- added patch to fix http://sourceforge.net/p/scidavis/svn/1458/

* Sat Dec 20 2014 Christian Dersch <lupinix@fedoraproject.org> - 1.D8-6
- added missing find_lang macro
- adjusted condition for 32/64 bit decision

* Mon Dec 15 2014 Christian Dersch <lupinix@fedoraproject.org> - 1.D8-5
- added ExcludeArch for arm as scidavis doesn't build there

* Mon Dec 15 2014 Christian Dersch <lupinix@fedoraproject.org> - 1.D8-4
- fixed spec
- added post/postun scripts
- removed versioned .so files
- don't package compiled versions of scidavisrc.py config file

* Thu Aug  7 2014 Christian Dersch <lupinix@fedoraproject.org> - 1.D8-3
- fixed spec to be conform with guidelines

* Mon Aug  4 2014 Christian Dersch <lupinix@fedoraproject.org> - 1.D8-2
- fixed BuildRequires

* Mon Aug  4 2014 Christian Dersch <lupinix@fedoraproject.org> - 1.D8-1
- initial spec
- inspired by old scidavis spec http://pkgs.fedoraproject.org/cgit/scidavis.git/tree/scidavis.spec?h=f15
