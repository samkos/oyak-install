# -*- coding: cp1252 -*-
from Tkinter import *
import string
import urllib
import os
import time
import shutil
import traceback

maxDigits=130
cible=os.path.exists('\Platform')
oneFrame=01
version="0.22"
time_last_key=0
isServeurInjoignable=0

if cible:
    zoomedWindow=1
    erreurCatch=0
    debugMessages=0
    raiseError=0
    isReadFromServer=0
    website_address="http://192.168.111.77/phpmyfactures"
else:
    erreurCatch=0
    debugMessages=1
    zoomedWindow=0
    raiseError=1
    isReadFromServer=1
    website_address="http://127.0.0.1/phpmyfactures"


Produits={}
ProduitsFournisseurs={}
ProduitsRacourcis={}
ProduitsCodes={}
Clients={}
Vendeurs={}
Fournisseurs={}
Fournisseurs['9999']=('XXXX','xxxx','9999','0000000000000')
Releases={}
Factures={}
clientNB = {}


for i in range(10):
    clientNB[i]=0
    
clefsClients=list()
nbChamps = {"vendeurs":4, "fournisseurs":4, "clients":4,
            "releases":2,"produits":8}
isAlreadyLoaded = {"vendeurs":0, "fournisseurs":0, "clients":0,
            "releases":0,"produits":0}

formatFact="%5.2f|%15s|%5.2f"
enteteFact="%5s|%15s|%5s"%("quant","produit","prix")



url_send_commande=website_address+"/query/index.php?"
url_update_commande=website_address+"/query/download.php?"

fichierBackup_Template='\Oyak\%s.bak'
url_get_Template=website_address+"/query/get_data.php?%s=1"

sep1=";"
sep2="!"


vendeurChoisi=(0,"xxx",'xx')
factureCurrent=0
ihm=0


###################################################################
#
#  fonction IHM annexe
#
###################################################################

def getNBfacture() :
    global clientNB
    i=1
    for i in range(10):
        if clientNB[i]==0:
            clientNB[i]=1
            return i
    return -1

def getFirstFacture() :
    global clientNB

    for i in range(10):
        if clientNB[i]>0:
            return i
    return -1

def releaseNBfacture(i):
    global clientNB
    clientNB[i]=0

def  isNBfacture(i):
    global clientNB

    return clientNB[i]

def bindElementKeysFunction(element, keys, func):
    for c in keys:
        element.bind(c,func)



###############################################################################################
# Gestion rationalisée de l'IHM
###############################################################################################


