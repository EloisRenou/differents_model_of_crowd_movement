###### Bibliothèques ######


from tkinter import Canvas, Tk, Label, BOTTOM, TOP
from math import sqrt
import random
import time


###### Fonctions Auxiliaires ######


def recherche_d_individu(i : int, x : float, y : float, personnes : list) -> list: #list of list (float, float)
    """Recherche les individus dans un rayon de 2.5*rayon autour de la personne i
    Entrées :
        i : int
        x : float
        y : float
        personnes : list
    Sortie :
        temp : list
    """
    temp=[]
    for j in range (len(personnes)):
        x2,y2=personnes[j][1],personnes[j][2]
        if j!=i:
            if sqrt((x2-x)**2+(y2-y)**2)<2.5*rayon:
                temp.append([x2,y2])
    return temp


def liste_des_positions_possibles(x : float, y : float) -> list: #list of list (float, float)
    """Crée une liste de 49 points autour de la personne i
    Entrées :
        x : absisse de la personne i
        y : ordonnée de la personne i
    Sortie :
        liste_point : liste des 63 positions possibles"""
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
        if ((liste_point[j][1]>longueur-bord-rayon) and (liste_point[j][0]>=sortiex1-rayon+12.5 and liste_point[j][0]<=sortiex2+rayon-12.5)):
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


def recherche_meilleur(liste_point : list, x : float, y : float, position_telephone : list) -> tuple: #tuple (float, float)
    """Recherche le meilleur point parmis les positions possibles"""
    """Recherche le meilleur point parmis les positions possibles
    Entrées :
        liste_point : liste de positions possibles
        x : absisse de la personne i
        y : ordonnée de la personne i
        position_telephone : position de l'objet perdu donc si position_telephone est non vide
        on doit aller vers l'objet sinon vers la sortie
    Sortie :
        nextx : absisse de la prochaine position
        nexty : ordonnée de la prochaine position
    """
    distance_mini=100000
    nextx=x
    nexty=y
    for i in range(len(liste_point)):
        testx,testy=liste_point[i][0],liste_point[i][1]
        if position_telephone== []:
            testx,testy=liste_point[i][0],liste_point[i][1]
            distance_sortie=sqrt((testx-sortiex)**2+(testy-sortiey)**2)
            if distance_sortie<distance_mini:
                distance_mini=distance_sortie
                nextx=testx
                nexty=testy
        else:
            distance_telephone=sqrt((testx-position_telephone[0])**2+(testy-position_telephone[1])**2)
            if distance_telephone<distance_mini:
                distance_mini=distance_telephone
                nextx=testx
                nexty=testy
    return(nextx,nexty)


