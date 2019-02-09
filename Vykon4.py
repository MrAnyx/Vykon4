from ctypes import *
from datetime import date
from tkinter import *
import tkinter as Tkinter
import tkinter as tk
import mysql.connector
import ctypes
import random
import time

############################## Joueur VS Joueur ################################

    # Classe du jeu

class Can(Canvas):

    def __init__(self):

            #Variables

        self.cases      = [] # Cases déjà  remplies
        self.listerouge = [] # Liste des cases rouges
        self.listejaune = [] # Liste des cases jaunes
        self.dgagnantes = [] # Cases déjà  gagnantes et donc ne peuvent plus l'être à  nouveau (cf "Continuer")
        self.running    = 1  # Type de partie en cours
        self.couleur    = ['Rouge', 'Jaune']
        self.color      = [couleur2, couleur]

            #Interface

        self.clair      = "light blue"
        self.fonce      = fond_coul
        self.ecriture   = bout_coul
        self.police1    = "Times 17 normal"
        self.police2    = "Arial 10 normal"
        self.police3    = "Times 15 bold"
        self.can        = Canvas.__init__(self, width =446, height = 430, bg=self.fonce, bd=0)

        self.grid(row = 1, columnspan = 5)

            # Joueur en cours

        self.joueur = 1
        self.create_rectangle(20,400,115,425,fill = self.clair)
        self.create_text(35, 405, text ="Joueur :", anchor = NW, fill = self.ecriture, font= self.police2)
        self.indiccoul = self.create_oval(85, 405, 100, 420, fill = self.color[1])

            #Bouton Nouveau Jeu

        self.create_rectangle(330,400,420,425,fill=self.clair)
        self.create_text(340, 405, text ="Nouveau jeu", anchor = NW, fill = self.ecriture, font= self.police2)

        self.create_rectangle(250,400,300,425,fill=self.clair)
        self.create_text(255, 405, text ="Quitter", anchor = NW, fill = self.ecriture, font= self.police2)

            #Création des cases

        self.ovals = []
        for y in range(10, 390, 55):
            for x in range(10, 437, 63):
                self.ovals.append(self.create_oval(x, y, x + 50, y + 50 , fill= "white"))

            #En cas de click

        self.bind("<Button-1>", self.click)

            # Pour relier à  la fin les coordonnées des centres des cases

        self.coordscentres = []

            # Comptabilisation des suites de pièces

        self.rouges, self.jaunes = 0,0

            # Dictionnaire de reconnaissance

        self.dictionnaire = {}
        v = 0
        for y in range(10, 390, 55):
            for x in range(10, 437, 63):
                self.dictionnaire[(x, y, x + 50, y + 50)] = v
                v += 1
                self.coordscentres.append((x + 25, y + 25))

    def click(self,event): #En cas de click
        if 330 < event.x and 400 < event.y and event.x < 420 and event.y < 425:
            self.new()# =>Nouveau jeu

        if 250 <event.x and 400 < event.y and event.x < 300 and event.y < 425:
            self.quitter()

            #Jeu en cours: reconnaissance de la case jouée

        else :
            if self.running != 0:
                for (w, x, y, z) in self.dictionnaire:
                    if event.x > (w, x, y, z)[0] and event.y >(w, x, y, z)[1] and event.x < (w, x, y, z)[2] and event.y < (w, x, y, z)[3]:
                        self.colorier(self.dictionnaire[(w, x, y, z)]) # => Jouer

    def colorier(self, n, nb=0): #Gère la coloration des cases

        if n in self.cases : return # Une case coloriée ne peut plus changer de couleur

        if n + 7 not in self.cases and n + 7 < 49: #Si la case en dessous est vide et existe, on essaie d'abord de colorier celle-à
            self.colorier(n+7)

        else:

                #Sinon on colorie celle-ci

            self.itemconfigure(self.ovals[n], fill = self.color[self.joueur])
            self.cases.append(n)
            self.color[self.joueur] == str(couleur2) and self.listerouge.append(n) or self.listejaune.append(n)
            self.listejaune = [case for case in self.listejaune if case not in self.listerouge]
            self.verif(n)

                #Changement de joueur

            self.joueur = [0,1][[0,1].index(self.joueur)-1]
            self.itemconfigure(self.indiccoul, fill = self.color[self.joueur])

                #On regarde toutes les cases sont remplies

            self.verificationFinale()

        return

    def verif(self, n): # Vérifie si la pièce ajoutée s'aligne avec trois autres déjà placées

        if self.running == 0 : return

        if n in self.listerouge and n+7  in self.listerouge and n+14  in self.listerouge and n+21 in self.listerouge: # D'abord à la verticale,
                                                                                           # séparément car proximité d'un bord inintéressante
            liste=[n, n+7, n+14, n+21] # Pour gérér les parties "plurigagnantes"
            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
            return

            #idem pour jaunes

        if n in self.listejaune and n+7 in self.listejaune and n+14 in self.listejaune and n+21 in self.listejaune:
            liste=[n, n+7, n+14, n+21]
            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
            return

        for x in (1,-6,8):

            if n in self.listerouge: # en s'assurant qu'elles ne sont trop près des bords (pour ne pas arriver de l'autre coté du plateau)
                if n % 7 != 6 and n+x in self.listerouge:
                    if n % 7 != 5 and n+ 2*x in self.listerouge:
                        if n % 7 != 4 and n + 3*x in self.listerouge:
                            liste = [n, n+x, n+2*x, n+3*x]
                            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
                            return
                        if n%7 > 0 and (n-x) in self.listerouge:
                            liste = [n-x,n, n+x, n+2*x]
                            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
                            return
                    if n%7 > 1 and (n-x) in self.listerouge:
                        if n%7 > 2 and n-(2*x) in self.listerouge:
                            liste = [n-2*x, n-x,n, n+x]
                            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
                            return

                #Pareil pour les jaunes

            if n in self.listejaune:
                if n % 7 != 6 and n+x in self.listejaune:
                    if n % 7 != 5 and n+ 2*x in self.listejaune:
                        if n % 7 != 4 and n + 3*x in self.listejaune:
                            liste = [n, n+x, n+2*x, n+3*x]
                            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
                            return
                        if n%7 > 0 and (n-x) in self.listejaune:
                            liste = [n-x,n, n+x, n+2*x]
                            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
                            return
                    if n%7 > 1 and (n-x) in self.listejaune:
                        if n%7 > 2 and n-(2*x) in self.listejaune:
                            liste = [n-2*x, n-x,n, n+x]
                            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
                            return

        for x in (-1,6,-8):

            if n in self.listejaune:
                if n % 7 != 0 and (n+x) in self.listejaune:
                    if n % 7 != 1 and n+(2*x) in self.listejaune:
                        if n % 7 != 2 and n + (3*x) in self.listejaune:
                            liste = [n, n+x, n+2*x, n+3*x]
                            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
                            return
                        if n%7 <6 and (n-x) in self.listejaune:
                            liste = [n-x,n, n+x, n+2*x]
                            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
                            return
                    if n%7 < 5 and (n-x) in self.listejaune:
                        if n%7 < 4 and n-(2*x) in self.listejaune:
                            liste = [n-2*x, n-x,n, n+x]
                            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
                            return

            if n in self.listerouge:
                if n % 7 != 0 and (n+x) in self.listerouge:
                    if n % 7 != 1 and n+(2*x) in self.listerouge:
                        if n % 7 != 2 and n + (3*x) in self.listerouge:
                            liste = [n, n+x, n+2*x, n+3*x]
                            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
                            return
                        if n%7 <6 and (n-x) in self.listerouge:
                            liste = [n-x,n, n+x, n+2*x]
                            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
                            return
                    if n%7 < 5 and (n-x) in self.listerouge:
                        if n%7 < 4 and n-(2*x) in self.listerouge:
                            liste = [n-2*x, n-x,n, n+x]
                            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
                            return

    def verificationFinale(self):
        global text2 # Lorsque toutes les cases sont remplies

        if len(self.cases)==49: # On comptabilise les points
            typ =self.plus() # Type de partie gagnée
            if typ[1]==0:
                self.texte2 = Label(fen, text = typ[0] + " a définitivement gagné !", bg= self.fonce,
                                    fg=self.clair, font=self.police1)

            elif typ[1]==1:
                self.texte2 = Label(fen, text = typ[0] + " a gagné le premiers !", bg= self.fonce,
                                    fg=self.clair, font=self.police1)
                self.texte2.grid()

            else:
                self.texte2 = Label(fen, text = typ[0], bg= self.fonce, fg=self.clair, font=self.police1).grid(padx=110)

    def win(self, qui, p, d): # Partie gagnée

           #Marquage des pièces gagnantes

        self.create_line(self.coordscentres[p][0], self.coordscentres[p][1],
                         self.coordscentres[d][0], self.coordscentres[d][1],
                         fill="black")

        if qui=="rouges" : self.rouges += 1 #Comptabilisation des suites
        if qui=="jaunes" : self.jaunes += 1

        if self.running == 3:
            self.pRouges.config(text = pseudo2 + " : " + str(self.rouges))
            self.pJaunes.config(text = pseudo + " : " + str(self.jaunes))
            return

            #Affichage des scores
        if self.jaunes > self.rouges:
            self.qui = str(pseudo)
            self.texte = Label(fen, text="%s a gagné !" % (self.qui), bg= self.fonce, fg=self.clair, font=self.police1)
            self.texte.grid()
            self.running = 0

        elif self.rouges > self.jaunes:
            self.qui = str(pseudo2)
            self.texte = Label(fen, text="%s a gagné !" % (self.qui), bg= self.fonce, fg=self.clair, font=self.police1)
            self.texte.grid()
            self.running = 0

            #Proposition de continuer

        self.BtnContinuer = Button(fen, text=" Continuer cette partie", bd= 0, bg=self.fonce, fg=self.clair,
                                   font=self.police3, command=self.continuer)
        self.BtnContinuer.grid(padx=120)

    def continuer(self): # Si on choisi de poursuivre la même partie (déjà gagnée par un joueur)

        self.running = 3

            # Affichage des scores

        self.pRouges = Label(fen, text = "%s : %s" %(str(pseudo2), str(self.rouges)),
                             font=self.police3, bg=self.fonce, fg=self.clair)
        self.pJaunes = Label(fen, text = "%s : %s" %(str(pseudo), str(self.jaunes)),
                             font=self.police3, bg=self.fonce, fg=self.clair)

        self.BtnContinuer.destroy()
        self.texte.destroy()

        self.pJaunes.grid(padx=160)
        self.pRouges.grid(padx=160)

    def quitter(self):

        pt_gg=(str(self.jaunes))
        pt_gg=(int(pt_gg))

        cursor.execute("SELECT * FROM puissance WHERE pseudo='%s';" % (pseudo),)
        result=cursor.fetchone()
        result1=result[2]

        if result1<pt_gg:
            sql= ("UPDATE puissance SET score = %s WHERE pseudo = %s", (pt_gg, pseudo))
            cursor.execute(*sql)

        else:
            pass

        ag_gg=(int(self.jaunes))
        argent=ag_gg/2

        sql= ("UPDATE puissance SET argent = argent+%s WHERE pseudo = %s", (argent, pseudo))
        cursor.execute(*sql)

        pt_gg2=(str(self.rouges))
        pt_gg2=(int(pt_gg2))

        cursor.execute("SELECT * FROM puissance WHERE pseudo='%s';" % (pseudo2),)
        result2=cursor.fetchone()
        result3=result2[2]

        if result3<pt_gg2:
            sql= ("UPDATE puissance SET score = %s WHERE pseudo = %s", (pt_gg2, pseudo2))
            cursor.execute(*sql)

        else:
            pass

        ag_gg2=(int(self.rouges))
        argent1=ag_gg2/2

        sql= ("UPDATE puissance SET argent = argent+%s WHERE pseudo = %s", (argent1, pseudo2))
        cursor.execute(*sql)
        fen.destroy()

    def gagnantes(self, liste=[]): # On vérifie que les pièces ne sont pas encore gagnantes, et on les ajoute dans la liste si elles le deviennent

        for i in liste:
            if i in self.dgagnantes: return 0

        for n in liste:
            self.dgagnantes.append(n)

        return 1

    def plus(self):# Donner le résultat final

        if self.rouges > self.jaunes    : return pseudo2,0
        if self.jaunes > self.rouges    : return pseudo,0
        if self.rouges != 0             : return self.qui, 1 # En cas d'égalité, le premier à avoir aligné ses pièces gagne

        return "Personne n'a gagné", 2 #Sinon, tous deux ont perdu

    def new(self):# Nouveau Jeu

            # Opérations non certaines

        try:
            self.BtnContinuer.destroy()
        except:
            pass
        try:
            self.texte.destroy()
        except:
            pass
        try:
            self.texte2.destroy()
        except:
            pass
        try:
            self.pRouges.destroy()
        except:
            pass
        try:
            self.pJaunes.destroy()
        except:
            pass

        self.destroy()
        self.__init__()