class ihmRoot:

    def __init__(self):
       self.ihm=Tk()
       if cible:
           self.ihm.overrideredirect(1)

       self.ihmPanels={}
       self.ihmPanelsContents={}
       self.filtreChoice={}
       self.filtreLabel={}
       self.listbox={}
       self.listbox0={}
       self.facture={}
       self.factureButton={}
       self.okButton={}
       
       self.Xmax=38
       self.Ymax=24

       self.ihm.rowconfigure(0,weight=1)
       self.ihm.columnconfigure(0,weight=1)
       #self.ihm.master.grid(sticky=W+E+N+S)
       
       self.messagePanelCreate()
       self.messageOuiNonPanelCreate()

       self.progressBarCreate()
       self.menuCreate()
       self.adminCreate()
       
       self.currentShown="message"
       
    # fonctions de Management des fenetres types
    
    def title(self,s):
       self.ihm.title(s)

    def add(self,panelName,widgetName,widget,row,column,rowspan=1,colspan=1,sticky=N+E+W+S):
        if panelName in self.ihmPanels.keys():
           self.ihmPanels[panelName].append(widgetName)
        else:
           self.ihmPanels[panelName]=[widgetName]
        self.ihmPanelsContents[panelName,widgetName]=(widget,row,column,rowspan,colspan,sticky)
      
    def hide(self,panelName):
        for widgetName in self.ihmPanels[panelName]:
            (widget,row,column,rowspan,colspan,sticky)=self.ihmPanelsContents[panelName,widgetName]
            widget.grid_forget()
            
    def show(self,panelName,title="Oyak"):
        global zoomedWindow,Factures

        #self.oldFocus=self.ihm.tk.call('focus')
        #print "yyyyy",self.oldFocus
        
        self.hideAll()
        
        self.ihm.title(title)
        for widgetName in self.ihmPanels[panelName]:
            (widget,row,column,rowspan,colspan,sticky)=self.ihmPanelsContents[panelName,widgetName]
            widget.grid(row=row,column=column,rowspan=rowspan,columnspan=colspan,sticky=sticky)

        if zoomedWindow:
            self.ihm.wm_state(newstate="zoomed")

        self.previousShown=self.currentShown
        self.currentShown=panelName


    def hideAll(self):
        for panel in self.ihmPanels.keys():
            self.hide(panel)

    def returnPrevious(self):
        self.show(self.previousShown)
        #self.ihm.call('focus',self.oldFocus)


    # creation fenetre type message
    
    def messagePanelCreate(self):
        self.message=StringVar("")
        self.message.set("Message Type")
        self.MessageButton=Button(self.ihm,textvariable=self.message,width=self.Xmax,height=self.Ymax)
        self.add("message","texte",self.MessageButton,0,0)

    def showMessage(self,what,commande=0):
        self.message.set(what)
        if not(commande):
            self.MessageButton["command"]=self.returnPrevious
        else:
            self.MessageButton["command"]=commande
        self.show("message")

        self.MessageButton.bind("<Key>",lambda x="fake":self.MessageButton.invoke())
        self.MessageButton.focus_set()
        

    # creation fenetre type Oui/Non
    
    def messageOuiNonPanelCreate(self):
        self.messageOuiNon=StringVar("")
        self.messageOuiNon.set("Message Type")
        self.labelOuiNon=Label(self.ihm,textvariable=self.messageOuiNon,width=self.Xmax,height=self.Ymax/3)
        self.add("OuiNon","question",self.labelOuiNon,0,0)
        self.buttonOui=Button(self.ihm,text="Oui",width=self.Xmax,height=self.Ymax/3)
        self.add("OuiNon","oui",self.buttonOui,1,0)
        self.buttonNon=Button(self.ihm,text="Non",width=self.Xmax,height=self.Ymax/3)
        self.add("OuiNon","non",self.buttonNon,2,0)

    def showMessageOuiNon(self,what,siOui=0,siNon=0):
        self.messageOuiNon.set(what)
        if not(siOui):
            self.buttonOui["command"]=self.returnPrevious
        else:
            self.buttonOui["command"]=siOui

        if not(siNon):
            self.buttonNon["command"]=self.returnPrevious
        else:
            self.buttonNon["command"]=siNon

        self.show("OuiNon")

        self.buttonNon.bind("<Key>",lambda x="fake":self.buttonNon.invoke())
        self.buttonNon.focus_set()
        

    # creation fenetre type progressBar
    def progressBarCreate(self):
        self.messageBar=StringVar("")
        self.messageBar.set("Message Type")
        self.labelBar=Button(self.ihm,textvariable=self.messageBar,width=self.Xmax,height=self.Ymax-2)
        self.add("progress","texte",self.labelBar,0,0)
        self.progressBar=Canvas(self.ihm, width=self.Xmax, height=30)
        self.add("progress","bar",self.progressBar,1,0)

    def startProgressBar(self,what):
        self.show("progress")
        self.updateProgressBar(what,0)
    
    def updateProgressBar(self,what,ratio):
        self.messageBar.set(what)
        self.labelBar.update()
        self.progressBar.delete(ALL)
        self.progressBar.create_rectangle(0, 0, self.Xmax* ratio*6., 30, fill='blue')
        self.ihm.update()
        
        
    # creation fenetre type Menu
    
    def menuCreate(self):

        panelName = "menu"
        
        label = Button(self.ihm, text="Retour", command=self.returnPrevious,height=3,width=self.Xmax)
        self.add(panelName,"retour",label,1,0)

        label = Button(self.ihm, text="Factures en Cours", command=self.showFactureFirst,height=4,width=self.Xmax)
        self.add(panelName,"en cours",label,2,0)

        label = Button(self.ihm, text="Nouvelle Facture", command=processFacture,height=4,width=self.Xmax)
        self.add(panelName,"autre",label,3,0)


        label = Button(self.ihm, text="Reactiver Scanner", command=self.scanner,height=4,width=self.Xmax)
        self.add(panelName,"scanner",label,8,0)
        
        label = Button(self.ihm, text="TestReseau", command=self.testReseau,height=4,width=self.Xmax)
        self.add(panelName,"reseau",label,9,0)

        label = Button(self.ihm, text="Administrer", command=self.showAdmin,height=5,width=self.Xmax)
        self.add(panelName,"admin",label,10,0)

    # creation fenetre type Menu
    
    def adminCreate(self):

        panelName = "admin"
        
        label = Button(self.ihm, text="Retour", command=self.returnPrevious,height=3,width=self.Xmax)
        self.add(panelName,"retour",label,2,0)

        label = Button(self.ihm, text="Relire Donnée", command=self.rechargeBase,height=4,width=self.Xmax)
        self.add(panelName,"reloader",label,6,0)
        
        label = Button(self.ihm, text="Mettre a jour", command=chooseRelease,height=4,width=self.Xmax)
        self.add(panelName,"update",label,7,0)
        
        
        label = Button(self.ihm, text="QUITTER", command=self.ihm.quit,height=4,width=self.Xmax)
        self.add(panelName,"quitter",label,10,0)
        
    # creation fenetre type menu

    def showMenu(self):
        self.show("menu")

    def showAdmin(self):
        self.show("admin")

    def testReseau(self):
        os.system('\windows\nictt.exe')

    def scanner(self):
        os.system('\windows\startup\scanwedge.exe')


    # creation fenetre type Facture
    
    def factureCreate(self,num):

        what="%d"%num
        panelName = "facture"+what
        
        # Menu
        label = Button(self.ihm, text="MENU", command=self.showMenu,height=3,width=self.Xmax+1)
        self.add(panelName,"filtreLabel",label,0,0,colspan=5)
        
        # frame

        self.facture[what] = Frame(self.ihm,width=self.Xmax,height=self.Ymax-30)
        self.add(panelName,"facture",self.facture[what],1,0,colspan=5)

        button = Button(self.ihm, text="<<<", command=self.facturePrevious,height=3,width=6)
        self.add(panelName,"previous",button,3,0)

        button = Button(self.ihm, text="Nouvelle\nFacture", command=self.factureNew,height=3,width=6)
        self.factureButton[num,"ajouter"]=button
        self.add(panelName,"ajouter",button,3,1)
        
        button = Button(self.ihm, text="envoyer\nFacture", command=self.ihm.quit,height=3,width=6)
        self.factureButton[num,"envoyer"]=button
        self.add(panelName,"envoyer",button,3,2)
        
        button = Button(self.ihm, text="Annuler\nFacture", command=self.ihm.quit,height=3,width=6)
        self.factureButton[num,"annuler"]=button
        self.add(panelName,"annuler",button,3,3)

        button = Button(self.ihm, text=">>>", command=self.factureNext,height=3,width=6)
        self.add(panelName,"next",button,3,4)


        return self.facture[what]

    def start(self):
        global zoomedWindow,version
        
        if zoomedWindow:
            self.ihm.wm_state(newstate="zoomed")
        self.startProgressBar("OYAK v %s \n\n\n Bienvenue"%version)
        self.ihm.after(2000,self.lectureDonnee)
        self.ihm.mainloop()

    def facturePrevious(self):
        global factureCurrent,clientNB
        
        nbPrevious=factureCurrent-1

        while nbPrevious>=0:
            if clientNB[nbPrevious]>0:
                Factures[nbPrevious].show()
                return 
            nbPrevious = nbPrevious-1

        self.showMessage("Pas d'autre\nFacture!!!")

    def factureNext(self):
        global factureCurrent,clientNB
        
        nbNext=factureCurrent+1

        while nbNext<10:
            if clientNB[nbNext]>0:
                Factures[nbNext].show()
                return 
            nbNext = nbNext+1

        self.showMessage("Pas d'autre\nFacture!!!")

    def showFactureFirst(self,menu=0):
        i=getFirstFacture()
        if  i<0 and menu==0:
            self.factureNew()
        else:
            if i<0:
                chooseClient()
            else:
                Factures[i].show()

    def factureNew(self):
        self.showMessageOuiNon("Demarrer une \nautre Facture?",siOui=processFacture)

    def delCurrentFacture(self):
        global factureCurrent,Factures

        releaseNBfacture(factureCurrent)
        self.showFactureFirst(menu=1)

    def lectureDonnee(self):
        global isReadFromServer
        lisData(isReadFromServer)
        chooseVendeur()

    def rechargeBase(self):
        ihm.showMessage("Telechargement du serveur")
        lisData(readFromServer=1)
        ihm.showMessage("OK...",self.showMenu)



