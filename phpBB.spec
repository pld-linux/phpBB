Summary:	A feature-rich PHP discussion board
Summary(pl):	Forum dyskusyjne o du¿ych mo¿liwo¶ciach
Name:		phpBB
Version:	2.0.8a
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/phpbb/%{name}-%{version}.tar.bz2
# Source0-md5:	44d33a5851800f8f278d3c100fb2fcb3
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
URL:		http://www.phpbb.com/
Requires:	php-pcre
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpdir		/home/httpd/html/phpBB

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
%setup -q -n %{name}2

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_phpdir}/{admin,db,images,includes,install/schemas,language,templates}

install *.{php,inc}	$RPM_BUILD_ROOT%{_phpdir}
install admin/*.php	$RPM_BUILD_ROOT%{_phpdir}/admin
install db/*.php	$RPM_BUILD_ROOT%{_phpdir}/db
install includes/*.php	$RPM_BUILD_ROOT%{_phpdir}/includes
install install/*.php	$RPM_BUILD_ROOT%{_phpdir}/install
install install/schemas/*.sql $RPM_BUILD_ROOT%{_phpdir}/install/schemas

cp -R images/*		$RPM_BUILD_ROOT%{_phpdir}/images
cp -R language/*	$RPM_BUILD_ROOT%{_phpdir}/language
cp -R templates/*	$RPM_BUILD_ROOT%{_phpdir}/templates

tar zxfv %{SOURCE1} -C $RPM_BUILD_ROOT%{_phpdir}/language/
tar zxfv %{SOURCE2} -C $RPM_BUILD_ROOT%{_phpdir}/templates/

tar zxfv %{SOURCE3} -C $RPM_BUILD_ROOT%{_phpdir}/language/
tar zxfv %{SOURCE4} -C $RPM_BUILD_ROOT%{_phpdir}/templates/

tar zxfv %{SOURCE5} -C $RPM_BUILD_ROOT%{_phpdir}/language/
tar zxfv %{SOURCE6} -C $RPM_BUILD_ROOT%{_phpdir}/templates/

%clean
rm -rf $RPM_BUILD_ROOT

%post install
echo "For instalation: http://<your.site.address>/<path>/install/install.php"
echo "For upgrade: http://<your.site.address>/<path>/install/upgrade.php"
echo
echo "Remember to uninstall %{name}-install after initiation/upgrade of %{name}!!"

%triggerpostun  -- %{name} <= %{version}
echo "You have to install %{name}-install package to prepare upgrade!!!"
echo "For upgrade: http://<your.site.address>/<path>/install/upgrade.php"

%files
%defattr(644,root,root,755)
%doc docs/*
%attr(755,root,http) %dir %{_phpdir}
%attr(640,root,http) %config(noreplace) %{_phpdir}/config.php
%attr(640,root,http) %{_phpdir}/[^c]*.php
%attr(640,root,http) %{_phpdir}/common.php
%attr(640,root,http) %{_phpdir}/*.inc
%attr(750,root,http) %dir %{_phpdir}/admin
%attr(750,root,http) %dir %{_phpdir}/db
%attr(750,root,http) %dir %{_phpdir}/images
%attr(750,root,http) %dir %{_phpdir}/includes
%{_phpdir}/admin/*
%{_phpdir}/db/*
%{_phpdir}/images/*
%{_phpdir}/includes/*
%{_phpdir}/templates/index.htm
%attr(750,root,http) %dir %{_phpdir}/templates
%attr(750,root,http) %dir %{_phpdir}/templates/subSilver
%attr(750,root,http) %dir %{_phpdir}/templates/subSilver/admin
%attr(640,root,http) %{_phpdir}/templates/subSilver/admin/*
%attr(640,root,http) %{_phpdir}/templates/subSilver/*.*
%attr(750,root,http) %dir %{_phpdir}/templates/subSilver/images
%attr(640,root,http) %{_phpdir}/templates/subSilver/images/*.*
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
