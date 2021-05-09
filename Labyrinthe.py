# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 14:10:42 2016

@author: Quentin

La croix est active
"""

#Importation des bibliothèques nécessaires
import pygame
from pygame.locals import *
from random import choice
from random import randint
import random
import math
import time

#Initialisation de la bibliothèque Pygame
pygame.init()

CODAGEenCOURS=1

print("Le programme est lancé")

#                                       ***Création de la Grille de jeux***
offsetDroite=180
offsetHaut=60
NbLigneGrille=10
NbColonneGrille=10
grille=[1]*NbLigneGrille*NbColonneGrille

#                                       ***Création du terrain ***

# *-* Niveau 1 : grand Carré

i=1
while i<NbColonneGrille-1:
    j=1
    while j<NbLigneGrille-1:
        case=i+j*NbColonneGrille
        grille[case]=2
        j+=1
    i+=1

grille[1+1*NbColonneGrille]=0 #Plateforme Départ
grille[NbLigneGrille-2 + (NbLigneGrille-2)*NbColonneGrille]=6 #Plateforme Fin

# *-* Niveau 2 : large diagonale
"""
i=1
limite=NbColonneGrille*NbLigneGrille-1
while i<min(NbColonneGrille,NbLigneGrille)-1: #Plateforme classique
    case=i+i*NbColonneGrille
    grille[case]=2
    if case+NbLigneGrille<limite-1 :
        grille[case+NbLigneGrille]=2
    if case+1<limite-NbColonneGrille :
        grille[case+1]=2
    i+=1
grille[1+1*NbColonneGrille]=0 #Plateforme Départ
grille[NbLigneGrille-2 + (NbLigneGrille-2)*NbColonneGrille]=6 #Plateforme Fin
"""
# *-* Niveau 3 : Troll dead end
"""
i=1
while i<NbColonneGrille-1:
    case=i+1*NbColonneGrille
    grille[case]=2
    i+=1
i=1
while i<NbColonneGrille-1:
    case=1+i*NbColonneGrille
    grille[case]=2
    i+=1

grille[1+1*NbColonneGrille]=0 #Plateforme Départ
grille[NbLigneGrille-2 + (NbLigneGrille-2)*NbColonneGrille]=6 #Plateforme Fin
"""
# *-* Niveau 4 : L
"""
i=1
while i<NbColonneGrille-1:
    case=i+1*NbColonneGrille
    grille[case]=2
    i+=1
i=1
while i<NbColonneGrille-1:
    case=NbLigneGrille-2+i*NbColonneGrille
    grille[case]=2
    i+=1
    
