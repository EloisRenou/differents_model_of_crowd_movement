######## Bibliothèque ########

from tkinter import Canvas, Tk, Label, BOTTOM, TOP, Entry, Button, StringVar
from math import sqrt
import random
import time


######## Fonction auxilaire ########


def obstacle (x : float, y : float, dx : float, dy : float ) -> tuple: #tuple(float, float)
    """Renvoie le vecteur vitesse de la personne i en fonction de sa position
    Entrée :
        x : absice de la personne
        y : ordonnée de la personne
        dx : vecteur vitesse en x de la personne
        dy : vecteur vitesse en y de la personne
    Sortie :
        dx : vecteur vitesse en x de la personne en fonction des obstacles
        dy : vecteur vitesse en y de la personne en fonction des obstacls"""
    if y<11*taille-rayon and y>9*taille+rayon and x>9*taille:
        d=sqrt((20*taille-x-dx)**2+(10*taille+rayon-y-dy)**2)
        dx,dy=(20*taille-rayon-x-dx)/d, 0
    if x>8*taille-rayon and x<15.75*taille-rayon and y>12*taille-rayon:
        d=sqrt((15.75*taille-rayon-x-dx)**2+(11*taille+rayon-y-dy)**2)
        dx,dy=(15.75*taille-rayon-x-dx)/d, (11*taille+rayon -y-dy)/d
    if x>15.75*taille-rayon and x<16.5*taille+rayon and y>13*taille+rayon:
        d=sqrt((15*taille+rayon-x-dx)**2+(13*taille-rayon-y-dy)**2)
        dx,dy=(15*taille+rayon-x-dx)/d, (13*taille-rayon -y-dy)/d
    if x>8*taille-rayon and x<16.5*taille+rayon and y>11*taille+rayon and y<12*taille-rayon:
        d=sqrt((15.5*taille+rayon-x-dx)**2+(10*taille-rayon-y-dy)**2)
        dx,dy=(15.5*taille+rayon-x-dx)/d, (10*taille-rayon -y-dy)/d
    if x>16.5*taille-rayon and y>14*taille+rayon:
        d=sqrt((16*taille+rayon-x-dx)**2+(14*taille+rayon-y-dy)**2)
        dx,dy=(16*taille+rayon-x-dx)/d, (14*taille+rayon -y-dy)/d
    if x>15.75*taille-rayon and x<16.5*taille+rayon and y>13*taille+rayon:
        d=sqrt((15*taille+rayon-x-dx)**2+(13*taille+rayon-y-dy)**2)
        dx,dy=(15*taille+rayon-x-dx)/d, (13*taille+rayon -y-dy)/d
    if x>17.5*taille-rayon and y<14*taille+rayon and y>13*taille-rayon:
        d=sqrt((17.25*taille+rayon-x-dx)**2+(16*taille+rayon-y-dy)**2)
        dx,dy=(17.25*taille+rayon-x-dx)/d, (16*taille+rayon -y-dy)/d
    if x>16*taille+rayon and y>14*taille+rayon:
        d=sqrt((15.5*taille+rayon-x-dx)**2+(14*taille+rayon-y-dy)**2)
        dx,dy=(15.5*taille+rayon-x-dx)/d, (14*taille+rayon -y-dy)/d
    if x>8*taille+rayon and x<11*taille+rayon and y<11.5*taille-rayon and y>10 *taille-rayon:
        d=sqrt((6*taille+rayon-x-dx)**2+(10*taille-rayon-y-dy)**2)
        dx,dy= (6*taille+rayon-x-dx)/d, (10*taille-rayon -y-dy)/d
    if x>8*taille-rayon and x<11*taille+rayon and y>11.5*taille+rayon :
        dy=0
    if x>14.5*taille-rayon and x<15.5*taille+rayon and y<2*taille:
        d=sqrt((16*taille+rayon-x-dx)**2+(3*taille-rayon-y-dy)**2)
        dx,dy= (16*taille+rayon-x-dx)/d, (3*taille-rayon -y-dy)/d
    if x>4.5*taille-rayon and x<8*taille+rayon and y>11.5*taille-rayon:
        d=sqrt((3.5*taille+rayon-x-dx)**2+(11*taille+rayon-y-dy)**2)
        dx,dy= (3.5*taille+rayon-x-dx)/d, (11*taille+rayon -y-dy)/d
    if y>6*taille-rayon and y<7*taille+rayon and x<11*taille+rayon and x>9*taille-rayon:
        d=sqrt((8*taille+rayon-x-dx)**2+(4.5*taille+rayon-y-dy)**2)
        dx,dy= (8*taille+rayon-x-dx)/d, (4.5*taille+rayon -y-dy)/d
    if x>7*taille-rayon and x<9*taille+rayon and y<6*taille-rayon :
        dy=0
    if y>7*taille-rayon and y<8*taille+rayon and x<11*taille+rayon and x>9*taille-rayon:
        d=sqrt((8*taille+rayon-x-dx)**2+(9.5*taille+rayon-y-dy)**2)
        dx,dy= (8*taille+rayon-x-dx)/d, (9.5*taille+rayon -y-dy)/d
    if y<2*taille+rayon and x<15.5*taille+rayon and x>14.5*taille-rayon:
        d=sqrt((16*taille-rayon-x-dx)**2+(2.5*taille-rayon-y-dy)**2)
        dx,dy= (16*taille-rayon-x-dx)/d, (2.5*taille-rayon -y-dy)/d
    if x>7.5*taille+rayon and x<7.5*taille+1.1*rayon and y>10.5*taille-rayon and y<11*taille+rayon:
        dx=0
    return(dx,dy)