###################################################################
#
#  Lectures des datas
#
###################################################################

class lisData:

    def __init__(self,readFromServer=0):
        global ihm

        self.readFromServer=readFromServer
        es=ihm.updateProgressBar("Chargement Data",0.)
        
#        ihm.updateProgressBar("vendeur...",0.1)
#        getVendeurs(self.readFromServer)
#        ihm.updateProgressBar("Produits...",0.3)
#        getProduits(self.readFromServer)
#        ihm.updateProgressBar("client...",0.6)
#        getClients(self.readFromServer)
#        ihm.updateProgressBar("fournisseur...",0.9)
#        getFournisseurs(self.readFromServer)
#        ihm.updateProgressBar("Releases...",0.95)
#        getReleases(readFromServer=1)

    

class getData:

    def __init__(self,what,readFromServer):
        global ihm, fichierBackup_Template,url_get_Templare, nbChamps

        if not(isAlreadyLoaded[what]):
            self.choosePanelCreate(what)
            
            # initialisation
            self.create_backup=0
            self.what=what
            self.readFromServer=readFromServer
            self.urlName=url_get_Template%what
            self.fichierBackup=fichierBackup_Template%what

            lengthArticle=nbChamps[what]
            
            self.dataAvailable=self.openSource()
            if self.dataAvailable==0:
                self.readSource(lengthArticle)
                self.closeSource()

            isAlreadyLoaded[what]=1


    # creation fenetre type choix
    
    def choosePanelCreate(self,what):
        global ihm
        
        panelName = what
        panelName0 = what+"0"
        
        # Menu
        label = Button(ihm.ihm, text="MENU", command=ihm.showMenu,height=2)
        ihm.add(panelName,"menu",label,0,0,colspan=2)
        ihm.add(panelName0,"menu",label,0,0,colspan=2)
        
        # filtre
        ihm.filtreLabel[what]=StringVar("")
        ihm.filtreLabel[what].set("filtre >")
        label = Label(ihm.ihm, textvariable=ihm.filtreLabel[what],
                      width=ihm.Xmax-1, height=1,justify="left", fg="red")
        ihm.add(panelName,"filtreLabel",label,1,0,sticky="W")
        ihm.add(panelName0,"filtreLabel",label,1,0,sticky="W")
        
        # liste box

        scrollbar = Scrollbar(ihm.ihm)
        scrollbar0 = Scrollbar(ihm.ihm)
        ihm.add(panelName,"scrollbar",scrollbar,2,1,sticky=N+S)
        ihm.add(panelName0,"scrollbar",scrollbar0,2,1,sticky=N+S)
        
        ihm.listbox[what] = Listbox(ihm.ihm, height=ihm.Ymax-6, yscrollcommand=scrollbar.set)
        ihm.add(panelName,"listbox",ihm.listbox[what],2,0)
        scrollbar.config(command=ihm.listbox[what].yview)

        ihm.listbox0[what] = Listbox(ihm.ihm, height=ihm.Ymax-6, yscrollcommand=scrollbar.set)
        ihm.add(panelName0,"listbox",ihm.listbox0[what],2,0)
        scrollbar0.config(command=ihm.listbox0[what].yview)


        # Menu
        button = Button(ihm.ihm, text="OK", height=3)
        ihm.okButton[what]=button
        ihm.add(panelName,"OK",button,3,0,colspan=2)
        ihm.add(panelName0,"OK",button,3,0,colspan=2)




    def readFromUrl(self):
        global isServeurInjoignable
        try:
           self.origFileh = urllib.urlopen(self.urlName)
           if debugMessages:
              print "creation fichier Backup OK pour ",self.what
           self.create_backup=1
           self.backupFile = open(self.fichierBackup,"w")
           return 0
        except:
           if self.readFromServer:
               if not(isServeurInjoignable):
                   ihm.showMessage("Solveur injoignable\n Impossibe de télécharger les data du serveur \n Repli sur Backup")
               isServeurInjoignable=1
           return -1 
            
    def readFromBackup(self):
           global debugMessages

           try :
               self.origFileh = open(self.fichierBackup)
           except :
                return -1     
           if debugMessages:
              print "lecture fichier Backup OK pour ",self.what
           if self.origFileh:
                return 0
           else:
                return -1
            
    def openSource(self):
       global debugMessages
       
       if self.readFromServer:
           if debugMessages:
               print "Force la lecture des Data %s sur serveur"%self.what
           isreached=self.readFromUrl()
       if not(self.readFromServer) or isreached<0:
           isreached=self.readFromBackup()
           if isreached<0:
               isreached=self.readFromUrl()
       if isreached>=0:     
          self.fileList = self.origFileh.readlines()
          return 0
       else:
          return -1

    def readSource(self,lengthArticle):
        self.nbArticles=0
        for l in self.fileList:
            if self.create_backup:
                self.backupFile.write(l)
            articles=string.split(l,"=")
            for a in articles:
                article=string.split(a,"!")
                if len(article)==lengthArticle:
                    self.collect(article)
                    self.nbArticles+=1

    def closeSource(self):                    
        self.origFileh.close()
        if self.create_backup:
            self.backupFile.close()
        if debugMessages:
            print "%d %s lus "%(self.nbArticles,self.what)



