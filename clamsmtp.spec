Summary:	clamsmtp - clamav-based antivirus SMTP-level gateway
Summary(pl):	clamsmtp - oparta na clamavie bramka antywirusowa SMTP
Name:		clamsmtp
Version:	1.0
Release:	0.1
License:	BSD
Group:		Applications/Networking
Source0:	http://memberwebs.com/nielsen/software/clamsmtp/%{name}-%{version}.tar.gz
# Source0-md5:	935a54b585c68258e9b68bceb7819a47
# Source0-size:	138446
Source1:	%{name}.init
URL:		http://memberwebs.com/nielsen/software/clamsmtp/
#BuildRequires:	pcre-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
# FIXME: which package in PLD provides 'netfilter' ? 
#Requires:	netfilter
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
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d \
	$RPM_BUILD_ROOT{%{_sbindir},%{_sysconfdir},/etc/rc.d/init.d,/var/spool/%{name}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install doc/clamsmtpd.conf $RPM_BUILD_ROOT%{_sysconfdir}
install src/clamsmtpd $RPM_BUILD_ROOT%{_sbindir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f /var/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/%{name} start\" to start inet server" 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README NEWS
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/clamsmtpd.conf
%dir /var/spool/%{name}
