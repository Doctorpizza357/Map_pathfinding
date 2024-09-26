
# Graph Animation Project

This project visualizes graph traversal algorithms (Dijkstra and A*) by generating frames of the graph at each step of the algorithm. The frames can be used to create an animation of the algorithm in action.

## Features

- Visualizes Dijkstra and A* algorithms.
- Generates frames for each step of the algorithm.
- Allows for random or custom start and end points.
- Supports starting the animation from a specific frame.

## Requirements

- Python 3.x
- Matplotlib
- NetworkX

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required packages:
    ```sh
    pip install matplotlib networkx
    ```

## Usage

1. Run the script:
    ```sh
    python animation.py
    ```

2. Choose the start and end points:
    - Option 1: Random start and end points.
    - Option 2: Custom start and end points.

3. Choose the algorithm:
    - Option 1: Dijkstra
    - Option 2: A*

4. Input the frame to start the animation from.

## Example

```sh
1: Random start and end points
2: Custom start and end points
> 1
Choose algorithm (1: Dijkstra, 2: A*): 1
Start = 0
End = 5
Input frame to start animation from: 10
```

## License

This project is licensed under the MIT License.
