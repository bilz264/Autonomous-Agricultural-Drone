import airsim
import time
import random
import json

# Connect to AirSim
client = airsim.MultirotorClient()
client.confirmConnection()

print("Connected!")

# Enable API control
client.enableApiControl(True)
client.armDisarm(True)

# Material paths
MATERIALS = {
    0: "/Game/Materials/M_Healthy.M_Healthy",
    1: "/Game/Materials/M_Mild.M_Mild",
    2: "/Game/Materials/M_Unhealthy.M_Unhealthy",
    3: "/Game/Materials/M_VeryBad.M_VeryBad"
}

# AirSim coordinates
positions = [-40, -20, 0, 20, 40]

# Crop state storage
crop_states = {}

# Spray metric
spray_count = 0

# Telemetry writer
def update_ui(status, target, health, intensity, queue, spray_count):

    telemetry = {
        "status": status,
        "target": target,
        "health": health,
        "intensity": intensity,
        "queue": queue,
        "spray_count": spray_count,
        "map": ""
    }

    # Build tactical map string
    map_data = []

    for y in positions:

        for x in positions:

            cell_name = f"Cell_{int(x*100)}_{int(y*100)}"

            # Unknown / unexplored
            if cell_name not in crop_states:
                map_data.append("4")

            else:
                state = crop_states[cell_name]
                map_data.append(str(state))

    telemetry["map"] = ",".join(map_data)

    with open("/home/user/AirSim/PythonClient/multirotor/drone_status.json", "w") as f:
        json.dump(telemetry, f)

# Initial UI state
update_ui(
    "INITIALISING",
    "NONE",
    "NONE",
    "0%",
    0,
    spray_count
)

print("\n🌱 Generating realistic crop disease map...")

# Generate TWO infection hotspots
hotspots = []

while len(hotspots) < 2:

    hx = random.choice(positions)
    hy = random.choice(positions)

    # Prevent hotspot on LaunchTile
    if hx == 0 and hy == 0:
        continue

    # Prevent duplicates
    if (hx, hy) not in hotspots:
        hotspots.append((hx, hy))

print("🦠 Infection hotspots:")

for hx, hy in hotspots:
    print(f"   -> Cell_{hx*100}_{hy*100}")

# Generate realistic disease spread
for x in positions:
    for y in positions:

        # Skip LaunchTile
        if x == 0 and y == 0:
            continue

        ux = int(x * 100)
        uy = int(y * 100)

        cell_name = f"Cell_{ux}_{uy}"

        # Find closest hotspot
        closest_distance = 999

        for hx, hy in hotspots:

            distance = abs(x - hx) + abs(y - hy)

            if distance < closest_distance:
                closest_distance = distance

        # Disease severity based on distance
        if closest_distance == 0:
            health = 3

        elif closest_distance <= 20:
            health = random.choice([2, 3])

        elif closest_distance <= 40:
            health = random.choice([1, 2])

        elif closest_distance <= 60:
            health = random.choice([0, 1])

        else:
            health = 0

        crop_states[cell_name] = health

        # Apply starting material
        client.simSetObjectMaterial(
            cell_name,
            MATERIALS[health]
        )

        time.sleep(0.05)

print("✅ Realistic crop map generated")

# Takeoff
print("\n🚁 Taking off...")

update_ui(
    "TAKING OFF",
    "LaunchTile",
    "NONE",
    "0%",
    0,
    spray_count
)

client.takeoffAsync().join()

# Move to altitude
client.moveToZAsync(-10, 5).join()

print("\n🧠 Starting perception-driven AI mission...")

# AI memory systems
known_cells = set()
visited_cells = set()
task_queue = []

current_position = (0, 0)

# Unknown exploration targets
exploration_targets = []

for x in positions:
    for y in positions:

        if x == 0 and y == 0:
            continue

        exploration_targets.append((x, y))