######## Fonctions principales ########


def initialisation() -> None:
    """Initialise les personnes dans la salle et renvoie une liste de coordonnées des personnes et une liste de rectangles
    Entrée :
        None
    Sortie :
        None"""
    while len(personnes)<nb_personne:
        compteur=True
        x = random.randint(taille+rayon,longueur-bord-rayon-taille)
        y = random.randint(rayon+taille,largeur-rayon-taille)
        if x>12*taille and x<taille*15 and y<8*taille and y>5*taille:
                compteur=False 
        if x>9*taille and x<11*taille and y>7*taille and y<10*taille:
                compteur=False
        if x<3*taille:
            compteur=False
        if x<13*taille+rayon and y<5*taille+rayon:
            compteur=False
        if x<13*taille+rayon and y>12*taille-rayon:
            compteur=False
        if x>7*taille-rayon and x<9*taille+rayon and y>6*taille-rayon and y<8*taille+rayon:
            compteur=False
        if x>4.5*taille-rayon and x<7.5*taille+rayon and y>10.5*taille-rayon and y<11*taille+rayon:
            compteur=False
        if x>11*taille-rayon and x<13*taille+rayon and y>8*taille-rayon and y<11*taille+rayon:
            compteur=False
        if  x<13*taille+rayon and x>11*taille-rayon and y<6.5*taille+rayon:
            compteur=False
        if y>8*taille-rayon and y<9*taille+rayon and x>11*taille:
            compteur=False
        if x>14.5*taille-rayon and x<15.5*taille+rayon and y>2*taille-rayon and y<4*taille+rayon:
            compteur=False
        if x>15*taille-rayon and x<17*taille+rayon and y>5.5*taille-rayon and y<6.5*taille+rayon:
            compteur=False
        if x>15*taille-rayon and y>12*taille-rayon and y<13*taille+rayon:
            compteur=False
        if x>16.5*taille-rayon and x<17.5*taille+rayon and y>11*taille-rayon and y<14*taille+rayon:
            compteur=False
        for i in range(len(personnes)):
            if sqrt((x-personnes[i][1])**2 + (y-personnes[i][2])**2)<2*rayon:
                compteur=False
        if compteur:
            if x>13*taille+rayon:
                if y<8.5*taille:
                    d=(sqrt((20*taille-x)**2+(7*taille - y)**2))
                    if d!=0:
                        dx, dy = (20*taille - x)/d, (7*taille - y)/d
                        numero_personne = can.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, width=1, fill='red')
                        personnes.append([numero_personne,x,y,dx,dy,rayon,d,0,-1])
                else:
                    d=(sqrt((20*taille-x)**2+(10*taille - y)**2))
                    if d!=0:
                        dx, dy = (20*taille - x)/d, (10*taille - y)/d
                        numero_personne = can.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, width=1, fill='red')
                        personnes.append([numero_personne,x,y,dx,dy,rayon,d,0,-1])
            else:
                d=(sqrt((sortiex-x)**2+(sortiey - y)**2))
                if d!=0:
                    dx, dy = (sortiex - x)/d, (sortiey - y)/d
                    numero_personne = can.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, width=1, fill='red')
                    personnes.append([numero_personne,x,y,dx,dy,d])
        can.compteur.config(text='%s'%nb_personne)
        personnes.sort(key=lambda personnes: personnes[5])
    mouvement(nb_personne,personnes)