############################# Joueur VS IA #####################################

class Can_IA(Canvas):

    def __init__(self):

            #Variables

        self.cases      = [] # Cases déjà remplies
        self.listerouge = [] # Liste des cases rouges
        self.listejaune = [] # Liste des cases jaunes
        self.dgagnantes = [] # Cases déjà gagnantes et donc ne peuvent plus l'être à nouveau (cf "Continuer")
        self.running    = 1  # Type de partie en cours
        self.couleur    = ["Rouges", "Jaunes"]
        self.color      = [couleur2, couleur]

            #Interface

        self.clair      = "light blue"
        self.fonce      = fond_coul
        self.ecriture   = bout_coul
        self.police1    = "Times 17 normal"
        self.police2    = "Arial 10 normal"
        self.police3    = "Times 15 bold"
        self.can        = Canvas.__init__(self, width =446, height = 430, bg=self.fonce, bd=0)

        self.grid(row = 1, columnspan = 5)

            # Joueur en cours

        self.joueur = 1
        self.create_rectangle(20,400,115,425,fill = self.clair)
        self.create_text(35, 405, text ="Joueur :", anchor = NW, fill = self.ecriture, font= self.police2)
        self.indiccoul = self.create_oval(85, 405, 100, 420, fill = self.color[1])

            #Bouton Nouveau Jeu

        self.create_rectangle(330,400,420,425,fill=self.clair)
        self.create_text(340, 405, text ="Nouveau jeu", anchor = NW, fill = self.ecriture, font= self.police2)

        self.create_rectangle(250,400,300,425,fill=self.clair)
        self.create_text(255, 405, text ="Quitter", anchor = NW, fill = self.ecriture, font= self.police2)

        self.create_rectangle(150,400,225,425,fill=self.clair)  #X0 Y0 X Y  X0 ET YO COINS SUPERIEURS GAUCHE ET X ET Y COINS INFERIEURS DROIT
        self.create_text(175, 405, text ="  IA", anchor = NW, fill = self.ecriture, font= self.police2)

            #Création des cases

        self.ovals = []
        for y in range(10, 390, 55):
            for x in range(10, 437, 63):
                self.ovals.append(self.create_oval(x, y, x + 50, y + 50 , fill= "white"))

            #En cas de click

        self.bind("<Button-1>", self.click)

            # Pour relier à la fin les coordonnées des centres des cases

        self.coordscentres = []

            # Comptabilisation des suites de pièces

        self.rouges, self.jaunes = 0,0

            # Dictionnaire de reconnaissance

        self.dictionnaire = {}
        v = 0
        for y in range(10, 390, 55):
            for x in range(10, 437, 63):
                self.dictionnaire[(x, y, x + 50, y + 50)] = v
                v += 1
                self.coordscentres.append((x + 25, y + 25))

    def click(self,event): #En cas de click
        if 330 < event.x and 400 < event.y and event.x < 420 and event.y < 425:
            self.new()# =>Nouveau jeu

        if 250 <event.x and 400 < event.y and event.x < 300 and event.y < 425:
            self.quitter()

        if 150 <event.x and 400 < event.y and event.x < 225 and event.y < 425:
            self.fin_du_tour()

            #Jeu en cours: reconnaissance de la case jouée

        else :
            if self.running != 0:
                for (w, x, y, z) in self.dictionnaire:
                    if event.x > (w, x, y, z)[0] and event.y >(w, x, y, z)[1] and event.x < (w, x, y, z)[2] and event.y < (w, x, y, z)[3]:
                        self.colorier(self.dictionnaire[(w, x, y, z)]) # => Jouer

    def colorier(self, n, nb=0): #Gère la coloration des cases

        if n in self.cases : return # Une case coloriée ne peut plus changer de couleur

        if n + 7 not in self.cases and n + 7 < 49: #Si la case en dessous est vide et existe, on essaie d'abord de colorier celle-là
            self.colorier(n+7)

        else:

                #Sinon on colorie celle-ci

            self.itemconfigure(self.ovals[n], fill = self.color[self.joueur])
            self.cases.append(n)
            self.color[self.joueur] == str(couleur2) and self.listerouge.append(n) or self.listejaune.append(n)
            self.listejaune = [case for case in self.listejaune if case not in self.listerouge]
            self.verif(n)

                #Changement de joueur

            self.joueur = [0,1][[0,1].index(self.joueur)-1]
            self.itemconfigure(self.indiccoul, fill = self.color[self.joueur])

                #On regarde toutes les cases sont remplies

            self.verificationFinale()

        return

    def verif(self, n): # Vérifie si la pièce ajoutée s'aligne avec trois autres déjà placées

        if self.running == 0 : return

        if n in self.listerouge and n+7  in self.listerouge and n+14  in self.listerouge and n+21 in self.listerouge: # D'abord à la verticale,
                                                                                            # séparément car proximité d'un bord inintéressante
            liste=[n, n+7, n+14, n+21] # Pour gérér les parties "plurigagnantes"
            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
            return

            #idem pour jaunes

        if n in self.listejaune and n+7 in self.listejaune and n+14 in self.listejaune and n+21 in self.listejaune:
            liste=[n, n+7, n+14, n+21]
            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
            return

        for x in (1,-6,8):

            if n in self.listerouge: # en s'assurant qu'elles ne sont trop près des bords (pour ne pas arriver de l'autre coté du plateau)
                if n % 7 != 6 and n+x in self.listerouge:
                    if n % 7 != 5 and n+ 2*x in self.listerouge:
                        if n % 7 != 4 and n + 3*x in self.listerouge:
                            liste = [n, n+x, n+2*x, n+3*x]
                            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
                            return
                        if n%7 > 0 and (n-x) in self.listerouge:
                            liste = [n-x,n, n+x, n+2*x]
                            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
                            return
                    if n%7 > 1 and (n-x) in self.listerouge:
                        if n%7 > 2 and n-(2*x) in self.listerouge:
                            liste = [n-2*x, n-x,n, n+x]
                            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
                            return

                #Pareil pour les jaunes

            if n in self.listejaune:
                if n % 7 != 6 and n+x in self.listejaune:
                    if n % 7 != 5 and n+ 2*x in self.listejaune:
                        if n % 7 != 4 and n + 3*x in self.listejaune:
                            liste = [n, n+x, n+2*x, n+3*x]
                            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
                            return
                        if n%7 > 0 and (n-x) in self.listejaune:
                            liste = [n-x,n, n+x, n+2*x]
                            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
                            return
                    if n%7 > 1 and (n-x) in self.listejaune:
                        if n%7 > 2 and n-(2*x) in self.listejaune:
                            liste = [n-2*x, n-x,n, n+x]
                            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
                            return

        for x in (-1,6,-8):

            if n in self.listejaune:
                if n % 7 != 0 and (n+x) in self.listejaune:
                    if n % 7 != 1 and n+(2*x) in self.listejaune:
                        if n % 7 != 2 and n + (3*x) in self.listejaune:
                            liste = [n, n+x, n+2*x, n+3*x]
                            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
                            return
                        if n%7 <6 and (n-x) in self.listejaune:
                            liste = [n-x,n, n+x, n+2*x]
                            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
                            return
                    if n%7 < 5 and (n-x) in self.listejaune:
                        if n%7 < 4 and n-(2*x) in self.listejaune:
                            liste = [n-2*x, n-x,n, n+x]
                            if self.gagnantes(liste) : self.win("jaunes", liste[0],liste[3])
                            return

            if n in self.listerouge:
                if n % 7 != 0 and (n+x) in self.listerouge:
                    if n % 7 != 1 and n+(2*x) in self.listerouge:
                        if n % 7 != 2 and n + (3*x) in self.listerouge:
                            liste = [n, n+x, n+2*x, n+3*x]
                            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
                            return
                        if n%7 <6 and (n-x) in self.listerouge:
                            liste = [n-x,n, n+x, n+2*x]
                            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
                            return
                    if n%7 < 5 and (n-x) in self.listerouge:
                        if n%7 < 4 and n-(2*x) in self.listerouge:
                            liste = [n-2*x, n-x,n, n+x]
                            if self.gagnantes(liste) : self.win("rouges", liste[0],liste[3])
                            return

    def verificationFinale(self): # Lorsque toutes les cases sont remplies

        if len(self.cases)==49: # On comptabilise les points
            typ =self.plus() # Type de partie gagnée
            if typ[1]==0:
                self.texte2 = Label(fenetre_IA, text = typ[0] + " a définitivement gagné !", bg= self.fonce,
                                    fg=self.clair, font=self.police1)

            elif typ[1]==1:
                self.texte2 = Label(fenetre_IA, text = typ[0] + " a gagné le premiers !", bg= self.fonce,
                                    fg=self.clair, font=self.police1)
                self.texte2.grid()

            else:
                self.texte2 = Label(fenetre_IA, text = typ[0], bg= self.fonce, fg=self.clair, font=self.police1)
                self.texte2.grid(padx=110)

    def win(self, qui, p, d): # Partie gagnée

            #Marquage des pièces gagnantes

        self.create_line(self.coordscentres[p][0], self.coordscentres[p][1],
                         self.coordscentres[d][0], self.coordscentres[d][1],
                         fill="black")

        if qui=="rouges" : self.rouges += 1 #Comptabilisation des suites
        if qui=="jaunes" : self.jaunes += 1

        if self.running == 3:
            self.pRouges.config(text = "IA" + " : " + str(self.rouges))
            self.pJaunes.config(text = pseudo + " : " + str(self.jaunes))
            return

            #Affichage des scores

        if self.jaunes > self.rouges:
            self.qui = str(pseudo)
            self.texte = Label(fenetre_IA, text="%s a gagné !" % (self.qui), bg= self.fonce, fg=self.clair, font=self.police1)
            self.texte.grid()
            self.running = 0

        elif self.rouges > self.jaunes:
            self.qui = "IA"
            self.texte = Label(fenetre_IA, text="l'%s a gagné !" % (self.qui), bg= self.fonce, fg=self.clair, font=self.police1)
            self.texte.grid()
            self.running = 0

            #Proposition de continuer

        self.BtnContinuer = Button(fenetre_IA, text=" Continuer cette partie", bd= 0, bg=self.fonce, fg=self.clair,
                                   font=self.police3, command=self.continuer)
        self.BtnContinuer.grid(padx=120)

    def continuer(self): # Si on choisi de poursuivre la même partie (déjà gagnée par un joueur)
            global score, points_R
            self.running = 3

                # Affichage des scores

            self.pRouges = Label(fenetre_IA, text = "IA : %s" %(str(self.rouges)),
                                 font=self.police3, bg=self.fonce, fg=self.clair)
            self.pJaunes = Label(fenetre_IA, text = "%s : %s" %(str(pseudo),str(self.jaunes)),
                                 font=self.police3, bg=self.fonce, fg=self.clair)

            self.BtnContinuer.destroy()
            self.texte.destroy()

            self.pJaunes.grid(padx=160)
            self.pRouges.grid(padx=160)

    def gagnantes(self, liste=[]): # On vérifie que les pièces ne sont pas encore gagnantes, et on les ajoute dans la liste si elles le deviennent

        for i in liste:
            if i in self.dgagnantes: return 0

        for n in liste:
            self.dgagnantes.append(n)

        return 1

    def quitter(self):

        pt_gg=(str(self.jaunes))
        pt_gg=(int(pt_gg))

        cursor.execute("SELECT * FROM puissance WHERE pseudo='%s';" % (pseudo),)
        result=cursor.fetchone()
        result1=result[2]

        if result1<pt_gg:
            sql= ("UPDATE puissance SET score = %s WHERE pseudo = %s", (pt_gg, pseudo))
            cursor.execute(*sql)

        else:
            pass

        ag_gg=(int(self.jaunes))
        argent=ag_gg/2

        sql= ("UPDATE puissance SET argent = argent+%s WHERE pseudo = %s", (argent, pseudo))
        cursor.execute(*sql)
        fenetre_IA.destroy()

    def gagnantes(self, liste=[]): # On vérifie que les pièces ne sont pas encore gagnantes, et on les ajoute dans la liste si elles le deviennent

        for i in liste:
            if i in self.dgagnantes: return 0

        for n in liste:
            self.dgagnantes.append(n)

        return 1

    def fin_du_tour(self):

        user32 = ctypes.windll.user32

        a = (user32.GetSystemMetrics(0))/2-183
        b = (user32.GetSystemMetrics(0))/2+183
        A = random.randrange(a,b,63)
        B = (user32.GetSystemMetrics(1))/2-190

        time.sleep(0.2)
        windll.user32.SetCursorPos(int(A),int(B))
        time.sleep(0.5)
        windll.user32.mouse_event(2,0,0,0,0)
        time.sleep(0.2)
        windll.user32.mouse_event(4,0,0,0,0)


    def plus(self): # Donner le résultat final

        if self.rouges > self.jaunes    : return "L'IA",0
        if self.jaunes > self.rouges    : return pseudo,0
        if self.rouges != 0             : return self.qui, 1 # En cas d'égalité, le premier à avoir aligné ses pièces gagne

        return "Personne n'a gagné", 2 #Sinon, tous deux ont perdu

    def new(self):# Nouveau Jeu

            # Opérations non certaines

        try:
            self.BtnContinuer.destroy()
        except:
            pass


        try:
            self.texte2.destroy()

        except:
            pass


        try:
            self.texte.destroy()
        except:
            pass


        try:
            self.pRouges.destroy()
        except:
            pass


        try:
            self.pJaunes.destroy()
        except:
            pass

            # Opérations qui le sont


        self.destroy()
        self.__init__()

