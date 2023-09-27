from Improvisor import *

# Improvisor(csv, steps, lam=0, show=False
imp = Improvisor("./grid.csv",5 , lam=0.007, eps=1, show=False)
imp.improvise()
output = grid_with_path(imp)
print(output)

with open("output.txt", "w") as file:
    file.write(output)

path = imp.path
print(path)