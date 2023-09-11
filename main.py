import tkinter as tk
from tkinter import ttk
import random
import matplotlib.cm as cm
import numpy as np
from scipy.spatial import KDTree
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Start Screen")
        
        # Set screen size and font size
        window_width = 1920
        window_height = 1080
        self.root.geometry(f"{window_width}x{window_height}")

        # Create a canvas for the start screen with background color
        self.canvas = tk.Canvas(root, width=window_width, height=window_height, bg='#222')
        self.canvas.pack()

        # Create a label for the title
        title_label = tk.Label(root, text="Agent-Based SIR Model Simulator - Ball", font=('Arial', 32, 'bold'), bg='#222', fg='white')
        title_label.place(relx=0.5, rely=0.3, anchor='center')

        # Create buttons with adjusted font size and custom colors
        button_font = ('Arial', 18, 'bold')  # Adjust the font size and make it bold
        about_button = tk.Button(root, text="About", command=self.show_about, font=button_font, bg='#3498db', fg='white')
        start_button = tk.Button(root, text="Start Simulation", command=self.start_simulation, font=button_font, bg='#27ae60', fg='white')

        about_button.place(relx=0.5, rely=0.45, anchor='center')
        start_button.place(relx=0.5, rely=0.55, anchor='center')

    def show_about(self):
        # Open a new window for the About text
        about_window = tk.Toplevel(self.root)
        about_window.title("About")

        # Create a text widget with adjusted font size and custom colors
        text_font = ('Arial', 14)
        about_text = tk.Text(about_window, wrap=tk.WORD, width=80, height=20, font=text_font, bg='#222', fg='white')
        about_text.insert(tk.END, """
        Our submission for the 2023 hackathon is an exciting and educational infectious disease transmission simulator. We embarked on this journey with a brainstorming session, eager to tackle a problem that would both engage the judges and offer a real-world solution.

        Our initial discussions revolved around the choice of programming language and the concept of infectious disease transmission. As we delved deeper into the possibilities, it became clear that simulating disease transmission in a population was not only a fascinating challenge but also a relevant and important topic.

        We contemplated various aspects, including the programming language, 3D modeling, and the user experience. Our team members had different preferences, but ultimately, we decided to pursue this endeavor in Python, a language familiar to one of our team members.

        The core concept of our simulation revolves around allowing users to explore the dynamics of infectious disease transmission. We wanted to give them the ability to adjust various parameters such as the type of disease, population density, location of the initial infection, and the infectiousness of the disease (R0). This would enable users to see how different factors affect the spread of the disease over time.

        One of the challenges we faced was making the simulation user-friendly while maintaining complexity and accuracy. Users would be able to select different settings and observe how the disease spreads within a simulated population. However, we needed to strike a balance between making it accessible and informative without overwhelming users with complexity.

        In our discussions, we also considered alternative ideas, such as simulating ecosystem evolution, exploring problems like pollution and deforestation, or even simulating how a virus spreads throughout the human body. While these were intriguing ideas, we ultimately gravitated toward the infectious disease transmission simulator due to its real-world relevance and potential for educational value.

        To make the simulator more engaging and informative, we discussed the possibility of implementing genetic algorithms to simulate the evolution of the virus itself. This could add an extra layer of complexity and realism to the simulation, allowing users to witness how viruses adapt and evolve over time.

        As we fine-tuned our concept, we reached out to our team member, Alejandro Villa Floran, to gather his thoughts. Alejandro expressed his support for the infectious disease transmission simulation, noting that it could be a more straightforward and impactful project given our limited timeframe.

        Our current prototype demonstrates basic disease transmission with random motion, high infectivity, and no recovery. We have started to implement features like social distancing and plan to incorporate the concept of R0 (reproduction number) to make the simulation even more realistic.

        As we move forward, we're excited to refine our simulation, enhance the user experience, and create a tool that not only captures the judges' attention but also educates users about the dynamics of infectious diseases. We recognize that this project presents challenges, but we're committed to delivering a simulation that is both visually appealing and scientifically accurate.

        We're also considering setting up a GitHub repository to collaborate on the development and track our progress as we work towards our hackathon submission. Together, we hope to create a valuable and impactful simulation that addresses a pressing real-world issue.
        """)
        about_text.pack()

    def start_simulation(self):
        # Close the start screen and start the simulation
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    start_screen = StartScreen(root)
    root.mainloop()

class Status(Enum):
    SUSCEPTIBLE = 'S'
    INFECTED = 'I'
    RECOVERED = 'R'

# Agent - an individual "person" in the simulation
class Agent:
    """ An agent in the simulation with a status, position, and sociability """
    def __init__(self, status, x0, y0, sociability=0.5):
        self.status = status
        self.x = x0
        self.y = y0
        self.sociability = sociability
        if status == Status.INFECTED:
            self.recovers_at = random.randint(100, 200)

