@ECHO OFF

@ECHO .
@ECHO -------------------------------------------------
@ECHO !        Configuration apache et PHP             !
@ECHO -------------------------------------------------

@copy archives\*.* "c:\Oyak\" >> c:\Oyak\out_inst.txt
c:
cd "c:\Program Files\EasyPHP1-8\apache\"
"c:\Program Files\7-Zip\7z.exe" x -y c:\Oyak\apache_config.7z 
@rem >> c:\Oyak\out_inst.txt
@copy conf\httpd.conf conf\httpd.conf >> c:\Oyak\out_inst.txt
@rename ..\php\php.ini ..\php\php_old.ini >> c:\Oyak\out_inst.txt
@copy conf\php.ini ..\php\php.ini >> c:\Oyak\out_inst.txt


@pause