######################## Les Différentes Fenetres ##############################

#fenetre Joueur VS Joueur

def fen_joueur():
    global fen, variable

    user32 = ctypes.windll.user32
    fen = Tk()
    fen.geometry("%dx%d%+d%+d" % (446,600,(user32.GetSystemMetrics(0)/2)-224, (user32.GetSystemMetrics(1)/2)-252))
    fen.resizable(width = False, height = False)
    fen.title("VYKON 4 | Joueur vs Joueur")
    fen.iconbitmap("Data/Logo/favicon.ico")
    fen.focus_set()
    fen.config(bg=fond_coul)
    lecan = Can() #affiche le plateau de jeu

#fenetre IA

def fenetre_IA():
    global fenetre_IA, variable
    fen_menu.destroy()
    user32 = ctypes.windll.user32
    fenetre_IA = Tk()
    fenetre_IA.geometry("%dx%d%+d%+d" % (446, 600,(user32.GetSystemMetrics(0)/2)-224, (user32.GetSystemMetrics(1)/2)-252))
    fenetre_IA.title("VYKON 4 | Joueur vs IA")
    fenetre_IA.resizable(width = False, height = False)
    fenetre_IA.iconbitmap("Data/Logo/favicon.ico")
    fenetre_IA.focus_set()
    fenetre_IA.config(bg = fond_coul)

    lecan1 = Can_IA() #affiche le plateau de jeu

######################## Récupérer les deux pseudos ############################

