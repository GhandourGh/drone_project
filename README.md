# Drone Project - Multi-Drone Path Planning System

A Python-based multi-drone navigation system that coordinates multiple drones to efficiently visit targets while avoiding no-fly zones (NFZs) on a grid map with real-time visualization and battery management.

## 📋 Project Overview

This system simulates multiple autonomous drones navigating a 2D grid to reach designated targets while:
- Avoiding no-fly zones (NFZs)
- Managing battery constraints
- Using A* pathfinding for optimal routing
- Providing real-time animated visualization
- Coordinating task assignment among multiple drones

## 🗂️ Project Structure

```
drone_project/
├── main.py              # Entry point for multi-drone simulation
├── config.py            # Configuration parameters (grid size, battery, file paths)
├── navigator.py         # Multi-drone coordination and task assignment logic
├── movement_utils.py    # A* pathfinding and grid movement utilities
├── grid_utils.py        # Grid boundary checks and NFZ mask generation
├── io_files.py          # CSV file loading for drones, targets, and NFZs
├── visualize.py         # Matplotlib-based real-time animation
└── data/                # Data directory for CSV input files
    ├── drones.csv       # Drone starting positions
    ├── targets.csv      # Target coordinates
    └── nfzs.csv         # No-fly zone boundaries
```

## 🔧 Core Components

### 1. **main.py**
The main entry point that orchestrates the entire simulation:
- Loads drone starting positions, targets, and NFZs from CSV files
- Initializes the grid and NFZ mask
- Sets up real-time visualization
- Runs the tick-based multi-drone simulation
- Displays summary statistics for each drone

### 2. **config.py**
Centralized configuration settings:
- `GRID_ROWS`: Grid height (default: 20)
- `GRID_COLS`: Grid width (default: 20)
- `BATTERY_CAPACITY_STEPS`: Maximum moves per drone (default: 30)
- Data file paths configuration

### 3. **navigator.py**
Multi-drone coordination using a tick-based system:
- **Dynamic Task Assignment**: Idle drones are assigned to the nearest unassigned target
- **Tick-Based Movement**: Each tick, every drone moves one step toward its target
- **Battery Management**: Tracks battery consumption per step; warns when battery ≤ 20%
- **Target Numbering**: Assigns stable IDs to targets based on input order
- **Reports Generation**: Records success/failure and steps taken for each target

**Key Algorithm**:
1. At each tick, idle drones claim the nearest available target
2. Assigned drones compute one A* step toward their target
3. On reaching a target, the drone is freed and records the result
4. Continues until all targets are reached or constraints are met

### 4. **movement_utils.py**
Pathfinding and navigation utilities:
- **A* Algorithm**: Implements A* pathfinding with Manhattan distance heuristic
- **Grid Navigation**: 4-directional movement (Up, Down, Left, Right)
- **Obstacle Avoidance**: Respects NFZ boundaries during pathfinding
- **Neighbor Generation**: Validates neighboring cells for bounds and NFZs

**Key Functions**:
- `a_star_path(start, goal, nfz_mask)`: Returns shortest path or None
- `a_star_next_step(current, target, nfz_mask)`: Returns next cell in path
- `manhattan(a, b)`: Calculates Manhattan distance between two points

### 5. **grid_utils.py**
Grid management and validation:
- **Boundary Checking**: Validates coordinates are within grid bounds
- **NFZ Mask Generation**: Creates boolean mask from NFZ rectangles
- **Start/Target Validation**: Ensures valid starting positions and filters unreachable targets

### 6. **io_files.py**
CSV data loading with robust error handling:
- **Multi-Drone Loading**: Reads multiple drone starting positions from `drones.csv`
- **Target Loading**: Parses target coordinates from `targets.csv`
- **NFZ Loading**: Processes no-fly zone rectangles from `nfzs.csv`
- **Silent Error Handling**: Gracefully handles missing or malformed files

**CSV Formats**:
- `drones.csv`: Each row is `row,col` (one per drone)
- `targets.csv`: Each row is `row,col` (one per target)
- `nfzs.csv`: Each row is `r1,c1,r2,c2` (rectangle corners)

### 7. **visualize.py**
Real-time Matplotlib animation:
- **Multi-Drone Trails**: Color-coded paths for each drone
- **Target Markers**: Blue stars for targets; purple when reached
- **NFZ Visualization**: Red semi-transparent rectangles
- **Battery Display**: Real-time battery percentage for each drone
- **Interactive Legend**: Shows all drones, targets, and NFZs
- **Dynamic Updates**: Smooth animation with configurable pause intervals

