Summary:	clamsmtp - clamav-based antivirus SMTP-level gateway
Summary(pl):	clamsmtp - oparta na clamavie bramka antywirusowa SMTP
Name:		clamsmtp
Version:	1.1
Release:	0.6
License:	BSD
Group:		Applications/Networking
Source0:	http://memberwebs.com/nielsen/software/clamsmtp/%{name}-%{version}.tar.gz
# Source0-md5:	dbb077492c1ed5acca9beb91f2808e0c
Source1:	%{name}.init
URL:		http://memberwebs.com/nielsen/software/clamsmtp/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
PreReq:		rc-scripts
Requires:	clamav
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
clamsmtp provides transparent antivirus scanner gateway for the SMTP
protocol.

%description -l pl
clamsmtp dostarcza przezroczyst± bramkê antywirusow± dla protoko³u
SMTP.

%prep
%setup -q

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
install -d $RPM_BUILD_ROOT{%{_mandir}/{man8,man5},/var/spool/%{name}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/clamsmtpd
install doc/clamsmtpd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install src/clamsmtpd $RPM_BUILD_ROOT%{_sbindir}
install doc/clamsmtpd.conf.5 $RPM_BUILD_ROOT%{_mandir}/man5/
install doc/clamsmtpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add clamsmtpd
if [ -f /var/lock/subsys/clamsmtpd ]; then
	/etc/rc.d/init.d/clamsmtpd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/clamsmtpd start\" to start inet server" 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/clamsmtpd ]; then
		/etc/rc.d/init.d/clamsmtpd stop 1>&2
	fi
	/sbin/chkconfig --del clamsmtpd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(754,root,root) /etc/rc.d/init.d/clamsmtpd
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/clamsmtpd.conf
%dir /var/spool/%{name}
%{_mandir}/man5/clamsmtpd.conf.5*
%{_mandir}/man8/clamsmtpd.8*
