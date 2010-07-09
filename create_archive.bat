@Echo off

@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO !  Creation disque d'installation               !
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------

PATH=e:\Program Files\Subversion\bin;c:\Program Files\EasyPHP1-8\mysql\bin;e:\Program Files\EasyPHP 2.0b1\mysql\bin;C:\WINDOWS\system32;c:\windows;c:\program Files\ghostgum\gsview;e:\program Files\ghostgum\gsview

@Echo un peu de menage
@del /Q disc\archives\phpmyfactures.7z
@del /Q disc\archives\apache_config.7z
@del /Q disc\archives\*.sql
@del /Q tmp
mkdir tmp



@Echo copying website
@svn export https://svn2.assembla.com/svn/Oyak/phpmyfactures-papa tmp/phpmyfactures ../ >> create_archive.out
@cd tmp >> create_archive.out
"c:\Program Files\7-Zip\7z.exe" a ..\disc\archives\phpmyfactures  "phpmyfactures"   "..\..\index.php"  >> create_archive.out
@cd .. >> create_archive.out


@Echo copying database
"mysqldump.exe" -u root oyak > disc\archives\oyak_fill.sql
@echo DROP DATABASE `oyak`  > disc\archives\oyak_drop.sql
@echo CREATE DATABASE `oyak`  > disc\archives\oyak_create.sql

@Echo copying apache and php config file
"c:\Program Files\7-Zip\7z.exe" a  disc\archives\apache_config  "..\..\..\apache\php.ini" "..\..\..\conf\httpd.conf" >> create_archive.out



@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO !  Creation archives  OK                        !
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------



@pause





