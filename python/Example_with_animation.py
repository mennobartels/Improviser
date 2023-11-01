from Improviser import *
from Animation import *

# Improviser(csv, steps, lam=0, show=False
imp = Improviser("./grid.csv", 6, lam=0.01, eps=1, show=True)
imp.improvise()
output = grid_with_path(imp)
print(output)
with open("output.txt", "w") as file:
    file.write(output)

path = imp.path
print(path)

an = PathAnimator(imp, path, save=True)
an.animate()