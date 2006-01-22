# Conditional build:
%bcond_without	php5		# build without php5 support
#
Summary:	A feature-rich PHP discussion board
Summary(pl):	Forum dyskusyjne o du¿ych mo¿liwo¶ciach
Name:		phpBB
Version:	2.0.19
%define	fver	20195
Release:	0.7
License:	GPL v2
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/phpbb-php5mod/%{fver}.tar.bz2
# Source0-md5:	49b3858da2f8e48e2fc5f0b144a05b6d
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
Source9:	http://dl.sourceforge.net/phpbb/%{name}-%{version}.tar.bz2
# Source9-md5:	7b8c6d6f7f92571afb34f192f3c242dd
URL:		http://www.phpbb.com/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	sed >= 4.0
Requires:	php-pcre
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_avatardir	/var/lib/%{name}/avatars
%define		_appdir		%{_datadir}/%{name}
%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}

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
%if %{without php5}
%setup -q -T -b 9 -n phpBB2
%else
%setup -q -c
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_appdir}/{admin,db,images,includes,install/schemas,language,templates} \
	$RPM_BUILD_ROOT{%{_sysconfdir},/etc/httpd,%{_avatardir}}

install *.{php,inc}	$RPM_BUILD_ROOT%{_appdir}
install admin/*.php	$RPM_BUILD_ROOT%{_appdir}/admin
install db/*.php	$RPM_BUILD_ROOT%{_appdir}/db
install includes/*.php	$RPM_BUILD_ROOT%{_appdir}/includes
install install/*.php	$RPM_BUILD_ROOT%{_appdir}/install
install install/schemas/*.sql $RPM_BUILD_ROOT%{_appdir}/install/schemas

cp -R images/*		$RPM_BUILD_ROOT%{_appdir}/images
cp -R images/avatars/*	$RPM_BUILD_ROOT%{_avatardir}
cp -R language/*	$RPM_BUILD_ROOT%{_appdir}/language
cp -R templates/*	$RPM_BUILD_ROOT%{_appdir}/templates
rm -rf $RPM_BUILD_ROOT%{_appdir}/images/avatars
ln -sf %{_avatardir} $RPM_BUILD_ROOT%{_appdir}/images/avatars

install config.php $RPM_BUILD_ROOT%{_sysconfdir}/config.php
install %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/favicon.ico
touch $RPM_BUILD_ROOT%{_sysconfdir}/robots.txt
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/config.php
ln -sf %{_sysconfdir}/favicon.ico $RPM_BUILD_ROOT%{_appdir}/favicon.ico
ln -sf %{_sysconfdir}/robots.txt $RPM_BUILD_ROOT%{_appdir}/robots.txt

tar zxf %{SOURCE1} -C $RPM_BUILD_ROOT%{_appdir}/language/
tar zxf %{SOURCE2} -C $RPM_BUILD_ROOT%{_appdir}/templates/
tar zxf %{SOURCE3} -C $RPM_BUILD_ROOT%{_appdir}/language/
tar zxf %{SOURCE4} -C $RPM_BUILD_ROOT%{_appdir}/templates/
tar zxf %{SOURCE5} -C $RPM_BUILD_ROOT%{_appdir}/language/
tar zxf %{SOURCE6} -C $RPM_BUILD_ROOT%{_appdir}/templates/
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install %{SOURCE7} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

find $RPM_BUILD_ROOT%{_appdir} -name Thumbs.db | xargs rm -f

%clean
rm -rf $RPM_BUILD_ROOT

%post
echo "You have to install %{name}-install package to prepare upgrade!!!"
echo "For upgrade: http://<your.site.address>/<path>/install/upgrade.php"

%post install
echo "For installation: http://<your.site.address>/<path>/install/install.php"
echo "For upgrade: http://<your.site.address>/<path>/install/upgrade.php"
echo
echo "Remember to uninstall %{name}-install after initiation/upgrade of %{name}!!"

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache >= 2.0.0
%webapp_register httpd %{_webapp}

%triggerun -- apache >= 2.0.0
%webapp_unregister httpd %{_webapp}

%triggerpostun -- %{name} <= 2.0.10-1
for i in `grep -lr "/home/\(services/\)*httpd/html/phpBB" /etc/httpd/*`; do
	cp $i $i.backup
	sed -i -e "s#/home/httpd/html/phpBB#%{_appdir}#g" $i
	sed -i -e "s#/home/services/httpd/html/phpBB#%{_appdir}#g" $i
	echo "File changed by trigger: $i (backup: $i.backup)"
done

%triggerpostun -- %{name} < 2.0.19-0.5
# rescue app config from various old locations
if [ -f /home/services/httpd/html/phpBB/config.php.rpmsave ]; then
	mv -f %{_sysconfdir}/config.php{,.rpmnew}
	mv -f /home/services/httpd/html/phpBB/config.php.rpmsave %{_sysconfdir}/config.php
fi

if [ -f /home/httpd/html/phpBB/config.php.rpmsave ]; then
	mv -f %{_sysconfdir}/config.php{,.rpmnew}
	mv -f /home/httpd/html/phpBB/config.php.rpmsave %{_sysconfdir}/config.php
fi

if [ -f /etc/%{name}/config.php.rpmsave ]; then
	mv -f %{_sysconfdir}/config.php{,.rpmnew}
	mv -f /etc/%{name}/config.php.rpmsave %{_sysconfdir}/config.php
fi

# nuke very-old config location (this mostly for Ra)
if [ -f /etc/httpd/httpd.conf ]; then
	sed -i -e "/^Include.*%{name}.conf/d" /etc/httpd/httpd.conf
fi

# migrate from httpd (apache2) config dir
if [ -f /etc/httpd/%{name}.conf.rpmsave ]; then
	cp -f %{_sysconfdir}/httpd.conf{,.rpmnew}
	mv -f /etc/httpd/%{name}.conf.rpmsave %{_sysconfdir}/httpd.conf
fi

rm -f /etc/httpd/httpd.conf/99_%{name}.conf
/usr/sbin/webapp register httpd %{_webapp}
%service httpd reload

%files
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/favicon.ico
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/robots.txt
%doc docs/*
%dir %{_appdir}
%{_appdir}/[!c]*.php
%{_appdir}/common.php
%{_appdir}/*.inc
%{_appdir}/admin
%{_appdir}/db
%{_appdir}/images
%{_appdir}/includes
%{_appdir}/templates/index.htm
%{_appdir}/templates/subSilver/*.*
%{_appdir}/templates/subSilver/admin/*.*
%{_appdir}/templates/subSilver/images/*.*
%{_appdir}/language/index.htm
%lang(en) %{_appdir}/language/lang_english
%lang(en) %{_appdir}/templates/subSilver/images/lang_english
%lang(pl) %{_appdir}/language/lang_polish
%lang(pl) %{_appdir}/templates/subSilver/images/lang_polish
%lang(de) %{_appdir}/language/lang_german
%lang(de) %{_appdir}/templates/subSilver/images/lang_german
%lang(fr) %{_appdir}/language/lang_french
%lang(fr) %{_appdir}/templates/subSilver/images/lang_french
%attr(710,root,http) %dir /var/lib/%{name}
%attr(1770,root,http) %dir %{_avatardir}
%{_avatardir}/index.htm
%{_avatardir}/gallery
%attr(640,root,http) %config(noreplace) %{_appdir}/config.php
%attr(640,root,http) %config(noreplace) %{_appdir}/favicon.ico
%attr(640,root,http) %config(noreplace) %{_appdir}/robots.txt

%files install
%defattr(644,root,root,755)
%doc install/schemas/*.zip
%{_appdir}/install/*.php
%{_appdir}/install/schemas/*.sql
