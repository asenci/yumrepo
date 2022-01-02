Name:           asenci-release
Version:        1
Release:        1
Summary:        @asenci personal repository configuration

Group:          System Environment/Base
License:        GPLv2
URL:            https://github.com/asenci/yumrepo

Source1:        asenci.repo

BuildArch:     noarch


%description
This package contains my personal repository configuration for yum.


%install
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/yum.repos.d/asenci.repo


%files
%defattr(644,root,root,755)
%config(noreplace) /etc/yum.repos.d/*


%changelog
* Sun Jan 02 2022 Andre Sencioles <asenci@gmail.com> - 1-1
- Initial release
