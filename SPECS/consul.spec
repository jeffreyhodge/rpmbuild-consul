%define debug_package %{nil}

Name:		consul
Version:	0.7.0
Release:	1%{dist}
Summary:	A tool for service discovery
Group:		Applications/Internet
License:	Mozilla Public License 2.0
URL:		https://www.consul.io
%ifarch x86_64 amd64
Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_amd64.zip
%else
Source0:        https://releases.hashicorp.com/%{name}/%{version}/%{name}_%{version}_linux_386.zip
%endif
Source1:        %{name}.json
Source2:        %{name}.init
Source3:        %{name}.logrotate
Source4:        %{name}.sysconfig
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Consul is a tool for service discovery and configuration. Consul is distributed, 
highly available, and extremely scalable.

%prep
%setup -c
%build
%install
%{__install} -d -m 0755 %{buildroot}%{_sbindir} \
                        %{buildroot}%{_sysconfdir}/%{name} \
                        %{buildroot}%{_sysconfdir}/logrotate.d \
                        %{buildroot}%{_sysconfdir}/rc.d/init.d \
                        %{buildroot}%{_sysconfdir}/sysconfig \
                        %{buildroot}%{_localstatedir}/{lib,log,run}/%{name}
         
%{__install} -m 0755 %{name} %{buildroot}%{_sbindir}
%{__install} -m 0600 %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}
%{__install} -m 0755 %{SOURCE2} %{buildroot}%{_sysconfdir}/rc.d/init.d/%{name}
%{__install} -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__install} -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
  useradd -r -g %{name} -s /sbin/nologin \
    -d %{_localstatedir}/lib/%{name} -c "RPM Created Consul User" %{name}

%post
/sbin/chkconfig --add %{name}

%preun
/sbin/service %{name} stop > /dev/null 2>&1
/sbin/chkconfig --del %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,consul,consul,-)
%attr(-,root,root) %{_sbindir}/%{name}
%attr(-,root,root) %{_sysconfdir}/logrotate.d/%{name}
%attr(-,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%attr(-,root,root) %{_sysconfdir}/sysconfig/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.*
%{_localstatedir}/lib/%{name}
%{_localstatedir}/log/%{name}
%{_localstatedir}/run/%{name}

%changelog
* Tue May 03 2016 Taylor Kimball <taylor@linuxhq.org> - 0.6.4-1
- Initial build.