## 🚀 How to Run

### Prerequisites
```bash
pip install numpy matplotlib
```

### Setup Data Files

Create a `data/` directory with three CSV files:

**data/drones.csv** (drone starting positions):


**data/targets.csv** (target coordinates):


**data/nfzs.csv** (no-fly zones as rectangles):


### Run the Simulation
```bash
python main.py
```

## 🎯 System Logic

### Task Assignment Strategy
- **Greedy Nearest Assignment**: Each idle drone selects the closest unassigned target
- **Dynamic Reassignment**: Drones are reassigned after completing or failing a task
- **Collision Avoidance**: Multiple drones can be assigned different targets simultaneously

### Battery Management
- Each movement step consumes 1 battery unit
- Critical warning at ≤20% battery
- Drones stop moving when battery reaches 0
- Battery status displayed in real-time

### Pathfinding
- **Algorithm**: A* with Manhattan heuristic (optimal for grid-based 4-directional movement)
- **Obstacle Handling**: NFZs are avoided during path calculation
- **Unreachable Targets**: System detects and reports blocked targets

### Simulation Flow
1. Load configuration and data files
2. Initialize grid with NFZ mask
3. Set up visualization
4. Enter tick-based loop:
   - Assign idle drones to nearest targets
   - Move each drone one step toward its target
   - Update battery and visualization
   - Mark targets as reached
5. Display final statistics

## 📊 Output

### Console Output
```
Multi-drone: 3 drones | 4 targets | 2 NFZs
Grid: 20x20
Drone 1: reached Target 1 in 10 steps
Drone 2: reached Target 2 in 8 steps
Drone 1: critical battery ≤ 20%
Drone 3: cannot reach Target 3
Drone 1: reached 2 targets | final (15, 15) | battery 5%
Drone 2: reached 1 targets | final (10, 10) | battery 22%
Drone 3: reached 0 targets | final (19, 0) | battery 30%

✅ Animation complete! Close the window to exit.
```

### Visual Output
- Real-time animated map showing drone movements
- Color-coded paths for each drone
- Battery indicators below the plot
- Legend with all entities
- Interactive window that stays open after completion

## ⚙️ Configuration Options

Edit `config.py` to customize:
- **Grid Size**: Adjust `GRID_ROWS` and `GRID_COLS`
- **Battery Capacity**: Modify `BATTERY_CAPACITY_STEPS`
- **Data Paths**: Change file locations if needed

Edit `main.py` to customize:
- **Number of Drones**: Change `expected=3` in `load_multi_starts()`
- **Animation Speed**: Adjust `pause_sec=0.02` in `on_step` callback
- **Max Steps**: Modify `max_steps_per_target` calculation

## 🔍 Key Features

✅ **Multi-Drone Coordination**: Efficient task distribution among multiple drones  
✅ **Optimal Pathfinding**: A* algorithm ensures shortest paths  
✅ **Real-Time Visualization**: Animated Matplotlib display  
✅ **Battery Constraints**: Realistic energy management  
✅ **Obstacle Avoidance**: NFZ detection and avoidance  
✅ **Robust Error Handling**: Graceful handling of invalid data  
✅ **Modular Design**: Clean separation of concerns  
✅ **Tick-Based Simulation**: Synchronized drone movements  

## 🛠️ Technical Details

- **Language**: Python 3
- **Dependencies**: NumPy, Matplotlib
- **Pathfinding**: A* with Manhattan distance heuristic
- **Movement Model**: 4-directional grid (no diagonals)
- **Coordination**: Greedy nearest-target assignment
- **Visualization**: Matplotlib with interactive mode

## 📝 Notes

- Targets inside NFZs are automatically filtered out
- Drones starting in invalid positions default to (0,0)
- If fewer drones than expected are defined, the system pads with the first drone's position
- CSV files can include comments (lines starting with `#`)
- Empty or malformed CSV rows are silently skipped

## 🔮 Future Enhancements

- Dynamic NFZ updates during simulation
- Advanced coordination algorithms (e.g., auction-based)
- 3D grid support
- Battery recharging stations
- Priority-based target assignment
- Collision avoidance between drones
- Multiple drone types with different capabilities

---

**Author**: GhandourGh  
**License**: Open Source  
**Repository**: https://github.com/GhandourGh/drone_project

This project is open source and available under the MIT License.

## Author

[GhandourGh](https://github.com/GhandourGh)