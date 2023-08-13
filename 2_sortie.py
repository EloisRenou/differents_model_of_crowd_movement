###### Bibliothèques ######


from tkinter import Canvas, Tk, Label, BOTTOM, TOP
from math import sqrt
import random
import time


###### Fonctions Auxiliaires ######


def recherche_d_individu(i : int, x : float, y: float, personnes : list) -> list: #list of list (float, float)
    """Renvoie la liste des personnes autour de la personne i dans un rayon de 2.5*rayon
    Entrée :
        i : numero de la personne
        x : absice de la personne
        y : ordonnée de la personne
        personnes : liste des personnes
    Sortie :
        temp : liste des personnes autour de la personne i"""
    temp=[]
    for j in range (len(personnes)):
        x2,y2=personnes[j][1],personnes[j][2]
        if j!=i:
            if sqrt((x2-x)**2+(y2-y)**2)<2.5*rayon:
                temp.append([x2,y2])
    return temp


def liste_des_positions_possibles(x : float, y : float) -> list: #list of list (float, float)
    """Renvoie la liste des positions possibles autour de la personne i
    Entrée :
        x : absice de la personne
        y : ordonnée de la personne
    Sortie :
        liste_point : liste des positions possibles autour de la personne i"""
    rr=sqrt(0.7**2+0.7**2)
    liste_point=[]
    for j in range(-1,6):
        for p in range(-5,6):
            liste_point.append([x+p*(rr/7),y+(j*rr/7)])
    return(liste_point)


def detection_des_positions_possibles(liste_point : list, temp : list) -> list: #list of list (float, float)
    """Renvoie la liste des positions possibles autour de la personne i sans celle proche des murs ou proche des personnes
    Entrée :
        liste_point : liste des positions possibles autour de la personne i
        temp : liste des personnes autour de la personne i
    Sortie :
        liste_point : liste des positions possibles autour de la personne i sans celle proche des murs ou proche des personnes"""
    j=0
    while 0<=j<len(liste_point):
        if ((liste_point[j][1]>longueur-bord-rayon) and (liste_point[j][0]>=sortiex12-rayon+12.5 and liste_point[j][0]<=sortiex21+rayon-12.5)):
            liste_point.pop(j)
            j-=1
        elif liste_point[j][0]>largeur-bord-rayon or liste_point[j][0]<bord+rayon:
            liste_point.pop(j)
            j-=1
        else:
            for p,(x2,y2)in zip(range(0,len(temp)),temp):
                if sqrt((x2-liste_point[j][0])**2+(y2-liste_point[j][1])**2)<=2*rayon:
                    liste_point.pop(j)
                    j-=1
                    break
        j+=1
    return(liste_point)


def recherche_meilleur(liste_point : list, x : float, y : float) -> tuple: #tuple(float, float)
    """Renvoie le meilleur point parmi les positions possibles autour de la personne i
    Entrée :
        liste_point : liste des positions possibles et atteignables autour de la personne i
        x : absice de la personne
        y : ordonnée de la personne
    Sortie :
        nextx : absice du meilleur point
        nexty : ordonnée du meilleur point"""
    distance_mini=100000
    nextx=x
    nexty=y
    for i in range(len(liste_point)):
        testx,testy=liste_point[i][0],liste_point[i][1]
        distance_sortie1=sqrt((testx-sortiex1)**2+(testy-sortiey)**2)
        distance_sortie2=sqrt((testx-sortiex2)**2+(testy-sortiey)**2)
        distance_sortie=min(distance_sortie1,distance_sortie2)
        if distance_sortie<distance_mini:
            distance_mini=distance_sortie
            nextx=testx
            nexty=testy
    return(nextx,nexty)


def antibug(a : float, b : float, temp : list) -> tuple: #tuple(float,float)
    """fait s'éloigner la personne i de la personne la plus proche pour décoincer les personnes
    Entrée :
        a : absice de la personne
        b : ordonnée de la personne
        temp : liste des personnes autour de la personne i
    Sortie :
        a : absice de la personne
        b : ordonnée de la personne"""
    distance_mini=100000
    prochex=temp[0][0]
    prochey=temp[0][1]
    for i in range (len(temp)):
        x2,y2=temp[i][0],temp[i][1]
        distance=sqrt((x2-a)**2+(y2-b)**2)
        if distance<distance_mini:
            distance_mini=distance
            prochex=x2
            prochey=y2
    if prochex>a:
        m=(prochey-b)/(prochex-a)
        c=b-m*a
        if ((m*(a-1)+c>longueur-bord-rayon) and (a-1<=sortiex1+rayon-5 or a-1>=sortiex2-rayon+5)):
            return(a,b)
        else:
            if (m*(a-1)+c-b)**2<=2:
                return(a-1,m*(a-1)+c)
            else:
                if prochey>b:
                    return((b-1-c)/m,b-1)
                else:
                    return((b+1-c)/m,b+1)
    else:
        m=(b-prochey)/(a-prochex)
        c=b-m*a
        if ((m*(a+1)+c>longueur-bord-rayon) and (a+1<=sortiex1+rayon-5 or a+1>=sortiex2-rayon+5)):
            return(a,b)
        else:
            if (m*(a+1)+c-b)**2<=2:
                return(a+1,m*(a+1)+c)
            else:
                if prochey>b:
                    return((b-1-c)/m,b-1)
                else:
                    return((b+1-c)/m,b+1)


