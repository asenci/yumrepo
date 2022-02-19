Name:     dump978-fa
Version:  7.1
Release:  2%{?dist}
Summary:  FlightAware 978MHz UAT decoder
License:  GPLv2
URL:      https://www.flightaware.com/
Source0:  https://github.com/flightaware/dump978/archive/refs/tags/v%{version}.tar.gz

Source1:  dump978-fa.sysconfig
Source2:  dump978-fa.service
Source3:  skyaware978.sysconfig
Source4:  skyaware978.service
Source5:  lighttpd-dump978-fa.conf

Provides:      dump978 = %{version}-%{release}
Obsoletes:     dump978 < %{version}-%{release}

BuildRequires: gcc make systemd-rpm-macros
BuildRequires: SoapySDR-devel
BuildRequires: boost-devel

%{?systemd_ordering}


%description
FlightAware ADS-B Ground Station System for SDRs
It talks to the SDR, demodulates UAT data, and provides the data in a variety of ways - either as raw messages or as json-formatted decoded messages, and either on a network port or to stdout.


%prep
%setup -q -n dump978-%{version}


%build
VERSION="%{version}"; export VERSION
%set_build_flags
%make_build all faup978


%install
install -Dpm 0755 dump978-fa %{buildroot}%{_bindir}/dump978-fa
install -Dpm 0755 faup978 %{buildroot}%{_bindir}/faup978
install -Dpm 0755 skyaware978 %{buildroot}%{_bindir}/skyaware978

install -Dpm 0644 %{SOURCE5} %{buildroot}%{_docdir}/%{name}/lighttpd-dump978-fa.conf

install -Dpm 0755 -d %{buildroot}%{_datarootdir}/skyaware978
cp -a skyaware %{buildroot}%{_datarootdir}/skyaware978/public_html

install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/dump978-fa
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/dump978-fa.service
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/skyaware978
install -Dpm 0644 %{SOURCE4} %{buildroot}%{_unitdir}/skyaware978.service


%pre
getent passwd dump978 >/dev/null 2>&1 || useradd \
  --comment 'FlightAware ADS-B Ground Station System' \
  --groups rtlsdr \
  --system \
  --home-dir '%{_datarootdir}/%{name}' \
  --shell /sbin/nologin \
  dump978

%post
%systemd_post dump978-fa.service skyaware978.service

%preun
%systemd_preun dump978-fa.service skyaware978.service

%postun
%systemd_postun_with_restart dump978-fa.service skyaware978.service


%files
%license LICENSE

%doc README.md
%doc %{_docdir}/%{name}/lighttpd-dump978-fa.conf

%config(noreplace) %{_sysconfdir}/sysconfig/dump978-fa
%config(noreplace) %{_sysconfdir}/sysconfig/skyaware978

%{_bindir}/dump978-fa
%{_bindir}/faup978
%{_bindir}/skyaware978
%{_unitdir}/dump978-fa.service
%{_unitdir}/skyaware978.service
%{_datarootdir}/skyaware978


%changelog
* Sat Feb 19 2022 Andre Sencioles <asenci@gmail.com> - 7.1-2
- Update lighttpd config

* Mon Feb  7 2022 Andre Sencioles <asenci@gmail.com> - 7.1-1
- Initial release