def mouvement(nb_personne : int, personnes : list) -> None:
    """Fait bouger les personnes dans la salle
    Entrée :
        nb_personne : nombre de personne
        personnes : liste des personnes
    Sortie :
        None"""
    temp=[]
    temps_debut = time.time()
    while True:
        i=0
        while i<nb_personne:
            numero_personne,x,y,dx,dy,d=personnes[i][0],personnes[i][1],personnes[i][2],personnes[i][3],personnes[i][4],personnes[i][5]
            x , y = x+dx , y+dy
            if x>13*taille+rayon:
                if y<8.5*taille:
                    d=(sqrt((20*taille-x)**2+(7*taille - y)**2))
                    if d!=0:
                        dx, dy = (20*taille - x)/d, (7*taille - y)/d
                else:
                    d=(sqrt((20*taille-x)**2+(10*taille - y)**2))
                    if d!=0:
                        dx, dy = (20*taille - x)/d, (10*taille - y)/d
            else:
                d=(sqrt((sortiex-x)**2+(sortiey - y)**2))
                if d!=0:
                    dx, dy = (sortiex - x)/d, (sortiey - y)/d
            dx,dy=obstacle(x,y,dx,dy)
            if (x<bord+rayon) and (y<=sortiey1+rayon or y>=sortiey2-rayon):
                dx = 0
            temp=[]
            j=0
            while j<nb_personne:
                numero_personne2,x2,y2,dx2,dy2,d2=personnes[j][0],personnes[j][1],personnes[j][2],personnes[j][3],personnes[j][4],personnes[j][5]
                if j!=i:
                    if sqrt((x2-x)*(x2-x)+(y2-y)*(y2-y))<=2*rayon:
                        if x2<=x:
                            temp.append([x2,y2])
                j+=1
            if len(temp)==1:
                if (y-dy-temp[0][1])<=0:
                    x=x-dx/2
                    y=-sqrt(31**2-(temp[0][0]-x)**2)+temp[0][1]
                else:
                    x=x-dx/2
                    y=y-dy
                    y=+sqrt(31**2-(temp[0][0]-x)**2)+temp[0][1]
            if len(temp)>=1:
                y=y-dy
                x=x-dx
            if (x<taille+rayon) and (y<=sortiey1+rayon or y>=sortiey2-rayon):
                dx = 0
            if (x>19*taille-rayon) and ((not (y>6*taille+rayon and y<8*taille-rayon)) and (not (y>9*taille+rayon and y<11*taille-rayon))):
                dx = 0
            if x<13*taille+rayon and x>12*taille:
                a=dx
                dx=0
                dy=3*dy
                if y>6*taille-rayon and y<11*taille+rayon:
                    if y>8.5*taille and dy<0:
                        dy=-dy
            if x>11*taille-rayon  and x<14*taille and y>6*taille+rayon and y<8*taille-rayon:
                dy=0
                if x<13*taille+rayon and x>12*taille:
                    dx=a
                dx=1.25*dx
            if x>11*taille-rayon and x<14*taille and y>10.5*taille+rayon and y<12.5*taille-rayon:
                dy=0
                if x<13*taille+rayon and x>12*taille:
                    dx=a
                dx=1.25*dx
            if x<taille+rayon:
                if y>9.5*taille-rayon or y<7.5*taille+rayon:
                    dx=0
            if x>15*taille-rayon and x<17*taille+rayon and y>5*taille and y<5.5*taille:
                dy=0
            if y>2*taille-rayon and y<4*taille+rayon and x>14.5*taille-rayon and x<14.5*taille:
                dx=0
            if x>14*taille-rayon and x<15*taille+rayon and y<6.5*taille+rayon and y>5.5*taille-rayon:
                dx=0
            if x>9*taille and y>8*taille-rayon and y<9*taille+rayon:
                x-=dx
                y-=dy
            can.coords(numero_personne, x-rayon, y-rayon, x+rayon, y+rayon)
            if y>=(sortiey1+rayon) and y<=(sortiey2-rayon) and x<(sortiex+bord):
                can.delete(numero_personne)
                personnes.pop(i)
                nb_personne -= 1
                i-=1
                can.compteur.config(text='%s'%nb_personne)
                if nb_personne == 0 :
                    temps_fin=time.time()
                    temps = temps_fin - temps_debut
                    print("Evacuation réussi en :",temps)
            elif (x>19*taille) and y>6*taille+rayon and y<8*taille-rayon:
                can.delete(numero_personne)
                personnes.pop(i)
                nb_personne -= 1
                i-=1
                can.compteur.config(text='%s'%nb_personne)
                if nb_personne == 0 :
                    temps_fin=time.time()
                    temps = temps_fin - temps_debut
                    print("Evacuation réussi en :",temps)
            elif (x>19*taille) and y>9*taille+rayon and y<11*taille-rayon:
                can.delete(numero_personne)
                personnes.pop(i)
                nb_personne -= 1
                i-=1
                can.compteur.config(text='%s'%nb_personne)
                if nb_personne == 0 :
                    temps_fin=time.time()
                    temps = temps_fin - temps_debut
                    print("Evacuation réussi en :",temps)
            else:
                d=(sqrt((sortiex-x)**2+(sortiey- y)**2))
                personnes[i]=[numero_personne,x,y,dx,dy,d]
            i+=1
            personnes.sort(key=lambda personnes: personnes[5])
        time.sleep(0.05)
        fen.update()


