#Autonomous Agricultural Drone Simulation

#Overview

This project is a fully autonomous agricultural drone simulation developed using Unreal Engine 4.27, **Microsoft AirSim**, and **Python AI mission logic**.

The purpose of the simulation is to demonstrate how an autonomous UAV can:
- survey a crop field,
- detect diseased crops,
- prioritise treatment targets intelligently,
- make autonomous navigation decisions,
- and visualise tactical mission data in real time through a live command-and-control UI.

The system combines:
- autonomous AI behaviour,
- real-time telemetry,
- tactical visualisation,
- environmental state management,
- and autonomous crop treatment procedures.

The simulation was built entirely inside Unreal Engine 4.27 using AirSim as the UAV simulation layer and Python as the autonomous mission controller.


#Core Features

Autonomous UAV Behaviour

The drone operates completely autonomously once the simulation begins.

The UAV:
- takes off independently,
- explores the crop field,
- scans surrounding crops,
- detects diseased regions,
- prioritises treatment targets,
- navigates between locations,
- sprays infected crops,
- updates tactical telemetry live,
- and finally returns home and lands automatically.

No manual piloting is required.



#Crop Disease Simulation

The crop field consists of a 5x5 grid of crop cells.

At the beginning of every simulation:
- the system randomly generates multiple disease hotspots,
- disease severity spreads outward from hotspot centres,
- and each crop receives a dynamically generated health state.

Each crop can exist in one of four health categories:

| State | Meaning |
|---|---|
| Healthy | No disease detected |
| Mild | Early-stage disease |
| Unhealthy | Significant infection |
| Very Bad | Critical infection |

Disease severity is visually represented using dynamic material changes inside Unreal Engine.



#AI Perception System

The drone does not immediately know the state of the entire field.

Instead, the system simulates perception-based exploration.

The AI maintains several internal memory systems:

| System | Purpose |
|---|---|
| known_cells | Crops already discovered |
| visited_cells | Crops already treated |
| task_queue | Pending treatment targets |
| exploration_targets | Unknown unexplored regions |

The drone explores the field incrementally and discovers crop states dynamically during flight.

This creates more realistic autonomous behaviour compared to hardcoded omniscient pathing systems.



#Intelligent Decision-Making System

The AI mission logic is entirely controlled through Python.

The drone continuously evaluates:
- nearby crop health,
- infection severity,
- target distance,
- queue priority,
- and mission efficiency.

When diseased crops are discovered:
- they are inserted into a dynamic task queue,
- sorted by infection priority,
- and processed autonomously.

The prioritisation system favours:
1. higher infection severity,
2. shorter travel distance,
3. untreated targets.

This allows the UAV to behave more intelligently than simple sequential waypoint systems.



#Mission Phases

The drone operates through several autonomous mission phases.

## 1. Initialisation Phase

During startup:
- AirSim connects,
- crop states are generated,
- disease hotspots are created,
- tactical telemetry is initialised,
- and the drone arms automatically.

---

#2. Takeoff Phase

The UAV:
- arms,
- lifts off,
- ascends to operational altitude,
- and transitions into exploration mode.

---

#3. Exploration Phase

The drone scans surrounding regions using a local perception radius.

Healthy crops are ignored permanently.

Diseased crops are:
- classified,
- added to the task queue,
- and prioritised for treatment.

---

#4. Priority Targeting Phase

The AI sorts detected targets according to:
- disease severity,
- and navigation efficiency.

The drone then selects the highest-priority target autonomously.

---

#5. Navigation Phase

The UAV:
- navigates to the selected crop,
- stabilises above the target,
- and prepares for treatment.

---

## 6. Spraying Phase

The drone sprays the diseased crop.

Spray intensity varies dynamically depending on infection severity:

| Health State | Spray Intensity |
|---|---|
| Mild | 30% |
| Unhealthy | 60% |
| Very Bad | 100% |

After treatment:
- the crop visually returns to healthy status,
- the tactical map updates,
- and AI memory systems are updated accordingly.

---

## 7. Return Home Phase

After all targets are processed:
- the UAV returns to the launch area,
- descends safely,
- lands autonomously,
- and disarms.

---

#Tactical Command-and-Control UI

A real-time tactical UI was developed entirely inside Unreal Engine using UMG widgets.

The interface displays:
- drone status,
- active target,
- crop health,
- spray intensity,
- treatment queue size,
- spray count,
- and a live tactical crop grid.



#Live Tactical Grid

The tactical map is a fully dynamic 2D battlefield-style grid.

Each tile represents a crop region in the environment.

Tile colours update live according to crop health state:

| Colour | Meaning |
|---|---|
| Green | Healthy |
| Yellow | Mild |
| Orange | Unhealthy |
| Red | Very Bad |
| Grey | Unknown / unexplored |

The tactical display updates continuously using live telemetry transferred from Python into Unreal Engine.



#Telemetry System

The simulation includes a custom telemetry bridge between Python and Unreal Engine.

Python writes mission telemetry into a JSON file containing:
- drone state,
- target information,
- crop health,
- tactical map data,
- spray intensity,
- and mission statistics.

A custom Unreal Engine C++ Blueprint Function Library reads the telemetry in real time and exposes it to Blueprint systems.

This allows:
- live UI updates,
- tactical rendering,
- and real-time mission monitoring.



#Technologies Used

| Technology | Purpose |
|---|---|
| Unreal Engine 4.27 | Simulation environment |
| Microsoft AirSim | UAV simulation |
| Python | Autonomous AI logic |
| C++ | Unreal telemetry integration |
| Blueprint | UI and tactical rendering |
| UMG | Real-time interface |
| JSON | Telemetry communication |

---

#Recreating the Project

#Requirements

Before recreating the project, install:

- Unreal Engine 4.27
- Microsoft AirSim
- Python 3
- Ubuntu Linux (recommended)


#Step 1 — Install Unreal Engine 4.27

Clone and build Unreal Engine 4.27 from Epic Games source.



#Step 2 — Install AirSim

Clone the Microsoft AirSim repository:

git clone https://github.com/microsoft/AirSim.git

Step 3 — Open the Blocks Environment

Place the `Blocks` project folder inside:

AirSim/Unreal/Environments/

#Step 4 — Generate Project Files

Inside the Blocks directory:

GenerateProjectFiles.sh

#Step 5 — Build the Unreal Project

~/UE4.27/Engine/Build/BatchFiles/Linux/Build.sh BlocksEditor Linux Development ~/AirSim/Unreal/Environments/Blocks/Blocks.uproject

#Step 6 — Launch Unreal Engine

~/UE4.27/Engine/Binaries/Linux/UE4Editor ~/AirSim/Unreal/Environments/Blocks/Blocks.uproject

#Step 7 — Run the Python AI Script

Navigate to:

AirSim/PythonClient/multirotor

Run:

python3 agri_drone.py

#Step 8 — Start the Simulation

Inside Unreal Engine:
- press Play,
- launch the Python AI script,
- and observe the fully autonomous mission execution.

#Final Notes

This project demonstrates how autonomous UAV systems can combine:
- AI decision-making,
- environmental awareness,
- tactical visualisation,
- telemetry systems,
- and autonomous treatment behaviour

inside a fully simulated agricultural environment.

The system was designed to emulate realistic autonomous crop treatment operations while maintaining real-time visual feedback and mission transparency through a tactical command-and-control interface.