def fen_choix_pseudo():
    global fen_choix_pseudo

    Fenetre_Principale.destroy()

    # Caractéristiques #
    fen_choix_pseudo = Tk()
    fen_choix_pseudo.geometry("800x400")
    fen_choix_pseudo.title("VYKON 4")
    fen_choix_pseudo.configure(bg = "#244352")
    fen_choix_pseudo.iconbitmap("Data/Logo/favicon.ico")

    menubar = Menu(fen_choix_pseudo)

    menu1 = Menu(menubar, tearoff = 0)
    menu1.add_command(label = 'Aide', command = fen_choix_pseudo_aide)
    menubar.add_cascade(label = 'Aide', menu = menu1)
    fen_choix_pseudo.config(menu = menubar)

    # Logo du jeu #

    imgPath = "Data/Logo/Logooo.gif"
    photo = PhotoImage(file = imgPath)
    label = Label(image = photo)
    label.image = photo
    canvas = Canvas( fen_choix_pseudo, width=800, height=100)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.configure(bg = "#094a5f")
    canvas.pack()

    #etes vous un ancien ?
    label = Label( fen_choix_pseudo, text="Êtes-vous ...", bg= "#244352", fg="#338099", font = ("Time", 20))
    label.pack(side="top", padx=10, pady=50)

   # Bonton ancien joueur #
    bouton_ancien=Button( fen_choix_pseudo, text="... un ancien joueur ?", bg="#338099", fg="#10303a", height = 4, width = 25,font = ("Time", 15), command = fen_pseudo_ancien)
    bouton_ancien.pack(side="right", padx=30, pady=10)

    # Bonton nouveau joueur #
    bouton_nouveau=Button( fen_choix_pseudo, text="... un nouveau joueur ?", bg="#338099", fg="#10303a", height = 4, width = 25,font = ("Time", 15),command = fen_pseudo_nouveau)
    bouton_nouveau.pack(side="left", padx=50, pady=10)

    t_base()
    fen_choix_pseudo.mainloop()

######################## SI NOUVEAU :

def fen_pseudo_nouveau():

    global Champ_Nouv, fen_pseudo_nouveau
    fen_choix_pseudo.destroy()

    # Caractéristiques #
    fen_pseudo_nouveau = Tk()
    fen_pseudo_nouveau.geometry("400x400")
    fen_pseudo_nouveau.title("VYKON 4 | Pseudo")
    fen_pseudo_nouveau.configure(bg = "#244352")
    fen_pseudo_nouveau.iconbitmap("Data/Logo/favicon.ico")

     # Logo du jeu #

    imgPath = "Data/Logo/Mini_Logoo.gif"
    photo = PhotoImage(file = imgPath)
    label = Label(image = photo)
    label.image = photo
    canvas = Canvas(fen_pseudo_nouveau, width=800, height=100)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.configure(bg = "#094a5f")
    canvas.pack()

    Bouton_valider = Button(fen_pseudo_nouveau, text = "Valider", bg="#338099", fg="#10303a", command = recupere_pseudo_nouveau)
    Bouton_valider.pack(side="bottom", padx=0, pady=10)
    Valeur=StringVar()
    Champ_Nouv = Entry(fen_pseudo_nouveau, textvariable= Valeur, fg='blue')
    Champ_Nouv.focus_set()
    Champ_Nouv.pack(side ='bottom', padx=0, pady=75)
    fen_pseudo_nouveau.bind("<Return>", Touche_du_clavier)

    label = Label( fen_pseudo_nouveau, text="Créer votre pseudo", bg= "#244352", fg="#338099", font = ("Time", 14))
    label.pack(side="bottom")

    fen_pseudo_nouveau.mainloop()

def recupere_pseudo_nouveau():
    global pseudo

    id=''
    pseudo=str(Champ_Nouv.get())
    score=''
    argent=0
    date=temps
    sql= ('''INSERT INTO puissance(id, pseudo, score, argent, date) VALUES (%s,%s,%s,%s,%s)''', (id, pseudo, score, argent, date))
    cursor.execute(*sql)
    fen_pseudo_nouveau_destroy()

def fen_pseudo_nouveau_destroy():

    fen_pseudo_nouveau.destroy()
    choix_pionts()

######################## SI ANCIEN :

def fen_pseudo_ancien():

    global fen_pseudo_ancien, Champ_Anc
    fen_choix_pseudo.destroy()

    fen_pseudo_ancien = Tk()
    fen_pseudo_ancien.geometry("400x400")
    fen_pseudo_ancien.title("VYKON 4 | Pseudo")
    fen_pseudo_ancien.configure(bg = "#244352")
    fen_pseudo_ancien.iconbitmap("Data/Logo/favicon.ico")

    # Logo du jeu #

    imgPath = "Data/Logo/Mini_Logoo.gif"
    photo = PhotoImage(file = imgPath)
    label = Label(image = photo)
    label.image = photo
    canvas = Canvas(fen_pseudo_ancien, width=800, height=100)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.configure(bg = "#094a5f")
    canvas.pack()

    Bouton_ancien = Button(fen_pseudo_ancien, text = "Valider", bg="#338099", fg="#10303a", command = recupere_pseudo_ancien)
    Bouton_ancien.pack(side="bottom", padx=0, pady=10)

    Valeur=StringVar()
    Champ_Anc = Entry(fen_pseudo_ancien, textvariable= Valeur, fg='blue')
    Champ_Anc.focus_set()
    Champ_Anc.pack(side ='bottom', padx=0, pady=75)
    fen_pseudo_ancien.bind("<Return>", Touche_du_clavier)

    label = Label( fen_pseudo_ancien, text="Entrez votre pseudo", bg= "#244352", fg="#338099", font = ("Time", 14))
    label.pack(side="bottom")

    fen_pseudo_ancien.mainloop()

def recupere_pseudo_ancien():
    global pseudo

    pseudo=str(Champ_Anc.get())
    fen_pseudo_ancien_destroy()

def fen_pseudo_ancien_destroy():

    fen_pseudo_ancien.destroy()
    choix_pionts()

######################## CHOIX DES PIONTS ######################################
def Choix_Couleur_piont(couleur):

    if couleur == 'Classique':
        Texte.set('Choix du pion : Classique')
    else:
        Texte.set('Choix du pion : ' + couleur)

def Choix_Couleur_Theme(couleur):

    if couleur == 'Classique':
        Texte2.set('Choix du thème : Classique')
    else:
        Texte2.set('Choix du thème : ' + couleur)

def choix_pionts():
   global fen_choix_pionts, Texte, Texte2

   fen_choix_pionts = Tk()
   fen_choix_pionts.geometry("1000x600")
   fen_choix_pionts.title("VYKON 4 | Menu")
   fen_choix_pionts.configure(bg = "#244352")
   fen_choix_pionts.iconbitmap("Data/Logo/favicon.ico")

   menubar = Menu(fen_choix_pionts)

   menu1 = Menu(menubar, tearoff = 0)
   menu1.add_command(label = 'Aide', command = choix_pions_aide)
   menubar.add_cascade(label = 'Aide', menu = menu1)
   fen_choix_pionts.config(menu = menubar)

   # Logo du jeu #

   imgPath = "Data/Logo/Logo_choix_pion.gif"
   photo = PhotoImage(file = imgPath)
   label = Label(image = photo)
   label.image = photo
   canvas = Canvas(fen_choix_pionts, width=1000, height=100)
   canvas.create_image(0, 0, anchor=NW, image=photo)
   canvas.configure(bg = "#094a5f")
   canvas.pack()


   Frame1 = Frame(fen_choix_pionts,borderwidth=2,relief=FLAT,bg = "#244352")
   Frame1.pack(side=TOP,padx=10,pady=10)
   Label(Frame1,text="Choisis ton pion ou ton thème !",font = ("Time",12),bg = "#244352", fg="#338099").pack(side=TOP, padx=10,pady=10)

   Frame2 = Frame(fen_choix_pionts,bg="#244352",borderwidth=2,relief=FLAT)
   Frame2.pack(side=BOTTOM,padx=10,pady=10)

   Frame3 = Frame(Frame1,bg="#244352",borderwidth=2,relief=FLAT)
   Frame3.pack(side=TOP,padx=10,pady=10)

   Frame4 = Frame(Frame1,bg="#244352",borderwidth=2,relief=FLAT)
   Frame4.pack(side=BOTTOM,padx=60,pady=10)

   Texte = StringVar()

   #Label(Frame3,text="PIONT").pack(side=LEFT,padx=10,pady=10)
   Bouton1 = Button(Frame3, text="Piont Violet",height = 4, width = 25, bg= "#cc55cc", fg="#10303a",font = ("Time", 8),command = violet_p).pack(side=LEFT,padx=10,pady=10)
   Bouton2 = Button(Frame3, text="Piont Vert",height = 4, width = 25, bg= "#66d585", fg="#10303a",font = ("Time", 8), command = vert_p).pack(side=LEFT,padx=10,pady=10)

   Choix_Couleur_piont('Classique')

   # Création d'un widget Label (texte 'Résultat sélectionné')
   LabelResultat = Label(Frame3, textvariable = Texte, fg = '#10303a', bg ='#338099')
   LabelResultat.pack(side = LEFT, padx = 10, pady = 10)

   Texte2 = StringVar()

  # Label(Frame4,text="THEME").pack(side=LEFT,padx=10,pady=10)
   Bouton3 = Button(Frame4, text="Thème bleu",bg= "#10c1db", fg="yellow", height = 4, width = 25,font = ("Time", 8), command = t_bleu).pack(side=LEFT,padx=10,pady=10)
   Bouton4 = Button(Frame4, text="Thème orange",bg= "#ffbb5b", fg="#1b983e", height = 4, width = 25,font = ("Time", 8), command = t_orange).pack(side=LEFT,padx=10,pady=10)
   Bouton5 = Button(Frame4, text="Thème rose",bg= "#f0a9f1",fg="#5493b8", height = 4, width = 25,font = ("Time", 8), command = t_rose).pack(side=LEFT,padx=10,pady=10)

   Choix_Couleur_Theme('Classique')

   # Création d'un widget Label (texte 'Résultat sélectionné')
   LabelResultat2 = Label(Frame4, textvariable = Texte2, fg="#10303a", bg ='#338099')
   LabelResultat2.pack(side = LEFT, padx = 10, pady = 10)

   Bouton6 = Button(Frame2, text="JOUER",height = 4, width = 25,bg="#338099",fg="#10303a", font = ("Time", 12), command = fen_menu).pack(side=LEFT,padx=10,pady=10)
   Bouton7 = Button(Frame2, text="BOUTIQUE",height = 4, width = 25,bg="#338099", fg="#10303a",font = ("Time", 12), command = boutique).pack(side=RIGHT,padx=10,pady=10)

   fen_choix_pionts.mainloop()

