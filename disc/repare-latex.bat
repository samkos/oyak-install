@Echo off

@ECHO .
@ECHO -------------------------------------------------
@ECHO !        Copying patch file                     !
@ECHO -------------------------------------------------

@copy archives\*.ltx "c:\Oyak\" >> c:\Oyak\out_inst.txt
c:


@ECHO .
@ECHO -------------------------------------------------
@ECHO ! Installation du logiciel de mise en page LaTeX!
@ECHO -------------------------------------------------


cd "c:\Program Files\"

@copy c:\Oyak\latex5.ltx  "C:\Program Files\MiKTeX 2.5\tex\latex\base\latex.ltx" >> c:\Oyak\out_inst.txt
@copy c:\Oyak\latex6.ltx  "C:\Program Files\MiKTeX 2.6\tex\latex\base\latex.ltx" >> c:\Oyak\out_inst.txt



@echo Latex est repare
@pause

