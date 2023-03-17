import argparse

argParse = argparse.ArgumentParser()

argParse.add_argument("-d", "--dim", type=int, help="entier supérieur à 1")
argParse.add_argument("-a", "--affiche", type=str, help='"oui" ou "non", affiche ou non la génération du labyrinthe')
argParse.add_argument("-nbr", "--nombreR", type=int, help='Nombre de robot: 1 ou plus')
args = argParse.parse_args()

ok = True
if(args.nombreR == None or args.affiche == None or args.dim == None):
    print("Paramètres manquant!")
    ok = False
else:
    if(args.dim < 2):
        print("Dimension trop petite")
        ok = False
    if(args.affiche == 'oui'):
        print("affichage!")
        
    if(args.nombreR <= 0):
        print("Nombre de robots incorrect!")
        ok = False
    elif(args.nombreR == 1):
        print("Solo")
    elif(args.nombreR < args.dim):
        print("Cooperation")
    else:
        print("Trop de robots!")
        ok = False

print(ok)