def antibug(a : float, b : float, temp : list) -> tuple: #tuple (float, float)
    """Fonction qui permet de ne pas avoir de bug lorsque la personne est bloquée
    Entrées :
        a : absisse de la personne i
        b : ordonnée de la personne i
        temp : liste des personnes dans un rayon de 2.5*rayon autour de la personne i
    Sortie :
        a : absisse de la prochaine position
        b : ordonnée de la prochaine position"""
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
    """Initialise les personnes et les pompiers
    Entrées :
        None
    Sortie :
        nb_personne : nombre de personne(s) au départ
        personnes : liste des positions et autes des personnes
        antecedent : liste des positions et autres des personnes à l'étape précédente"""
    while len(personnes)<nb_personne:
        compteur=True
        x = random.randint(bord+rayon,largeur-bord-rayon)
        y = random.randint(bord+rayon,270-rayon)
        d=sqrt((sortiex-x)**2+(sortiey- y)**2)
        for i in range(len(personnes)):
            if sqrt((x-personnes[i][1])**2 + (y-personnes[i][2])**2)<2*rayon:
                compteur=False
        if compteur:
            numero_personne = can.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, width=1, fill='red')
            personnes.append([numero_personne,x,y,d,0,-1,[]])
            antecedent.append([x,y,d,0])
    if pompier:
        for i in range(2):
            numero_pompier=can.create_oval(largeur/2,longueur-(2*i-1)*rayon-bord,largeur/2+2*rayon,longueur-(2*i+1)*rayon-bord,width=1,fill='blue')
            d = sqrt((largeur/2-pompierx)**2+(longueur+bord+3*i*rayon-pompiery)**2)
            personnes.append([numero_pompier,largeur/2+rayon,longueur-3*i*rayon-bord,d,3,-1,[pompierx,pompiery]])
            antecedent.append([largeur/2+rayon,longueur-3*i*rayon-bord,d,0])
        for i in range(2):
            numero_pompier=can.create_oval(largeur/2-2*rayon,longueur-(2*i-1)*rayon-bord,largeur/2,longueur-(2*i+1)*rayon-bord,width=1,fill='blue')
            d = sqrt((largeur/2-pompierx)**2+(longueur+bord+3*i*rayon-pompiery)**2)
            personnes.append([numero_pompier,largeur/2-rayon,longueur-3*i*rayon-bord,d,3,-1,[pompierx,pompiery]])
            antecedent.append([largeur/2-rayon,longueur-3*i*rayon-bord,d,0])
    personnes.sort(key=lambda personnes: personnes[3])
    mouvement(nb_personne,personnes,antecedent)


def mouvement(nb_personne : int, personnes : list, antecedent : list) -> None:
    """Fonction qui permet le mouvement des personnes
    Entrées :
        nb_personne : nombre de personne(s) au départ
        personnes : liste des positions et autes des personnes
        antecedent : liste des positions et autres des personnes à l'étape précédente
    Sortie :
        None"""
    timere=0
    temps_debut = time.time()
    if pompier:
            nb_personne+=4
    while True:
        i=0
        temps_calcul_debut=time.time()
        while i<nb_personne:
            numero_personne,x,y,d,etat,wait,position_telephone=personnes[i][0],personnes[i][1],personnes[i][2],personnes[i][3],personnes[i][4],personnes[i][5],personnes[i][6]
            antecedent_etat=antecedent[i][3]
            previous_x=x
            previous_y=y
            if tomber and etat==0:
                proba_tomber=random.randint(0,500)
                if proba_tomber==1:
                    etat=1
            if telephone and etat==0:
                proba_telephone=random.randint(0,1000)
                if proba_telephone==1:
                    etat=2
            if etat==0:
                temp=recherche_d_individu(i,x,y,personnes)
                liste_point=liste_des_positions_possibles(x,y)
                liste_point=detection_des_positions_possibles(liste_point,temp)
                x,y=recherche_meilleur(liste_point,x,y,position_telephone)
                if antecedent[i][0]==x and antecedent[i][1]==y and antecedent_etat==10:
                    x,y=antibug(x,y,temp)
                    antecedent_etat=0
                if antecedent[i][0]==x and antecedent[i][1]==y and antecedent_etat<10:
                    antecedent_etat+=1
                else:
                    antecedent_etat=0
            if etat ==1:
                if wait==-1:
                   can.itemconfigure(numero_personne,fill='black')
                   wait=50
                if wait==0:
                    etat=0
                    can.itemconfigure(numero_personne,fill='red')
                    wait=-1
                else:
                    wait-=1
            if etat==2:
                if wait==-1:
                    can.itemconfigure(numero_personne,fill='green')
                    waitx=random.randint(bord+rayon,largeur-bord-rayon)
                    waity = random.randint(bord+rayon,270-rayon)
                    position_telephone = [waitx,waity]
                    wait=0
                if wait==0 and sqrt((x-position_telephone[0])**2+(y-position_telephone[1])**2)<=rayon:
                    etat=0
                    can.itemconfigure(numero_personne,fill='red')
                    wait=-1
                    position_telephone=[]
                else:
                    temp=recherche_d_individu(i,x,y,personnes)
                    liste_point=liste_des_positions_possibles(x,y)
                    liste_point=detection_des_positions_possibles(liste_point,temp)
                    x,y=recherche_meilleur(liste_point,x,y,position_telephone)
            if etat==3:
                if wait==0 and sqrt((x-position_telephone[0])**2+(y-position_telephone[1])**2)<=rayon:
                    etat=0
                    can.itemconfigure(numero_personne,fill='red')
                    wait=-1
                    position_telephone=[]
                else:
                    position_telephone=[pompierx,pompiery]
                    temp=recherche_d_individu(i,x,y,personnes)
                    liste_point=liste_des_positions_possibles(x,y)
                    liste_point=detection_des_positions_possibles(liste_point,temp)
                    x,y=recherche_meilleur(liste_point,x,y,position_telephone)
            if ((y>longueur-bord-rayon) and (x<=sortiex1+rayon-12.5 or x>=sortiex2-rayon+12.5)):
                x=previous_x
                y=previous_y
            can.coords(numero_personne, x-rayon, y-rayon, x+rayon, y+rayon)
            if y>(longueur-2) and etat!=3:
                can.delete(numero_personne)
                personnes.pop(i)
                nb_personne -= 1
                if nb_personne == 0 :
                    temps_fin=time.time()
                    temps=temps_fin-temps_debut
                    print("Voici le temps d'évacuation : ", temps)
            else:
                d=(sqrt((sortiex-x)**2+(sortiey- y)**2))
                antecedent[i][2]=0
                personnes[i]=[numero_personne,x,y,d,etat,wait,position_telephone]
                antecedent[i]=[x,y,d,antecedent_etat]
            personnes.sort(key=lambda personnes: personnes[3])
            antecedent.sort(key=lambda personnes: personnes[2])
            i+=1
        temps_calcul_fin=time.time()
        temps_calcul=temps_calcul_fin-temps_calcul_debut
        time.sleep(0.5-temps_calcul)
        can.timer.config(text='%s'%nb_personne)
        fen.update()


