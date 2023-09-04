import tkinter as tk
import random
import matplotlib.cm as cm
import numpy as np
from scipy.spatial import KDTree
from enum import Enum

class Status(Enum):
    SUSCEPTIBLE = 'S'
    INFECTED = 'I'
    RECOVERED = 'R'

# Agent - an individual "person" in the simulation
class Agent:
    def __init__(self, status, x0, y0, sociability=0.5):
        self.status = status
        self.x = x0
        self.y = y0
        self.sociability = sociability
        if status == Status.INFECTED:
            self.recovers_at = random.randint(100, 200)

class SIRSimulatorUI:
    def __init__(self, root, total_population=10000, initial_infectious=1, beta=1, num_time_steps=1000, exposure_distance=50):
        self.root = root
        self.root.title("Agent-Based SIR Model Simulator - Ball")
        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()
        self.social_distancing = tk.BooleanVar()
        self.check_button = tk.Checkbutton(root, text="Social Distancing", variable=self.social_distancing)
        self.check_button.pack()
        self.positions = np.random.randint(0, 400, size=(total_population, 2))
        # Generate sociabilities from a normal distribution around 0.5
        self.sociabilities = np.random.normal(0.5, 0.1, size = total_population)
        # Create agents with initial status, position, and sociability
        self.agents = [Agent(Status.INFECTED, self.positions[i][0], self.positions[i][1], sociability=self.sociabilities[i]) if i < initial_infectious else Agent(Status.SUSCEPTIBLE, self.positions[i][0], self.positions[i][1], sociability=self.sociabilities[i]) for i in range(total_population)]
        self.beta = beta
        self.num_time_steps = num_time_steps
        self.current_step = 0
        self.exposure_distance = exposure_distance
        self.root.after(100, self.run_simulation)

    def agent_color(self, agent):
        if agent.status == Status.SUSCEPTIBLE:
            return 'blue'
        elif agent.status == Status.INFECTED:
            # Stage of infection as a percentage of recovery time
            stage = self.current_step/agent.recovers_at
            if (stage) < 0.3:
                # Set color to range from blue to yellow to red
                colormap = cm.get_cmap("RdYlBu")
                color_interval = 1-(stage/0.3)
            else: 
                colormap = cm.get_cmap("RdYlGn")
                # Set color to red 
                if stage < 0.9:
                    color_interval = 0
                else: 
                    color_interval = stage #set color to between yellow and green
            rgba = colormap(color_interval)
            rgb = rgba[:3]
            rgb = [int(255 * x) for x in rgb]
            return '#%02x%02x%02x' % tuple(rgb)  # Unpack the list into individual arguments to convert to HEX
        else:
            return 'green'

    def update_ui(self):
        if self.current_step % 2 != 0:  # Update UI every 10 steps
            return
        self.canvas.delete("all")
        counts = {'S': 0, 'I': 0, 'R': 0}
        
        agent_drawings = []
        for agent in self.agents:
            color = self.agent_color(agent)
            agent_drawings.append((agent.x, agent.y, color))
            counts[agent.status.value] += 1
            
        for x, y, color in agent_drawings:
            self.canvas.create_oval(x, y, x+5, y+5, fill=color)

        canvas_height = self.canvas.winfo_height()
        self.canvas.create_rectangle(0, canvas_height - 50, 50, canvas_height, fill='white', outline='white')
        self.canvas.create_text(10, canvas_height - 35, text=f"T: {self.current_step}", fill='black', anchor='sw')
        for idx, (status, color) in enumerate([('S', 'blue'), ('I', 'red'), ('R', 'green')]):
            self.canvas.create_text(10, canvas_height - (25 - idx * 10), text=f"{status}: {counts[status]}", fill=color, anchor='sw')

    def run_simulation(self):
        if self.current_step >= self.num_time_steps: 
            return

        # Convert list of agents to numpy array for efficient computation
        agent_positions = self.positions
        agent_statuses = np.array([agent.status for agent in self.agents])
        infectious_agents = agent_statuses == Status.INFECTED
        susceptible_agents = agent_statuses == Status.SUSCEPTIBLE

        # Calculate distances between each pair of agents using a KD-tree
        tree = KDTree(agent_positions)
        pairs = tree.query_ball_tree(tree, r=self.exposure_distance)  # Find pairs of agents within distance 10
        for i, pair in enumerate(pairs):
            for j in pair:
                if i<j and infectious_agents[i] and susceptible_agents[j] and random.random() < self.beta:
                    self.agents[j].status = Status.INFECTED
                    self.agents[j].recovers_at = self.current_step + random.randint(100, 200)

        # Update status of infectious agents to recovered if recovery time has passed
        for agent in self.agents:
            if agent.status == Status.INFECTED and self.current_step >= agent.recovers_at:
                agent.status = Status.RECOVERED

        # Adjust movements based on social distancing flag, sociability, and random movement
        max_movement = np.array([1, 1]) if self.social_distancing.get() else np.array([5, 5])
        movement = np.random.randint(-max_movement, max_movement + 1, size=(len(self.agents), 2))
        sociabilities = np.array(self.sociabilities).reshape(-1, 1) 
        movement = movement * sociabilities
        self.positions = np.clip(self.positions + movement, 0, 400)

        for i, agent in enumerate(self.agents):
            agent.x, agent.y = self.positions[i]
            
        self.update_ui()
        self.current_step += 1
        self.root.after(40, self.run_simulation)

if __name__ == "__main__":
    root = tk.Tk()
    ui = SIRSimulatorUI(root)
    root.mainloop()