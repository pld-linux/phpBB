Summary:	A feature-rich PHP discussion board
Summary(pl):	Forum dyskusyjne o du¿ych mo¿liwo¶ciach
Name:		phpBB
Version:	2.0.3
Release:	5
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://prdownloads.sourceforge.net/phpbb/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/phpbb/lang_polish.tar.gz
Source2:	http://prdownloads.sourceforge.net/phpbb/subSilver_polish.tar.gz
Source3:	http://prdownloads.sourceforge.net/phpbb/lang_german.tar.gz
Source4:	http://prdownloads.sourceforge.net/phpbb/subSilver_german.tar.gz
Source5:	http://prdownloads.sourceforge.net/phpbb/lang_french.tar.gz
Source6:	http://prdownloads.sourceforge.net/phpbb/subSilver_french.tar.gz
Patch0:		%{name}-viewtopic-sec_fix.patch
URL:		http://www.phpbb.com/
Requires:	php-mysql >= 4.1.0
Requires:	php-pcre
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_phpdir		/home/services/httpd/html/phpBB

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
Summary:	A feature-rich PHP discussion board
Summary(pl):	Forum dyskusyjne o du¿ych mo¿liwo¶ciach
Group:		Applications/Databases/Interfaces
Requires:	phpBB

%description install
Package needed for %{name} formu instalation.

%description install -l pl
Pakiet potrzebny do instalacji forum %{name}.

%prep
%setup -q -n %{name}2
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_phpdir}/{admin,db,images,includes,language,templates}

install *.{php,inc}	$RPM_BUILD_ROOT%{_phpdir}
install admin/*.php	$RPM_BUILD_ROOT%{_phpdir}/admin
install db/*.php	$RPM_BUILD_ROOT%{_phpdir}/db
install includes/*.php	$RPM_BUILD_ROOT%{_phpdir}/includes

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
echo "Remember to uninstall %{name}-install after initiation of %{name}!!"

%files
%defattr(644,root,root,755)
%doc docs/* db/schemas/*
%attr(755,root,http) %dir %{_phpdir}
%attr(640,root,http) %config(noreplace) %{_phpdir}/config.php
%attr(640,root,http) %{_phpdir}/[efglmpsv]*.php
%attr(640,root,http) %{_phpdir}/index.php
%attr(640,root,http) %{_phpdir}/com*.php
%attr(640,root,http) %{_phpdir}/*.inc
%attr(640,root,http) %{_phpdir}/admin
%attr(640,root,http) %{_phpdir}/includes
%attr(640,root,http) %{_phpdir}/db
%attr(640,root,http) %{_phpdir}/images
%attr(640,root,http) %dir %{_phpdir}/language
# ?
%attr(640,root,http) %{_phpdir}/language/*.htm
%attr(640,root,http) %{_phpdir}/templates/subSilver/admin/
%attr(640,root,http) %{_phpdir}/templates/subSilver/*.*
%attr(640,root,http) %{_phpdir}/templates/subSilver/images/*.*

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
%attr(640,root,http) %{_phpdir}/install.php
%attr(640,root,http) %{_phpdir}/up*.php