class SIRSimulatorUI:
    def __init__(self, root, total_population=1000, initial_infectious=1, beta=1, num_time_steps=1000, exposure_distance=50):
        self.root = root
        self.root.geometry("1400x900")  # Width x Height
        self.root.title("Agent-Based SIR Model Simulator - Ball")
        
        # Main frame to hold all other frames
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(side=tk.LEFT, padx=0, pady=0, fill=tk.BOTH, expand=True)

        # Canvas for simulation
        self.canvas = tk.Canvas(self.main_frame, width=800, bg='white')
        self.canvas.grid(row = 0, column=0, sticky='nsew')

        # Frame for Matplotlib graphs: 1x2 grid of subplots - one for SIR model, one for pie chart
        self.fig, (self.ax, self.pie_ax) = plt.subplots(2, 1, figsize=(3, 7))
        self.fig.subplots_adjust(hspace=0.75)  # Adjust the space between subplots
        self.canvas_fig = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas_fig.get_tk_widget().grid(row = 0, column=1, sticky='nsew')

        # Frame for Tkinter widgets
        self.frame = ttk.Frame(self.main_frame)
        
        # Checkbox for social distancing
        self.social_distancing = tk.BooleanVar()
        self.check_button = tk.Checkbutton(self.frame, text="Social Distancing", variable=self.social_distancing)
        self.check_button.pack()
        self.frame.grid(row=2, sticky='nsew')

        # Configure the grid system
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=8)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Generate random positions for agents
        self.positions = np.random.randint(0, 800, size=(total_population, 2))
        # Generate sociabilities from a normal distribution around 0.5
        self.sociabilities = np.random.normal(0.5, 0.1, size = total_population)
        # Create agents with initial status, position, and sociability
        self.agents = [Agent(Status.INFECTED, self.positions[i][0], self.positions[i][1], sociability=self.sociabilities[i]) if i < initial_infectious else Agent(Status.SUSCEPTIBLE, self.positions[i][0], self.positions[i][1], sociability=self.sociabilities[i]) for i in range(total_population)]
        self.beta = beta
        self.num_time_steps = num_time_steps
        self.current_step = 0
        self.exposure_distance = exposure_distance
        self.history = np.array([(total_population - initial_infectious), initial_infectious, 0]) 
        self.root.after(100, self.run_simulation)

    def agent_color(self, agent):
        """ Return the color of the agent based on its status """
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
        """ Update the UI with the current agent positions and status counts """
        if self.current_step % 2 != 0:  # Update UI every 2 steps
            return
        self.canvas.delete("all")
        
        if self.current_step % 10 == 0:  # Update graphs every 10 steps
            self.show_sir() 
            self.update_pie_chart()

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
        """ Run the simulation for one time step """
        if self.current_step >= self.num_time_steps: 
            return

        # Convert list of agents to numpy array for efficient computation
        agent_positions = self.positions
        agent_statuses = np.array([agent.status for agent in self.agents])
        infectious_agents = agent_statuses == Status.INFECTED
        susceptible_agents = agent_statuses == Status.SUSCEPTIBLE
        self.history = np.vstack((self.history, [np.sum(susceptible_agents), np.sum(infectious_agents), np.sum(agent_statuses == Status.RECOVERED)]))

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
        self.positions = np.clip(self.positions + movement, 0, 800)

        for i, agent in enumerate(self.agents):
            agent.x, agent.y = self.positions[i]
            
        self.update_ui()
        self.current_step += 1
        self.root.after(40, self.run_simulation)

    def show_sir(self):
        """ Create SIR model plot with matplotlib """
        self.ax.clear()
        history_arr = np.array(self.history)
        self.ax.plot(history_arr[:, 0], label='Susceptible')
        self.ax.plot(history_arr[:, 1], label='Infected')
        self.ax.plot(history_arr[:, 2], label='Recovered')
        self.ax.legend()
        self.ax.set_title("History")
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Population")
        self.canvas_fig.draw()
    
    def update_pie_chart(self):
        """Update the pie chart based on the current status counts."""
        self.pie_ax.clear()

        history_arr = np.array(self.history)
        counts = {'S': history_arr[-1, 0], 'I': history_arr[-1, 1], 'R': history_arr[-1, 2]}
        
        # Labels for the sections of our pie chart
        labels = ['Susceptible', 'Infected', 'Recovered']
        sizes = [counts['S'], counts['I'], counts['R']]
        
        self.pie_ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        self.pie_ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

        self.pie_ax.set_title("Current Distribution")
        self.canvas_fig.draw()

if __name__ == "__main__":
    root = tk.Tk()
    ui = SIRSimulatorUI(root)
    root.mainloop()