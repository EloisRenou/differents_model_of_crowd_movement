###### Bibliothèques ######


from tkinter import Canvas, Tk, Label, BOTTOM, TOP
from math import sqrt
import random
import time


###### Fonctions Auxiliaires ######


def recherche_d_individu(i : int, x : float, y : float, personnes : list ) -> list:
    """Fonction qui permet de rechercher les individus proches
    entrée :
        i : numéro de la personne
        x : abscisse de la personne
        y : ordonnée de la personne
        personnes : liste des personnes
    sortie :
        temp : liste des positions des personnes proches"""
    temp=[]
    for j in range (len(personnes)):
        x2,y2=personnes[j][1],personnes[j][2]
        if j!=i:
            if sqrt((x2-x)**2+(y2-y)**2)<2.5*rayon:
                temp.append([x2,y2])
    return temp


def liste_des_positions_possibles(x : float,y : float) -> list:
    """Fonction qui permet de donner la listes des positions possibles (les 63 positions) autour de la personne
    entrée:
        x : abscisse de la personne
        y : ordonnée de la personne
    sortie:
        liste_point : liste des positions possibles"""
    rr=sqrt(0.7**2+0.7**2)
    liste_point=[]
    for j in range(-1,6):
        for p in range(-5,6):
            liste_point.append([x+p*(rr/7),y+(j*rr/7)])
    return(liste_point)


def detection_des_positions_possibles(liste_point : list, temp : list) -> list :
    """Fonction qui permet d'enlever les positions impossibles
    (les positions qui sont dans les murs ou dans les autres personnes)
    entrées :
        liste_point : liste des positions possibles
        temp : liste des positions des personnes proches
    sortie :
        liste_point : liste des positions possibles"""
    j=0
    while 0<=j<len(liste_point):
        if ((liste_point[j][1]>longueur-bord-rayon) and (liste_point[j][0]<=sortiex1+rayon-12.5 or liste_point[j][0]>=sortiex2-rayon+12.5)):
            liste_point.pop(j)
            j-=1
        else:
            p=0
            while p<len(temp):
                x2,y2=temp[p][0],temp[p][1]
                if sqrt((x2-liste_point[j][0])**2+(y2-liste_point[j][1])**2)<=2*rayon:
                    liste_point.pop(j)
                    j-=1
                    break
                p+=1
            j+=1
    return(liste_point)


def recherche_meilleur(liste_point : list, x : float, y : float, i : int) -> tuple : #tuple(float, float)
    """Fonction qui permet de rechercher la meilleure position possible
    entrées :
        liste_point : liste des positions possibles
        x : abscisse de la personne
        y : ordonnée de la personne
        i : numéro de la personne
    sortie :
        nextx : abscisse de la personne
        nexty : ordonnée de la personne"""
    distance_mini=100000
    nextx=x
    nexty=y
    for i in range(len(liste_point)):
        testx,testy=liste_point[i][0],liste_point[i][1]
        if y<=obstacle_bas : #toujours vrai
            if x<=largeur/2:
                distance_sortie=sqrt((obstacle_coin_gauche-rayon-testx)**2+(10000-testy)**2)
                if distance_sortie<distance_mini:
                    distance_mini=distance_sortie
                    nextx=testx
                    nexty=testy
            else:
                distance_sortie=sqrt((obstacle_coin_droit+rayon-testx)**2+(10000-testy)**2)
                if distance_sortie<distance_mini:
                    distance_mini=distance_sortie
                    nextx=testx
                    nexty=testy
        else:
            if x<=largeur/2:
                distance_sortie=sqrt((testx-sortiex2)**2+(testy-sortiey)**2)
                if distance_sortie<=distance_mini: #n'est jamais vrai
                    distance_mini=distance_sortie
                    nextx=testx
                    nexty=testy
            else:
                distance_sortie=sqrt((testx-sortiex1)**2+(testy-sortiey)**2)
                if distance_sortie<=distance_mini:
                    distance_mini=distance_sortie
                    nextx=testx
                    nexty=testy
    return(nextx,nexty)


def antibug(a : float, b:float ,temp : list) -> tuple: #tuple(float, float)
    """Fonction qui permet d'éviter les bloquages
    entrées:
        a : abscisse de la personne
        b : ordonnée de la personne
        temp : liste des positions des personnes proches
    sortie:
        a : abscisse de la personne
        b : ordonnée de la personne
        """
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


