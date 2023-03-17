import random
import keyboard as kb
import labyrinthe as lb
from time import sleep


def communication(action):
    match action:
        case 'droite':
            print("Je tourne à droite bip boup!")
        case 'gauche':
            print("Je tourne à gauche bip boup!")
        case 'avancer':
            print("J'avance boup bip!")
        case 'demitour':
            print("Je fais un 180° beep!")
        case 'none':
            print("Chômage technique boup boup!")
    sleep(0.3)


# ALEATOIRE

def leDestin():
    action = random.randint(1,4)
    match action:
        case 1:
            action = 'droite'
        case 2:
            action = 'gauche'
        case 3:
            action = 'avancer'
        case 4:
            action = 'demitour'
    
    return action


# DROITE

def toujoursDroite(carte,dir,pos):
    
    # Coordonnées initiales de position
    y = 2*pos[0]+1
    x = 4*pos[1]+2

    match dir:
        case 'X':
            action = 'droite'
        case '→':
            if(carte[y+1][x] == ' '):
                action = 'droite'
            elif(carte[y][x+2] == ' '):
                action = 'avancer'
            elif(carte[y-1][x] == ' '):
                action = 'gauche'
            else:
                action = 'demitour'
        
        case '←':
            if(carte[y-1][x] == ' '):
                action = 'droite'
            elif(carte[y][x-2] == ' '):
                action = 'avancer'
            elif(carte[y+1][x] == ' '):
                action = 'gauche'
            else:
                action = 'demitour'

        case '↑':
            if(carte[y][x+2] == ' '):
                action = 'droite'
            elif(carte[y-1][x] == ' '):
                action = 'avancer'
            elif(carte[y][x-2] == ' '):
                action = 'gauche'
            else:
                action = 'demitour'

        case '↓':
            if(carte[y][x-2] == ' '):
                action = 'droite'
            elif(carte[y+1][x] == ' '):
                action = 'avancer'
            elif(carte[y][x+2] == ' '):
                action = 'gauche'
            else:
                action = 'demitour'       

    return action


# POIDS

def affichePoids(poids):
    print("Poids : \n")
    for i in range(len(poids)):
        for j in range(len(poids[i])):
            esp = "    "
            if(poids[i][j]>9):
                esp ="   "
            if(poids[i][j]>99):
                esp ="  "
            print(poids[i][j], end=esp)
        print()
    print()


def initPoids(dim,arrivee):
    
    # Paramètres initialisation
    ya = arrivee[0]
    xa = arrivee[1]
    poids = [[0 for j in range(0,dim)] for i in range(0,dim)]

    for j in range(0,dim):
        for i in range(0,dim):
            poids[j][i] = abs(ya-j) + abs(xa-i)
            
    return poids


def calculCoord(t,dim):
    # f(x)=-(x-2 a floor(((x)/(2 a))+((1)/(2)))) (-1)^(floor(((x)/(2 a))+((1)/(2)))) => geogebra
    a = 2*dim
    b = int((t/a)+(0.5))

    y = -(t - a*b)*(-1)**b
    t = t+dim
    b = int((t/a)+(0.5))

    x = -(t - a*b)*(-1)**b

    return [x,y]


def estActualisable(parcours,carte,x,y,xc,yc):
    dim = len(parcours)
    actualisable = False
    if(x-1>=0):
        if(parcours[y][x-1] == 1):
            if(carte[yc][xc-2] == ' '):
                    actualisable = True
    if(x+1<dim):
        if(parcours[y][x+1] == 1):
            if(carte[yc][xc+2] == ' '):
                    actualisable = True
    if(y-1>=0):
        if(parcours[y-1][x] == 1):
            if(carte[yc-1][xc] == ' '):
                    actualisable = True
    if(y+1<dim):
        if(parcours[y+1][x] == 1):
            if(carte[yc+1][xc] == ' '):
                    actualisable = True

    return actualisable