def fen_menu():
    global fen_menu

    fen_choix_pionts.destroy()
    try:
        fen_bout.destroy()
    except:
        pass

    fen_menu = Tk()
    fen_menu.geometry("800x400")
    fen_menu.title("VYKON 4 | Choix du mode de jeu")
    fen_menu.configure(bg = "#244352")
    fen_menu.iconbitmap("Data/Logo/favicon.ico")

    menubar = Menu(fen_menu)

    menu1 = Menu(menubar, tearoff = 0)
    menu1.add_command(label = 'Aide', command = fen_menu_aide)
    menubar.add_cascade(label = 'Aide', menu = menu1)
    fen_menu.config(menu = menubar)

    # Logo du jeu #

    imgPath = "Data/Logo/Logooo.gif"
    photo = PhotoImage(file = imgPath)
    label = Label(image = photo)
    label.image = photo
    canvas = Canvas(fen_menu, width=800, height=100)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.configure(bg = "#094a5f")
    canvas.pack()

    Bouton_joueur = Button(fen_menu, text = "Joueur Vs Joueur", bg = "#338099",fg="#10303a",height = 4, width = 25,font = ("Time", 15),relief=GROOVE, command=fen_choix_pseudo2)
    Bouton_joueur.pack(side=RIGHT,padx=30,pady=10)
    Bouton_IA = Button(fen_menu, text = "Joueur Vs IA", bg = "#338099",fg="#10303a",height = 4, width = 25,font = ("Time", 15),relief=GROOVE, command=fenetre_IA)
    Bouton_IA.pack(side=LEFT,padx=30,pady=10)
    fen_menu.mainloop()

def fen_choix_pseudo2():
    global fen_choix_pseudo2

    fen_menu.destroy()
    # Caractéristiques #
    fen_choix_pseudo2 = Tk()
    fen_choix_pseudo2.geometry("800x400")
    fen_choix_pseudo2.title("VYKON 4")
    fen_choix_pseudo2.configure(bg = "#244352")
    fen_choix_pseudo2.iconbitmap("Data/Logo/favicon.ico")

    menubar = Menu(fen_choix_pseudo2)

    menu1 = Menu(menubar, tearoff = 0)
    menu1.add_command(label = 'Aide', command = fen_choix_pseudo2_aide)
    menubar.add_cascade(label = 'Aide', menu = menu1)
    fen_choix_pseudo2.config(menu = menubar)

    # Logo du jeu #

    imgPath = "Data/Logo/Logooo.gif"
    photo = PhotoImage(file = imgPath)
    label = Label(image = photo)
    label.image = photo
    canvas = Canvas(fen_choix_pseudo2, width=800, height=100)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.configure(bg = "#094a5f")
    canvas.pack()

    #etes vous un ancien ?
    label2 = Label( fen_choix_pseudo2, text="Êtes-vous ...", bg= "#244352", fg="#338099", font = ("Time", 20))
    label2.pack(side="top", padx=10, pady=50)

   # Bonton ancien joueur #
    bouton_ancien2=Button( fen_choix_pseudo2, text="... un ancien joueur ?", bg="#338099", fg="#10303a", height = 4, width = 25,font = ("Time", 15), command = fen_pseudo2_ancien)
    bouton_ancien2.pack(side="right", padx=30, pady=10)

    # Bonton nouveau joueur #
    bouton_nouveau2=Button( fen_choix_pseudo2, text="... un nouveau joueur ?", bg="#338099", fg="#10303a", height = 4, width = 25,font = ("Time", 15),command = fen_pseudo2_nouveau)
    bouton_nouveau2.pack(side="left", padx=50, pady=10)

    fen_choix_pseudo2.mainloop()
######################## SI NOUVEAU :

def fen_pseudo2_nouveau():

    global fen_pseudo2_nouveau, Champ_Nouv_2

    fen_choix_pseudo2.destroy()
    fen_pseudo2_nouveau = Tk()
    fen_pseudo2_nouveau.geometry("400x400")
    fen_pseudo2_nouveau.title("VYKON 4 | Pseudo")
    fen_pseudo2_nouveau.configure(bg = "#244352")
    fen_pseudo2_nouveau.iconbitmap("Data/Logo/favicon.ico")

    # Logo du jeu #

    imgPath = "Data/Logo/Mini_Logoo.gif"
    photo = PhotoImage(file = imgPath)
    label = Label(image = photo)
    label.image = photo
    canvas = Canvas(fen_pseudo2_nouveau, width=800, height=100)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.configure(bg = "#094a5f")
    canvas.pack()

    Bouton_nouveau = Button(fen_pseudo2_nouveau, text = "Valider", bg="#338099", fg="#10303a", command = recupere_pseudo2_nouveau)
    Bouton_nouveau.pack(side="bottom", padx=0, pady=10)

    Valeur=StringVar()
    Champ_Nouv_2 = Entry(fen_pseudo2_nouveau, textvariable= Valeur, fg='blue')
    Champ_Nouv_2.focus_set()
    Champ_Nouv_2.pack(side ='bottom', padx=0, pady=75)
    fen_pseudo2_nouveau.bind("<Return>", Touche_du_clavier)

    label = Label( fen_pseudo2_nouveau, text="Créer votre pseudo", bg= "#244352", fg="#338099", font = ("Time", 14))
    label.pack(side="bottom")

    fen_pseudo2_nouveau.mainloop()

def recupere_pseudo2_nouveau():
    global pseudo2

    id=''
    pseudo2=str(Champ_Nouv_2.get())
    score=''
    argent=0
    date=temps
    cursor.execute('''INSERT INTO puissance(id, pseudo, score, argent, date) VALUES (%s,%s,%s,%s,%s)''', (id, pseudo2, score, argent, date))
    fen_pseudo2_nouveau_destroy()

def fen_pseudo2_nouveau_destroy():

    fen_pseudo2_nouveau.destroy()

    fen_joueur()

######################## SI ANCIEN :

def fen_pseudo2_ancien():

    global fen_pseudo2_ancien, Champ_Anc_2

    fen_choix_pseudo2.destroy()
    fen_pseudo2_ancien = Tk()
    fen_pseudo2_ancien.geometry("400x400")
    fen_pseudo2_ancien.title("VYKON 4 | Pseudo")
    fen_pseudo2_ancien.configure(bg = "#244352")
    fen_pseudo2_ancien.iconbitmap("Data/Logo/favicon.ico")

    # Logo du jeu #

    imgPath = "Data/Logo/Mini_Logoo.gif"
    photo = PhotoImage(file = imgPath)
    label = Label(image = photo)
    label.image = photo
    canvas = Canvas(fen_pseudo2_ancien, width=800, height=100)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.configure(bg = "#094a5f")
    canvas.pack()

    Bouton_nouveau = Button(fen_pseudo2_ancien, text = "Valider", bg="#338099", fg="#10303a", command = recupere_pseudo2_ancien)
    Bouton_nouveau.pack(side="bottom", padx=0, pady=10)

    Valeur=StringVar()
    Champ_Anc_2 = Entry(fen_pseudo2_ancien, textvariable= Valeur, fg='blue')
    Champ_Anc_2.focus_set()
    Champ_Anc_2.pack(side ='bottom', padx=0, pady=75)
    fen_pseudo2_ancien.bind("<Return>", Touche_du_clavier)

    label = Label( fen_pseudo2_ancien, text="Entrez votre pseudo", bg= "#244352", fg="#338099", font = ("Time", 14))
    label.pack(side="bottom")

    fen_pseudo2_ancien.mainloop()

def recupere_pseudo2_ancien():
    global pseudo2, Champ_Anc_2
    pseudo2=str(Champ_Anc_2.get())
    fen_pseudo2_ancien.destroy()
    fen_joueur()

################################## BOUTIQUE ####################################

def Ouverture_image_boutique(emplacement, chemin_acces, hauteur, largeur):

    imgPath_Bout = chemin_acces
    photo_Bout = PhotoImage(file = imgPath_Bout)
    label_Bout = Label(image = photo_Bout)
    label_Bout.image = photo_Bout
    canvas_Bout = Canvas(emplacement, width=largeur, height=hauteur)
    canvas_Bout.create_image(0, 0, anchor=NW, image=photo_Bout)
    canvas_Bout.pack(side=LEFT, padx=5,pady=5)

