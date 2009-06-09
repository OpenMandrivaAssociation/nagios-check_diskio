%define version 3.0.3
%define release %mkrel 1
%define upstream_name   check_diskio
%define name            nagios-%{upstream_name}

Name:      %{name}
Version:   %{version}
Release:   %{release}
Summary:   Nagios plugin to monitor the amount of disk I/O
License:   GPL
Group:     Applications/System
URL:        https://trac.id.ethz.ch/projects/nagios_plugins/wiki/check_diskio
Source:     http://www.id.ethz.ch/people/allid_list/corti/%{upstream_name}-%{version}.tar.gz
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}

%description
Nagios plugin to monitor the amount of disk I/O

%prep
%setup -q -n %{upstream_name}-%{version}

%build
pod2man check_diskio.pod > check_diskio.1

%install
rm -rf %{buildroot}
install -m 755 -d %{buildroot}%{_datadir}/nagios/plugins
install -m 755 -d %{buildroot}%{_mandir}/man1
install -m 755 check_diskio %{buildroot}%{_datadir}/nagios/plugins/check_diskio
install -m 644 check_diskio.1 %{buildroot}%{_mandir}/man1

perl -pi -e 's|^#!perl|#!%{_bindir}/perl|' \
    %{buildroot}%{_datadir}/nagios/plugins/check_diskio

install -m 755 -d %{buildroot}%{_sysconfdir}/nagios/plugins.d
cat > %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_diskio.cfg <<'EOF'
define command {
	command_name    check_connections
	command_line    %{_datadir}/nagios/plugins/check_diskio
}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS Changes NEWS README INSTALL TODO COPYING VERSION
%{_datadir}/nagios/plugins/check_diskio
%{_mandir}/man1/check_diskio.1*
%config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_diskio.cfg

