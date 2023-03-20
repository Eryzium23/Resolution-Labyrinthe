import pickle

obj0 = 1
obj1 = 2
obj2 = 3

# Saving the objects:
with open('objs.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([obj0, obj1, obj2], f)

# Getting back the objects:
with open('objs.pkl', 'rb') as f:  # Python 3: open(..., 'rb')
    a, b, c = pickle.load(f)

print(a)
print(c)