######## Variables ########


compt = 0
temps = 0.00
personnes = []

taille=40
largeur = 17*taille
longueur = 20*taille
rayon = 15
bord = 15
sortiey1 = 7.5*taille
sortiey2 = 9.5*taille
sortiex = 0
sortiey = (abs(sortiey1+sortiey2)/2)

print("Donnez le nombre de personne : ")
nb_personne=int(input())

######## Fenêtre Tkinter ########

fen = Tk()
fen.title("TIPE Mouvement de foule : musée avec 2 sorties (Eloïs RENOU 30191)")

can = Canvas(fen,bg='white',height=largeur, width=longueur)
can.pack(side=TOP, padx =5, pady =5)

#contour
rec1=can.create_rectangle(0,3.5*taille,13*taille,4.5*taille,fill='black') #barre en haut a gauche
rec2=can.create_rectangle(0,12.5*taille,13*taille,13.5*taille,fill='black') #barre en bas a gauche
rec3=can.create_rectangle(12*taille,0,13*taille,6*taille,fill='black') #barre verticale du milieu haut
rec4=can.create_rectangle(12*taille,12.5*taille,13*taille,17*taille,fill='black') #barre verticale du milieu bas
rec5=can.create_rectangle(13*taille,0,20*taille,taille,fill='black')#barre horizontale haut tres haut
rec6=can.create_rectangle(13*taille,16*taille,20*taille,17*taille,fill='black')#barre horizontale bas tres bas
rec7=can.create_rectangle(11*taille,8*taille,13*taille,10.5*taille,fill='black') #gros bloc du milieu
rec9=can.create_rectangle(19*taille,0,20*taille,18*taille,fill='black') #barre verticale du droite tres droite
rec14=can.create_rectangle(19*taille,6*taille,20*taille,8*taille,fill='white',outline='white')
rec15=can.create_rectangle(19*taille,9*taille,20*taille,11*taille,fill='white',outline='white')
rec8=can.create_rectangle(13*taille,8*taille,20*taille,9*taille,fill='black') #l'horizontal du milieu
rec10=can.create_rectangle(0,4.5*taille,taille,7.5*taille,fill='black') #barre verticale au dessus de la sortie
rec11=can.create_rectangle(0,9.5*taille,taille,12.5*taille,fill='black')#barre verticale en dessous de la sortie
rec13=can.create_rectangle(11*taille,4.5*taille,13*taille,6*taille,fill='black')


#obstacle
rec13=can.create_rectangle(4.5*taille,10.5*taille,7.5*taille,11*taille,fill='black') #petit rectangle du bas secteur milieu
rec14=can.create_rectangle(7*taille,6*taille,9*taille,8*taille,fill='black') #carre du milieu
rec15=can.create_rectangle(14.5*taille,2*taille,15.5*taille,4*taille,fill='black') #rectangle du haut secteur haut
rec16=can.create_rectangle(15*taille,5.5*taille,17*taille,6.5*taille,fill='black')# rectangle du bas secteur haut
rec17=can.create_rectangle(15.75*taille,12*taille,19*taille,13*taille,fill='black') #barre horizontale de la croix
rec18=can.create_rectangle(16.5*taille,11.5*taille,17.5*taille,14*taille,fill='black') #barre verticale de la croix


can.compteur=Label(fen,text='0',fg='black')
Label(fen,text="Nombre de personne(s) restantes",fg='black').pack()


can.compteur.pack()
Label(fen,text=" ",fg='white').pack()
initialisation()
fen.mainloop()


######## Fin ########