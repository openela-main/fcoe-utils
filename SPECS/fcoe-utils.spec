# https://fedoraproject.org/wiki/Packaging:Guidelines#Compiler_flags
%global _hardened_build 1

# v1.0.33-9-g848bcc6ba8c
%global commit0      848bcc6ba8cda1f344663b4e73f1bc4857bcb4e3
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:               fcoe-utils
Version:            1.0.33
Release:            4.git%{shortcommit0}%{?dist}
Summary:            Fibre Channel over Ethernet utilities
Group:              Applications/System
License:            GPLv2
URL:                http://www.open-fcoe.org
Source0:            https://github.com/openSUSE/fcoe-utils/archive/%{commit0}.tar.gz#/%{name}-%{version}-%{shortcommit0}.tar.gz
Source1:            quickstart.txt
Source2:            fcoe.service
Source3:            fcoe.config
ExcludeArch:        ppc s390
Patch0:             fcoe-utils-set-default-DCB_REQUIRED-to-no.patch
Patch1:             0001-Revert-fcoemon-Correctly-handle-options-in-the-servi.patch
Patch2:             0002-Revert-Make-gcc-compiler-happy-about-ifname-string-t.patch
Patch3:             0003-fix-VLAN-device-name-overflow-check.patch
Patch4:             0004-fix-regressions-caused-by-safe_makepath-change-in-li.patch
Patch5:             0005-minor-fcoeadm-output-issues.patch

BuildRequires:      autoconf
BuildRequires:      automake
BuildRequires:      libpciaccess-devel
BuildRequires:      libtool
BuildRequires:      lldpad-devel >= 0.9.43
BuildRequires:      systemd
Requires:           lldpad >= 0.9.43
Requires:           iproute
Requires:           device-mapper-multipath
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
Fibre Channel over Ethernet utilities
fcoeadm - command line tool for configuring FCoE interfaces
fcoemon - service to configure DCB Ethernet QOS filters, works with lldpad

%prep
%autosetup -p1 -n fcoe-utils-%{commit0}
cp -v %{SOURCE1} quickstart.txt

