import pickle as p

f = open ("labyrinthe.txt","wb")

x = 2
p.dump(f,x)
f.close()