grille[1+1*NbColonneGrille]=0 #Plateforme Départ
grille[NbLigneGrille-2 + (NbLigneGrille-2)*NbColonneGrille]=6 #Plateforme Fin
"""
# *-* Niveau 5 : plateforme et pont

# *-* Niveau 6 : ZigZag



#Variable de TEMPS du Jeu
tempsPause=0.3 #temps du tic du jeu
tempsJeu=NbLigneGrille*NbColonneGrille
print "tempsJeu = ", tempsJeu
tempsVictoire=tempsJeu
compteurTempsJeu=0

#                                       ***Création de l' IA ***
nbInput=4 #6 avec cst
nbNeuroneParCouche=3
nbCouche=3
nbOutput=4
nbIA=5 # DarwinMode
pourcentCoeffModif=10 # en %
generation=0

TabCoucheIn=[0]*nbInput*nbNeuroneParCouche
TabCoucheN=[0]*nbInput*(nbCouche-1)*nbNeuroneParCouche
TabCoucheOut=[0]*nbNeuroneParCouche*nbOutput
TabBufferNeurone=[0]*nbNeuroneParCouche
TabOutput=[0]*nbOutput

tailleIA=nbInput*nbNeuroneParCouche+nbInput*(nbCouche-1)*nbNeuroneParCouche+nbNeuroneParCouche*nbOutput
nbCoeffModif=tailleIA*pourcentCoeffModif*100
IA=[0]*tailleIA*nbIA
bufferMeilleurIA=[0]*tailleIA
i=0
while i<nbIA: #parcour les IA
    j=0
    while j<tailleIA: #parcour les coéficients d'une IA
        IA[i*tailleIA+j]=(random.randint(0,100)-50)/50
        j+=1
    i+=1

IASelect=0
ScoreIA=[0]*nbIA

debut=IASelect*tailleIA
i=0
while i<nbInput*nbNeuroneParCouche:
    TabCoucheIn[i]=IA[i+debut]
    i+=1
debut=nbInput*nbNeuroneParCouche+IASelect*tailleIA
i=0
while i<nbInput*(nbCouche-1)*nbNeuroneParCouche:
    TabCoucheN[i]=IA[i+debut]
    i+=1
debut=nbInput*nbNeuroneParCouche+nbInput*(nbCouche-1)*nbNeuroneParCouche+IASelect*tailleIA
i=0
while i<nbNeuroneParCouche*nbOutput:
    TabCoucheOut[i]=IA[i+debut]
    i+=1
    
print "génération : ",generation
print "   IA : ",IASelect

#                                       *** FIN Création de l' IA ***

tailleEcran=600 #nombre de pixel de la hauteur et largeur de la fenetre
fenetre = pygame.display.set_mode([ tailleEcran
    , tailleEcran])

carrePlateforme = pygame.image.load("CarrePlateforme.png").convert() #image de 30 pixels de côté
carreVide = pygame.image.load("CarreVide.png").convert()
carreStart = pygame.image.load("CarrePlateformeStart.png").convert()
carreFin = pygame.image.load("CarrePlateformeFin.png").convert()
tailleCase=30

carrePion = pygame.image.load("CarrePion.png").convert()
taillePion=10


fond = pygame.image.load("fondNoir.jpg").convert() #de la taille de tailleEcran
carreNoir=pygame.image.load("carreNoir.jpg").convert()

positionPion=[1,1]# sur la grille
positionPrecedentePion=[1,1]#sur la grille aussi
position=[tailleEcran/2,tailleEcran/2] #position[0] et position[1] en pixel

direction=8
direction2=8

continuer=1
ecran=0
tempsAv= time.localtime()
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer=0
    if ecran==0 : #Initialisation
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer=0
                pygame.quit()
            """if event.type==KEYDOWN and (event.key==K_BACKSPACE or event.key==K_KP_ENTER) or CODAGEenCOURS==1 :
            """ #préparation de l'écran de jeu
                #print("vous avez tappé sur entrée")
        ecran=1
        gameOver=0
        positionPion[0]=1
        positionPion[1]=1
        positionPrecedentePion[0]=1
        positionPrecedentePion[1]=1
        
        # *+* Début Affichage du terrain
        i=0
        while i<NbColonneGrille :
            j=0
            while j<NbLigneGrille:
                if grille[i+j*NbColonneGrille]==1: # Vide
                     fenetre.blit(carreVide,[j*30+offsetDroite,i*30+offsetHaut])
                if grille[i+j*NbColonneGrille]==2: # Plateforme
                    fenetre.blit(carrePlateforme,[j*30+offsetDroite,i*30+offsetHaut])
                if grille[i+j*NbColonneGrille]==0: # Départ
                    fenetre.blit(carreStart,[j*30+offsetDroite,i*30+offsetHaut])
                if grille[i+j*NbColonneGrille]==6: # Arrivé
                    fenetre.blit(carreFin,[j*30+offsetDroite,i*30+offsetHaut])
                if positionPion[0]==i and positionPion[1]==j:
                    fenetre.blit(carrePion,[j*30+10+offsetDroite,i*30+10+offsetHaut])
                j+=1
            i+=1
        pygame.display.flip()
        # *+* Fin Affichage du terrain
        direction = 0
        compteurTempsJeu=0
                
    
    if ecran==1:#si écran play
        #*** Attente
        #time.sleep(tempsPause)
        compteurTempsJeu+=1
        #print compteurTempsJeu
        #*** Efface pion
        positionPrecedentePion[0]=positionPion[0]
        positionPrecedentePion[1]=positionPion[1]
        i=positionPion[0]
        j=positionPion[1]
        if grille[i+j*NbColonneGrille]==1: # Vide
            fenetre.blit(carreVide,[j*30+offsetDroite,i*30+offsetHaut])
        if grille[i+j*NbColonneGrille]==2: # Plateforme
            fenetre.blit(carrePlateforme,[j*30+offsetDroite,i*30+offsetHaut])
        if grille[i+j*NbColonneGrille]==0: # Départ
            fenetre.blit(carreStart,[j*30+offsetDroite,i*30+offsetHaut])
        if grille[i+j*NbColonneGrille]==6: # Arrivé
            fenetre.blit(carreFin,[j*30+offsetDroite,i*30+offsetHaut])
                
        #*** Réflexion IA

        #Début Pour test graphique
        #direction=direction%10+2
        """if direction==6:
            direction=2
        elif direction==2:
            direction=6
        elif direction==0:
            direction=2"""
        #Fin Pour un test graphique

        #*- Input - Vision
        haut=   grille[positionPion[0]+positionPion[1]*NbColonneGrille-1]%2
        bas=    grille[positionPion[0]+positionPion[1]*NbColonneGrille+1]%2
        droite= grille[positionPion[0]+positionPion[1]*NbColonneGrille+NbColonneGrille]%2
        gauche= grille[positionPion[0]+positionPion[1]*NbColonneGrille-NbColonneGrille]%2
        #print positionPion[0],positionPion[1]
        #print "haut=",haut," bas=", bas, " droite=", droite," gauche=", gauche
        #*- Input - Constante
        constante1=0
        constante0=1
        #*- Input - Synthese
        TabInput=[haut,bas,droite,gauche,constante0,constante1]
        #*- Traitement
        #$ Couche 1

        #Parcour le tableau TabCoucheIn et TabInput pour remplire TabBuffer
        i=0
        while i<nbNeuroneParCouche: #parcour les neurones de la couche suivante
            j=0
            somme=0
            while j<nbInput: #parcour les coefficients (=nb de neurone précédent)
                somme+=TabCoucheIn[i*nbInput+j]*TabInput[j]
                j+=1
            TabBufferNeurone[i]=-1+2/(1+math.exp(somme))
            i+=1
            
        #$ Couche 1 < N <= nbCouche-1
            
        #Parcour le tableau TabCoucheN pour remplire TabBuffer
        k=0
        while k<nbCouche-1: #parcour les couches
            i=0
            while i<nbNeuroneParCouche: #parcour les neurones de la couche suivante
                j=0
                somme=0
                while j<nbNeuroneParCouche: #parcour les coefficients (=nb de neurone précédent)
                    somme+=TabCoucheN[i*nbNeuroneParCouche+j+k*(nbCouche-1)*nbNeuroneParCouche]*TabBufferNeurone[j]
                    j+=1
                TabBufferNeurone[i]=-1+2/(1+math.exp(somme))
                i+=1
            k+=1

        #$ Dernière Couche 
        
        #Parcour le tableau TabCoucheOut pour remplire TabOutput
        i=0
        while i<nbOutput: #parcour les neurones de la couche suivante
            j=0
            somme=0
            while j<nbNeuroneParCouche: #parcour les coefficients (=nb de neurone précédent)
                somme+=TabCoucheOut[i*nbNeuroneParCouche+j]*TabBufferNeurone[j]
                j+=1
            TabOutput[i]=-1+2/(1+math.exp(somme))
            i+=1
            
        #*- Output
        #recherche du max de TabOutput[]
        somme=TabOutput[0]+TabOutput[1]+TabOutput[2]+TabOutput[3]
        outMax=0
        i=1
        while i<nbOutput:
            if TabOutput[outMax]<TabOutput[i]:
                outMax=i
            i+=1

        if outMax==0:
            direction=2
        elif outMax==1:
            direction=4
        elif outMax==2:
            direction=6
        elif outMax==3:
            direction=8
        else:
            direction=0

        #*** Fin réflexion IA
            
        #*** Déplacement
        if direction==8:
            positionPion[1]-=1
            print "gauche"
            time.sleep(tempsPause)
        elif direction==2:
            positionPion[1]+=1
            print "droite"
            time.sleep(tempsPause)
        elif direction==4:
            positionPion[0]-=1
            print "haut"
            time.sleep(tempsPause)
        elif direction==6:
            positionPion[0]+=1
            print "bas"
            time.sleep(tempsPause)
        
        # *+* Début Affichage du Pion
        i=positionPion[0]
        j=positionPion[1]
        fenetre.blit(carrePion,[j*30+10+offsetDroite,i*30+10+offsetHaut])
        pygame.display.flip()
        # *+* Fin Affichage du Pion
        
        #Annalyse Game Over et Victoire
        if grille[positionPion[0]+positionPion[1]*NbColonneGrille]==1: #Vide
            gameOver=1
            ecran=2
        if compteurTempsJeu==tempsJeu: #Temps écoulé
            gameOver=2
            ecran=2
        if grille[positionPion[0]+positionPion[1]*NbColonneGrille]==6: #annalyse Victoire
            gameOver=-1
            ecran=2
        
        
    if ecran==2:#si écran Game Over
        #Calcul du score
        score=positionPrecedentePion[0]+positionPrecedentePion[1]
        if gameOver==-1:
            score+=(tempsJeu-compteurTempsJeu)
            print "IA arrivé"
            time.sleep(1)
        elif gameOver==1: #vide
            score-=5
        
        print "Score",score
        #Traitement IA
        ScoreIA[IASelect]=score

        
        if IASelect==nbIA-1: #si fin du round
            generation+=1
            print "génération : ",generation
            IASelect=0
            #Recalcule IA
            #copie de la meiller IA
            numMeilleurIA=0
            i=1
            while i<nbIA: #parcour les scores des IA
                if ScoreIA[numMeilleurIA]<=ScoreIA[i]:
                    numMeilleurIA=i
                i+=1
            i=0
            while i<tailleIA: #parcour la ligne de la meilleur IA
                bufferMeilleurIA[i]=IA[i+numMeilleurIA*tailleIA]
                i+=1
            j=0
            while j<nbIA: #colle la meilleur IA sur tout les slot d'IA
                i=0
                while i<tailleIA:
                    IA[i+j*tailleIA]=bufferMeilleurIA[i]
                    i+=1
                j+=1
            #modiffication aléatoire : MUTATION
            i=1
            while i<nbIA:
                j=0
                while j<nbCoeffModif:
                    coeffAlea=random.randint(tailleIA*i,tailleIA*(i+1)-1)
                    IA[coeffAlea]=(random.randint(0,100)-50)/50
                    j+=1
                i+=1
        else:
            IASelect+=1   
        print "   IA : ",IASelect
        #affecte une nouvelle IA au jeu
        debut=IASelect*tailleIA
        i=0
        while i<nbInput*nbNeuroneParCouche:
            TabCoucheIn[i]=IA[i+debut]
            i+=1
        debut=nbInput*nbNeuroneParCouche+IASelect*tailleIA
        i=0
        while i<nbInput*(nbCouche-1)*nbNeuroneParCouche:
            TabCoucheN[i]=IA[i+debut]
            i+=1
        debut=nbInput*nbNeuroneParCouche+nbInput*(nbCouche-1)*nbNeuroneParCouche+IASelect*tailleIA
        i=0
        while i<nbNeuroneParCouche*nbOutput:
            TabCoucheOut[i]=IA[i+debut]
            i+=1
        
        #time.sleep(tempsPause)
        ecran=0
pygame.quit()
        
            
 