def boutique():
    global fen_bout

    fen_choix_pionts.destroy()

    fen_bout = Tk()
    fen_bout.geometry("1200x600")
    fen_bout.title("VYKON 4 | Boutique")
    fen_bout.configure(bg = "#244352")
    fen_bout.iconbitmap("Data/Logo/favicon.ico")

    Frame1 = Frame(fen_bout,borderwidth=2,relief=FLAT, bg="#244352")
    Frame1.pack(side=TOP,padx=5,pady=5)
    Label(Frame1,text="Pions : 10φ",bg="#338099",fg="#10303a",font = ("Time",12)).pack(side=TOP, padx=5,pady=5)

    Frame2 = Frame(fen_bout,borderwidth=2,relief=FLAT, bg="#244352")
    Frame2.pack(side=TOP,padx=5,pady=5)
    Label(Frame2,text="Thème : 30φ",bg="#338099",fg="#10303a",font = ("Time",12)).pack(side=TOP, padx=5,pady=5)

    Frame3 = Frame(Frame1,borderwidth=2,relief=FLAT, bg="#2d576a")
    Frame3.pack(side=LEFT,padx=5,pady=5)
    Bouton1 = Button(Frame3, text="Achat : Vert",height = 4, width = 15,font = ("Time", 8),bg="#338099",fg="#10303a", command = bout_vert).pack(side=LEFT,padx=5,pady=5)
    Ouverture_image_boutique(Frame3,"Data/Boutique\pion vert.gif", 127, 144)

    Frame4 = Frame(Frame1,borderwidth=2,relief=FLAT,bg="#2d576a")
    Frame4.pack(side=LEFT,padx=5,pady=5)
    Bouton2 = Button(Frame4, text='Achat : Violet',height = 4, width = 15,font = ("Time", 8), bg="#338099",fg="#10303a",command = bout_violet).pack(side=LEFT,padx=5,pady=5)
    Ouverture_image_boutique(Frame4,"Data/Boutique\pion violet.gif", 127, 144)

    Frame5 = Frame(Frame2,borderwidth=2,relief=FLAT,bg="#2d576a")
    Frame5.pack(side=LEFT,padx=5,pady=5)
    Bouton3 = Button(Frame5, text='Achat : Bleu',height = 4, width = 15,font = ("Time", 8), bg="#338099",fg="#10303a",command = bout_t_bleu).pack(side=LEFT,padx=5,pady=5)
    Ouverture_image_boutique(Frame5,"Data/Boutique\Theme_bleu.gif", 200, 200)

    Frame6 = Frame(Frame2,borderwidth=2,relief=FLAT, bg="#2d576a")
    Frame6.pack(side=LEFT,padx=5,pady=5)
    Bouton4 = Button(Frame6, text='Achat : Orange',height = 4, width = 15,font = ("Time", 8), bg="#338099",fg="#10303a",command = bout_t_orange).pack(side=LEFT,padx=5,pady=5)
    Ouverture_image_boutique(Frame6,"Data/Boutique\Theme_country.gif",200, 200)

    Frame7 = Frame(Frame2,borderwidth=2,relief=FLAT, bg="#2d576a")
    Frame7.pack(side=LEFT,padx=5,pady=5)
    Bouton5 = Button(Frame7, text='Achat : Rose',height = 4, width = 15,font = ("Time", 8), bg="#338099",fg="#10303a",command = bout_t_rose).pack(side=LEFT,padx=5,pady=5)
    Ouverture_image_boutique(Frame7,"Data/Boutique\Theme_girl.gif",200, 200)

    Bouton6 = Button(fen_bout, text='Retour',font = ("Time", 12), bg="#338099",fg="#10303a",height = 0, width = 0,command = Retour).pack(side=LEFT,padx=350,pady=5)

    cursor.execute("SELECT * FROM puissance WHERE pseudo='%s';" % (pseudo),)
    result=cursor.fetchone()
    result1=result[3]
    argent_bout=result1

    Label(fen_bout,text="Vous possédez : %s φ"%(str(argent_bout)),bg="#338099",fg="#10303a",font = ("Time",12)).pack(side=LEFT, padx=0,pady=0)

    fen_bout.mainloop()

def Retour():

    fen_bout.destroy()
    choix_pionts()

def bout_vert():

        cursor.execute("SELECT * FROM puissance WHERE pseudo='%s';" % (pseudo),)
        result=cursor.fetchone()
        result1=result[3]

        print(result)
        print(result1)

        if result1-30>=0:
            result_f=result1-30
            cursor.execute("UPDATE puissance SET argent = %s WHERE pseudo = %s", (result_f, pseudo))
            print("CHANGEMENT")
            fichier = open('Data/Pions/Vert/Bouton.txt',"w")
            fichier.write("#000000")
            fichier.close()
            fichier = open('Data/Pions/Vert/Pions2.txt',"w")
            fichier.write("red")
            fichier.close()
            fichier = open('Data/Pions/Vert/Pions1.txt',"w")
            fichier.write("#009933")
            fichier.close()
            fichier = open('Data/Pions/Vert/Fond.txt',"w")
            fichier.write("navy blue")
            fichier.close()
        else :
            boutique_erreur()

def bout_violet():
        cursor.execute("SELECT * FROM puissance WHERE pseudo='%s';" % (pseudo),)
        result=cursor.fetchone()
        result1=result[3]

        print(result)
        print(result1)

        if result1-30>=0:
            result_f=result1-30
            cursor.execute("UPDATE puissance SET argent = %s WHERE pseudo = %s", (result_f, pseudo))
            print("CHANGEMENT")
            fichier = open('Data/Pions/Violet/Bouton.txt',"w")
            fichier.write("#000000")
            fichier.close()
            fichier = open('Data/Pions/Violet/Pions2.txt',"w")
            fichier.write("red")
            fichier.close()
            fichier = open('Data/Pions/Violet/Pions1.txt',"w")
            fichier.write("#C474BA")
            fichier.close()
            fichier = open('Data/Pions/Violet/Fond.txt',"w")
            fichier.write("navy blue")
            fichier.close()
        else:
            boutique_erreur()

def bout_t_bleu():

        cursor.execute("SELECT * FROM puissance WHERE pseudo='%s';" % (pseudo),)
        result=cursor.fetchone()
        result1=result[3]

        print(result)
        print(result1)

        if result1-30>=0:
            result_f=result1-30
            cursor.execute("UPDATE puissance SET argent = %s WHERE pseudo = %s", (result_f, pseudo))
            print("CHANGEMENT")
            fichier = open('Data/Thème/Bleu/Bouton.txt',"w")
            fichier.write("#000000")
            fichier.close()
            fichier = open('Data/Thème/Bleu/Pions1.txt',"w")
            fichier.write("#29B6C3")
            fichier.close()
            fichier = open('Data/Thème/Bleu/Pions2.txt',"w")
            fichier.write("#F4F115")
            fichier.close()
            fichier = open('Data/Thème/Bleu/Fond.txt',"w")
            fichier.write("#52a5d8")
            fichier.close()
        else:
            boutique_erreur()

def bout_t_rose():

        cursor.execute("SELECT * FROM puissance WHERE pseudo='%s';" % (pseudo),)
        result=cursor.fetchone()
        result1=result[3]

        print(result)
        print(result1)

        if result1-30>=0:
            result_f=result1-30
            cursor.execute("UPDATE puissance SET argent = %s WHERE pseudo = %s", (result_f, pseudo))
            print("CHANGEMENT")
            fichier = open('Data/Thème/Rose/Bouton.txt',"w")
            fichier.write("#000000")
            fichier.close()
            fichier = open('Data/Thème/Rose/Pions1.txt',"w")
            fichier.write("#C474BA")
            fichier.close()
            fichier = open('Data/Thème/Rose/Pions2.txt',"w")
            fichier.write("#ADD8E6")
            fichier.close()
            fichier = open('Data/Thème/Rose/Fond.txt',"w")
            fichier.write("#ed6fed")
            fichier.close()
        else:
            boutique_erreur()

def bout_t_orange():

        cursor.execute("SELECT * FROM puissance WHERE pseudo='%s';" % (pseudo),)
        result=cursor.fetchone()
        result1=result[3]

        print(result)
        print(result1)

        if result1-30>=0:
            result_f=result1-30
            cursor.execute("UPDATE puissance SET argent = %s WHERE pseudo = %s", (result_f, pseudo))
            print("CHANGEMENT")
            fichier = open('Data/Thème/Orange/Bouton.txt',"w")
            fichier.write("#000000")
            fichier.close()
            fichier = open('Data/Thème/Orange/Pions2.txt',"w")
            fichier.write("#6495ED")
            fichier.close()
            fichier = open('Data/Thème/Orange/Pions1.txt',"w")
            fichier.write("#EE7621")
            fichier.close()
            fichier = open('Data/Thème/Orange/Fond.txt',"w")
            fichier.write("#009933")
            fichier.close()
        else:
            boutique_erreur()

################################ BLOC NOTE PIONTS ##############################

def t_base():
    global couleur, couleur2, fond_coul, bout_coul

    fichier = open('Data/Thème/Base/Bouton.txt' , "w")

    fichier.write("#000000")

    fichier.close()

    fichier = open('Data/Thème/Base/Pions2.txt',"w")
    fichier.write("red")
    fichier.close()

    fichier = open('Data/Thème/Base/Pions1.txt',"w")
    fichier.write("yellow")
    fichier.close()

    fichier = open('Data/Thème/Base/Fond.txt',"w")
    fichier.write("navy blue")
    fichier.close()

    try:
        with open('Data/Thème/Base/Pions1.txt'):
            fichier = open('Data/Thème/Base/Pions1.txt','r')
            bonjour = fichier.read()
            liste = []
            for i in bonjour:
                liste.append(i)
            couleur = "".join(liste)
            print(couleur)
            fichier.close()

        with open('Data/Thème/Base/Pions2.txt'):
            fichier1 = open('Data/Thème/Base/Pions2.txt','r')
            bonjour1 = fichier1.read()
            liste1 = []
            for i in bonjour1:
                liste1.append(i)
            couleur2 = "".join(liste1)
            print(couleur2)
            fichier1.close()

        with open('Data/Thème/Base/Fond.txt'):
            fichier2 = open('Data/Thème/Base/Fond.txt','r')
            bonjour2 = fichier2.read()
            liste2 = []
            for i in bonjour2:
                liste2.append(i)
            fond_coul = "".join(liste2)
            print(fond_coul)
            fichier2.close()

        with open('Data/Thème/Base/Bouton.txt'):
            fichier3 = open('Data/Thème/Base/Bouton.txt','r')
            bonjour3 = fichier3.read()
            liste3 = []
            for i in bonjour3:
                liste3.append(i)
            bout_coul = "".join(liste3)
            print(bout_coul)
            fichier3.close()
    except IOError:
        choix_erreur()

