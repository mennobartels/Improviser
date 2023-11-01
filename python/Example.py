from Improviser import *

# Improviser(csv, steps, lam=0, show=False
imp = Improviser("./grid.csv", 6 , lam=0.001, eps=1, show=False)
imp.improvise()
output = grid_with_path(imp)
print(output)

with open("output.txt", "w") as file:
    file.write(output)

path = imp.path
print(path)