###### Fonctions Principales ######


def initialisation() -> None:
    """Initialise les personnes dans la salle et renvoie une liste de coordonnées des personnes et la liste des coordonnées précédentes
    Entrée :
        None
    Sortie :
        None"""
    while len(personnes)<nb_personne:
        compteur=True
        x = random.randint(bord+rayon,largeur-bord-rayon)
        y = random.randint(bord+rayon,270-rayon)
        d1=sqrt((sortiex1-x)**2+(sortiey- y)**2)
        d2=sqrt((sortiex2-x)**2+(sortiey- y)**2)
        d=min(d1,d2)
        for i in range(len(personnes)):
            if sqrt((x-personnes[i][1])**2 + (y-personnes[i][2])**2)<2*rayon:
                compteur=False
        if compteur :
            numero_personne = can.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, width=1, fill='red')
            personnes.append([numero_personne,x,y,d,0,-1])
            antecedent.append([x,y,d,0])
    personnes.sort(key=lambda personnes: personnes[3])
    movement(nb_personne,personnes,antecedent)


def movement(nb_personne : int, personnes : list,antecedent : list) -> None:
    """Fait bouger les personnes dans la salle
    Entrée :
        nb_personne : nombre de personne
        personnes : liste des personnes
        antecedent : liste des coordonnées précédentes
    Sortie :
        None"""
    temps_debut = time.time()
    while True:
        i=0
        temps_calcul_debut=time.time()
        while i<nb_personne:
            numero_personne,x,y,d,etat,wait=personnes[i][0],personnes[i][1],personnes[i][2],personnes[i][3],personnes[i][4],personnes[i][5]
            antecedent_etat=antecedent[i][3]
            previous_x=x
            previous_y=y
            temp=recherche_d_individu(i,x,y,personnes)
            liste_point=liste_des_positions_possibles(x,y)
            liste_point=detection_des_positions_possibles(liste_point,temp)
            x,y=recherche_meilleur(liste_point,x,y)
            if antecedent[i][0]==x and antecedent[i][1]==y and antecedent_etat==10: #anitbug
                if len(temp)!=0:
                    x,y=antibug(x,y,temp)
                antecedent_etat=-20
            if antecedent[i][0]==x and antecedent[i][1]==y and antecedent_etat<10: #anitbug
                antecedent_etat+=1
            else:
                antecedent_etat=0
            if((y>longueur-bord-rayon) and (x>=sortiex12-rayon+12.5 and x<=sortiex21+rayon-12.5)):
                x=previous_x
                y=previous_y
            if x>largeur-bord-rayon or x<bord+rayon:
                x=previous_x
                y=previous_y
            can.coords(numero_personne, x-rayon, y-rayon, x+rayon, y+rayon)
            if y>(longueur-2):
                can.delete(numero_personne)
                personnes.pop(i)
                nb_personne -= 1
                if nb_personne == 0 :
                    temps_fin=time.time()
                    temps=temps_fin-temps_debut
                    print(temps)
            else:
                d1=sqrt((sortiex1-x)**2+(sortiey- y)**2)
                d2=sqrt((sortiex2-x)**2+(sortiey- y)**2)
                d=min(d1,d2)
                antecedent[i][2]=0
                personnes[i]=[numero_personne,x,y,d,etat,wait]
                antecedent[i]=[x,y,d,antecedent_etat]
            personnes.sort(key=lambda personnes: personnes[3])
            antecedent.sort(key=lambda personnes: personnes[2])
            i+=1
        temps_calcul_fin=time.time()
        temps_calcul=temps_calcul_fin-temps_calcul_debut
        time.sleep(0.5-temps_calcul)
        fen.update()


###### Variables ######


personnes = []
antecedent=[]


longueur = 400
largeur = 600
rayon = 15
bord = 15
sortiex11 = bord+40
sortiex12 = bord+80
sortiex1 = (abs(sortiex11+sortiex12)/2)
sortiex21 = largeur-bord-80
sortiex22 = largeur-bord
sortiex2 = (abs(sortiex21+sortiex22)/2)
sortiey = longueur

###### demande a enlever ######


print("Donnez le nombre de personne : ")
nb_personne=int(input())


###### Fenêtre Tkinter ######


fen = Tk()
fen.title("TIPE Mouvement De Foule : 2 sorties (Eloïs RENOU 30191)")


can = Canvas(fen,bg='black',height=longueur+25, width=largeur)
can.pack(side=TOP, padx =5, pady =5)



salle = can.create_rectangle(bord, bord, largeur-bord, longueur-bord,fill='white')
sortie1=can.create_rectangle(bord+1,longueur-bord,bord+80,longueur+27,fill='white',width=0)
sortie2=can.create_rectangle(largeur-bord-80,longueur-bord,largeur-bord,longueur+27,fill='white',width=0)


Label(fen,text=' ', fg='white').pack()
Label(fen,text="Temps :", fg='black').pack()
can.timer=Label(fen,text='0',fg='black')
Label(fen,text="Nombre de personne(s) restantes",fg='black').pack()


can.timer.pack()
Label(fen,text='', fg='white').pack(side=BOTTOM)
initialisation()


fen.mainloop()


###### Fin ######