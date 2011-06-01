@Echo off

@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO !        Installation logiciel Oyak Mai 2007    !
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------

@rem goto TEST

@ECHO
@ECHO -------------------------------------------------
@ECHO !        Installation logiciel de base          !
@ECHO -------------------------------------------------


@ECHO Installation de 7zip
softs\7z442.exe


@ECHO Installation de Python
softs\python-2.4.4.msi


@ECHO Installation de easyphp
@Echo .... Tapez sur suivant plusieurs fois, Puis...
@ECHO .... fermez toutes les fenetres sauf
@echo         celle de controle avec les feux verts!
softs\easyphp1-8_setup.exe

@ECHO Installation de ghostscript
softs\gs853w32.exe


@ECHO Installation de ghostsview
softs\gsv48w32.exe

:DATABASE

@ECHO .
@ECHO -------------------------------------------------
@ECHO !        creation des repertoires de travail    !
@ECHO !        copie des fichiers d'archives          !
@ECHO -------------------------------------------------

@md c:\oyak 
@md c:\ventesjour > c:\Oyak\out_inst.txt 
@copy archives\*.* "c:\Oyak\" >> c:\Oyak\out_inst.txt

c:

@ECHO .
@ECHO -------------------------------------------------
@ECHO !        Installation du site web               !
@ECHO -------------------------------------------------

cd "c:\Program Files\EasyPHP1-8\www\"
"c:\Program Files\7-Zip\7z.exe" x  -y c:\Oyak\phpmyfactures.7z >> c:\Oyak\out_inst.txt
copy phpmyfactures\index_root.html index.html

@ECHO .
@ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@ECHO :                                               :
@ECHO : EasyPHP doit ABSOLUMENT ETRE DEMARRE          :
@ECHO : Verifier que les deux serveurs sont ok        :
@ECHO : ne refermez PAS la fenetre EasyPHP            :
@ECHO :  ... et tapez une touche                      :
@ECHO :                                               :
@ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@echo .
@pause 

@ECHO .
@ECHO -------------------------------------------------
@ECHO !        Installation de la base de donnee      !
@ECHO -------------------------------------------------


"c:\Program Files\EasyPHP1-8\mysql\bin\mysql.exe" -u root < c:\Oyak\oyak_drop.sql >> c:\Oyak\out_inst.txt
"c:\Program Files\EasyPHP1-8\mysql\bin\mysql.exe" -u root < c:\Oyak\oyak_create.sql >> c:\Oyak\out_inst.txt
"c:\Program Files\EasyPHP1-8\mysql\bin\mysql.exe" --database=oyak -u root < c:\Oyak\oyak_fill.sql >> c:\Oyak\out_inst.txt





@ECHO .
@ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@ECHO :                                               :
@ECHO : d'ici moins d'une minute                      :
@ECHO : vous devriez avoir une fenetre ouverte sur le :
@ECHO : site web Oyak listant les produits...         :
@ECHO :                                               :
@ECHO :  si oui, tout est OK, fermer la fenetre       :
@ECHO :      ... et tapez une touche                  :
@ECHO :  si non, quelquechose cloche,                 :
@ECHO :      ...  arretez l'installation par CTRL-C   :
@ECHO :                                               :
@ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

@explorer "http://127.0.0.1/phpmyfactures/produits/index.php"


@echo .
@pause



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



@ECHO .
@ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@ECHO :                                               :
@ECHO : EasyPHP doit etre demarre!!!!!                :
@ECHO :  ... cliquer droit sur le petit e. clignotant :
@ECHO :      en bas a droite de l'écran dans la barre :
@ECHO :      des taches      et choisir   Demarrer    :
@ECHO :                                               :
@ECHO : Verifier que les deux serveurs sont ok        :
@ECHO :  ... et tapez une touche                      :
@ECHO :                                               :
@ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@ECHO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


@ECHO .
@ECHO -------------------------------------------------
@ECHO ! Installation du logiciel de mise en page LaTeX!
@ECHO -------------------------------------------------


cd "c:\Program Files\"
"c:\Program Files\7-Zip\7z.exe" x -y  c:\Oyak\latex.7z >> c:\Oyak\out_inst.txt


:TEST

@ECHO .
@ECHO -------------------------------------------------
@ECHO !               Menage post-installation        !
@ECHO -------------------------------------------------

@del c:\Oyak\*.7z >> c:\Oyak\out_inst.txt
@del c:\Oyak\oyak_*.sql >> c:\Oyak\out_inst.txt



@ECHO .
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO !        Installation logiciel Oyak OK          !
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------
@ECHO -------------------------------------------------

@explorer "http://127.0.0.1"


@echo .
@pause

