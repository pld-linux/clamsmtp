Summary:	clamav-based antivirus SMTP-level gateway
Summary(pl.UTF-8):	Oparta na clamavie bramka antywirusowa SMTP
Name:		clamsmtp
Version:	1.9
Release:	1
License:	BSD
Group:		Applications/Networking
Source0:	http://memberwebs.com/nielsen/software/clamsmtp/%{name}-%{version}.tar.gz
# Source0-md5:	cdc7a318e9583f7c3ff925f6ef5f6ae7
Source1:	%{name}.init
Patch0:		%{name}-config.patch
URL:		http://memberwebs.com/nielsen/software/clamsmtp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	clamav
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
clamsmtp provides transparent antivirus scanner gateway for the SMTP
protocol.

%description -l pl.UTF-8
clamsmtp dostarcza przezroczystą bramkę antywirusową dla protokołu
SMTP.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}

%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},/etc/rc.d/init.d}
install -d $RPM_BUILD_ROOT{%{_mandir}/{man8,man5},/var/spool/clamsmtpd/tmp}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/clamsmtpd
install doc/clamsmtpd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install src/clamsmtpd $RPM_BUILD_ROOT%{_sbindir}
install doc/clamsmtpd.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/
install doc/clamsmtpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add clamsmtpd
%service clamsmtpd restart

%preun
if [ "$1" = "0" ]; then
	%service clamsmtpd stop
	/sbin/chkconfig --del clamsmtpd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(754,root,root) /etc/rc.d/init.d/clamsmtpd
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/clamsmtpd.conf
%dir %attr(770,root,clamav) /var/spool/clamsmtpd
%dir %attr(770,root,clamav) /var/spool/clamsmtpd/tmp
%{_mandir}/man5/clamsmtpd.conf.5*
%{_mandir}/man8/clamsmtpd.8*