################################################################################
# Choix Vendeur, client, Produits, fournisseurs
##################################################################################

class chooseXXX(getData):

    def __init__(self,what,filtre="",killable=0):
        global ihm,isReadFromServer

        # chargement des données
        getData.__init__(self,what,isReadFromServer)

        
        self.listbox = ihm.listbox[what]
        self.listbox0 = ihm.listbox0[what]
        self.clefs0={}
        
        self.what=what
        self.killable=killable

        
        self.filtre=filtre

        self.initPanel()

        self.setFiltre(filtre)

        self.ihmChoix()

        ihm.okButton[what]["command"]=lambda x="fake" : self.go("fake")
        
        self.listePrepare()

        ihm.show(what)

        self.action()
        

    def initPanel(self):
        pass
            
    def listePrepare(self):
        pass
            
    def setFiltre(self,filtre):
        ihm.filtreLabel[self.what].set(self.filtreName+filtre)
        
    def addchar(self,event):
        self.filtre=self.filtre+event.char
        self.setFiltre(self.filtre)
        self.action()

    def delchar(self,event):
        if len(self.filtre)==0 and self.killable:
            ihm.returnPrevious()
            return
        self.filtre=self.filtre[:-1]
        self.setFiltre(self.filtre)
        self.action()


    def ihmChoix(self):

        bindElementKeysFunction(self.listbox,
                                "0123456789abcdefghijklmnopqrstuvwxyz'-*+",
                                self.addchar)

        bindElementKeysFunction(self.listbox0,
                                "0123456789abcdefghijklmnopqrstuvwxyz'-*+",
                                self.addchar)

        self.listbox.bind("<space>",self.addchar) 
        self.listbox.bind("<BackSpace>",self.delchar)
        self.listbox.bind("<Return>",self.go) 

        self.listbox0.bind("<space>",self.addchar) 
        self.listbox0.bind("<BackSpace>",self.delchar)
        self.listbox0.bind("<Return>",self.go) 




