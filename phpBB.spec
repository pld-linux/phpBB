Summary:	A feature-rich PHP discussion board
Summary(pl):	Forum dyskusyjne o du¿ych mo¿liwo¶ciach
Name:		phpBB
Version:	2.0.3
Release:	2
License:	GPL v2
Group:		Applications/Databases/Interfaces
Source0:	http://prdownloads.sourceforge.net/phpbb/%{name}-%{version}.tar.gz
Source1:	http://prdownloads.sourceforge.net/phpbb/lang_polish.tar.gz
Source2:	http://prdownloads.sourceforge.net/phpbb/subSilver_polish.tar.gz
URL:		http://www.phpbb.com/
Requires:	php-mysql >= 4.1.0
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

%prep
%setup -q -n %{name}2

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
#mkdir 			$RPM_BUILD_ROOT%{_phpdir}/images/avatars

tar zxfv %{SOURCE1} -C $RPM_BUILD_ROOT%{_phpdir}/language/
tar zxfv %{SOURCE2} -C $RPM_BUILD_ROOT%{_phpdir}/templates/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/* db/schemas/*
%dir %{_phpdir}
%{_phpdir}/*.php
%{_phpdir}/*.inc
%dir %{_phpdir}/admin
%dir %{_phpdir}/includes
%dir %{_phpdir}/db
%dir %{_phpdir}/images
%dir %{_phpdir}/images/smiles
%dir %{_phpdir}/images/avatars
%dir %{_phpdir}/images/avatars/*
%dir %{_phpdir}/language/*.htm
%{_phpdir}/admin/*.php
%{_phpdir}/db/*.php
%{_phpdir}/includes/*.php
%{_phpdir}/images/*.gif
%{_phpdir}/images/*.htm
%{_phpdir}/images/smiles/*.gif
%{_phpdir}/templates/*.htm

%lang(en) %{_phpdir}/language/lang_english
%lang(en) %{_phpdir}/templates/subSilver/images/lang_english/*.gif
%lang(pl) %{_phpdir}/language/lang_polish
%lang(pl) %{_phpdir}/templates/subSilver/images/lang_polish/*.gif