# Main AI mission loop
while exploration_targets or task_queue:

    print("\n🛰 Exploring nearby environment...")

    nearby_cells = []

    # Scan local area only
    for tx, ty in exploration_targets:

        distance = abs(tx - current_position[0]) + abs(ty - current_position[1])

        # Perception radius = 1 tile
        if distance <= 20:

            nearby_cells.append((tx, ty))

    # Discover nearby cells
    for x, y in nearby_cells:

        ux = int(x * 100)
        uy = int(y * 100)

        cell_name = f"Cell_{ux}_{uy}"

        if cell_name in known_cells:
            continue

        known_cells.add(cell_name)

        health = crop_states[cell_name]

        # Healthy cells ignored permanently
        if health == 0:

            print(f"✅ {cell_name} healthy")

            visited_cells.add(cell_name)

        else:

            print(f"👀 Diseased crop detected: {cell_name}")

            task_queue.append({
                "cell": cell_name,
                "x": x,
                "y": y,
                "health": health,
                "priority": health
            })

    # Remove discovered cells from unexplored list
    exploration_targets = [
        t for t in exploration_targets
        if f"Cell_{int(t[0]*100)}_{int(t[1]*100)}" not in known_cells
    ]

    # PRIORITY TREATMENT MODE
    if task_queue:

        print(f"📋 Queue: {len(task_queue)} waiting")

        # Intelligent sorting
        task_queue.sort(
            key=lambda t: (
                -t["priority"],
                abs(t["x"] - current_position[0]) +
                abs(t["y"] - current_position[1])
            )
        )

        target = task_queue.pop(0)

        cell_name = target["cell"]
        x = target["x"]
        y = target["y"]
        health = target["health"]

        # Prevent revisits
        if cell_name in visited_cells:
            continue

        print("🚨 Priority target acquired")
        print(f"📍 Target: {cell_name}")

        # AI spray decision
        if health == 3:
            state = "Very Bad"
            spray = 100

        elif health == 2:
            state = "Unhealthy"
            spray = 60

        else:
            state = "Mild"
            spray = 30

        update_ui(
            "TARGET ACQUIRED",
            cell_name,
            state,
            f"{spray}%",
            len(task_queue),
            spray_count
        )

        print(f"🌱 Health: {state}")
        print(f"💧 Intensity: {spray}%")

        print("➡️ Navigating to target...")

        update_ui(
            "NAVIGATING",
            cell_name,
            state,
            f"{spray}%",
            len(task_queue),
            spray_count
        )

        # Move drone
        client.moveToPositionAsync(
            x,
            y,
            -10,
            5
        ).join()

        client.hoverAsync().join()

        time.sleep(1)

        # Spray crop
        print("🚿 Spraying...")

        update_ui(
            "SPRAYING",
            cell_name,
            state,
            f"{spray}%",
            len(task_queue),
            spray_count
        )

        time.sleep(1.5)

        print("✔ Treatment complete")

        spray_count += 1

        # Heal crop visually
        for attempt in range(3):

            client.simSetObjectMaterial(
                cell_name,
                MATERIALS[0]
            )

            time.sleep(0.1)

        # Update AI memory
        visited_cells.add(cell_name)

        crop_states[cell_name] = 0

        current_position = (x, y)

    # EXPLORATION MODE
    elif exploration_targets:

        # Move toward nearest unknown cell
        exploration_targets.sort(
            key=lambda t:
            abs(t[0] - current_position[0]) +
            abs(t[1] - current_position[1])
        )

        x, y = exploration_targets[0]

        print("🧭 No priority targets")
        print(f"➡️ Exploring toward Cell_{int(x*100)}_{int(y*100)}")

        update_ui(
            "EXPLORING",
            f"Cell_{int(x*100)}_{int(y*100)}",
            "NONE",
            "0%",
            len(task_queue),
            spray_count
        )

        client.moveToPositionAsync(
            x,
            y,
            -10,
            5
        ).join()

        client.hoverAsync().join()

        time.sleep(1)

        current_position = (x, y)

# Return home
print("\n🏠 Returning home...")

update_ui(
    "RETURNING HOME",
    "LaunchTile",
    "NONE",
    "0%",
    0,
    spray_count
)

client.moveToPositionAsync(
    0,
    0,
    -10,
    4
).join()

client.hoverAsync().join()

time.sleep(2)

# Controlled descent
client.moveToZAsync(-3, 1).join()

time.sleep(1)

# Land
print("🛬 Landing...")

update_ui(
    "LANDING",
    "LaunchTile",
    "NONE",
    "0%",
    0,
    spray_count
)

client.landAsync().join()

# Cleanup
client.armDisarm(False)
client.enableApiControl(False)

update_ui(
    "MISSION COMPLETE",
    "NONE",
    "NONE",
    "0%",
    0,
    spray_count
)

print("✅ Mission complete")
