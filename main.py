import tkinter as tk
import random

class Agent:
    def __init__(self, status):
        self.status = status  # 'S' for Susceptible, 'I' for Infectious, 'R' for Recovered
        self.x = random.randint(0, 400)
        self.y = random.randint(0, 400)

class SIRSimulatorUI:
    def __init__(self, root, total_population=1000, initial_infectious=1, beta=0.25, gamma=0.0005, num_time_steps=1000):
        self.root = root
        self.root.title("Agent-Based SIR Model Simulator")

        # Create Canvas
        self.canvas = tk.Canvas(root, width=400, height=400, bg='white')
        self.canvas.pack()

        self.agents = [Agent('I') if i < initial_infectious else Agent('S') for i in range(total_population)]

        self.beta = beta
        self.gamma = gamma
        self.num_time_steps = num_time_steps

        self.current_step = 0
        self.root.after(0, self.run_simulation)

    def update_ui(self):
        self.canvas.delete("all")

        susceptible_count = 0
        infected_count = 0
        recovered_count = 0
        
        for agent in self.agents:
            color = 'blue' if agent.status == 'S' else 'red' if agent.status == 'I' else 'green'
            self.canvas.create_oval(agent.x, agent.y, agent.x+5, agent.y+5, fill=color)
            
            if agent.status == 'S':
                susceptible_count += 1
            elif agent.status == 'I':
                infected_count += 1
            elif agent.status == 'R':
                recovered_count += 1

        canvas_height = self.canvas.winfo_height()

        # Add shadow behind the labels to make them easier to read
        self.canvas.create_rectangle(0, canvas_height - 50, 50, canvas_height, fill='white', outline='white')

        # Add labels of the susceptible, infected, and recovered population
        self.canvas.create_text(10, canvas_height - 30, text=f"S: {susceptible_count}", fill='blue', anchor='sw')
        self.canvas.create_text(10, canvas_height - 20, text=f"I: {infected_count}", fill='red', anchor='sw')
        self.canvas.create_text(10, canvas_height - 10, text=f"R: {recovered_count}", fill='green', anchor='sw')


    def run_simulation(self):
        print(self.current_step)
        if self.current_step >= self.num_time_steps:
            return

        for agent in self.agents:
            if agent.status == 'I':
                for other_agent in self.agents:
                    if other_agent.status == 'S':
                        distance = ((agent.x - other_agent.x)**2 + (agent.y - other_agent.y)**2)**0.5
                        if distance < 10:  # Threshold for considering an interaction
                            if random.random() < self.beta:
                                other_agent.status = 'I'
                if random.random() < self.gamma:
                    agent.status = 'R'
                
            # Move the agents randomly
            agent.x += random.randint(-2, 2)
            agent.y += random.randint(-2, 2)
            
            # Boundary conditions
            agent.x = max(min(agent.x, 400), 0)
            agent.y = max(min(agent.y, 400), 0)
            
        self.update_ui()
        self.current_step += 1
        self.root.after(40, self.run_simulation)

if __name__ == "__main__":
    root = tk.Tk()
    ui = SIRSimulatorUI(root)
    root.mainloop()