class chooseVendeur(chooseXXX):

    def __init__(self):
        chooseXXX.__init__(self,"vendeurs")        

    def collect(self,article):
        (numero,nom,prenom,timestamp)=article
        Vendeurs[numero]=(numero,nom,prenom)

    def initPanel(self):
        self.filtreName="Vendeur > "

    def go(self,event):
        global vendeurChoisi
        global ihm
        
        try :
          #print len(self.clefs0)
          if len(self.filtre)==0 and len(self.clefs0)>0:
              clef=self.listbox0.curselection()[0]
              choix=self.clefs0[int(clef)]
              print clef,choix
          else:
              clef=self.listbox.curselection()[0]
              choix=self.clefs[int(clef)]
        except:
          ihm.showMessage("Choix impossible!!!")
          return
          
        self.filtre=""
        self.setFiltre(self.filtre)
        
        vendeurChoisi=choix
        chooseClient()

    def action(self,event="fake"):
        self.listbox.delete(0,END)


        self.clefs={}
        i=0
        liste=Vendeurs.keys()
        liste.sort(key=str.lower)
        for clef in liste:
               (numero,nom,prenom) = Vendeurs[clef]
               nom.lower()
               if string.lower(nom[:len(self.filtre)])==self.filtre:
                   self.listbox.insert(END, "%s %s"%(nom,prenom))
                   self.clefs[i]=(numero,nom,prenom)
                   i=i+1
        self.listbox.focus_set()
#        self.listbox.selection_set(0)



class chooseClient(chooseXXX):

    def __init__(self):
        chooseXXX.__init__(self,"clients")
        

    def collect(self,article):
        (societe,ville,clef,timestamp)=article
        Clients[societe+"/"+ville]=(societe,ville,clef)

    def listePrepare(self):
        clefsClients=Clients.keys()
        clefsClients.sort(key=str.lower)

        i=0
        for clef in clefsClients:
            self.listbox0.insert(END,clef)
            self.clefs0[i]=clef
            i=i+1
        #print self.listbox0

        pass

    def initPanel(self):
        self.clefs={}
        (numero,nom,prenom)=vendeurChoisi
        self.filtreName="%s > "%prenom

    def go(self,event):

        try :
          if len(self.filtre)==0 and len(self.clefs0)>0:
              clef=self.listbox0.curselection()[0]
              choix=Clients[self.clefs0[int(clef)]]
          else:
              clef=self.listbox.curselection()[0]
              choix=Clients[self.clefs[int(clef)]]
        except:
          if debugMessages:
              ihm.showMessage("Choix impossible!!!")
              return 0

        self.filtre=""
        self.setFiltre(self.filtre)
                
        processFacture(client=choix)

    def action(self,event="fake"):
        global clefsClients


        i=0
        n=len(self.filtre)
        if n==0:
            ihm.show("clients0")
            self.listbox0.focus_set()
#            self.listbox0.selection_set(0)
        else:
            self.listbox.delete(0,END)
            ihm.show("clients")
#            self.listbox.focus_set()
            self.listbox.selection_set(0)
            for clef in Clients.keys():
                if string.lower(clef[:n])==self.filtre:
                    self.listbox.insert(END, clef)
                    self.clefs[i]=clef
                    i=i+1




class chooseProduit(chooseXXX):

    def __init__(self,facture,valeur):
        
        self.liste0={}
        self.clefs0={}
        
        self.facture=facture
        self.valeur=valeur
        (societe,ville,clef) = facture.client
        self.filtreName="%s >"%societe
        chooseXXX.__init__(self,"produits",killable=1)
        
    def initPanel(self):
        self.filtre=self.valeur
        

    def collect(self,article):
         (code,clef,fournisseur,prix,prix_plancher,poids,libele,timestamp)=article
         #racourci = int(code[2:7])
         racourci = int(clef)
         ProduitsRacourcis[racourci]=libele
         if racourci in ProduitsFournisseurs.keys():
            ProduitsFournisseurs[racourci].append(fournisseur)
         else:
            ProduitsFournisseurs[racourci]=[fournisseur]
         ProduitsCodes[racourci,fournisseur]=code
         Produits[code]=(libele,prix,racourci,prix_plancher,poids,fournisseur)


    def listePrepare(self):
        self.liste=ProduitsRacourcis.keys()
        self.liste.sort()
        
    def go(self,event):
        try:
            clef=self.listbox.curselection()[0]
            (racourci,libelle)=self.clefs[int(clef)]
        except:
            return

        chooseFournisseur(self.facture,racourci)


    def action(self,event="fake"):
        self.listbox.delete(0,END)

        self.clefs={}
        i=0

        for racourci in self.liste:
            (libelle) = ProduitsRacourcis[racourci]
            libelle.lower()
            s="%04d-%s"%(racourci,libelle)
            c="%s"%racourci
            n=len(self.filtre)
            if string.lower(libelle[:n])==self.filtre or c.find(self.filtre)==0:
                self.listbox.insert(END, s)
                self.clefs[i]=(racourci,libelle)
                i=i+1
                if i==25:
                   self.listbox.update()
                
        self.listbox.focus_set()
#        self.listbox.selection_set(0)