def actuPoids(poids,carte,arrivee):

    dim = len(poids)
    ya = arrivee[0]
    xa = arrivee[1]

    poidsNv = [[0 for j in range(0,dim)] for i in range(0,dim)]
    parcours = [[0 for j in range(0,dim)] for i in range(0,dim)]
    parcours[ya][xa] = 1

    for j in range(0,dim):
        for i in range(0,dim):
            poidsNv[j][i] = poids[j][i]
    
    cptActualisation = 1

    while(cptActualisation < dim**2):
        for i in range(1,(dim)*2-1):
            for j in range(0,4*i):
                [y,x] = calculCoord(j,i)
                y = ya + y
                x = xa + x
                yc = 2*y+1
                xc = 4*x+2
                
                poidsMin = 10000

                if(y >= 0 and y < dim and x >= 0 and x < dim):
                    if(estActualisable(parcours,carte,x,y,xc,yc) and parcours[y][x] == 0):
                        if(x-1 >= 0 and carte[yc][xc-2] == ' '):
                            if(poidsNv[y][x-1] < poidsMin and parcours[y][x-1] == 1):
                                poidsMin = poidsNv[y][x-1]

                        if(x+1 < dim and carte[yc][xc+2] == ' '):
                            if(poidsNv[y][x+1] < poidsMin and parcours[y][x+1] == 1):
                                poidsMin = poidsNv[y][x+1]

                        if(y-1 >= 0 and carte[yc-1][xc] == ' '):
                            if(poidsNv[y-1][x] < poidsMin and parcours[y-1][x] == 1):
                                poidsMin = poidsNv[y-1][x]

                        if(y+1 < dim and carte[yc+1][xc] == ' '):
                            if(poidsNv[y+1][x] < poidsMin and parcours[y+1][x] == 1):
                                poidsMin = poidsNv[y+1][x]

                        if (poidsNv[y][x] > 0):
                            poidsNv[y][x] = poidsMin + 1

                        parcours[y][x] = 1
                        cptActualisation += 1
    return poidsNv


# Choix de l'action en fonction du plus petit poids

def poids(carte,dim,dir,pos,poids):
    
    # Coordonnées initiales de position
    y = pos[0]
    x = pos[1]
    yc = 2*pos[0]+1
    xc = 4*pos[1]+2

    action = 'none'
    dirChoix = 'avancer'
    
    # On choisit la case avec le plus petit poids
    poidsOpti = 10000

    # Droit
    if(x+1 < dim and carte[yc][xc+2] == ' '):
        if(poids[y][x+1] < poidsOpti):
            poidsOpti = poids[y][x+1]
            dirChoix = 'droite'

    # Gauche
    if(x-1 >= 0 and carte[yc][xc-2] == ' '):
        if (poids[y][x-1] < poidsOpti):
            poidsOpti = poids[y][x-1]
            dirChoix = 'gauche'
    
    # Haut
    if(y-1 >= 0 and carte[yc-1][xc] == ' '):
        if( poids[y-1][x] < poidsOpti):
                poidsOpti = poids[y-1][x]
                dirChoix = 'haut'

    # Bas        
    if(y+1 < dim and carte[yc+1][xc] == ' '):
        if( poids[y+1][x] < poidsOpti):
                poidsOpti = poids[y+1][x]
                dirChoix = 'bas'

    # Décision de l'action à entreprendre
    match dirChoix:
        case 'droite':
            match dir:
                case '→' :
                    action = 'avancer'
                case '↓':
                    action = 'gauche'
                case '←':
                    action = 'demitour'
                case '↑':
                    action = 'droite'
        case 'gauche':
            match dir:
                case '→' :
                    action = 'demitour'
                case '↓':
                    action = 'droite'
                case '←':
                    action = 'avancer'
                case '↑':
                    action = 'gauche'
        case 'haut':
            match dir:
                case '→' :
                    action = 'gauche'
                case '↓':
                    action = 'demitour'
                case '←':
                    action = 'droite'
                case '↑':
                    action = 'avancer'
        case 'bas':
            match dir:
                case '→' :
                    action = 'droite'
                case '↓':
                    action = 'avancer'
                case '←':
                    action = 'gauche'
                case '↑':
                    action = 'demitour'
    
    #if(action == 'none'):
    #    action = toujoursDroite(carte,dir,pos)

    return [action,poids]