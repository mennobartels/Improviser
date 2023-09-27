# Improvisor

**Improvisor** is a pathfinding tool that utilizes the ApproxMC and Z3 libraries. This project was developed as part of a research internship. It allows you to discover a path using the Approximate Model Counter (ApproxMC) algorithm. Below, you'll find details on how to use this tool and an overview of its main features.

## Description

The repository contains files for the Improvisor, which can find paths using the ApproxMC algorithm. In the `Example.py` file, you can find a basic example of how to use it.

The `Improvisor` class accepts the following arguments:

- `csv` - the input file in CSV format.
- `steps` - the number of steps the Improvisor may take.
- `lam` - the lambda value used (set to 0 if uninitialized).
- `eps` - the epsilon value used (set to 0.8 if uninitialized).
- `show` - a boolean for printing out intermediate results (set to False if uninitialized).

**CSV File Format:**

- `0` represents an open square.
- `S` marks the starting square.
- `F` designates the finishing square.
- `W` indicates a wall or obstacle.
  
Please note that `S` and `F` can only appear once in the grid.

## Usage

When cloning the repository, there are two primary ways to use the code: via Docker or locally.

### Docker

1. Build the Docker image with the following command:

   ```bash
   docker build -t improviser-image .

    Run a container with an interactive session:

    bash

docker run -it --rm improviser-image /bin/bash

This command provides an interactive session within the container.

Inside the container, run the example:

bash

    python Example.py

    You can also use the nano text editor within the container to modify the example or grid. If the grid changes, adjust the input for the number of steps and lambda accordingly.

Please note that animations are not available when running the container, as it provides a command-line interface only.
Local

To run the files locally, it is recommended to set up a virtual environment (venv) and install the required packages from the requirements.txt file. Then, execute Example.py within the virtual environment as usual.

Additionally, you can use Example_with_animation.py locally, which will save animations as MP4 files.

Feel free to explore and adapt the Improvisor tool to suit your pathfinding needs!

Enjoy pathfinding with Improvisor!

