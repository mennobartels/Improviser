import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import FancyArrow
from matplotlib.colors import ListedColormap

# Define colors
colors = {
    'white': (1, 1, 1),
    'black': (0, 0, 0),
    'red': (1, 0, 0),
    'brown': (0.647, 0.165, 0.165),  # Brown color
    'green': (0, 1, 0),
}

# Create a custom colormap
cmap_colors = [colors['white'], colors['black'], colors['brown'],colors['red'],]
cmap = ListedColormap(cmap_colors, name='custom_cmap', N=len(cmap_colors))

class PathAnimator:
    def __init__(self, imp, path, save=True):
        self.path = path
        self.size_x = imp.size_x
        self.size_y = imp.size_y
        self.start_x = imp.start_x
        self.start_y = imp.start_y
        self.finish_x = imp.finish_x
        self.finish_y = imp.finish_y
        self.obstacles = imp.obstacles
        self.save = save

    def animate(self):
        # Define the grid size
        grid_size = (self.size_y, self.size_x)
        start = (self.start_y, self. start_x)
        finish = (self.finish_y, self.finish_x)

        # Define the initial grid
        grid = np.zeros(grid_size)

        steps = []

        # ( 0,  1), down
        # ( 0, -1), up
        # ( 1,  0), right
        # (-1,  0), left
        # Define the steps to generate the path
        for step in self.path:
            if step == "r":
                steps.append(( 1,  0))
            if step == "d":
                steps.append(( 0,  1))
            if step == "l":
                steps.append((-1,  0))
            if step == "u":
                steps.append(( 0, -1))

        # Generate the path based on the steps
        path = [(0, 0)]
        x, y = 0, 0

        for step in steps:
            x += step[1]
            y += step[0]
            path.append((x, y))

        # Create a figure and axis
        fig = plt.figure(num=f'Improvisor {self.size_x}x{self.size_y}')
        ax = plt.axes()
        # Color the walls 
        for (x, y) in self.obstacles:
            grid[y, x] = 2
        
        # Color finish
        grid[self.finish_y, self.finish_x] = 2
        # Function to update the grid at each step
        def update(step):
            ax.clear()
            ax.set_title(f'Step {step} of Improvisor {self.size_x}x{self.size_y}')

            for i, (x, y) in enumerate(path[:step]):
                if i == step - 1:
                    grid[x, y] = 3 # Highlight the latest step in red
                else:
                    grid[x, y] = 1  # Keep the rest of the squares in black

            ax.set_xticks(np.arange(-0.5, self.size_x - 0.5, 1), minor=True)
            ax.set_yticks(np.arange(-0.5, self.size_y - 0.5, 1), minor=True)
            ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
            ax.matshow(grid, cmap=cmap)

        # Create an animation
        ani = animation.FuncAnimation(fig, update, frames=len(self.path)+2, repeat=False, interval=300)
        
        if self.save:
            # Save the animation as an MP4 file
            ani.save(f'Improvisor {self.size_x}x{self.size_y}.mp4', writer='ffmpeg')
        
         # Define the initial grid
        grid = np.zeros(grid_size)

         # Color the walls black
        for (x, y) in self.obstacles:
            grid[y, x] = 2  
        grid[self.finish_y, self.finish_x] = 3

        # Display the animation
        plt.show()