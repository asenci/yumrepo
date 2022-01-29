Name:     rtlsdr-airband
Version:  4.0.2
Release:  3%{?dist}
Summary:  SDR AM/NFM demodulator
License:  GPLv3
URL:      https://github.com/szpajder/RTLSDR-Airband
Source0:  https://github.com/szpajder/RTLSDR-Airband/archive/v%{version}.tar.gz

Source1:  rtl_airband.sysconfig

Patch0: rtlsdr-airband-4.0.2.patch

BuildRequires: cmake cmake-rpm-macros gcc-c++ systemd-rpm-macros
BuildRequires: fftw-devel
BuildRequires: lame-devel
BuildRequires: libconfig-devel
BuildRequires: libshout-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: rtl-sdr-devel
BuildRequires: SoapySDR-devel

%{?systemd_ordering}

%description
RTLSDR-Airband receives analog radio voice channels and produces audio
streams which can be routed to various outputs, such as online
streaming services like LiveATC.net. Originally the only SDR type
supported by the program was Realtek DVB-T dongle (hence the project's
name). However, thanks to SoapySDR vendor-neutral SDR library, other
radios are now supported as well.


%prep
%setup -qn RTLSDR-Airband-%{version}
%patch0 -p1

%build
%cmake
%cmake_build

%install
%cmake_install

# copy sample configuration files
install -Dpm 0644 -t %{buildroot}%{_pkgdocdir}/examples config/*

install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/rtl_airband
install -Dpm 0644 init.d/rtl_airband.service %{buildroot}%{_unitdir}/rtl_airband.service

%pre
getent passwd rtl_airband >/dev/null 2>&1 || useradd \
  --comment 'SDR AM/NFM demodulator' \
  --groups rtlsdr \
  --system \
  --home-dir / \
  --shell /sbin/nologin \
  rtl_airband

%post
%systemd_post rtl_airband.service

%preun
%systemd_preun rtl_airband.service

%postun
%systemd_postun_with_restart rtl_airband.service


%files
%license LICENSE

%doc README.md
%doc examples

%config(noreplace) %{_sysconfdir}/sysconfig/rtl_airband

%{_bindir}/rtl_airband
%{_unitdir}/rtl_airband.service


%changelog
* Sat Jan 29 2022 Andre Sencioles <asenci@gmail.com> - 4.0.2-3
- Update systemd unit file to add support to a sysconfig file

* Mon Jan 03 2022 Andre Sencioles <asenci@gmail.com> - 4.0.2-2
- Create rtl_airband user during installation

* Sun Jan 02 2022 Andre Sencioles <asenci@gmail.com> - 4.0.2-1
- Initial release