class chooseFournisseur(chooseXXX):

    def __init__(self,facture,racourci):
        self.facture=facture
        self.racourci=racourci
        chooseXXX.__init__(self,"fournisseurs",killable=1)
        
    def initPanel(self):
        self.fournisseurs = ProduitsFournisseurs[self.racourci]
        self.filtreName="%s > "%ProduitsRacourcis[self.racourci]

    def collect(self,article):
        (societe,ville,clef,timestamp)=article
        Fournisseurs[clef]=(societe,ville,clef)

    def go(self,event):
        try:
          clef=self.listbox.curselection()[0]
          choix=self.clefs[int(clef)]
        except:
          return  

        (societe,ville,clef) = choix
        self.facture.acceptProduit(self.racourci,clef)

    def action(self,event="fake"):
        self.listbox.delete(0,END)

        self.clefs={}
        i=0
        liste=self.fournisseurs
        n=len(self.filtre)
        for code in liste:
            (societe,ville,clef)=Fournisseurs[code]
            s="%04d-%s"%(int(clef),societe)
            c="%d"%int(clef)
            n=len(self.filtre)
            if string.lower(societe[:n])==self.filtre or c.find(self.filtre)==0:
                self.listbox.insert(END, s)
                self.clefs[i]=(societe,ville,clef)
                i=i+1
                
        self.listbox.focus_set()
#        self.listbox.selection_set(0)



class chooseRelease(chooseXXX):

    def __init__(self,facture,racourci,save=0):
        chooseXXX.__init__(self,"releases",killable=1)

    def panelInit(self):
        self.facture=facture
        self.save=save
        self.filtreName="Oyak Version > "

    def collect(self,article):
        (numero,filename)=article
        Releases[numero]=(numero,filename)

    def go(self,event):
        global ihm

        try:
          clef=self.listbox.curselection()[0]
          choix=self.clefs[int(clef)]
        except:
          ihm.returnPrevious()  

        (numero,filename) = choix
        ihm.messageShow("telechargement %s"%filename)
        loadRelease(filename,self.save)


    def action(self,event="fake"):
        self.listbox.delete(0,END)

        self.clefs={}
        i=0
        liste=Releases.keys()
        n=len(self.filtre)
        for code in liste:
            (numero,filename)=Releases[code]
            s="%s"%(filename)
            n=len(self.filtre)
            if filename.find(self.filtre)==0:
                self.listbox.insert(END, s)
                self.clefs[i]=(numero,filename)
                i=i+1
                
        self.listbox.focus_set()
#        self.listbox.selection_set(0)




###################################################################
#
#  Gestion de la mise a jour
#
###################################################################

def loadRelease(filename,save):
    global ihm
    
    if not(save):
        params = urllib.urlencode({'dwn': filename})
        try:
            f = urllib.urlopen(url_update_commande, params)
        except:
            ihm.showMessage("Le serveur Release ne répond pas!")
            return
        try:
          os.remove("\\Oyak\\%s"%filename)
        except:
          pass

        new=open("\\Oyak\\%s"%filename,"w")
        program=f.readlines()
        for l in program :
            new.write("%s\n"%l[:-1])
        new.close()
        try:
            shutil.copy("\\Oyak\\%s"%filename,"\\Windows\\Desktop\\%s"%filename)
        except:
            pass
    else:
        try:
            shutil.copy("\\Oyak\\%s"%filename,"\\Application\\Python\\vendeur.pyw")
            ihm.showMessage("Device Flashe avec %s"%filename)
        except:
            ihm.showMessage("Pb dans la mise a jour %s"%filename)
        

    





################################################################################
# Saisie nom Facture
################################################################################

