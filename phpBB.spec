Summary:	A feature-rich PHP discussion board
Summary(pl):	Forum dyskusyjne o du¿ych mo¿liwo¶ciach
Name:		phpBB
Version:	2.0.11
Release:	2
License:	GPL v2
Group:		Applications/WWW
#Source0:	http://dl.sourceforge.net/phpbb/%{name}-%{version}.tar.bz2
Source0:	http://dl.sourceforge.net/phpbb-php5mod/20112.tar.gz
# Source0-md5:	5f1d4db2882c5b50a04d6fb245d1e71d
Source1:	http://dl.sourceforge.net/phpbb/lang_polish.tar.gz
# Source1-md5:	db020ef788d4bd50ce04014964e3e043
Source2:	http://dl.sourceforge.net/phpbb/subSilver_polish.tar.gz
# Source2-md5:	9367f7a761aef3795ffa296b413136b4
Source3:	http://dl.sourceforge.net/phpbb/lang_german.tar.gz
# Source3-md5:	afc686072978b896e18fa211210c3b13
Source4:	http://dl.sourceforge.net/phpbb/subSilver_german.tar.gz
# Source4-md5:	8340f310ee4892f3e19da3e000fdb708
Source5:	http://dl.sourceforge.net/phpbb/lang_french.tar.gz
# Source5-md5:	c81f843d4adf0a086efef590074478e6
Source6:	http://dl.sourceforge.net/phpbb/subSilver_french.tar.gz
# Source6-md5:	419157eb144fa81b7464a5f2edeea434
Source7:	%{name}.conf
Source8:	%{name}.ico
URL:		http://www.phpbb.com/
Requires:	php-pcre
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpdir		%{_datadir}/%{name}
%define		_sysconfdir	/etc/%{name}

%description
phpBB is a UBB-style dissussion board written in PHP backended by a
MySQL database. It includes features such as posting/replying/editing
messages, private messages, private forums, user and anonymous
posting, robust theming, user ranking by posts or by special, admin
definable, ranks, and much more.

%description -l pl
phpBB jest forum dyskusyjnym w stylu UBB napisanym w PHP z u¿yciem
bazy danych MySQL. Ma mo¿liwo¶ci takie jak: wysy³anie, odpisywanie,
edycja wiadomo¶ci, prywatne wiadomo¶ci, prywatne fora, wysy³anie jako
u¿ytkownik i anonimowe, bogaty wybór motywów, ranking u¿ytkowników
wed³ug ich wiadomo¶ci lub specjalne, definiowane przez administratora,
rankingi i wiele innych.

%package install
Summary:	A feature-rich PHP discussion board - installer
Summary(pl):	Forum dyskusyjne o du¿ych mo¿liwo¶ciach - instalator
Group:		Applications/Databases/Interfaces
Requires:	phpBB

%description install
Package needed for %{name} forum instalation.

%description install -l pl
Pakiet potrzebny do instalacji forum %{name}.

%prep
%setup -q -c %{name}2

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_phpdir}/{admin,db,images,includes,install/schemas,language,templates} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/httpd}