%build
./bootstrap.sh
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -rf %{buildroot}/etc/init.d
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig %{buildroot}%{_unitdir}
rm -f %{buildroot}%{_unitdir}/*
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/fcoe
mkdir -p %{buildroot}%{_libexecdir}/fcoe
for file in \
    contrib/*.sh \
    debug/*sh
    do install -m 755 ${file} %{buildroot}%{_libexecdir}/fcoe/
done
# We supply our own config for fcoe.service
rm -f %{buildroot}/%{_sysconfdir}/fcoe/config

%post
%systemd_post fcoe.service

%preun
%systemd_preun fcoe.service

%postun
%systemd_postun_with_restart fcoe.service

%files
%doc README COPYING QUICKSTART quickstart.txt
%{_sbindir}/*
%{_mandir}/man8/*
%{_unitdir}/fcoe.service
%{_sysconfdir}/fcoe/
%config(noreplace) %{_sysconfdir}/fcoe/cfg-ethx
%config(noreplace) %{_sysconfdir}/sysconfig/fcoe
%{_datadir}/bash-completion/completions/*
%{_libexecdir}/fcoe/

%changelog
* Thu Jun 10 2021 Chris Leech <cleech@redhat.com> - 1.0.33-4.git848bcc6
- rebuilt for 8.5

* Tue Mar 23 2021 Chris Leech <cleech@redhat.com> - 1.0.33-3.git848bcc6
- 1918561 regression in fipvlan VLAN name generation and fcoeadm commands

* Mon Jan 18 2021 Chris Leech <cleech@redhat.com> - 1.0.33-2.git848bcc6
- 1897503 revert breaking upstream change to command line options

* Tue Nov 03 2020 Chris Leech <cleech@redhat.com> - 1.0.33-1.git848bcc6
- 1889536 add back default change of DCB_REQUIRED="no" for RHEL 8

* Tue Nov 03 2020 Chris Leech <cleech@redhat.com> - 1.0.33-0.git848bcc6
- 1889536 new version

* Fri Dec 06 2019 Chris Leech <cleech@redhat.com> - 1.0.32-7
- 1776492 fcoemon: fix ignored devices from recv buffer resize bug

* Tue Aug 07 2018 Chris Leech <cleech@redhat.com> - 1.0.32-6
- remove fcoe from SUPPORTED_DRIVERS in /etc/sysconfig/fcoe
- add qedf to SUPPORTED_DRIVERS in /etc/sysconf/fcoe
- added upstream fix for large fcoe ctrl numbers

* Fri Mar 16 2018 Chris Leech <cleech@redhat.com> - 1.0.32-5
- fix some newer gcc 8 truncation format errors

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.32-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Feb 09 2017 Chris Leech <cleech@redhat.com> - 1.0.32-1
- update to 1.0.32

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.30-5.git91c0c8c
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb 01 2016 Chris Leech <cleech@redhat.com> - 1.0.30-4.git91c0c8c
- 1303433 package should not attempt to own /etc/bash_completion.d

* Mon Jul 06 2015 Chris Leech <cleech@redhat.com> - 1.0.30-2
- fix display when libhbalinux includes hosts without a serial number

* Tue Jun 16 2015 Chris Leech <cleech@redhat.com> - 1.0.30-1
- rebase to upstream v1.0.30-2-g91c0c8c

* Fri Oct 24 2014 Chris Leech <cleech@redhat.com> - 1.0.29-7
- enable vn2vn mode in fcoeadm

* Tue Oct 07 2014 Chris Leech <cleech@redhat.com> - 1.0.29-6
- update to upstream v1.0.29-29-g9267509

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Nov 07 2013 Petr Šabata <contyk@redhat.com> - 1.0.29-3
- Fix configure.ac for automake 1.14

* Thu Nov 07 2013 Petr Šabata <contyk@redhat.com> - 1.0.29-2
- Don't install the old configuration file alongside the new one
- Add bnx2fc to the SUPPORTED_DRIVERS for consistency with previous configuration

* Thu Aug 29 2013 Petr Šabata <contyk@redhat.com> - 1.0.29-1
- 1.0.29 bump

* Wed Jul 31 2013 Petr Šabata <contyk@redhat.com> - 1.0.28-4
- Drop the initscript-specific config patch

* Wed Jul 31 2013 Petr Šabata <contyk@redhat.com> - 1.0.28-3
- Require just 'systemd' instead of 'systemd-units'
- Patch the fcoemon manpage with a note for systemd users

* Mon Jun 10 2013 Petr Šabata <contyk@redhat.com> - 1.0.28-2
- Enhance the format strings patch to fix ppc64 build failures too

* Tue Jun 04 2013 Petr Šabata <contyk@redhat.com> - 1.0.28-1
- 1.0.28 bump

* Wed Mar 06 2013 Petr Šabata <contyk@redhat.com> - 1.0.27-1
- 1.0.27 bump

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 09 2013 Petr Šabata <contyk@redhat.com> - 1.0.25-2
- Don't build for s390x since it's not supported by kernel either

* Tue Nov 27 2012 Petr Šabata <contyk@redhat.com> - 1.0.25-1
- 1.0.25 (with latest fixes)
- Simplify the spec a bit
- Fix bogus dates in changelog

* Thu Nov 01 2012 Petr Šabata <contyk@redhat.com> - 1.0.25-1

* Tue Aug 28 2012 Petr Šabata <contyk@redhat.com> - 1.0.24-2
- Migrate to systemd scriptlets (#850104)

* Wed Aug 15 2012 Petr Šabata <contyk@redhat.com> - 1.0.24-1
- 1.0.24 bump

* Mon Jul 23 2012 Petr Šabata <contyk@redhat.com> - 1.0.23-3
- Don't exclude s390x.
- Add AM_PROG_AR to configure.ac.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Petr Šabata <contyk@redhat.com> - 1.0.23-1
- Update to 1.0.23
- Re-introduce ExcludeArch to be in line with EL.

* Thu Feb 16 2012 Petr Šabata <contyk@redhat.com> - 1.0.22-2
- Fix the incorrect libhbalinux runtime dependency

* Mon Jan 23 2012 Petr Šabata <contyk@redhat.com> - 1.0.22-1
- 1.0.22 bump
- Remove dcbd from Description

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 24 2011 Petr Šabata <contyk@redhat.com> - 1.0.21-1
- 1.0.21 bump

* Mon Oct 31 2011 Petr Sabata <contyk@redhat.com> - 1.0.20-5
- Remove useless PIDFile from fcoe.service unit file

* Thu Oct 06 2011 Petr Sabata <contyk@redhat.com> - 1.0.20-4
- Do not enable fcoemon by default (#701999)
- Silence systemctl output

* Fri Sep 23 2011 Petr Sabata <contyk@redhat.com> - 1.0.20-3
- Enable hardened build

* Mon Jul 18 2011 Petr Sabata <contyk@redhat.com> - 1.0.20-2
- Drop SysV support in favor of systemd (#714683)
- Remove ancient scriptlets (pre-1.0.7 era)
- Update quickstart.txt to reflect new changes

* Thu Jul 07 2011 Petr Sabata <contyk@redhat.com> - 1.0.20-1
- 1.0.20 bump

* Thu Jun 02 2011 Petr Sabata <contyk@redhat.com> - 1.0.19-1
- 1.0.19 bump

* Tue May  3 2011 Petr Sabata <psabata@redhat.com> - 1.0.18-2
- fcoemon: Do not create a world and group writable PID file

* Wed Apr 20 2011 Petr Sabata <psabata@redhat.com> - 1.0.18-1
- 1.0.18 bump with latest bugfixes
- Removing ExcludeArch completely; not related for Fedora
- Buildroot cleanup

* Tue Apr 19 2011 Karsten Hopp <karsten@redhat.com> 1.0.17-1.1
- remove excludearch ppc, required by anaconda.ppc

* Thu Feb 24 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.17-1
- Pull in new upstream release (required to build)
- Fix git clone URL in comments
- Drop fcoe-utils-1.0.7-init.patch, fcoe-utils-1.0.7-init-condrestart.patch
  and fcoe-utils-1.0.8-init-LSB.patch that are now upstream
- Drop fcoe-utils-1.0.8-includes.patch and use a copy of kernel headers
  for all architectures (rename fcoe-sparc.patch to fcoe-include-headers.patch)
  Upstream added detection to avoid inclusion of kernel headers in the build
  and it expects to find the userland headers installed. Those have not
  yet propagated in Fedora.
  Use temporary this workaround, since fcoe is a requiment for anaconda
  and it failed to build for a while
- Drop BuildRequires on kernel-devel
- Add BuildRequires on autoconf (it is used and not installed by default
  on all build chroots)

* Wed Feb 23 2011 Dennis Gilmore <dennis@ausil.us> - 1.0.14-5
- patch in headers used from kernel-devel on 32 bit sparc 

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 30 2010 Petr Sabata <psabata@redhat.com> - 1.0.14-3
- Removing dependency on vconfig, rhbz#658525

* Mon Jun 28 2010 Jan Zeleny <jzeleny@redhat.com> - 1.0.14-2
- added device-mapper-multipath to requires (#603242)
- added missing man pages for fcrls, fcnsq and fcping
- update of init script - added condrestart, try-restart
  and force-reload options
- added vconfig to requires (#589608)

* Mon May 24 2010 Jan Zeleny <jzeleny@redhat.com> - 1.0.14-1
- rebased to 1.0.14, see bug #593824 for complete changelog

* Mon Apr 12 2010 Jan Zeleny <jzeleny@redhat.com> - 1.0.13-1
- rebased to v1.0.13, some bugfixes, new fcoe related scripts

* Tue Mar 30 2010 Jan Zeleny <jzeleny@redhat.com> - 1.0.12-2.20100323git
- some upstream updates
- better fipvlan support
- added fcoe_edd.sh script

* Tue Mar 16 2010 Jan Zeleny <jzeleny@redhat.com> - 1.0.12-1
- rebased to version 1.0.12, improved functionality with lldpad
  and dcbd
- removed /etc/fcoe/scripts/fcoeplumb

* Thu Dec 10 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.9-2.20091204git
- excluded s390 and ppc

* Fri Dec 04 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.9-1.20091204git
- rebase to latest version of fcoe-utils

* Mon Sep 14 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.8-3
- update of init script to be LSB-compliant

* Fri Jul 31 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.8-2
- patch for clean compilation without usage of upstream's ugly hack

* Thu Jul 30 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.8-1
- rebase of fcoe-utils to 1.0.8, adjusted spec file

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 9 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.7-7
- added quickstart file to doc (#500759)

* Thu May 14 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.7-6
- renamed init script to fcoe, changed lock filename to fcoe
  (#497604)
- init script modified to do condrestart properly
- some modifications in spec file to apply previous change
  to older versions od init script during update
- fixed issue with accepting long options (#498551)

* Mon May 4 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.7-5
- fixed SIGSEGV when fcoe module isn't loaded (#498550)

* Mon Apr 27 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.7-4
- added libhbalinux to Requires (#497605)
- correction of spec file (_initddir -> _initrddir)

* Wed Apr 8 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.7-3
- more minor corrections in spec file

* Thu Apr 2 2009 Jan Zeleny <jzeleny@redhat.com> - 1.0.7-2
- minor corrections in spec file
- moved init script to correct location
- correction in the init script (chkconfig directives)

* Mon Mar 2 2009 Chris Leech <christopher.leech@intel.com> - 1.0.7-1
- initial rpm build of fcoe tools

