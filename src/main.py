import labyrinthe as lb
import algos
import argparse
import pickle
from time import sleep
from os import system

def main():

    # ARGUMENTS DU SCRIPT
    argParse = argparse.ArgumentParser()

    argParse.add_argument("-d", "--dim", type=int, help="Dimension du labyrinthe : entier supérieur à 1.")
    argParse.add_argument("-a", "--affiche", action='store_true', help='Affichage de la génération')
    argParse.add_argument("-nbr", "--nombreR", type=int, help='Nombre de robot : 1 ou plus')
    argParse.add_argument("-l", "--load",  type=str, help='Chargement de labyrinthe')
    argParse.add_argument("-w", "--write", type=str, help="Path d'enregistrement de labyrinthe ")
    args = argParse.parse_args()

    ok = True
    if(args.nombreR == None or args.dim == None):
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

    affiche = args.affiche

    # Arguments Valides <=> ok = True
    if(ok):
        
        # Paramètres de créations du labyrinthe
        pil = "o"
        murH = "-"
        murV = "|"

        # Arguments utilisés
        dim = args.dim
        nbreRobot = args.nombreR
        
        system('cls')

        # Création du Labyrinthe, Départ(s), Arrivée, Carte
        if(not(args.load == None)):
            try:
                with open("./lab/"+args.load+'.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
                    lab, depart, arrivee = pickle.load(f)
                    print("Labyrinthe chargé! \n")
            except:
                print("Fichier introuvable!")
                exit()
        else:
            lab = lb.labInit(dim,pil,murH,murV)
            [lab,depart,arrivee] = lb.taillage(lab,dim,nbreRobot,affiche)
        carte = lb.labInit(dim,pil,murH,murV)
        lb.carteInit(carte)
        

        ### Affichage menu approprié
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

        ##### PHASE DEPLACEMENTS 
        dir = []
        run = True
        pos = []
        pas = 0
        for i in range(0,nbreRobot):
            dir.append('X')
            pos.append([depart[i][0],depart[i][1]])

        # MANUEL
        if(option == 'manuel' and nbreRobot == 1):
            while(run):
                [run,carte,pos[0],dir[i],pas] = lb.deplacement(lab,carte,dir[i],depart,pos[0],arrivee,pas)

        # DROITE
        elif(option == 'droite'):
            while(run):
                for i in range(0,nbreRobot):
                    if(run):
                        action = algos.toujoursDroite(carte,dir[i],pos[i])
                        algos.communication(action)
                        [run,carte,pos[i],dir[i],pas] = lb.deplacementAlgo(action,lab,carte,dir[i],depart,pos[i],arrivee,pas)
                    else: break
        
        # ALEATOIRE
        elif(option == 'aléatoire'):
            while(run):
                for i in range(0,nbreRobot):
                    if(run):
                        action = algos.leDestin()
                        algos.communication(action)
                        [run,carte,pos[i],dir[i],pas] = lb.deplacementAlgo(action,lab,carte,dir[i],depart,pos[i],arrivee,pas)
                    else: break
        
        # POIDS
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
        if(not(run)):
            if(not(args.write == None)):
                with open("./lab/"+args.write+'.pkl', 'wb') as f:
                    pickle.dump([lab, depart,arrivee], f)
                    print("Labyrinthe enregistré! \n")

main()