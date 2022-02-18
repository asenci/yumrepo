Name:     dump1090-fa
Version:  6.1
Release:  6%{?dist}
Summary:  FlightAware ADS-B Ground Station System for SDRs
License:  GPLv2
URL:      https://www.flightaware.com/
Source0:  https://github.com/flightaware/dump1090/archive/refs/tags/v%{version}.tar.gz

Source1:  dump1090-fa.sysconfig
Source2:  dump1090-fa.service
Source3:  lighttpd-dump1090-fa.conf

Patch0:   dump1090-fa-6.1.patch

Provides:      dump1090 = %{version}-%{release}
Obsoletes:     dump1090 < %{version}-%{release}

BuildRequires: gcc make systemd-rpm-macros
BuildRequires: hackrf-devel
BuildRequires: libusb1-devel
BuildRequires: ncurses-devel
BuildRequires: rtl-sdr-devel

%{?systemd_ordering}


%description
FlightAware ADS-B Ground Station System for SDRs
Networked Aviation Mode S / ADS-B decoder/translator with support
for RTL-SDR, BladeRF, HackRF, and LimeSDR software defined radio USB
device support.


%prep
%setup -q -n dump1090-%{version}
%patch0 -p1


%build
DUMP1090_VERSION="%{version}"; export DUMP1090_VERSION
%undefine _hardened_build
%set_build_flags
%make_build all faup1090


%install
install -Dpm 0755 dump1090 %{buildroot}%{_bindir}/dump1090-fa
install -Dpm 0755 faup1090 %{buildroot}%{_bindir}/faup1090
install -Dpm 0755 view1090 %{buildroot}%{_bindir}/view1090-fa

install -Dpm 0644 %{SOURCE3} %{buildroot}%{_docdir}/%{name}/lighttpd-dump1090-fa.conf

install -Dpm 0755 starch-benchmark %{buildroot}%{_libdir}/%{name}/starch-benchmark
install -Dpm 0755 debian/generate-wisdom %{buildroot}%{_libdir}/%{name}/generate-wisdom

install -Dpm 0755 -d %{buildroot}%{_datarootdir}/%{name}
cp -a public_html %{buildroot}%{_datarootdir}/%{name}/
cp -a bladerf %{buildroot}%{_datarootdir}/%{name}/

install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/dump1090-fa
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_unitdir}/dump1090-fa.service


%pre
getent passwd dump1090 >/dev/null 2>&1 || useradd \
  --comment 'FlightAware ADS-B Ground Station System' \
  --groups rtlsdr \
  --system \
  --home-dir '%{_datarootdir}/%{name}' \
  --shell /sbin/nologin \
  dump1090

%post
%systemd_post dump1090-fa.service

%preun
%systemd_preun dump1090-fa.service

%postun
%systemd_postun_with_restart dump1090-fa.service


%files
%license LICENSE

%doc README*.md
%doc debian/README.librtlsdr
%doc %{_docdir}/%{name}/lighttpd-dump1090-fa.conf

%config(noreplace) %{_sysconfdir}/sysconfig/dump1090-fa

%{_bindir}/dump1090-fa
%{_bindir}/faup1090
%{_bindir}/view1090-fa
%{_unitdir}/dump1090-fa.service
%{_libdir}/%{name}
%{_datarootdir}/%{name}


%changelog
* Sat Feb 19 2022 Andre Sencioles <asenci@gmail.com> - 6.1-6
- Update sysconfig defaults

* Mon Jan 31 2022 Andre Sencioles <asenci@gmail.com> - 6.1-5
- Add faup1090 to the package
- Enable Beast output by default

* Sat Jan 29 2022 Andre Sencioles <asenci@gmail.com> - 6.1-4
- Update wisdom file path

* Sat Jan 29 2022 Andre Sencioles <asenci@gmail.com> - 6.1-3
- Fix Systemd unit file

* Sat Jan 29 2022 Andre Sencioles <asenci@gmail.com> - 6.1-2
- Update dump1090-fa.sysconfig

* Sat Jan 29 2022 Andre Sencioles <asenci@gmail.com> - 6.1-1
- Initial release