def vert_p():
    global couleur, couleur2, fond_coul, bout_coul

    Choix_Couleur_piont('Vert')

    try:
        with open('Data/Pions/Vert/Pions1.txt'):
            fichier = open('Data/Pions/Vert/Pions1.txt','r')
            bonjour = fichier.read()
            liste = []
            for i in bonjour:
                liste.append(i)
            couleur = "".join(liste)
            print(couleur)
            fichier.close()

        with open('Data/Pions/Vert/Pions2.txt'):
            fichier1 = open('Data/Pions/Vert/Pions2.txt','r')
            bonjour1 = fichier1.read()
            liste1 = []
            for i in bonjour1:
                liste1.append(i)
            couleur2 = "".join(liste1)
            print(couleur2)
            fichier1.close()

        with open('Data/Pions/Vert/Fond.txt'):
            fichier2 = open('Data/Pions/Vert/Fond.txt','r')
            bonjour2 = fichier2.read()
            liste2 = []
            for i in bonjour2:
                liste2.append(i)
            fond_coul = "".join(liste2)
            print(fond_coul)
            fichier2.close()

        with open('Data/Pions/Vert/Bouton.txt'):
            fichier3 = open('Data/Pions/Vert/Bouton.txt','r')
            bonjour3 = fichier3.read()
            liste3 = []
            for i in bonjour3:
                liste3.append(i)
            bout_coul = "".join(liste3)
            print(bout_coul)
            fichier3.close()
    except IOError:
        choix_erreur()

def violet_p():
    global couleur, couleur2, fond_coul, bout_coul

    Choix_Couleur_piont('Violet')

    try:
        with open('Data/Pions/Violet/Pions1.txt'):
            fichier = open('Data/Pions/Violet/Pions1.txt','r')
            bonjour = fichier.read()
            liste = []
            for i in bonjour:
                liste.append(i)
            couleur = "".join(liste)
            print(couleur)
            fichier.close()

        with open('Data/Pions/Violet/Pions2.txt'):
            fichier1 = open('Data/Pions/Violet/Pions2.txt','r')
            bonjour1 = fichier1.read()
            liste1 = []
            for i in bonjour1:
                liste1.append(i)
            couleur2 = "".join(liste1)
            print(couleur2)
            fichier1.close()

        with open('Data/Pions/Violet/Fond.txt'):
            fichier2 = open('Data/Pions/Violet/Fond.txt','r')
            bonjour2 = fichier2.read()
            liste2 = []
            for i in bonjour2:
                liste2.append(i)
            fond_coul = "".join(liste2)
            print(fond_coul)
            fichier2.close()

        with open('Data/Pions/Violet/Bouton.txt'):
            fichier3 = open('Data/Pions/Violet/Bouton.txt','r')
            bonjour3 = fichier3.read()
            liste3 = []
            for i in bonjour3:
                liste3.append(i)
            bout_coul = "".join(liste3)
            print(bout_coul)
            fichier3.close()
    except IOError:
        choix_erreur()

def t_bleu():
    global couleur, couleur2, fond_coul, bout_coul

    Choix_Couleur_Theme('Bleu')

    try:
        with open('Data/Thème/Bleu/Pions1.txt'):
            fichier = open('Data/Thème/Bleu/Pions1.txt','r')
            bonjour = fichier.read()
            liste = []
            for i in bonjour:
                liste.append(i)
            couleur = "".join(liste)
            print(couleur)
            fichier.close()

        with open('Data/Thème/Bleu/Pions2.txt'):
            fichier1 = open('Data/Thème/Bleu/Pions2.txt','r')
            bonjour1 = fichier1.read()
            liste1 = []
            for i in bonjour1:
                liste1.append(i)
            couleur2 = "".join(liste1)
            print(couleur2)
            fichier1.close()

        with open('Data/Thème/Bleu/Fond.txt'):
            fichier2 = open('Data/Thème/Bleu/Fond.txt','r')
            bonjour2 = fichier2.read()
            liste2 = []
            for i in bonjour2:
                liste2.append(i)
            fond_coul = "".join(liste2)
            print(fond_coul)
            fichier2.close()

        with open('Data/Thème/Bleu/Bouton.txt'):
            fichier3 = open('Data/Thème/Bleu/Bouton.txt','r')
            bonjour3 = fichier3.read()
            liste3 = []
            for i in bonjour3:
                liste3.append(i)
            bout_coul = "".join(liste3)
            print(bout_coul)
            fichier3.close()
    except IOError:
        choix_erreur()

def t_orange():
    global couleur, couleur2, fond_coul, bout_coul

    Choix_Couleur_Theme('Orange')

    try:
        with open('Data/Thème/Orange/Pions1.txt'):
            fichier = open('Data/Thème/Orange/Pions1.txt','r')
            bonjour = fichier.read()
            liste = []
            for i in bonjour:
                liste.append(i)
            couleur = "".join(liste)
            print(couleur)
            fichier.close()

        with open('Data/Thème/Orange/Pions2.txt'):
            fichier1 = open('Data/Thème/Orange/Pions2.txt','r')
            bonjour1 = fichier1.read()
            liste1 = []
            for i in bonjour1:
                liste1.append(i)
            couleur2 = "".join(liste1)
            print(couleur2)
            fichier1.close()

        with open('Data/Thème/Orange/Fond.txt'):
            fichier2 = open('Data/Thème/Orange/Fond.txt','r')
            bonjour2 = fichier2.read()
            liste2 = []
            for i in bonjour2:
                liste2.append(i)
            fond_coul = "".join(liste2)
            print(fond_coul)
            fichier2.close()

        with open('Data/Thème/Orange/Bouton.txt'):
            fichier3 = open('Data/Thème/Orange/Bouton.txt','r')
            bonjour3 = fichier3.read()
            liste3 = []
            for i in bonjour3:
                liste3.append(i)
            bout_coul = "".join(liste3)
            print(bout_coul)
            fichier3.close()
    except IOError:
        choix_erreur()

def t_rose():
    global couleur, couleur2, fond_coul, bout_coul

    Choix_Couleur_Theme('Rose')

    try:
        with open('Data/Thème/Rose/Pions1.txt'):
            fichier = open('Data/Thème/Rose/Pions1.txt','r')
            bonjour = fichier.read()
            liste = []
            for i in bonjour:
                liste.append(i)
            couleur = "".join(liste)
            print(couleur)
            fichier.close()

        with open('Data/Thème/Rose/Pions2.txt'):
            fichier1 = open('Data/Thème/Rose/Pions2.txt','r')
            bonjour1 = fichier1.read()
            liste1 = []
            for i in bonjour1:
                liste1.append(i)
            couleur2 = "".join(liste1)
            print(couleur2)
            fichier1.close()

        with open('Data/Thème/Rose/Fond.txt'):
            fichier2 = open('Data/Thème/Rose/Fond.txt','r')
            bonjour2 = fichier2.read()
            liste2 = []
            for i in bonjour2:
                liste2.append(i)
            fond_coul = "".join(liste2)
            print(fond_coul)
            fichier2.close()

        with open('Data/Thème/Rose/Bouton.txt'):
            fichier3 = open('Data/Thème/Rose/Bouton.txt','r')
            bonjour3 = fichier3.read()
            liste3 = []
            for i in bonjour3:
                liste3.append(i)
            bout_coul = "".join(liste3)
            print(bout_coul)
            fichier3.close()
    except IOError:
        choix_erreur()

################################ AUTRE #########################################

def Touche_du_clavier (event):

    touche = event.keysym
    if touche == "Return":
        try:
            recupere_pseudo_nouveau()
        except:
            pass
        try:
            recupere_pseudo_ancien()
        except:
            pass
        try:
            recupere_pseudo2_nouveau()
        except:
            pass
        try:
            recupere_pseudo2_ancien()
        except:
            pass

def fen_bug_destroy():
    fen_bug.destroy()

def fen_bout_erreur_destroy():
    fen_bout_erreur.destroy()

def fen_choix_erreur_destroy():
    fen_choix_erreur.destroy()

def boutique_erreur():
    global fen_bout_erreur

    fen_bout_erreur=Tk()
    fen_bout_erreur.title("Solde insuffisant")
    fen_bout_erreur.geometry("600x200")
    fen_bout_erreur.resizable(width=False, height=False)
    fen_bout_erreur.configure(bg = "#244352")
    fen_bout_erreur.iconbitmap("Data/Logo/favicon.ico")

    # message d'érreur #
    label = Label(fen_bout_erreur, text="Votre solde n'est pas suffisant pour acquérir cet élément.\n Vous pouvez consulter votre dans la boutique.", bg= "#244352", fg="#338099", font = ("Time", 15))
    label.pack(side="top", padx=10, pady=30)

    # bouton pour fermer #
    Bouton_valider = Button(fen_bout_erreur, text = "Fermer", bg="#338099", fg="#10303a",command= fen_bout_erreur_destroy)
    Bouton_valider.pack(side="top")
    fen_bout_erreur.mainloop()

