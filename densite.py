###### Bibliothèques ######

from tkinter import Canvas, Tk, LEFT
from math import sqrt
import random
import time

###### Fonctions Auxiliaires ######


def grille () -> list:
    """Crée une grille de 30x19 et renvoie une liste de 30x19 rectangles, les rectangles sont des figures tkinter
    Entrée :
        None
    Sortie :
        rectangle : list"""
    rectangle=[]
    tab=[]
    for i in range(30):
        tab.append([])
        rectangle.append([])
        for j in range(19):
            tab[i].append(0)
            rec=can.create_rectangle(15+19*i,15+19*j,15+19*(i+1),15+19*(j+1),fill='',width=0)
            rectangle[i].append(rec)
    return(rectangle)


def tab_vide() -> list:
    """Crée une list de 30x19 et renvoie un tableau a 2 dimensions de taille 30x19
    Entrée :
        None
    Sortie :
        tab : list"""
    tab=[]
    for i in range(30):
        tab.append([])
        for j in range(19):
            tab[i].append(0)
    return(tab)


###### Fonctions Principales ######

def initialisation() -> None:
    """Initialise les personnes dans la salle et renvoie une liste de coordonnées des personnes et une liste de rectangles
    Entrée :
        None
    Sortie :
        None"""
    rectangle=grille()
    tab=tab_vide()
    for i in range(0, nb_personne):
        x = random.randint(200,570)
        y = random.randint(bord+10,longueur-30-bord)
        recx=(x-15)//19
        recy=(y-15)//19
        tab[recx][recy]+=1
        personnes.append([x,y])
    for i in range(len(tab)):
        for j in range(len(tab[0])):
            if tab[i][j]>=1 and tab[i][j]<3:
                can.itemconfigure(rectangle[i][j], fill='yellow')
            if tab[i][j]==3 or tab[i][j]==4:
                can.itemconfigure(rectangle[i][j], fill='orange')
            if tab[i][j]==5 or tab[i][j]==6:
                can.itemconfigure(rectangle[i][j], fill='red')
            if tab[i][j]>=7:
                can.itemconfigure(rectangle[i][j], fill='purple')
    mouvement(personnes,rectangle)


def mouvement(personnes : list, rectangle : list) -> None:
    """Fait bouger les personnes dans la salle et en fonction de leur positon colorie le rectangle correspondant
    Entrée :
        personnes : list
        rectangle : list
    Sortie :
        None"""
    while True:
        tab=tab_vide()
        p=0
        while p<len(personnes):
            x,y=personnes[p][0],personnes[p][1]
            d=(sqrt((sortiex-x)**2+(sortiey - y)**2))
            dx, dy = (sortiex - x)/d, (sortiey - y)/d
            x , y = x+dx , y+dy
            recx=int((x-15)//19)
            recy=int((y-15)//19)
            if y>=(sortiey1) and y<=(sortiey2) and x<(bord):
                personnes.pop(p)
                p-=1
                if len(personnes)==0:
                    print("Evacuation terminée")
                    break
                if p==(len(personnes)):
                    break
            if tab[recx][recy]>5:
                x=x-dx
                y=y-dy
                recx=int((x-15)//19)
                recy=int((y-15)//19)
                tab[recx][recy]+=1
            else:
                if (x<bord) and (y<=sortiey1 or y>=sortiey2):
                    dx = 0
                    tab[recx][recy]+=1
                if  y>=(sortiey1) and y<=(sortiey2):
                    dy = 0
                    tab[recx][recy]+=1
                else:
                    recx=int((x-15)//19)
                    recy=int((y-15)//19)
                    tab[recx][recy]+=1
                personnes[p]=[x,y]
            p+=1
        for i in range(len(tab)):
            for j in range(len(tab[0])):
                if tab[i][j]==0:
                    can.itemconfigure(rectangle[i][j], fill='white')
                if tab[i][j]==1:
                    can.itemconfigure(rectangle[i][j], fill='#fdfd96')
                if tab[i][j]==2:
                    can.itemconfigure(rectangle[i][j], fill='#F1BF00')
                if tab[i][j]==3:
                    can.itemconfigure(rectangle[i][j], fill='#D96000')
                if tab[i][j]==4:
                    can.itemconfigure(rectangle[i][j], fill='#ba0000')
                if tab[i][j]==5:
                    can.itemconfigure(rectangle[i][j], fill='#941a1c')
                if tab[i][j]==6:
                    can.itemconfigure(rectangle[i][j], fill='#5e0a0b')
                if tab[i][j]>=7:
                    can.itemconfigure(rectangle[i][j], fill='#0A0018')
        can.itemconfigure(rectangle[29][8],fill='white')
        can.itemconfigure(rectangle[29][9],fill='white')
        time.sleep(0.1)
        fen.update()

###### Variables ######

personnes = []
longueur = 400
largeur = 600
bord = 15
sortiey1 = 145
sortiey2 = 210
sortiex = 0
sortiey = (abs(sortiey1+sortiey2)/2)


###### Demande ######


print("Donnez le nombre de personne : ")
nb_personne=int(input())

###### Fenêtre Tkinter ######

fen = Tk()
fen.title("TIPE Mouvement de foule : modèle macroscopique (Eloïs RENOU 30191)")


can = Canvas(fen,bg='black',height=longueur, width=largeur+100)
can.pack(side=LEFT, padx =5, pady =5)

fond=can.create_rectangle(610,0,700,400,fill='white',outline='white')
rec = can.create_rectangle(630, 25,680, 75,fill='#fdfd96')
rec = can.create_rectangle(630, 75, 680, 125,fill='#F1BF00')
rec = can.create_rectangle(630, 125, 680, 175,fill='#D96000')
rec = can.create_rectangle(630, 175, 680, 225,fill='#ba0000')
rec = can.create_rectangle(630,225,680,275,fill='#941a1c')
rec = can.create_rectangle(630,275,680,325,fill='#5e0a0b')
rec = can.create_rectangle(630,325,680,375,fill='#0A0018')

salle = can.create_rectangle(bord, bord, largeur-bord, longueur-bord,fill='white')
sortie=can.create_rectangle(0,sortiey1,bord,sortiey2,fill='white',outline='white')


grille()

initialisation()


fen.mainloop()

###### Fin ######