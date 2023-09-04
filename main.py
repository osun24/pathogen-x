import tkinter as tk
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Agent - an individual "person" in the simulation
class Agent:
    def __init__(self, status):
        self.status = status  # 'S' for Susceptible, 'I' for Infectious, 'R' for Recovered
        self.sociability = random.random()  # A number between 0 and 1 representing how sociable the agent is
        
        if status == 'I':
            self.recovers_at = random.randint(100, 200)  # The time step at which the agent will recover
        else:
            self.recovers_at = 0

        # Randomly initialize the position of the agent
        self.x = random.randint(0, 400) 
        self.y = random.randint(0, 400)

class SIRSimulatorUI:
    def __init__(self, root, total_population=1000, initial_infectious=1, beta=0.25, num_time_steps=1000):
        self.root = root
        self.root.title("Agent-Based SIR Model Simulator")

        # Create Canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()

        # Create a checkbox to enable social distancing
        self.social_distancing = tk.BooleanVar()  
        self.check_button = tk.Checkbutton(root, text="Social Distancing", variable=self.social_distancing)
        self.check_button.pack()

        # Create agents and define their initial status
        self.agents = [Agent('I') if i < initial_infectious else Agent('S') for i in range(total_population)]


        # Define the parameters of the simulation
        self.beta = beta # Probability of infection
        self.num_time_steps = num_time_steps # Number of time steps to run the simulation for

        self.current_step = 0
        self.root.after(100, self.run_simulation)

    def agent_color(self, agent):
        if agent.status == 'S':
            return 'blue'
        elif agent.status == 'I':
            stage = self.current_step/agent.recovers_at
            if (stage) < 0.2:
                colormap = cm.get_cmap("RdYlBu")
                color_interval = (1-stage)/0.2
            else: 
                colormap = cm.get_cmap("RdYlGn")
                if stage < 0.8:
                    color_interval = (stage-0.2)/0.6
                else: color_interval = stage
            rgba = colormap(color_interval)
            rgb = rgba[:3]
            rgb = [int(255 * x) for x in rgb]
            return '#%02x%02x%02x' % tuple(rgb)  # Unpack the list into individual arguments
        else:
            return 'green'

    def update_ui(self):
        self.canvas.delete("all")

        # Count the number of agents in each state
        susceptible_count = 0
        infected_count = 0
        recovered_count = 0
        
        for agent in self.agents:
            # Draw the agents on the canvas
            color = self.agent_color(agent)
            self.canvas.create_oval(agent.x, agent.y, agent.x+5, agent.y+5, fill=color)
            
            if agent.status == 'S':
                susceptible_count += 1
            elif agent.status == 'I':
                infected_count += 1
            elif agent.status == 'R':
                recovered_count += 1

        canvas_height = self.canvas.winfo_height()

        # Add a box behind the labels to make them easier to read
        self.canvas.create_rectangle(0, canvas_height - 50, 50, canvas_height, fill='white', outline='white')

        # Add a label for the current step
        self.canvas.create_text(10, canvas_height - 35, text=f"T: {self.current_step}", fill='black', anchor='sw')
        
        # Add labels of the susceptible, infected, and recovered population in the bottom left corner
        self.canvas.create_text(10, canvas_height - 25, text=f"S: {susceptible_count}", fill='blue', anchor='sw')
        self.canvas.create_text(10, canvas_height - 15, text=f"I: {infected_count}", fill='red', anchor='sw')
        self.canvas.create_text(10, canvas_height - 5, text=f"R: {recovered_count}", fill='green', anchor='sw')


    def run_simulation(self):
        if self.current_step >= self.num_time_steps: 
            return

        for agent in self.agents:
            if agent.status == 'I':
                for other_agent in self.agents:
                    if other_agent.status == 'S':
                        # Calculate the distance between the two agents
                        distance = ((agent.x - other_agent.x)**2 + (agent.y - other_agent.y)**2)**0.5

                        # If the distance is less than 10, then the two agents are close enough to infect
                        if distance < 10:  
                            if random.random() < self.beta: # Randomly infect the susceptible agent
                                other_agent.status = 'I'
                                other_agent.recovers_at = self.current_step + random.randint(100, 200) # Set the time to recovery to a random number between 100 and 200

                # Recover the agent after the specified number of time steps
                if agent.recovers_at <= self.current_step: 
                    agent.status = 'R'
                
            # Move the agents randomly, with a smaller movement if social distancing is enabled
            max_movement = 1 if self.social_distancing.get() else 5  
            agent.x += random.randint(-max_movement, max_movement)  
            agent.y += random.randint(-max_movement, max_movement)  
            
            # Boundary conditions
            agent.x = max(min(agent.x, 400), 0)
            agent.y = max(min(agent.y, 400), 0)
            
        self.update_ui()
        self.current_step += 1
        self.root.after(40, self.run_simulation) # Advance to the next step after 40 milliseconds

if __name__ == "__main__":
    root = tk.Tk()
    ui = SIRSimulatorUI(root)
    root.mainloop()
