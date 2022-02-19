%{!?tcl_version: %global tcl_version %(echo 'puts $tcl_version' | tclsh)}
%{!?tcl_sitearch: %global tcl_sitearch %{_libdir}/tcl%{tcl_version}}
Name:     piaware
Version:  7.1
Release:  3%{?dist}
Summary:  Client-side package and programs for forwarding ADS-B data to FlightAware
License:  Copyright FlightAware LLC
URL:      https://github.com/flightaware/piaware
Source0:  https://github.com/flightaware/piaware/archive/v%{version}.tar.gz
Source1:  https://github.com/flightaware/piaware-web/archive/v%{version}.zip

Source2:  piaware.service
Source3:  piaware.sysconfig
Source4:  lighttpd-piaware.conf

Patch0: piaware-7.1.patch

BuildRequires: openssl-perl systemd-rpm-macros tcl which
BuildRequires: tcl-tcllauncher

Requires: itcl
Requires: net-tools
Requires: tcl-tcllauncher
Requires: tcllib
Requires: tcltls

Recommends: dump1090-fa
Recommends: dump978-fa
Recommends: mlat-client

%{?systemd_ordering}

%description
The basic aim of the piaware package is to forward data read from an ADS-B receiver to FlightAware.
It does this using a program, piaware, aided by some support programs.
piaware - establishes an encrypted session to FlightAware and forwards data
piaware-config - used to configure piaware like with a FlightAware username and password
piaware-status - used to check the status of piaware


%prep
%setup -qn piaware-%{version}
%setup -qa 1
%patch0 -p1

%install
%set_build_flags
%make_install \
  BINDIR=%{_bindir} \
  ETCDIR=%{_sysconfdir} \
  LIBDIR=%{tcl_sitearch} \
  MANDIR=%{_mandir}

rm -f %{buildroot}%{_bindir}/piaware
ln -s tcllauncher %{buildroot}%{_bindir}/piaware

rm -f %{buildroot}%{_bindir}/piaware-config
ln -s tcllauncher %{buildroot}%{_bindir}/piaware-config

rm -f %{buildroot}%{_bindir}/piaware-status
ln -s tcllauncher %{buildroot}%{_bindir}/piaware-status

rm -f %{buildroot}%{_bindir}/pirehose
ln -s tcllauncher %{buildroot}%{_bindir}/pirehose

rm -f %{buildroot}%{_mandir}/man1/faup1090.1

install -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/piaware.service
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/piaware

install -Dpm 0644 %{SOURCE4} %{buildroot}%{_docdir}/%{name}/lighttpd-piaware.conf
install -Dpm 0755 -d %{buildroot}%{_datarootdir}/%{name}
cp -a piaware-web-%{version}/web %{buildroot}%{_datarootdir}/%{name}/public_html
rm -f %{buildroot}%{_datarootdir}/%{name}/public_html/README.md
mv %{buildroot}%{_datarootdir}/%{name}/public_html/translations/en.js %{buildroot}%{_datarootdir}/%{name}/public_html/translations/lang.js


%pre
getent passwd piaware >/dev/null 2>&1 || useradd \
  --comment 'FlightAware ADS-B uploader' \
  --system \
  --home-dir / \
  --shell /sbin/nologin \
  piaware

%post
%systemd_post piaware.service

%preun
%systemd_preun piaware.service

%postun
%systemd_postun_with_restart piaware.service


%files
%doc %{_docdir}/%{name}/lighttpd-piaware.conf

%config(noreplace) %{_sysconfdir}/sysconfig/piaware

%{_bindir}/piaware
%{_bindir}/piaware-config
%{_bindir}/piaware-status
%{_bindir}/pirehose
%{_unitdir}/piaware.service
%{tcl_sitearch}
%{_mandir}
%{_datarootdir}/%{name}/public_html

%changelog
* Sat Feb 19 2022 Andre Sencioles <asenci@gmail.com> - 7.1-4
- Add status web page

* Sat Feb 19 2022 Andre Sencioles <asenci@gmail.com> - 7.1-3
- Update systemd unit file

* Sat Feb 19 2022 Andre Sencioles <asenci@gmail.com> - 7.1-2
- Update mlat client path

* Sat Feb 19 2022 Andre Sencioles <asenci@gmail.com> - 7.1-1
- Initial release
