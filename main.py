import random
import math

class Drone:
    def __init__(self, id, x, y, decision_function):
        self.id = id
        self.x = x
        self.y = y
        self.make_decision = decision_function
        self.destination = None
        self.radius = 0.5  # Drone's physical size
        self.safe_distance = 2 * self.radius  # Minimum safe distance between drones

class Simulation:
    def __init__(self, num_drones, sources, destinations):
        self.drones = []
        self.sources = sources
        self.destinations = destinations
        
        for i in range(num_drones):
            source = random.choice(sources)
            self.drones.append(Drone(i, source[0], source[1], self.default_decision))
    
    def default_decision(self, drone, neighbors):
        if drone.destination is None:
            drone.destination = random.choice(self.destinations)
        
        dx = drone.destination[0] - drone.x
        dy = drone.destination[1] - drone.y
        distance = math.sqrt(dx**2 + dy**2)
        
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
        magnitude = math.sqrt(final_dx**2 + final_dy**2)
        if magnitude > 0:
            final_dx, final_dy = final_dx / magnitude, final_dy / magnitude
        
        return final_dx, final_dy
    
    def avoid_collisions(self, drone, neighbors):
        avoid_dx, avoid_dy = 0, 0
        for other in neighbors:
            dx = drone.x - other.x
            dy = drone.y - other.y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < drone.safe_distance:
                # Calculate repulsion force (inverse square law)
                force = (drone.safe_distance - distance) ** 2
                avoid_dx += (dx / distance) * force
                avoid_dy += (dy / distance) * force
        
        # Normalize avoidance vector
        magnitude = math.sqrt(avoid_dx**2 + avoid_dy**2)
        if magnitude > 0:
            avoid_dx, avoid_dy = avoid_dx / magnitude, avoid_dy / magnitude
        
        return avoid_dx, avoid_dy
    
    def run(self, steps):
        for _ in range(steps):
            for drone in self.drones:
                neighbors = [d for d in self.drones if d != drone]
                dx, dy = drone.make_decision(drone, neighbors)
                drone.x += dx
                drone.y += dy
            
            self.display()
    
    def display(self):
        # Implement visualization logic here
        pass

# Example usage remains the same
