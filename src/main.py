import labyrinthe as lb
import algos
from time import sleep
from os import system
import argparse

def main():

    # ARGUMENTS DU SCRIPT
    argParse = argparse.ArgumentParser()

    argParse.add_argument("-d", "--dim", type=int, help="entier supérieur à 1")
    argParse.add_argument("-a", "--affiche", type=str, help='"oui" ou "non", affiche ou non la génération du labyrinthe')
    argParse.add_argument("-nbr", "--nombreR", type=int, help='Nombre de robot: 1 ou plus')
    args = argParse.parse_args()

    ok = True
    if(args.nombreR == None or args.affiche == None or args.dim == None):
        print("Paramètres manquants!")
        ok = False
    else:
        # DIMENSION
        if(args.dim < 2):
            print("Dimension trop petite!")
            ok = False

        # AFFICHE
        if(args.affiche == 'oui' or args.affiche == 'o' or args.affiche == 'y' or args.affiche == 'yes'):
            affiche = True
        elif(args.affiche == 'non' or args.affiche == 'n' or args.affiche == 'no'):
            affiche = False

        # NOMBRE ROBOT
        if(args.nombreR <= 0):
            print("Nombre de robots incorrect!")
            ok = False
        if(args.nombreR > int((args.dim)/2)):
            print("Trop de robots pour la dimension choisie!")
            ok = False


    # Arguments Valides <=> ok = True
    if(ok):
        # Paramètres de créations du labyrinthe
        pil ="o"
        murH = "-"
        murV = "|"

        # Arguments utilisés
        dim = args.dim
        nbreRobot = args.nombreR
        
        system('cls')

        # Création du Labyrinthe, Départ(s), Arrivée, Carte
        lab = lb.labInit(dim,pil,murH,murV)
        [lab,depart,arrivee] = lb.taillage(lab,dim,nbreRobot,affiche)
        carte = lb.labInit(dim,pil,murH,murV)
        lb.carteInit(carte)
        

        # Affichage menu approprié
        # SOLO
        if(nbreRobot == 1):
            ok = False
            while(not(ok)):
                option = input("Mode de résolution : \n ¤ manuel \n ¤ droite \n ¤ aléatoire \n ¤ poids \n \n")
                if(option == 'manuel' or option == 'droite' or option == 'aléatoire' or option == 'poids'):
                    ok = True
                else:
                    print("Choix invalide: choisir une option dans la liste \n")

        # COOPERATION
        else:
            ok = False
            while(not(ok)):
                option = input("Mode de résolution : \n ¤ droite \n ¤ aléatoire \n ¤ poids \n \n")
                if(option == 'manuel' or option == 'droite' or option == 'aléatoire' or option == 'poids'):
                    ok = True
                else:
                    print("Choix invalide: choisir une option dans la liste \n")

        system('cls')

        # On démarre la phase de déplacement avec l'algo choisi / mode manuel
        dir = []
        run = True
        pos = []
        pas = 0
        for i in range(0,nbreRobot):
            dir.append('X')
            pos.append([depart[i][0],depart[i][1]])

        # Mode manuel
        if(option == 'manuel' and nbreRobot == 1):
            while(run):
                [run,carte,pos[0],dir[i],pas] = lb.deplacement(lab,carte,dir[i],depart,pos[0],arrivee,pas)

        # Toujours à droite
        elif(option == 'droite'):
            while(run):
                for i in range(0,nbreRobot):
                    if(run):
                        action = algos.toujoursDroite(carte,dir[i],pos[i])
                        algos.communication(action)
                        [run,carte,pos[i],dir[i],pas] = lb.deplacementAlgo(action,lab,carte,dir[i],depart,pos[i],arrivee,pas)
                    else: break
        
        elif(option == 'aléatoire'):
            while(run):
                for i in range(0,nbreRobot):
                    if(run):
                        action = algos.leDestin()
                        algos.communication(action)
                        [run,carte,pos[i],dir[i],pas] = lb.deplacementAlgo(action,lab,carte,dir[i],depart,pos[i],arrivee,pas)
                    else: break
        
        elif(option ==  'poids'):
            premierPassage = True
            while(run):
                if(premierPassage):
                    # Données initiales utiles pour l'algorithme
                    for i in range(0,nbreRobot):
                        dir[i] = "↑"
                    poids = algos.initPoids(dim,arrivee)
                    premierPassage = False

                for i in range(0,nbreRobot):
                    if(run):
                        [action,poids] = algos.poids(carte,dim,dir[i],pos[i],poids)
                        [run,carte,pos[i],dir[i],pas] = lb.deplacementAlgo(action,lab,carte,dir[i],depart,pos[i],arrivee,pas)
                        poids = algos.actuPoids(poids,carte,arrivee)
                        algos.affichePoids(poids)
                        algos.communication(action)
                        sleep(0.2)
                    else: break

        else: print("Choix invalide: choisir une option de la liste")


main()