###### Variables ######


personnes = []
antecedent=[]
pompiers=[]


longueur = 400
largeur = 600
rayon = 15
bord = 15
sortiex1 = 267.5
sortiex2 = 332.5
sortiex = (abs(sortiex1+sortiex2)/2)
sortiey = longueur


###### Demandes  ######
print("Personne qui tombe? 0 Non 1 oui ")
temp_tomber=int(input())
if temp_tomber==1:
    tomber=True
else:
    tomber=False


print("Personne qui oublie son telephone? 0 Non 1 oui ")
temp_telephone=int(input())
if temp_telephone==1:
    telephone=True
else:
    telephone=False


print("Voulez-vous des pompiers? 0 Non 1 oui ")
temp_pompier=int(input())
if temp_pompier==1:
    pompier=True
    pompierx=random.randint(bord+rayon,largeur-bord-rayon)
    pompiery=random.randint(bord+rayon,220-rayon)
else:
    pompier=False


print("Donnez le nombre de personne : ")
nb_personne=int(input())


###### Fenêtre Tkinter ######


fen = Tk()
fen.title("TIPE Mouvement De Foule (Eloïs RENOU 30191)")


can = Canvas(fen,bg='black',height=longueur+25, width=largeur)
can.pack(side=TOP, padx =5, pady =5)


salle = can.create_rectangle(bord, bord, largeur-bord, longueur-bord,fill='white')
sortie=can.create_rectangle(267.5-7.5,longueur-bord,332.5+7.5,longueur+27,fill='white',width=0)




Label(fen,text=" ", fg='black').pack()
can.timer=Label(fen,text='0',fg='black')
Label(fen,text="Nombre de personne(s) restantes",fg='black').pack()
can.timer.pack()
Label(fen,text='', fg='white').pack(side=BOTTOM)
initialisation()


fen.mainloop()


###### Fin ######