class processFacture:

    def __init__(self,nb=0,client=0,check=0):
        global ihm,zoomedWindow,vendeurChoisi,factureCurrent,Factures

        self.nb=nb

        self.selectedCode={}
        self.selectedRacourci={}
        self.selectedFournisseur={}
        self.selectedDate={}
        self.selectedPrix={}
        self.selectedQuantite={}


        
        if self.nb==0 and client==0:
            self.vendeur=vendeurChoisi
            self.clefs={}
        
            chooseClient()
            return

        else:
            self.client=client
            (societe,ville,clef)=self.client
        

            self.nb=getNBfacture()
            factureCurrent=self.nb
            Factures[self.nb]=self
            
            self.root=ihm.factureCreate(self.nb)

            if zoomedWindow:
                ihm.ihm.wm_state(newstate="zoomed")
            
            (numero,nom,prenom)=vendeurChoisi
            self.vendeur_prenom=prenom
            self.vendeur_numero=numero

            self.ihmFacture()

            ihm.factureButton[self.nb,"annuler"]["command"]=self.annuler
            ihm.factureButton[self.nb,"envoyer"]["command"]=self.envoyer
        
            ihm.show("facture%d"%self.nb)

    def __del__(self):
        global clientNB

        try:
            if self.nb>0:
                releaseNBfacture(self.nb)
                self.root.quit()
        except:
            pass
           
    def show(self):
        global factureCurrent

        factureCurrent=self.nb
        ihm.show("facture%d"%self.nb)
        self.goToArticle()

    def annuler(send):
        global ihm
        ihm.showMessageOuiNon("Annuler la \n Facture?",siOui=ihm.delCurrentFacture)
        

    def addLabelEntry(self,s):
        sVar= StringVar()
        sVar.set(s)

        label = Label(self.nameFrame, textvariable=sVar,  fg="red" )
        label.pack(side=TOP)

        e = Entry(self.inputFrame, fg="black" )
        e.pack(side=TOP)
        return (sVar,e)

    def ihmFacture(self):
        global ihm
        
        # division de la fenetre en trois
        
        self.clientFrame = Frame(self.root)
        self.clientFrame.pack(side=TOP)
        
        self.prixFrame = Frame(self.root)
        self.prixFrame.pack(side=TOP)

        self.nameFrame = Frame(self.prixFrame)
        self.nameFrame.pack(side=LEFT)

        self.inputFrame = Frame(self.prixFrame)
        self.inputFrame.pack(side=LEFT)

        
        self.listFrame = Frame(self.root)
        self.listFrame.pack(side=TOP,expand=1,fill=BOTH)


        (societe,ville,clef)=self.client
        self.clientClef=clef

        # rappel nom client
        label = Label(self.clientFrame,
                      text="%s>%s"%(self.vendeur_prenom,societe), justify="center", fg="red",width=36)
        label.pack(side=TOP)

        # quantite, prix, article, fournisseur, date

        self.quantite_label,self.quantite = self.addLabelEntry("Quantite:")
        self.prix_label,self.prix = self.addLabelEntry("Prix:")
        self.article_label,self.article = self.addLabelEntry("Article:")
        self.fournisseur_label,self.fournisseur = self.addLabelEntry("Fournisseur:")
        self.date_label,self.date = self.addLabelEntry("Date:")

        # liste box

        scrollbar = Scrollbar(self.listFrame)
        scrollbar.pack(side=RIGHT, expand=0, fill=BOTH)

        self.listbox = Listbox(self.listFrame, yscrollcommand=scrollbar.set)
        self.listbox.pack(side=LEFT, expand=1, fill=BOTH)
        scrollbar.config(command=self.listbox.yview)

        # Bindings...

        self.article.focus_set()
        self.article.bind(".",self.processProduit)
        
        self.article.bind("<Return>",self.route)
        self.date.bind("<Return>",self.goToQuantite)
        self.quantite.bind("<Return>",self.goToPrice)
        self.prix.bind("<Return>",self.addFacture)
        
        self.listbox.delete(0,END)
        self.listbox.insert(END, enteteFact)
        self.nbArticles=0

        self.selectedCode[self.nbArticles]=""
        self.selectedRacourci[self.nbArticles]=""
        self.selectedFournisseur[self.nbArticles]=""
        self.selectedDate[self.nbArticles]=""
        self.selectedQuantite[self.nbArticles]=""
        self.selectedPrix[self.nbArticles]=""



    def processProduit(self,event):
        valeur=self.article.get()
        self.article.delete(0,END)
        chooseProduit(self,valeur)


    def acceptProduit(self,racourci,fournisseur):
        global ihm
        try:
          # que se passe-t-il si on vire la fenetre de facturation qui
          # a appelé??
          self.article.delete(0,END)
          self.fournisseur.delete(0,END)
          self.prix.delete(0,END)
        except:
          return
            
        ihm.show("facture%d"%self.nb,title="Oyak? Facture ")
        # le produit selectionne a un code barre
        if (racourci,fournisseur) in ProduitsCodes.keys():
            code = ProduitsCodes[racourci,fournisseur]
            (libelle,prix,racourci,prix_plancher,poids,fournisseur)=Produits[code]
            (societe,ville,clef)=Fournisseurs[fournisseur]
            self.fournisseur.insert(END,societe)
            self.fournisseur_label.set("Fournisseur : %s"%fournisseur)
              
            self.article.insert(END,libelle)
            self.article_label.set("Article : %d"%racourci)
      
            self.quantite_label.set("Quantite : ("+"%6.2f"%(eval(poids)+0.00)+")")
            self.prix_label.set("Prix : ("+"%6.2f"%(eval(prix)+0.00)+")")
            self.prix_default=prix
            self.prix_plancher=prix_plancher
            self.poids=poids
            self.produit=code

            self.selectedCode[self.nbArticles]=code
            self.selectedRacourci[self.nbArticles]=racourci
            self.selectedFournisseur[self.nbArticles]=fournisseur    

            self.date.focus_set()
        else:
            ihm.showMessage("Article a part numero %s fournisseur %s",racourci,fournisseur)
                
    def deleteCode(self,event):
        self.article.delete(0,END)
        self.article_label.set("Article :")
        self.fournisseur.delete(0,END)
        self.fournisseur_label.set("Fournisseur :")
        self.date.delete(0,END)
        self.prix.delete(0,END)
        self.prix_label.set("Prix :")
        self.quantite.delete(0,END)
        self.article.focus_set()

    def goToArticle(self,event="fake"):
        ihm.show("facture%d"%self.nb,title="Oyak? Facture ")
        self.article.focus_set()


    def goToPrice(self,event):
        self.prix.focus_set()

    def goToQuantite(self,event):
        self.quantite.focus_set()

    def addFacture(self,event):
        global ihm

        prix=self.prix.get()
        if len(prix)==0:
                prix=self.prix_default
        try :
          if (eval(prix)+0.0)<eval(self.prix_plancher)+0.:
            ihm.showMessage("Impossible le prix plancher est %6.2f > %s"%((eval(self.prix_plancher)+0.00),prix),
                            self.goToPrice)
            return
        except:
            self.prix.delete(0,END)
            ihm.showMessage("le prix "+prix+" n'est pas reconnu",self.goToPrice)
            return
        quantite=self.quantite.get()
        if len(quantite)==0:
                quantite=self.poids

        article=self.article.get()
        try :
          self.listbox.insert(END, formatFact%(float(quantite),article,float(prix)))
        except :
            self.deleteCode("fake")

        self.selectedPrix[self.nbArticles]=prix
        self.selectedQuantite[self.nbArticles]=quantite
        self.selectedDate[self.nbArticles]=self.date.get()
        self.nbArticles=self.nbArticles+1

        self.selectedCode[self.nbArticles]=""
        self.selectedRacourci[self.nbArticles]=""
        self.selectedFournisseur[self.nbArticles]=""
        self.selectedDate[self.nbArticles]=""
        self.selectedQuantite[self.nbArticles]=""
        self.selectedPrix[self.nbArticles]=""

        self.deleteCode("fake")

    def envoyer(self):
        global ihm

        if self.nbArticles==0:
              self.article.delete(0,END)
              ihm.showMessage("La commande est vide!!!",self.goToArticle)
              return            

        s="%s%s"%(self.clientClef,sep1)
        for l in range(0,self.nbArticles):
             s=s+"%s%s"%(self.selectedCode[l],sep2)
             s=s+"%s%s"%(self.selectedRacourci[l],sep2)
             s=s+"%s%s"%(self.selectedFournisseur[l],sep2)
             s=s+"%s%s"%(self.selectedDate[l],sep2)
             s=s+"%s%s"%(self.selectedQuantite[l],sep2)
             s=s+"%s%s"%(self.selectedPrix[l],sep1)
        params = urllib.urlencode({'vendeur': self.vendeur_numero, 'commande':s})
        try:
            f = urllib.urlopen(url_send_commande, params)
        except:
            ihm.showMessage("Le serveur ne répond pas!",self.goToArticle)
            return
        ack=f.readlines()
        ok=ack[0]
        if (ok[0]=="0"):
            ihm.showMessage("Commande %s!"%ok[2:],ihm.delCurrentFacture)
        else:
            ihm.showMessage("Commande perdue!",ihm.delCurrentFacture)
            return
            
    
    def route(self,event):
        global ihm
        
        racourci=self.article.get()
        if racourci in Produits.keys():
            (libelle,prix,racourci,prix_plancher,poids,fournisseur)=Produits[racourci]
            self.acceptProduit(racourci,fournisseur)
            return
        fournisseur=self.fournisseur.get()
        if racourci=="e" or fournisseur=="e":
            l=self.listbox.size()
            if l>1:
                self.listbox.delete(l-1,l)
                self.nbArticles=self.nbArticles-1
            self.deleteCode("fake")
            return
        # * ->  La commande est envoye
        if racourci=="*" or fournisseur=="*":
            self.envoyer()
            return
        # * ou x ->  on tue la facture courrante
        if racourci=="x" or fournisseur=="x":
            self.annuler()
            return
        if racourci=="DDD" or racourci=="ddd":
            ihm.showMessage("Telechargement du serveur")
            lisData(readFromServer=1)
            ihm.showMessage("OK...",self.goToArticle)
            return
        if racourci=="vvv" or racourci=="vvv":
            chooseRelease(self,racourci)
            return
        if racourci=="sss" or racourci=="sss":
            chooseRelease(self,racourci,save=1)
            return
        # sinon on process le couple (racourci,fournisseur)
        try :
            racourci=int(racourci)
        except:
            self.article.delete(0,END)
            ihm.showMessage("%s n'est pas un code reconnu!"%racourci,self.goToArticle)
            return
        if racourci in ProduitsRacourcis.keys() and len(fournisseur)==0:
            chooseFournisseur(self,racourci)
        else:
            self.article.delete(0,END)
            ihm.showMessage("%d n'est pas un code reconnu!"%racourci,self.goToArticle)



        
def run():
    global isReadFromServer
    global ihm

    if oneFrame:
       ihm = ihmRoot()
       ihm.start()
    else:
##        if erreurCatch:
##            try:
##               lisData() 
##               choixVendeur()
##            except:
##               pass
##        else:
            lisData(isReadFromServer) 
            choixVendeur()


if __name__ == "__main__":
    if cible:
        try:
            run()
        except:
             f=open('\Oyak\except.out',"w")
             f.write("Exception in user code:\n")
             f.write('-'*60)
             traceback.print_exc(file=f)
             f.write( '-'*60)
             f.close()
             if ihm:
                 ihm.showMessage("Une Erreur est survenue!")
    else:
        run()
