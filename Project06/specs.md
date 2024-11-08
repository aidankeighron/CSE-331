# Project 6: Graphs

**Due: Friday, Nov 22nd at 9:00pm**

_This is not a team project, do not copy someone else’s work._

_This project is more complicated than previous ones, so we suggest starting it early and not leaving it until the last minute. _

## Assignment Overview

### What is A\* Search?

Instead of searching the "next closest" vertex as is done in Dijkstra's algorithm, [A\* Search](https://en.wikipedia.org/wiki/A*_search_algorithm) (A-Star Search) picks the vertex which is "next closest to the goal" by weighting vertices more cleverly.

Recall that in Dijkstra's algorithm, vertices are stored in a priority queue with a priority key equal to the current shortest path to that vertex. If we denote the current shortest path to a vertex _V_ by **g(v)**, then on each iteration of Dijkstra's algorithm, we search on the vertex with **min(g(v)).**

A\* search takes the same approach to selecting the next vertex, but instead of setting the priority key of a vertex equal to **g(v)** and selecting **min(g(v))**, it uses the value **f(v)** and selects the vertex with **min(f(v))** where

**f(v) = g(v) + h(v)**

**\= current_shortest_path_to_v + estimated_distance_between_v_and_target**

### In English, Please...

A\* Search prioritizes vertices _V_ to search based on the value **f(v)**, which is the sum of

- **g(v)**, or the current shortest known path to vertex _V_, and
- **h(v)**, which is the estimated (Euclidean or Taxicab) distance between the vertex _V_ and the target vertex you're searching for

The result is that A\* prioritizes vertices to search that (1) are _close to the origin along a known path_ AND which (2) are _in the right direction towards the target._ Vertices with a small **g(v)** are _close to the origin along a known path_ and vertices with a small **h(v)** are _in the right direction towards the target**,**_ so we pick vertices with the smallest sum of these two values.

