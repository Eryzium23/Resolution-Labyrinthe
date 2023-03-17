import labyrinthe as lb
import algos
from time import sleep
from os import system


def main():
    
    system('cls')

    # Paramètres de créatio ns du labyrinthe
    pil ="o"
    murH = "-"
    murV = "|"


    # Interactions utilisateurs pour initialiser les paramètres
    print("Bienvenue dans le Simulateur de Résolution de Labyrinthe! \n ")

    ok = False
    while(not(ok)):
        dim = input("Dimension du labyrinthe souhaité? (nombre entier) ")
        try:
            dim = int(dim)
            ok = True
        except:
            print("Choix invalide : choisir un nombre entier \n" )

    ok = False
    while(not(ok)):
        affiche = input('Voulez-vous afficher la génération du Labyrinthe? ("oui" ou "non") ')
        if(affiche == 'oui'):
            affiche = True
            ok = True
        elif(affiche == 'non'):
            affiche = False
            ok = True
        else:
            print('Choix invalide: répondre par "oui" ou "non" \n')

    ok = False
    while(not(ok)):
        nbreRobot = input("Combien de robots pour la résolution? (nombre entier)")
        try:
            nbreRobot = int(nbreRobot)
            ok = True
        except:
            print("Choix invalide: choisir un nombre entier \n")

    system('cls')
    
    # Création du Labyrinthe + Carte
    lab = lb.labInit(dim,pil,murH,murV)                      # On initie un labyrinthe vierge
    [lab,depart,arrivee] = lb.taillage(lab,dim,affiche)              # On le dim/sculpte
    carte = lb.labInit(dim,pil,murH,murV)
    lb.carteInit(carte)                                      # On initialise un labyrinthe avec que les murs extérieurs
    
    # On Choisit le menu approprié en fonction du nombre de robot
    if(nbreRobot == 0):
        print("Choix invalide")
        return
    if(nbreRobot == 1):
        option = input("Mode de résolution : \n ¤ manuel \n ¤ droite \n ¤ aléatoire \n ¤ poids \n \n")
    else:
        option = input("Mode de résolution : \n ¤ droite \n ¤ aléatoire \n ¤ poids \n \n")

    system('cls')

    # On démarre la phase de déplacement
    run = True
    dir = 'X'
    pos = [depart[0],depart[1]]
    pas = 0

    if(option == 'manuel' and nbreRobot == 1):
        while(run):
            [run,carte,pos,dir,pas] = lb.deplacement(lab,carte,dir,depart,pos,arrivee,pas)

    elif(option == 'droite'):
        while(run):
            action = algos.toujoursDroite(carte,dir,pos)
            algos.communication(action)
            [run,carte,pos,dir,pas] = lb.deplacementAlgo(action,lab,carte,dir,depart,pos,arrivee,pas)
    
    elif(option == 'aléatoire'):
        while(run):
            action = algos.leDestin()
            algos.communication(action)
            [run,carte,pos,dir,pas] = lb.deplacementAlgo(action,lab,carte,dir,depart,pos,arrivee,pas)
    
    elif(option ==  'poids'):
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

    else: print("Choix invalide")


main()

# Autre programme pour la résolution
# Séparer les méthodes