@Echo off

@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO !  Creation disque d'installation               !
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------

@Echo un peu de menage
@del /Q disc\archives\*.*



@Echo copying website
@svn export svn://localhost/Oyak/phpmyfactures tmp/phpmyfactures > c:\Oyak\create_disc.out
@cd tmp >> c:\Oyak\create_disc.out
"c:\Program Files\7-Zip\7z.exe" a  ..\disc\archives\phpmyfactures  "phpmyfactures"   "c:\Program Files\EasyPHP1-8\www\index.php"  >> c:\Oyak\create_disc.out
@cd .. >> c:\Oyak\create_disc.out

@Echo copying fichier cible
svn export svn://localhost/Oyak/cible tmp/cible >> c:\Oyak\create_disc.out
@cd tmp >> c:\Oyak\create_disc.out
"c:\Program Files\7-Zip\7z.exe" a  ..\disc\archives\cible  "cible"  >> c:\Oyak\create_disc.out
@cd .. >> c:\Oyak\create_disc.out 

@Echo copying database
"c:\Program Files\EasyPHP1-8\mysql\bin\mysqldump.exe" -u root oyak > disc\archives\oyak_fill.sql
@echo DROP DATABASE `oyak`  > disc\archives\oyak_drop.sql
@echo CREATE DATABASE `oyak`  > disc\archives\oyak_create.sql

@Echo copying apache and php config file
"c:\Program Files\7-Zip\7z.exe" a  disc\archives\apache_config  "c:\Program Files\EasyPHP1-8\apache\php.ini" "c:\Program Files\EasyPHP1-8\apache\conf\httpd.conf" >> c:\Oyak\create_disc.out


@Echo copying LaTeX 
"c:\Program Files\7-Zip\7z.exe" a  disc\archives\latex  "c:\Program Files\MiKTeX 2.5" >> c:\Oyak\create_disc.out

@echo copying vendeur.pyw et updateDatabase.py 
@copy "c:\Program Files\EasyPHP1-8\www\serveur\sql\*.py"  disc\archives >> c:\Oyak\create_disc.out
@copy "c:\Program Files\EasyPHP1-8\www\cible\pocketPC\vendeur.pyw"  disc\archives >> c:\Oyak\create_disc.out



@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO !  Creation disque d'installation  OK           !
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------



@pause