[We strongly recommend you watch this video to build your intuition behind A\* Search!](https://www.youtube.com/watch?v=ySN5Wnu88nE)

A\* is extremely versatile. Here we use Euclidean and Taxicab distances to prioritize certain directions of search, but note that any [metric](<https://en.wikipedia.org/wiki/Metric_(mathematics)#Definition>) **h(v, target)** could be used should the need arise. See [here](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html) for more information on situations where different metrics may be practical.

![astar](img/a_star.gif)

## Assignment Notes

- **We strongly encourage that you read through and thoroughly understand the provided graph methods. You will need to use some of them and understanding the implementation details will save a lot of time.**
- A plotting function is provided to help you visualize the progression of various search algorithms
  - Be sure to read the specs explaining **plot()**
  - If you don't want to use it, just comment out the related import statements and **plot()** function
- Python allows representation of the value infinity using **float('inf')**
- No negative edge weights will ever be added to the graph
  - All edge weights are numeric values greater than or equal to zero
- Time complexities are specified in terms of _V_ and _E_, where _V_ represents the number of vertices in the graph and _E_ represents the number of edges in a graph
  - Recall that E is bounded above by _V_^2; a graph has _E_ = _V_^2 edges if and only if every vertex is connected to every other vertex
- Recall that **list.insert(0, element)** and **list.pop(0)** are both _O(N)_ calls on a Python list
  - Recall that python's 'lists' are not lists in the more common sense of the word: linked lists. They are dynamically managed tuples, stored in memory as contiguous arrays of pointers to elements elsewhere in memory. This allows indexing into a 'list' in constant time. The downside of this, however, is that adding to a python 'list' at a specific index, _i,_ requires shifting the pointer to every element past _i_ by one in the underlying array: a linear operation.
  - Be careful when implementing **bfs, astar,** and the Application Problem to ensure you do not break time complexity by popping or inserting from the front of a list when reconstructing a path
  - Instead of inserting into / popping from the front of the list, simply append to or pop from the end, then reverse the list _once_ at the end
    - If you have N calls to **list.insert(0, element)**, that is _O(N^2)_
    - If you instead have N calls to **list.append(element)**, followed by a single call to **list.reverse()**, that is _O(N)_
    - Both methods will result in the same list being constructed, but the second is far more efficient

## Assignment Specifications

### class Vertex

Represents a vertex object, the building block of a graph.

**_DO NOT MODIFY the following attributes/functions_**

- **Attributes**
  - **id:** A string used to uniquely identify a vertex
  - **adj:** A dictionary of type **{other_id : number}** which represents the connections of a vertex to other vertices; the existence of an entry with key other_id indicates connection from this vertex to the vertex with id other_id by an edge with weight **number**
    - Note that as of Python 3.7, [insertion ordering](https://stackoverflow.com/a/57072435) in normal dictionaries is guaranteed and ensures traversals will select the next neighbor to visit deterministically
  - **visited:** A boolean flag used in search algorithms to indicate that the vertex has been visited
  - **x:** The x-position of a vertex (used in assignment) (defaults to zero)
  - **y:** The y-position of a vertex (used in assignment) (defaults to zero)
- **\_\_init\_\_(self, idx: str, x: float=0, y: float=0) -> None:**
  - Constructs a Vertex object
- **\_\_eq\_\_(self, other: Vertex) -> bool:**
  - Compares this vertex for equality with another vertex
- **\_\_repr\_\_(self) -> str:**
  - Represents the vertex as a string for debugging
- **\_\_str\_\_(self) -> str:**
  - Represents the vertex as a string for debugging
- **\_\_hash\_\_(self) -> int:**
  - Allows the vertex to be hashed into a set; used in unit tests

**_USE the following functions however you'd like_**

- **deg(self) -> int:**
  - Returns the number of outgoing edges from this vertex; i.e., the outgoing degree of this vertex
  - _Time Complexity: O(1)_
  - _Space Complexity: O(1)_
- **get_outgoing_edges(self) -> Set[Tuple(str, float)]:**
  - Returns a **set** of tuples representing outgoing edges from this vertex
  - Edges are represented as tuples **(other_id, weight)** where
    - **other_id** is the unique string id of the destination vertex
    - **weight** is the weight of the edge connecting this vertex to the other vertex
  - Returns an empty set if this vertex has no outgoing edges
  - _Time Complexity: O(degV)_
  - _Space Complexity: O(degV)_
- **euclidean_distance(self, other: Vertex) -> float:**
  - Returns the [euclidean distance](http://rosalind.info/glossary/euclidean-distance/) \[based on two-dimensional coordinates\] between this vertex and vertex **other**
  - Used in AStar
  - _Time Complexity: O(1)_
  - _Space Complexity: O(1)_
- **taxicab_distance(self, other: Vertex) -> float:**
  - Returns the [taxicab distance](https://en.wikipedia.org/wiki/Taxicab_geometry) \[based on two-dimensional coordinates\] between this vertex and vertex **other**
  - Used in AStar
  - _Time Complexity: O(1)_
  - _Space Complexity: O(1)_

### class Graph

Represents a graph object

**_DO NOT MODIFY the following attributes/functions_**

- **Attributes**
  - **size:** The number of vertices in the graph
  - **vertices:** A dictionary of type **{id : Vertex}** storing the vertices of the graph, where **id** represents the unique string id of a **Vertex** object
    - Note that as of Python 3.7, [insertion ordering](https://stackoverflow.com/a/57072435) in normal dictionaries is guaranteed and ensures **get_edges(self)** and **get_vertices(self)** will return deterministically ordered lists
  - **plot_show**: If true, calls to **plot()** display a rendering of the graph in matplotlib; if false, all calls to **plot()** are ignored (see **plot()** below)
  - **plot_delay**: Length of delay in **plot()** (see **plot()** below)
- **\_\_init\_\_(self, plt_show: bool=False) -> None:**
  - Constructs a Graph object
  - Sets **self.plot_show** to False by default
- **\_\_eq\_\_(self, other: Graph) -> bool:**
  - Compares this graph for equality with another graph
- **\_\_repr\_\_(self) -> str:**
  - Represents the graph as a string for debugging
- **\_\_str\_\_(self) -> str:**
  - Represents the graph as a string for debugging
- **add_to_graph(self, start_id: str, dest_id: str=None, weight: float=0) -> float:**
  - Adds a vertex / vertices / edge to the graph
    - Adds a vertex with id **start_id** to the graph if no such vertex exists
    - Adds a vertex with id **dest_id** to the graph if no such vertex exists and **dest_id** is not None
    - Adds an edge with weight **weight** if **dest_id** is not None
  - If a vertex with id **start_id** or **dest_id** already exists in the graph, this function will not overwrite that vertex with a new one
  - If an edge already exists from vertex with id **start_id** to vertex with id **dest_id**, this function will overwrite the weight of that edge
- **matrix2graph(self, matrix: Matrix) -> None:**
  - Constructs a graph from a given adjacency matrix representation
  - **matrix** is guaranteed to be a square 2D list (i.e. list of lists where # rows = # columns), of size **[V+1]** x **[V+1]**
    - **matrix[0][0]** is None
    - The first row and first column of **matrix** hold string ids of vertices to be added to the graph and are symmetric, i.e. **matrix[i][0] = matrix[0][i]** for i = 1, ..., n
    - **matrix[i][j]** is None if no edge exists from the vertex **matrix[i]0\]** to the vertex **matrix[0][j]**
    - **matrix[i][j]** is a **number** if an edge exists from the vertex **matrix[i][0]** to the vertex **matrix[0]j\]** with weight **number**
- **graph2matrix(self) -> None:**
  - Constructs and returns an adjacency matrix from a graph
  - The output matches the format of matrices described in **matrix2graph**
  - If the graph is empty, returns **None**
- **graph2csv(self, filepath: str) -> None:**

  - Encodes the graph (if non-empty) in a csv file at the given location

- **reset_vertices(self) -> None:**
  - Resets visited flags to False of all vertices within the graph
  - Used in unit tests to reset graphs between tests
  - Time Complexity: O(V)
  - Space Complexity: O(V)
- **get_vertex_by_id(self, v_id: str) -> Vertex:**
  - Returns the vertex object with id v_id if it exists in the graph
  - Returns None if no vertex with unique id v_id exists
  - Time Complexity: O(1)
  - Space Complexity: O(1)
- **get_all_vertices(self) -> Set[Vertex]:**
  - Returns a set of all Vertex objects held in the graph
  - Returns an empty set if no vertices are held in the graph
  - Time Complexity: O(V)
  - Space Complexity: O(V)
- **get_edge_by_ids(self, begin_id: str, end_id: str) -> Tuple(str, str, float):**
  - Returns the edge connecting the vertex with id begin_id to the vertex with id end_id in a tuple of the form (begin_id, end_id, weight)
  - If the edge or either of the associated vertices does not exist in the graph, returns None
  - Time Complexity: O(1)
  - Space Complexity: O(1)
- **get_all_edges(self) -> Set[Tuple(str, str, float)]:**
  - Returns a set of tuples representing all edges within the graph
  - Edges are represented as tuples (begin_id, end_id, weight) where
    - begin_id is the unique string id of the starting vertex
    - end_id is the unique string id of the starting vertex
    - weight is the weight of the edge connecitng the starting vertex to the destination vertex
  - Returns an empty set if the graph is empty
  - Time Complexity: O(V+E)
  - Space Complexity: O(E)
- **build_path(self, back_edges: Dict[str, str], begin_id: str, end_id: str) -> Tuple[List[str], float]:**
  _ Given a dictionary of back-edges (a mapping of vertex id to predecessor vertex id), reconstructs the path from start_id to end_id and computes the total distance
  _ Returns tuple of the form ([path], distance) where
  [path] is a list of vertex id strings beginning with begin\*id, terminating with end_id, and including the ids of all intermediate vertices connecting the two
  distance is the sum of the weights of the edges along the [path] traveled
  - Handle the cases where no path exists from vertex with id begin\*id to vertex with end_id or if one of the vertices does not exist
  - Time Complexity: O(V) \* Space Complexity: O(V)

**_USE the following function however you'd like, without changing them_**

- **empty(self) -> bool:**

  - Return true if the graph is empty

- **plot(self) -> None:**

  - Renders a visual representation of the graph using matplotlib and displays graphic in PyCharm
    - [Follow this tutorial to install matplotlib and numpy if you do not have them](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html), or follow the tooltip auto-suggested by PyCharm
  - Provided for use in debugging
  - If you call this in your searches and **self.\*\***plot_show** is true, the search process will be animated in successive plot renderings (with time between frames controlled by **self.plot_delay\*\*)
  - Not tested in any testcases
    - All testcase graphs are constructed with **self.plot_show** set to False
  - If vertices have (x,y) coordinates specified, they will be plotted at those locations
  - If vertices do not have (x,y) coordinates specified, they will be plotted at a random point on the unit circle
  - To install the necessary packages (matplotlib and numpy), follow the auto-suggestions provided by PyCharm
  - Vertices and edges are labeled; edges are color-coded by weight
    - If a bi-directional edge exists between vertices, two color-coded weights will be displayed

- **unvisit_vertices(self) -> None:**
  - Resets visited flags of all vertices within the graph
  - Used in unit tests to reset graph between searches
  - _Time Complexity: O(V)_
  - _Space Complexity: O(V)_
- **get_vertex(self, vertex_id: str) -> Vertex:**
  - Returns the Vertex object with id **vertex_id** if it exists in the graph
  - Returns None if no vertex with unique id **vertex_id** exists
  - _Time Complexity: O(1)_
  - _Space Complexity: O(1)_
- **get_vertices(self) -> Set(Vertex):**
  - Returns a **set** of all Vertex objects held in the graph
  - Returns an empty set if no vertices are held in the graph
  - _Time Complexity: O(V)_
  - _Space Complexity: O(V)_
- **get_edge(self, start_id: str, dest_id: str) -> Tuple(str, str, float):**
  - Returns the edge connecting the vertex with id **start_id** to the vertex with id **dest_id** in a tuple of the form **(start_id, dest_id, weight)**
  - If the edge or either of the associated vertices does not exist in the graph, returns **None**
  - _Time Complexity: O(1)_
  - _Space Complexity: O(1)_
- **get_edges(self) -> Set[Tuple(str, str, float)]:**
  - Returns a **set** of tuples representing all edges within the graph
  - Edges are represented as tuples **(start_id, other_id, weight)** where
    - **start_id** is the unique string id of the starting vertex
    - **other_id** is the unique string id of the destination vertex
    - **weight** is the weight of the edge connecting the starting vertex to the destination vertex
  - Returns an empty set if the graph is empty
  - _Time Complexity: O(V+E)_
  - _Space Complexity: O(E)_

**_IMPLEMENT the following functions_**

- **bfs(self, begin_id: str, end_id: str) -> Tuple(List[str], float):**
  - Perform a breadth-first search beginning at vertex with id **begin_id** and terminating at vertex with id **end_id**
  - **MUST CALL build_path!**
  - **As you explore from each vertex, iterate over neighbors using vertex.adj (not vertex.get_edges()) to ensure neighbors are visited in proper order**
  - Returns tuple of the form **(path, distance)** where
    - **path** is a list of vertex id strings beginning with **begin_id**, terminating with **end_id**, and including the ids of all intermediate vertices connecting the two
    - **distance** is the sum of the weights of the edges along the **path** traveled
  - If no path exists from vertex with id **begin_id** to vertex with **end_id** or if one of the vertices does not exist, returns tuple **(\[\],0)**
  - Guaranteed that **begin_id != end_id** (since that would be a trivial path)
  - Because our adjacency maps use [insertion ordering](https://stackoverflow.com/a/57072435), neighbors will be visited in a deterministic order, and thus you do not need to worry about the order in which you visit neighbor vertices at the same depth
  - Use the [SimpleQueue](https://docs.python.org/3/library/queue.html) class to guarantee O(1) pushes and pops on the queue
  - _Time Complexity: O(V+E)_
  - _Space Complexity: O(V)_
- **a_star(self, start_id: str, target_id: str, metric: Callable([Vertex, Vertex], float) -> Tuple[List[str], float\]**
  - Perform an A\* search beginning at vertex with id **start_id** and terminating at vertex with id **end_id**
  - As you explore from each vertex, iterate over neighbors using **vertex.adj** (not vertex.get_edges()) to ensure neighbors are visited in proper order
  - Use the **metric** parameter to estimate h(v), the remaining distance, at each vertex
    - This is a callable parameter and will always be **Vertex.euclidean_distance** or **Vertex.taxicab_distance**
  - **MUST CALL build_path!**
  - Returns tuple of the form **([path], distance)** where
    - **[path]** is a list of vertex id strings beginning with **start_id**, terminating with **end_id**, and including the ids of all intermediate vertices connecting the two
    - **distance** is the sum of the weights of the edges along the **[path]** traveled
  - If no path exists from vertex with id **start_id** to vertex with **end_id** or if one of the vertices does not exist, returns tuple **(\[\],0)**
  - Guaranteed that **start_id != target_id** (since that would be a trivial path)
  - Recall that vertices are prioritized in increasing order of **f(v) = g(v) + h(v)**, where
    - **g(v)** is the shortest known path to this vertex
    - **h(v)** is the Euclidean distance from _V_ to the target vertex
  - Use the given AStarPriorityQueue class to simplify priority key updates in a search priority queue
  - **Implementations of this function which do not utilize the heuristic metric will not receive any credit**
    - **Do not simply implement Dijkstra's Algorithm**
  - _Time Complexity: O((E + V)log(V))_
  - _Space Complexity: O(V)_

To simplify the operation of updating a priority key in your search priority queue, use the following given class.

### class PriorityQueue

_DO NOT MODIFY the following attributes/functions_

- **Attributes**
  - **data:** Underlying data list of priority queue
  - **locator:** Dictionary to locate vertices within the priority queue
  - **counter:** Used to break ties between vertices
- **\_\_init\_\_(self)**
  - Constructs an AStarPriorityQueue object
- **\_\_repr\_\_(self)**
  - Represents the priority queue as a string for debugging
- **\_\_str\_\_(self)**
  - Represents the priority queue as a string for debugging
- **empty(self)**
  - Returns boolean indicating whether priority queue is empty
- **push(self, priority, vertex)**
  - Push the **vertex** object onto the priority queue with a given **priority** key
  - This priority queue has been specially designed to hold Vertex objects as values ranked by priority keys; be sure you push Vertex objects and NOT vertex id strings onto the queue
- **pop(self)**
  - Visit, remove and return the Vertex object with the highest priority (i.e. lowest priority key) as a **(priority, vertex)** tuple
- **update(self, new_priority, vertex)**
  - Update the priority of the **vertex** object in the queue to have a **new_priority**

## Application Problem: A New Jumanji...

You get home, ready for a night of video-games with your friends, you are all set with your 90's themed games! You get your snacks, your comforter and tell your mom you will be locked in your cave for the better part of the next 14 hours, and you turn on the video-game. Suddenly, before you can warn anyone, you get sucked into the game, and worse, it is an old game with only 0s and 1s, you now need to find your way out to escape this and enjoy the time you have left before school starts again next day.

### Objective

Implement the A* search algorithm to find the shortest path between two positions in a 2D grid. Each cell in the grid can be a free space (`0`) or an obstacle (`1`). Your task is to navigate from a specified start node to an end node using the A* algorithm.

### Grid Representation

- **Input:** A 2D array (grid) of `0`s and `1`s.
  - `0` indicates a free space.
  - `1` indicates an obstacle.
- **Dimensions:** The grid dimensions are defined by the number of rows and columns in the array.

### Task Description

Write a function that computes the shortest path from a start position to an end position in the given grid using the A\* search algorithm.
You may use the A\* function you already implemented for the Graph ADT, just adapting how to convert the matrix into the Graph ADT, or create a completely new one - no need to say which one is easier right?

- **Inputs:**
  - `start_row` and `start_col`: Coordinates of the start position.
  - `end_row` and `end_col`: Coordinates of the end position.
- **Output:** An array of coordinates (`[row, col]`), representing the shortest path from the start node to the end node, and the distance on the path. This array should include both the start and end positions, as well as all intermediate nodes in order visited.

### Path Characteristics

- **jumanji_path(start_row: int, start_col: int, end_row: int, end_col: int, graph: List[List[int]]) -> Tuple[List[List[int]], float\]**

  - Nodes are connected vertically and horizontally (not diagonally). This should be a hint on which Metric should be used for the heuristic, which one is more suited for a movement that can't go diagonally? _cough "Not euclidian" cough_
  - The distance between adjacent nodes is considered `1`.
  - The start and end positions are guaranteed to be free spaces and will not overlap or be out of bounds.
  - If no path exists, the function returns tuple **(\[\],0)**
  - Paths going vertically should take precedence over paths going horizontally.

  ```
  # When different paths are possible, pathSouth should be the expected answer.
  # Hint: If using the Graph ADT this can be done by adding edges in different orders.

  pathSouth = [[0, 0], [1, 0], [1, 1], [1, 2], [1, 3]]
  pathEast = [[0, 0], [0, 1], [0, 2], [0, 3], [1, 3]]
  pathMiddle = [[0, 0], [0, 1], [0, 2], [1, 2], [1, 3]]

  ```

- **start_row: int:** Starting row position on graph
- **start_col: int:** Starting col position on graph
- **end_row: int:** Ending row position on graph
- **start_col: int:** Ending row position on graph
- _Time Complexity: `O(w*h*log(w*h))`, where `w` is the grid width and `h` is the grid height._
- _Space Complexity: `O(w*h)`._

### Sample Input

```python
start_row = 0
start_col = 1
end_row = 4
end_col = 3
graph = [
  [0, 0, 0, 0, 0],
  [0, 1, 1, 1, 0],
  [0, 0, 0, 0, 0],
  [1, 0, 1, 1, 1],
  [0, 0, 0, 0, 0]
]
```

### Expected Output

```python
([[0, 1], [0, 0], [1, 0], [2, 0], [2, 1], [3, 1], [4, 1], [4, 2], [4, 3]], 8)
```

### Visualization of the Shortest Path

The path through the grid is marked with dots (`.`), indicating the route from the start node to the end node. Here's how the grid looks:

```plaintext
[.,.,0,0,0],
[.,1,1,1,0],
[.,.,0,0,0],
[1,.,1,1,1],
[0,.,.,.,0]
```

**A note from the authors:** This problem, thought a very common idea, can become handy to you on job interviews; one of the author's was given this problem to solve on a coding interview from a FAANG company, so even if the story is simple, don't disregard the importance of knowing algorithms like this.

## One more thing...

Wow, you are getting good at this kind of thing, so good that MSU now wants you to help them make the university better. Every student, specially freshman, know how busy a adviser schedule can be, and you are tasked with helping with that. You will need to create a system, that given the requirements for classes, it will check if a given schedule is valid.

### class Schedule

_DO NOT MODIFY the following attributes/functions_

**IT IS MANDATORY TO USE THE `requirements` GRAPH TO STORE THE REQUIREMENTS, BUT YOU MAY CHOOSE HOW TO USE IT AS YOU SEE FIT**

- **Attributes**

  - **requirements: Graph:** Graph to store all the requirements for classes

- **\_\_init\_\_(self):**

  - Initializes the requirements as an empty graph.

- **isEmpty(self):**
  - Checks if the `self.requirements` attribute is empty.

_MODIFY THE FOLLOWING METHODS_

- **addRequirements(requirementsToAdd: Dict[str, List[str]]) -> bool**
  - Adds all the requirements to the `requirements` attribute. It checks if the requirements are valid (i.e. if they include a cycle like CSE 331 requires CSE 260 and CSE 260 requires). If the requirements are valid, add them in a suitable format to the `requirements` graph and return `True`. If they are not valid, the `requirements` attribute should be empty, and return `False`.
  - You can use the `visited` attribute of nodes in order to mark a node as True or False, in case you think it is useful.
  - **requirements: Dict[str, List[str]]:** Dictionary representing the requirements for classes. The key is a class, and the value is a list with the requirements for that class.
  - **return**: `True` if requirements added, else `False`
  - _Time Complexity: `O(n * m)`, where `n` is the number of requirements and `m` is the number of dependencies._
  - _Space Complexity: `O(n + m)` where `n` is the number of requirements and `m` is the number of dependencies._

- **checkSchedule(classes: List[List[str]]) -> bool**
  - Checks if the given classes form a valid schedule. Each inner list in the classes list represents the classes to be taken in a given semester. The first inner list is the first semester to be taken, and each following list is a following semester.
  - You can assume that after calling checkSchedule the function `unvisit_vertices` will be called on the `requirements` graph.
  - **classes: List[List[str]]:** Nested list with each inner list representing a semester. The list outer list is sorted in ascending semester order.
  - _Time Complexity: `O(n)`, where `n` is the total number of classes._
  - _Space Complexity: `O(n)` where `n` is the total number of classes._

- You CAN assume that all the classes given in the list will have been previously given in the `requirementsToAdd` argument.

### Example Cases:

```
r = {
  'CSE 231': [], #CSE 231 has no requirements, it is a freshman class
  'CSE 232': ['CSE 231'],
  'CSE 331': ['CSE 232'],
}

s = Schedule()

s.addRequirements(r) # Returns True

studentSchedule = [
  ['CSE 231'], ['CSE 232'], ['CSE 331']
]

s.checkSchedule(studentSchedule) # Returns true
s.requirements.unvisit_vertices()

wrongSchedule = [
  ['CSE 232'], ['CSE 231'], ['CSE 331']
]
s.checkSchedule(wrongSchedule) # Returns false
```

- In this next example the schedule has a cycle, so it is invalid.

```
r = {
  'CSE 231': [], #CSE 231 has no requirements, it is a freshman class
  'CSE 232': ['CSE 331'],
  'CSE 331': ['CSE 232'],
}

s = Schedule()

s.addRequirements(r) # Returns False
```

### Grading

The following 100-point rubric will be used to determine your grade on Project 6

- Policies

  - Using a different algorithm than the one specified for some function will result in the loss of all automated and manual points for that function.

- tests (70)

  - 1 - **bfs** : \_\_/12
  - 2 - **a_star** : \_\_/28
  - 3 - **jumanji_path** : \_\_/15
  - 4 - **addRequirements** : \_\_/10
  - 5 - **checkSchedule** : \_\_/5


- Manual (30)

  - Time and space complexity points are **all-or-nothing** for each function. If you fail to meet time or space complexity in a given function, you do not receive manual points for that function.
  - Manual points for each function require passing all tests for that function, except for the comprehensive tests.
  - Time & Space Complexity (30)
    - M1 - **bfs** :\_\_/6
      - _Time Complexity: O(V+E)_
      - _Space Complexity: O(V)_
    - M2 - **a_star**: \_\_/10
      - _Trust that our heuristic function is admissible, consistent and calculated in O(1) time._
      - _The log(V) comes from using a priority queue._
      - _Time Complexity: O((V + E)log(V))_
      - _Space Complexity: O(V)_
    - M3 - **jumanji_path**:\_\_/4
      - _Time Complexity: `O(w*h*log(w*h))`, where `w` is the grid width and `h` is the grid height._
      - _Space Complexity: `O(w*h)`._
    - M4 - **addRequirements**:\_\_/5
      - _Time Complexity: `O(n * m)`, where `n` is the number of requirements and `m` is the number of dependencies._
      - _Space Complexity: `O(n + m)` where `n` is the number of requirements and `m` is the number of dependencies._
    - M5 - **checkSchedule**:\_\_/5
      - _Time Complexity: `O(n)`, where `n` is the total number of classes._
      - _Space Complexity: `O(n)` where `n` is the total number of classes._

# **Submission Guidelines**

### **Deliverables:**

For each project, a `solution.py` file will be provided. Ensure to write your Python code within this file. For best results:

- 📥 **Download** both `solution.py` and `tests.py` to your local machine.
- 🛠️ Use **PyCharm** for a smoother coding and debugging experience.

### **How to Work on a Project Locally:**

Choose one of the two methods below:

---

#### **APPROACH 1: Using D2L for Starter Package**

1. 🖥️ Ensure PyCharm is installed.
2. 📦 **Download** the starter package from the _Projects_ tab on D2L. _(See the tutorial video on D2L if needed)_.
3. 📝 Write your code and, once ready, 📤 **upload** your `solution.py` to Codio. _(Refer to the D2L tutorial video for help)_.

---

#### **APPROACH 2: Directly from Codio**

1. 📁 On your PC, create a local folder like `Project01`.
2. 📥 **Download** `solution.py` from Codio.
3. 📥 **Download** `tests.py` from Codio for testing purposes.
4. 🛠️ Use PyCharm for coding.
5. 📤 **Upload** the `solution.py` back to Codio after ensuring the existing file is renamed or deleted.
6. 🔚 Scroll to the end in Codio's Guide editor and click the **Submit** button.

---

### **Important:**

- Always **upload** your solution and **click** the 'Submit' button as directed.
- All project submissions are due on Codio. **Any submission after its deadline is subject to late penalties** .

**Tip:** While Codio can be used, we recommend working locally for a superior debugging experience in PyCharm. Aim to finalize your project locally before submitting on Codio.

Please submit your solution.py by Nov 22nd 9:00 pm. Click Submit and Mark Complete.

### Congratulations on Finishing your Last Project!

- [What time is it?!](https://youtu.be/3hOP7qPDyI4)

**Important reminder**

Note students can not use Chegg or similar sites, see syllabus for details, use of outside resources for the application problem is strictly forbidden, use of outside resources is limited to max of 2 functions in a project.

    * **DOCSTRING** is not provided for this project. Please use Project 1 as a template for your DOCSTRING .
    To learn more on what is a DOCSTRING visit the following website: [What is Docstring?](https://peps.python.org/pep-0257/)
      * One point per function that misses DOCSTRING.
      * Up to 5 points of deductions

<input type="checkbox"> <b>STEP 1 :Rename the old solution file by clicking Rename button below. This button renames your file to **solution_old.py** </b>
{Rename}(mv solution.py solution_old.py)

<input type="checkbox"> <b>STEP 2 : Refresh your file tree by clicking on the refresh button under project name or refresh your browser. </b>

<input type="checkbox"> <b>STEP 3 : Upload your **solution.py** from your computer to Codio File Tree on the left. Refresh your file tree or browser to see if it actually updated the solution.py </b>

<input type="checkbox"> <b>STEP 4:Submit your code, by clicking the Submit button, you can submit as many times as you like, no limit on submission.

Submit button is tied to tests.py in our secure folder, and it always gets the updated version of the tests.py. In case of any tests.py update, students will always get the latest version to test their code through the submit button.
{SUBMIT!|assessment}(test-3379255259)
Please note that there will be manual grading after you submit your work. Clicking Submit only runs the Auto-grader for the test cases. Manual Grading is 30 points in this project. (30 pts for Run Time and Space complexity

<input type="checkbox"> <b>STEP 5: Please make sure to **scroll all the way down on Guide Editor page**, Guide is the specs document, it is the document you are reading right now, scroll all the way down, and **click at the Mark as Completed button**, see below for the image of the button so you know what it looks like. Please scroll down and actually push the button. If you do not mark complete yourself, Codio will mark it at the end of the last penalty day, which will give 0 to your project. </b>


This project is created by Joel Nataren, Arnav Deol, David Rackerby, and Aman Thamminana, adapted from the work by Adam Kasumovic, Brooke Osterkamp, Andrew Haas, Tanawan Premsri, and Andrew McDonald.
