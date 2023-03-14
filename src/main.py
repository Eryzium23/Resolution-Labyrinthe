import labyrinthe as lb
import algos
from time import sleep
from os import system


def main():
    # Interactions utilisateurs pour initialiser les paramètres
    system('cls')
    print("Bienvenue dans le Simulateur de Résolution de Labyrinthe! \n ")
    dim = int(input("Dimension du labyrinthe souhaité? "))
    affiche = input('Voulez-vous afficher la génération du Labyrinthe? ("oui" ou "non") ')
    if(affiche == 'oui'):
        affiche = True
    elif(affiche == 'non'):
        affiche = False
    option = input("Mode de résolution : \n ¤ manuel \n ¤ droite \n ¤ aléatoire \n ¤ poids \n \n")

    # Paramètres de créatio ns du labyrinthe
    pil ="o"
    murH = "-"
    murV = "|"

    system('cls')

    lab = lb.labInit(dim,pil,murH,murV)                      # On initie un labyrinthe vierge
    [lab,depart,arrivee] = lb.taillage(lab,dim,affiche)              # On le dim/sculpte
    carte = lb.labInit(dim,pil,murH,murV)
    lb.carteInit(carte)                                      # On initialise un labyrinthe avec que les murs extérieurs
    
    # On démarre la phase de déplacement
    run = True
    dir = 'X'
    pos = [depart[0],depart[1]]
    pas = 0
    
    match option:
        case 'manuel':
            while(run):
                [run,carte,pos,dir,pas] = lb.deplacement(lab,carte,dir,depart,pos,arrivee,pas)

        case 'droite':
            while(run):
                action = algos.toujoursDroite(carte,dir,pos)
                algos.communication(action)
                [run,carte,pos,dir,pas] = lb.deplacementAlgo(action,lab,carte,dir,depart,pos,arrivee,pas)
        
        case 'aléatoire':
            while(run):
                action = algos.leDestin()
                algos.communication(action)
                [run,carte,pos,dir,pas] = lb.deplacementAlgo(action,lab,carte,dir,depart,pos,arrivee,pas)
        
        case 'poids':
            premierPassage = True
            while(run):
                if(premierPassage):
                    # Données initiales utiles pour l'algorithme
                    dir = "↑"
                    poids = algos.initPoids(dim,arrivee)
                    premierPassage = False

                [action,poids] = algos.poids(carte,dim,dir,pos,poids)
                [run,carte,pos,dir,pas] = lb.deplacementAlgo(action,lab,carte,dir,depart,pos,arrivee,pas)
                poids = algos.actuPoids(poids,carte,arrivee)
                algos.affichePoids(poids)
                algos.communication(action)
                sleep(0.2)

main()

# Autre programme pour la résolution
# Séparer les méthodes