def choix_erreur():
    global fen_choix_erreur

    fen_choix_erreur=Tk()
    fen_choix_erreur.title("Elément non possédé")
    fen_choix_erreur.geometry("600x200")
    fen_choix_erreur.resizable(width=False, height=False)
    fen_choix_erreur.configure(bg = "#244352")
    fen_choix_erreur.iconbitmap("Data/Logo/favicon.ico")

    # message d'érreur #
    label = Label(fen_choix_erreur, text="Vous ne possédez pas cet élément,\n vous pouvez vous rendre dans la boutique pour l'acquérir.", bg= "#244352", fg="#338099", font = ("Time", 15))
    label.pack(side="top", padx=10, pady=30)

    # bouton pour fermer #
    Bouton_valider = Button(fen_choix_erreur, text = "Fermer", bg="#338099", fg="#10303a",command= fen_choix_erreur_destroy)
    Bouton_valider.pack(side="top")
    fen_choix_erreur.mainloop()

#########################   AIDE   #############################################

def fen_choix_pseudo_aide():

    fen_choix_pseudo_aide = Tk()
    fen_choix_pseudo_aide.resizable(width = False, height = False)
    fen_choix_pseudo_aide.title("Aide | VYKON 4")
    fen_choix_pseudo_aide.geometry("1100x220")
    fen_choix_pseudo_aide.config(bg = "#87c2e0")
    fen_choix_pseudo_aide.iconbitmap("Data/Logo/favicon.ico")
    label = Label(fen_choix_pseudo_aide, text = "\nChoix de l'ancienneté.\n", bg = "#87c2e0", font = ('Time', 15)).pack()
    label1 = Label(fen_choix_pseudo_aide, text = "Si vous êtes un nouveau joueur, autrement dit, si vous n'avez jamais joué au jeu, merci de cliquer sur le bouton '... un nouveau joueur ?'.\n", bg = "#87c2e0", font = ('Time', 12)).pack()
    label2 = Label(fen_choix_pseudo_aide, text = "Si vous êtes un ancien joueur, autrement dit, si vous avez déjà un compte, merci de cliquer sur le bouton '... un ancien joueur ?'.\n" ,bg = "#87c2e0", font = ('Time', 12)).pack()
    label3 = Label(fen_choix_pseudo_aide, text = "Si vous êtes un ancien joueur, veuillez à bien écrire le même pseudo que celui que vous avez écrit en vous enregistrant au risque de problème majeur.", bg = "#87c2e0", font = ('Time', 12)).pack()
    fen_choix_pseudo_aide.mainloop()

def choix_pions_aide():
    fen_choix_pions_aide = Tk()
    fen_choix_pions_aide.resizable(width = False, height = False)
    fen_choix_pions_aide.title("Aide | VYKON 4")
    fen_choix_pions_aide.geometry("980x270")
    fen_choix_pions_aide.config(bg = "#87c2e0")
    fen_choix_pions_aide.iconbitmap("Data/Logo/favicon.ico")
    label = Label(fen_choix_pions_aide, text = "\nChoix des pions OU du thème.\n", bg = "#87c2e0", font = ('Time', 15)).pack()
    label1 = Label(fen_choix_pions_aide, text = "Vous avez la possibilité de choisir un pion OU un thème.\n" ,bg = "#87c2e0", font = ('Time', 12)).pack()
    label2 = Label(fen_choix_pions_aide, text = "Si vous voulez acheter des pions ou des thèmes, merci de cliquer sur le bouton 'Boutique'.\n", bg = "#87c2e0", font = ('Time', 12)).pack()
    label3 = Label(fen_choix_pions_aide, text = "Si vous avez déjà acheté des pions ou des thèmes, vous avez la possibilité de sélectionner le pion OU le thème désiré,\npour ce faire, vous avez différents boutons vous indiquant les types de pions ou de thèmes disponibles.", bg = "#87c2e0", font = ('Time', 12)).pack()
    label4 = Label(fen_choix_pions_aide, text = "\nAttention, si vous choisissez un thème puis un pion, seul le pion sera pris en compte et inversement." ,bg = "#87c2e0", font = ('Time', 12)).pack()
    fen_choix_pions_aide.mainloop()

def fen_menu_aide():
    fen_aide_type_de_partie = Tk()
    fen_aide_type_de_partie.resizable(width = False, height = False)
    fen_aide_type_de_partie.title("Aide | VYKON 4")
    fen_aide_type_de_partie.geometry("830x230")
    fen_aide_type_de_partie.config(bg = "#87c2e0")
    fen_aide_type_de_partie.iconbitmap("Data/Logo/favicon.ico")
    label = Label(fen_aide_type_de_partie, text = "\nChoix du type de partie.\n", bg = "#87c2e0", font = ('Time', 15)).pack()
    label1 = Label(fen_aide_type_de_partie, text = "Si vous sélectionnez 'Joueur vs Joueur' vous allez jouer contre un ami sur le même ordinateur.\nPar la suite, le pseudo du second joueur vous sera demandé." ,bg = "#87c2e0", font = ('Time', 12)).pack()
    label2 = Label(fen_aide_type_de_partie, text = "\nSi vous sélectionnez 'Joueur vs IA' vous allez jouer contre l'intelligence artificielle que nous avons élaborée.", bg = "#87c2e0", font = ('Time', 12)).pack()
    label3 = Label(fen_aide_type_de_partie, text = "\nAttention, si vous choisissez 'Joueur vs IA', veuillez à ne surtout pas bouger la fenêtre.", bg = "#87c2e0", font = ('Time', 12)).pack()
    fen_aide_type_de_partie.mainloop()

def fen_choix_pseudo2_aide():
    fen_choix_pseudo2_aide = Tk()
    fen_choix_pseudo2_aide.resizable(width = False, height = False)
    fen_choix_pseudo2_aide.title("Aide | VYKON 4")
    fen_choix_pseudo2_aide.geometry("1100x220")
    fen_choix_pseudo2_aide.config(bg = "#87c2e0")
    fen_choix_pseudo2_aide.iconbitmap("Data/Logo/favicon.ico")
    label = Label(fen_choix_pseudo2_aide, text = "\nChoix de l'ancienneté.\n", bg = "#87c2e0", font = ('Time', 15)).pack()
    label1 = Label(fen_choix_pseudo2_aide, text = "Si vous êtes un nouveau joueur, autrement dit, si vous n'avez jamais joué au jeu, merci de cliquer sur le bouton '... un nouveau joueur ?'.\n", bg = "#87c2e0", font = ('Time', 12)).pack()
    label2 = Label(fen_choix_pseudo2_aide, text = "Si vous êtes un ancien joueur, autrement dit, si vous avez déjà un compte, merci de cliquer sur le bouton '... un ancien joueur ?'.\n" ,bg = "#87c2e0", font = ('Time', 12)).pack()
    label3 = Label(fen_choix_pseudo2_aide, text = "Si vous êtes un ancien joueur, veuillez à bien écrire le même pseudo que celui que vous avez écrit en vous enregistrant au risque de problème majeur.", bg = "#87c2e0", font = ('Time', 12)).pack()
    fen_choix_pseudo2_aide.mainloop()

################## Main ###################

try:
    temps=date.today()
    conn = mysql.connector.connect(host="process.env.HOST", user="process.env.USER", password="process.env.PASSWORD", database="process.env.DATABASE")
    cursor = conn.cursor()

    # Caractéristiques #
    Fenetre_Principale = Tk()
    Fenetre_Principale.geometry("800x400")
    Fenetre_Principale.resizable(width = False, height = False)
    Fenetre_Principale.title("VYKON 4")
    Fenetre_Principale.configure(bg = "#244352")
    Fenetre_Principale.iconbitmap("Data/Logo/favicon.ico")

    # Logo du jeu #

    imgPath = "Data/Logo/Logooo.gif"
    photo = PhotoImage(file = imgPath)
    label = Label(image = photo)
    label.image = photo # keep a reference!
    canvas = Canvas(Fenetre_Principale, width=800, height=100)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    canvas.configure(bg = "#094a5f")
    canvas.pack()

    # Bonton jouer #
    bouton_jouer=Button(Fenetre_Principale, text="JOUER", fg="#244352",width=70,height=20,bg= "#338099",command= fen_choix_pseudo, font = ("Time", 25))
    bouton_jouer.pack(padx=30, pady=30)

    Fenetre_Principale.mainloop()

except:
    # Caractéristiques #
    fen_bug=Tk()
    fen_bug.title("Erreur de connexion")
    fen_bug.geometry("400x200")
    fen_bug.resizable(width=False, height=False)
    fen_bug.configure(bg = "#244352")
    fen_bug.iconbitmap("Data/Logo/favicon.ico")

    # message d'érreur #
    label = Label( fen_bug, text="Une erreur de connexion est survenue, \nvérifiez votre connexion à internet. \nVeuillez réessayer ultérieurement.", bg= "#244352", fg="#338099", font = ("Time", 15))
    label.pack(side="top", padx=10, pady=30)

    # bouton pour fermer #
    Bouton_valider = Button(fen_bug, text = "Quitter", bg="#338099", fg="#10303a",command= fen_bug_destroy)
    Bouton_valider.pack(side="top")
    fen_bug.mainloop()

try:
    fen.mainloop()
except:
    pass

try:
    fenetre_IA.mainloop()
except:
    pass
