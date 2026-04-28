"""
Traffic Control Simulation

This script simulates traffic flow through a 4-lane intersection.
Each lane gets a green light in sequence, allowing up to 10 cars
to pass per cycle.
"""

import numpy as np
from collections import deque


def initialize_lanes(n_cars: int = 300):
    """
    Initialize lanes with randomly assigned cars and directions.

    Args:
        n_cars (int): Total number of cars in the simulation.

    Returns:
        dict: Dictionary of lanes with queued cars.
    """
    dir_map = {0: "Left", 1: "Straight", 2: "Right"}
    lanes = {i: deque() for i in range(4)}

    for i in range(n_cars):
        lane = np.random.randint(0, 4)
        direction = dir_map[np.random.randint(0, 3)]
        lanes[lane].append((f"Car{i}", direction))

    return lanes


def print_lanes(lanes: dict):
    """Print the current state of all lanes."""
    print("Initial lane queues:")
    for lane, q in lanes.items():
        print(f"Lane {lane}: {list(q)}")


def run_simulation(lanes: dict):
    """
    Run the traffic light simulation.

    Args:
        lanes (dict): Dictionary of lanes with queued cars.
    """
    print("\n--- Traffic Control Simulation ---")

    lane_order = [0, 1, 2, 3]
    time_step = 0

    while any(lanes.values()):
        lane = lane_order[time_step % 4]
        print(f"\nGreen light for Lane {lane}")

        for _ in range(10):
            if not lanes[lane]:
                break

            car, direction = lanes[lane].popleft()
            print(f"{car} goes {direction}")

        time_step += 1

    print("\nAll cars have passed!")


def main():
    lanes = initialize_lanes(n_cars=300)
    print_lanes(lanes)
    run_simulation(lanes)


if __name__ == "__main__":
    main()
