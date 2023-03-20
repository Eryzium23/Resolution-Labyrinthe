import labyrinthe as lb
import argparse
import keyboard as kb
import pickle
from os import system
from time import sleep


def creation(lab,dim,dir,pos):

    # Coordonnées initiales de position
    y = 2*pos[0]+1
    x = 4*pos[1]+2
    run = True

    # Paramètres utiles aux calculs de déplacement
    murH = lab[0][1]
    murV = lab[1][0]

    if(dir == 'X'):
        system('cls')
        print("D = Départ ; X = position initiale ;\nAppuyer sur z/q/s/d ou les flèches pour vous déplacer, echap pour quitter :")
        lb.afficheLab(lab)

    event = kb.read_event()
    if (event.event_type == kb.KEY_DOWN):
        match event.name:
            
            # DROITE
            case 'd' | 'droite':
                if(lab[y][x+2] == murV and x < 4*dim+2):
                    lab[y][x+2] = ' '
                else:
                    print("Hors limite!")
                if(lab[y][x+2] == " "):
                    lab[y][x] = " "
                    x+=4
                    pos[1]+=1
                    dir = '→'
                    lab[y][x] = dir

            # GAUCHE
            case 'q' | 'gauche':
                if(lab[y][x-2] == murV and x > 0):
                    lab[y][x-2] = ' '
                else:
                    print("Hors limite!")
                if(lab[y][x-2] == " "):
                    lab[y][x] = " "
                    x-=4
                    pos[1]-=1
                    dir = '←'  
                    lab[y][x] = dir      

            # HAUT
            case 'z' | 'haut':
                if(lab[y-1][x] == murH and y > 0):
                    lab[y-1][x-1] = ' '
                    lab[y-1][x] = ' '
                    lab[y-1][x+1] = ' '
                else:
                    print("Hors limite!")
                if(lab[y-1][x] == " "):
                    lab[y][x] = " "
                    y-=2
                    pos[0]-=1
                    dir = '↑'
                    lab[y][x] = dir
            
            # BAS
            case 's' | 'bas':
                if(lab[y+1][x] == murH and y < 2*dim+1):
                    lab[y+1][x-1] = ' '
                    lab[y+1][x] = ' '
                    lab[y+1][x+1] = ' '
                else:
                    print("Hors limite!")
                if(lab[y+1][x] == " "):
                    lab[y][x] = " "
                    y+=2
                    pos[0]+=1
                    dir = '↓'
                    lab[y][x] = dir

            # QUITTER    
            case 'esc':
                run = False

    system('cls')
    print("D = Départ ; X = position initiale ;\nAppuyer sur z/q/s/d ou les flèches pour vous déplacer ; Echap pour finir :")
    lb.afficheLab(lab)
    if(lab[y][x] == " "):
        lab[y][x] = "D"

    return [lab,pos,dir,run]


def coordonneU(dim):
    ok = False
    while(not(ok)):
        # On demande le point de départ de création
        coord = input('Coordonnées? "x,y" ')
        coord = coord.split(',')
        
        # On transforme en entier
        coord[0] = int(coord[0])
        coord[1] = int(coord[1])

        # On vérifie que le départ est correct
        if(len(coord) == 2 and coord[0] >= 0 and coord[0] < dim and coord[1] >= 0 and coord[1] < dim):
            ok = True
            # On inverse pour l'algorithme
            temp = coord[0]
            coord[0] = coord[1]
            coord[1] = temp
        else:
            print("Coordonnées incorrects!")
    return coord


##### MAIN #####

def main():

    # ARGUMENTS DU SCRIPT
    argParse = argparse.ArgumentParser()

    argParse.add_argument("-d", "--dim", type=int, help="Dimension du labyrinthe : entier supérieur à 1.")
    argParse.add_argument("-nbr", "--nombreR", type=int, help='Nombre de robot : 1 ou plus')
    argParse.add_argument("-w", "--write", type=str, help="Chemin d'enregistrement de labyrinthe ")
    args = argParse.parse_args()


    ok = True
    if(args.nombreR == None or args.dim == None or args.write == None):
        print("Paramètres manquants!")
        ok = False
    else:
        # DIMENSION
        if(args.dim < 2):
            print("Dimension trop petite!")
            ok = False
        # NOMBRE ROBOT
        if(args.nombreR <= 0):
            print("Nombre de robots incorrect!")
            ok = False
        if(args.nombreR > int((args.dim)/2)):
            print("Trop de robots pour la dimension choisie!")
            ok = False

    if(ok):
        lab = lb.labInit(args.dim,'o','-','|')
        ok = False
        departs = []
        # On demande un ou des départs corrects
        print("Point de départ(s) :\n")
        for i in range(0,args.nombreR):
            departs.append(coordonneU(args.dim))
                
        # On initialise la phase de déplacements/taillage manuel
        run = True
        dir = 'X'
        depart = departs[0]
        y = depart[0]
        x = depart[1]
        lab[2*y+1][4*x+2] = dir
        pos = [y,x]
        lb.afficheLab(lab)

        # Phase déplacement
        while(run):
            [lab,pos,dir,run] = creation(lab,args.dim,dir,pos)
        lab[2*pos[0]+1][4*pos[1]+2] = " "
        
        # On demande l'arrivée
        system('cls')
        arrivee = coordonneU(args.dim)
        
        if(not(run)):
            if(not(args.write == None)):
                with open("./lab/"+args.write+'.pkl', 'wb') as f:
                    pickle.dump([lab,departs,arrivee,args.dim,args.nombreR], f)
                    print("Labyrinthe enregistré! \n")


main()