def initialisation():
    """Fonction qui permet de créer les personnes sur le canvas
    entrées :
        None
    sortie :
        nb_personne : nombre de personnes
        personnes : liste des personnes
        antecedent : liste des antecedents des personnes
    """
    while len(personnes)<nb_personne+97:
        compteur=True
        x = random.randint(bord+rayon,largeur-bord-rayon)
        y = random.randint(bord+rayon,270-rayon)
        d=sqrt((sortiex-x)**2+(sortiey- y)**2)
        for i in range(len(personnes)):
            if sqrt((x-personnes[i][1])**2 + (y-personnes[i][2])**2)<2*rayon:
                compteur=False
        if compteur:
            numero_personne = can.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, width=1, fill='red')
            personnes.append([numero_personne,x,y,d,0])
            antecedent.append([x,y,d,0])
    personnes.sort(key=lambda personnes: personnes[3])
    mouvement(nb_personne+97,personnes,antecedent)


def mouvement(nb_personne : list , personnes : int, antecedent: list) -> None:
    """Fonction qui permet de faire bouger les personnes
    entrées :
        nb_personne : nombre de personnes
        personnes : liste des personnes
        antecedent : liste des antecedents des personnes
    sortie :
        None"""
    temps_debut = time.time()
    while True:
        i=0
        temps_calcul_debut=time.time()
        while i<nb_personne:
            numero_personne,x,y,d,etat=personnes[i][0],personnes[i][1],personnes[i][2],personnes[i][3],personnes[i][4]
            antecedent_etat=antecedent[i][3]
            previous_x=x
            previous_y=y
            temp=recherche_d_individu(i,x,y,personnes)
            if etat==0: #etat=0 : la personne est en mouvement, etat=1 : la personne fait partie de l'obstacle elle ne doit donc pas bouger
                liste_point=liste_des_positions_possibles(x,y)
                liste_point=detection_des_positions_possibles(liste_point,temp)
                x,y=recherche_meilleur(liste_point,x,y,i)
                if antecedent[i][0]==x and antecedent[i][1]==y and antecedent_etat==5:
                    x,y=antibug(x,y,temp)
                    antecedent_etat=0
                if antecedent[i][0]==x and antecedent[i][1]==y and antecedent_etat<10:
                    antecedent_etat+=1
                else:
                    antecedent_etat=0
            if ((y>longueur-bord-rayon) and (x<=sortiex1+rayon-12.5 or x>=sortiex2-rayon+12.5)):
                x=previous_x
                y= previous_y
                if x>largeur/2:
                    x=previous_x-0.05
                else:
                    x=previous_x+0.05
            can.coords(numero_personne, x-rayon, y-rayon, x+rayon, y+rayon)
            if y>(longueur-2):
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
                personnes[i]=[numero_personne,x,y,d,etat]
                antecedent[i]=[x,y,d,antecedent_etat]
            personnes.sort(key=lambda personnes: personnes[3])
            antecedent.sort(key=lambda personnes: personnes[2])
            i+=1
        temps_calcul_fin=time.time()
        temps_calcul=temps_calcul_fin-temps_calcul_debut
        time.sleep(0.5-temps_calcul)
        can.timer.config(text='%s'%(nb_personne-97))
        fen.update()


###### Variables ######


personnes = []
antecedent=[]

longueur = 400
largeur = 600
rayon = 15
bord = 15
sortiex1 = 267.5
sortiex2 = 332.5
sortiex = (abs(sortiex1+sortiex2)/2)
sortiey = longueur
obstacle_bas=330
obstacle_coin_gauche=235
obstacle_coin_droit=365

###### Demandes  ######


print("Donnez le nombre de personne : ")
nb_personne=int(input())


###### Fenêtre Tkinter ######


fen = Tk()
fen.title("TIPE Mouvement De Foule : obstacle (Eloïs RENOU 30191)")


can = Canvas(fen,bg='black',height=longueur+25, width=largeur)
can.pack(side=TOP, padx =5, pady =5)


salle = can.create_rectangle(bord, bord, largeur-bord, longueur-bord,fill='white')
sortie=can.create_rectangle(267.5-7.5,longueur-bord,332.5+7.5,longueur+27,fill='white',width=0)
for i in range(97):
    x=252+i
    y1=sqrt(50**2-(x-largeur/2)**2)+280
    y2=-sqrt(50**2-(x-largeur/2)**2)+325
    #obstacle=can.create_oval(x-rayon+5,y1-rayon+5,x+rayon-5,y1+rayon-5,fill='black')
    #personnes.append([obstacle,x,y1,0,1,0,[]])
    #antecedent.append([x,y1,0,0])
    obstacle2=can.create_oval(x-rayon+5,y2-rayon+5,x+rayon-5,y2+rayon-5,fill='black')
    personnes.append([obstacle2,x,y2,0,1,0,[]])
    antecedent.append([x,y2,0,0])



Label(fen,text=" ", fg='black').pack()
can.timer=Label(fen,text='0',fg='black')
Label(fen,text="Nombre de personne(s) restantes",fg='black').pack()
can.timer.pack()
Label(fen,text='', fg='white').pack(side=BOTTOM)
initialisation()


fen.mainloop()


###### Fin ######