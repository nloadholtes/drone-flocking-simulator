import matplotlib

matplotlib.use("Qt5Agg")

import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Drone:
    def __init__(self, id, x, y, decision_function):
        self.id = id
        self.x = x
        self.y = y
        self.make_decision = decision_function
        self.destination = None
        self.radius = 0.5  # Drone's physical size
        self.safe_distance = 2 * self.radius  # Minimum safe distance between drones
        self.dead = False  # New attribute to track if the drone is 'dead'


class Simulation:
    def __init__(self, num_drones, sources, destinations):
        self.drones = []
        self.sources = sources
        self.destinations = destinations

        for i in range(num_drones):
            source = random.choice(sources)
            self.drones.append(Drone(i, source[0], source[1], self.default_decision))
        self.fig, self.ax = plt.subplots(figsize=(10, 10))
        self.scatter = None
        self.current_step = 0
        self.active_drones = self.drones.copy()  # Keep track of active drones

    def default_decision(self, drone, neighbors):
        if drone.destination is None:
            drone.destination = random.choice(self.destinations)

        dx = drone.destination[0] - drone.x
        dy = drone.destination[1] - drone.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance < 1:
            drone.destination = None
            return 0, 0

        # Normalize the direction vector
        dx, dy = dx / distance, dy / distance

        # Collision avoidance
        collision_dx, collision_dy = self.avoid_collisions(drone, neighbors)

        # Combine destination direction with collision avoidance
        # You can adjust these weights to change the behavior
        final_dx = 0.7 * dx + 0.3 * collision_dx
        final_dy = 0.7 * dy + 0.3 * collision_dy

        # Normalize the final direction
        magnitude = math.sqrt(final_dx ** 2 + final_dy ** 2)
        if magnitude > 0:
            final_dx, final_dy = final_dx / magnitude, final_dy / magnitude

        return final_dx, final_dy

    def avoid_collisions(self, drone, neighbors):
        avoid_dx, avoid_dy = 0, 0
        for other in neighbors:
            dx = drone.x - other.x
            dy = drone.y - other.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

            if distance < drone.safe_distance:
                # Calculate repulsion force (inverse square law)
                if distance == 0:
                    distance = 0.01
                force = (drone.safe_distance - distance) ** 2
                avoid_dx += (dx / distance) * force
                avoid_dy += (dy / distance) * force

        # Normalize avoidance vector
        magnitude = math.sqrt(avoid_dx ** 2 + avoid_dy ** 2)
        if magnitude > 0:
            avoid_dx, avoid_dy = avoid_dx / magnitude, avoid_dy / magnitude

        return avoid_dx, avoid_dy

    def check_collisions(self):
        for i, drone in enumerate(self.active_drones):
            if drone.dead:
                continue
            for other in self.active_drones[i + 1 :]:
                if other.dead:
                    continue
                distance = math.sqrt(
                    (drone.x - other.x) ** 2 + (drone.y - other.y) ** 2
                )
                if distance < drone.radius + other.radius:
                    drone.dead = True
                    other.dead = True
        self.active_drones = [drone for drone in self.active_drones if not drone.dead]

    def run(self, steps):
        def update(frame):
            self.current_step = frame
            for drone in self.active_drones:
                neighbors = [d for d in self.active_drones if d != drone]
                dx, dy = drone.make_decision(drone, neighbors)
                drone.x += dx
                drone.y += dy

            self.check_collisions()
            return self.display()

        self.animation = FuncAnimation(
            self.fig, update, frames=steps, interval=50, blit=True
        )
        plt.show()

    def display(self):
        if self.scatter:
            self.scatter.remove()

        x = [drone.x for drone in self.drones if not drone.dead]
        y = [drone.y for drone in self.drones if not drone.dead]

        self.scatter = self.ax.scatter(x, y, c="blue", s=50)

        # Plot dead drones
        dead_x = [drone.x for drone in self.drones if drone.dead]
        dead_y = [drone.y for drone in self.drones if drone.dead]
        self.ax.scatter(dead_x, dead_y, c="red", s=50, marker="x")

        # Plot sources and destinations
        sources_x, sources_y = zip(*self.sources)
        destinations_x, destinations_y = zip(*self.destinations)

        self.ax.scatter(
            sources_x, sources_y, c="green", s=100, marker="^", label="Sources"
        )
        self.ax.scatter(
            destinations_x,
            destinations_y,
            c="red",
            s=100,
            marker="s",
            label="Destinations",
        )

        self.ax.set_xlim(-5, 20)
        self.ax.set_ylim(-5, 20)
        self.ax.legend()
        self.ax.set_title(
            f"Drone Simulation (Step: {self.current_step}, Active: {len(self.active_drones)})"
        )

        return [self.scatter]


# Example usage remains the same
sources = [(0, 0), (0, 10), (10, 0)]
destinations = [(5, 5), (15, 15), (0, 15), (15, 0)]

sim = Simulation(10, sources, destinations)
sim.run(200)  # Run for 200 steps