install *.{php,inc}	$RPM_BUILD_ROOT%{_phpdir}
install admin/*.php	$RPM_BUILD_ROOT%{_phpdir}/admin
install db/*.php	$RPM_BUILD_ROOT%{_phpdir}/db
install includes/*.php	$RPM_BUILD_ROOT%{_phpdir}/includes
install install/*.php	$RPM_BUILD_ROOT%{_phpdir}/install
install install/schemas/*.sql $RPM_BUILD_ROOT%{_phpdir}/install/schemas

cp -R images/*		$RPM_BUILD_ROOT%{_phpdir}/images
cp -R language/*	$RPM_BUILD_ROOT%{_phpdir}/language
cp -R templates/*	$RPM_BUILD_ROOT%{_phpdir}/templates

install config.php $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/favicon.ico
touch $RPM_BUILD_ROOT%{_sysconfdir}/robots.txt
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_phpdir}/config.php
ln -sf %{_sysconfdir}/favicon.ico $RPM_BUILD_ROOT%{_phpdir}/favicon.ico
ln -sf %{_sysconfdir}/robots.txt $RPM_BUILD_ROOT%{_phpdir}/robots.txt

tar zxfv %{SOURCE1} -C $RPM_BUILD_ROOT%{_phpdir}/language/
tar zxfv %{SOURCE2} -C $RPM_BUILD_ROOT%{_phpdir}/templates/

tar zxfv %{SOURCE3} -C $RPM_BUILD_ROOT%{_phpdir}/language/
tar zxfv %{SOURCE4} -C $RPM_BUILD_ROOT%{_phpdir}/templates/

tar zxfv %{SOURCE5} -C $RPM_BUILD_ROOT%{_phpdir}/language/
tar zxfv %{SOURCE6} -C $RPM_BUILD_ROOT%{_phpdir}/templates/

install %{SOURCE7} $RPM_BUILD_ROOT/etc/httpd/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	if [ -f /etc/httpd/httpd.conf ] && ! grep -q "^Include.*%{name}.conf" /etc/httpd/httpd.conf; then
		echo "Include /etc/httpd/%{name}.conf" >> /etc/httpd/httpd.conf
	elif [ -d /etc/httpd/httpd.conf ]; then
		ln -sf /etc/httpd/%{name}.conf /etc/httpd/httpd.conf/99_%{name}.conf
	fi
	if [ -f /var/lock/subsys/httpd ]; then
		/usr/sbin/apachectl graceful 1>&2
	fi
fi

%post install
echo "For instalation: http://<your.site.address>/<path>/install/install.php"
echo "For upgrade: http://<your.site.address>/<path>/install/upgrade.php"
echo
echo "Remember to uninstall %{name}-install after initiation/upgrade of %{name}!!"

%preun
if [ "$1" = "0" ]; then
	umask 027
	if [ -d /etc/httpd/httpd.conf ]; then
		rm -f /etc/httpd/httpd.conf/99_%{name}.conf
	else
		grep -v "^Include.*%{name}.conf" /etc/httpd/httpd.conf > \
			/etc/httpd/httpd.conf.tmp
		mv -f /etc/httpd/httpd.conf.tmp /etc/httpd/httpd.conf
		if [ -f /var/lock/subsys/httpd ]; then
			/usr/sbin/apachectl graceful 1>&2
		fi
	fi
fi

%triggerpostun -- %{name} < %{version}
echo "You have to install %{name}-install package to prepare upgrade!!!"
echo "For upgrade: http://<your.site.address>/<path>/install/upgrade.php"

%triggerpostun -- %{name} <= 2.0.10-1
if [ -f /home/services/httpd/html/phpBB/config.php.rpmsave ]; then
	mv -f /home/services/httpd/html/phpBB/config.php.rpmsave /etc/phpBB/config.php
else
	if [ -f /home/httpd/html/phpBB/config.php.rpmsave ]; then
		mv -f /home/httpd/html/phpBB/config.php.rpmsave /etc/phpBB/config.php
	fi
fi
for i in `grep -lr "/home/\(services/\)*httpd/html/phpBB" /etc/httpd/*`; do
	cp $i $i.backup
	%{__perl} -pi -e "s#/home/httpd/html/phpBB#%{_phpdir}#g" $i
	%{__perl} -pi -e "s#/home/services/httpd/html/phpBB#%{_phpdir}#g" $i
	echo "File changed by trigger: $i (backup: $i.backup)"
done
if [ -f /var/lock/subsys/httpd ]; then
	/usr/sbin/apachectl graceful 1>&2
fi

%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}
%attr(640,root,http) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*
%config(noreplace) %verify(not size mtime md5) /etc/httpd/%{name}.conf
%doc docs/*
%attr(755,root,http) %dir %{_phpdir}
%attr(640,root,http) %{_phpdir}/[!c]*.php
%attr(640,root,http) %{_phpdir}/common.php
%attr(640,root,http) %{_phpdir}/*.inc
%attr(750,root,http) %dir %{_phpdir}/admin
%attr(750,root,http) %dir %{_phpdir}/db
%attr(750,root,http) %dir %{_phpdir}/images
%attr(640,root,http) %{_phpdir}/images/*.gif
%attr(640,root,http) %{_phpdir}/images/index.htm
%attr(750,root,http) %dir %{_phpdir}/images/smiles
%attr(1770,root,http) %dir %{_phpdir}/images/avatars
%attr(750,root,http) %dir %{_phpdir}/includes
%{_phpdir}/admin/*
%{_phpdir}/db/*
%{_phpdir}/images/smiles/*
%{_phpdir}/images/avatars/*
%{_phpdir}/includes/*
%{_phpdir}/templates/index.htm
%attr(750,root,http) %dir %{_phpdir}/templates
%attr(750,root,http) %dir %{_phpdir}/templates/subSilver
%attr(750,root,http) %dir %{_phpdir}/templates/subSilver/admin
%attr(640,root,http) %{_phpdir}/templates/subSilver/admin/*
%attr(640,root,http) %{_phpdir}/templates/subSilver/*.*
%attr(750,root,http) %dir %{_phpdir}/templates/subSilver/images
%attr(640,root,http) %{_phpdir}/templates/subSilver/images/*.*
%attr(750,root,http) %dir %{_phpdir}/language
%attr(640,root,http) %{_phpdir}/language/*.htm

%lang(en) %{_phpdir}/language/lang_english
%lang(en) %{_phpdir}/templates/subSilver/images/lang_english

%lang(pl) %{_phpdir}/language/lang_polish
%lang(pl) %{_phpdir}/templates/subSilver/images/lang_polish

%lang(de) %{_phpdir}/language/lang_german
%lang(de) %{_phpdir}/templates/subSilver/images/lang_german

%lang(fr) %{_phpdir}/language/lang_french
%lang(fr) %{_phpdir}/templates/subSilver/images/lang_french

%files install
%defattr(644,root,root,755)
%doc install/schemas/*.zip
%attr(750,root,http) %dir %{_phpdir}/install
%attr(640,root,http) %{_phpdir}/install/*.php
%attr(750,root,http) %dir %{_phpdir}/install/schemas
%attr(640,root,http) %{_phpdir}/install/schemas/*.sql
