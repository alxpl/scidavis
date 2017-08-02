%global pluginversion 1.0.0

Name:           scidavis
Version:        1.19
Release:        2%{?dist}
Summary:        Application for Scientific Data Analysis and Visualization

License:        GPLv2+ and GPLv3+
URL:            http://scidavis.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Patches by Miquel Garriga <gbmiquel.at.gmail.com>
Patch0:         fedora-rpm-with-system-liborigin3.patch
Patch1:         armv7hl-build.patch

BuildRequires:  desktop-file-utils
BuildRequires:  doxygen
BuildRequires:  gsl-devel
BuildRequires:  liborigin3-devel
BuildRequires:  muParser-devel
BuildRequires:  PyQt4-devel
BuildRequires:  python2-devel
BuildRequires:  qt-assistant-adp-devel
BuildRequires:  qt-devel
BuildRequires:  qwt5-qt4-devel
BuildRequires:  qwtplot3d-qt4-devel
BuildRequires:  sip-devel
BuildRequires:  zlib-devel

Requires:       PyQt4       


%description
SciDAVis is a free interactive application aimed at data analysis and 
publication-quality plotting. It combines a shallow learning curve and
an intuitive, easy-to-use graphical user interface with powerful 
features such as scriptability and extensibility.


%prep
%setup -q -n %{name}-%{version}
%patch0 -p1
%patch1 -p1
rm -rf 3rdparty/liborigin


%build
%if 0%{?__isa_bits} == 64
%qmake_qt4 PRESET=linux_package libsuff="64" CONFIG+=liborigin
%else
%qmake_qt4 PRESET=linux_package CONFIG+=liborigin
%endif
make %{?_smp_mflags}


%install
make INSTALL_ROOT="%{buildroot}" install

%{__mkdir_p} %{buildroot}%{_datadir}/{%{name}/translations,applications,mime/packages,mimelnk/application}
%{__cp} -p %{name}/translations/*.qm %{buildroot}%{_datadir}/%{name}/translations/
%find_lang %{name} --with-qt
%{__cp} -p %{name}/%{name}.desktop %{buildroot}/%{_datadir}/applications/
%{__cp} -p %{name}/%{name}.xml %{buildroot}%{_datadir}/mime/packages/
%{__cp} -p %{name}/x-sciprj.desktop %{buildroot}%{_datadir}/mimelnk/application/

for s in 16 22 32 48 64 128; do
   %{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
   %{__cp} -p %{name}/icons/hicolor-${s}/%{name}.png %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/%{name}.png
done

for s in 16 22 32; do
   %{__mkdir_p} %{buildroot}%{_datadir}/icons/locolor/${s}x${s}/apps
   %{__cp} -p %{name}/icons/locolor-${s}/%{name}.png %{buildroot}%{_datadir}/icons/locolor/${s}x${s}/apps/%{name}.png
done

# Plugins are unversioned .so files
cd %{buildroot}%{_libdir}/%{name}/plugins
for plugin in `ls *.so`
do 
    mv ${plugin}.%{pluginversion} ${plugin}
    rm -f ${plugin}.*
done

%{_fixperms} %{buildroot}/*


%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
# check available in Makefile but doesn't do anything right now
#make check


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files -f %{name}.lang
%doc CHANGES
%license gpl.txt LICENSE license.rtf
%{_bindir}/*
%{_docdir}/*
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_datadir}/mime/packages/*.xml
%{_datadir}/mimelnk/application/x-sciprj.desktop
%{_datadir}/icons/hicolor/*/apps/scidavis.*
%{_datadir}/icons/locolor/*/apps/scidavis.*


%changelog
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
