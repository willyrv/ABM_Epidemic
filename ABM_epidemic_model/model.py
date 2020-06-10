from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import pandas as pd

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return 1 + (1 / N) - 2 * B

def epidemy_state(model):
    agents_states = [agent.state for agent in model.schedule.agents]
    data = pd.DataFrame({'susceptible':[agents_states.count("susceptible")],
                         'exposed': [agents_states.count("exposed")],
                         'infected': [agents_states.count("infected")],
                         'recovered': [agents_states.count("recovered")]})
    return data

def get_num_susceptible(model):
    agents_states = [agent.state for agent in model.schedule.agents]
    return agents_states.count("susceptible")

def get_num_exposed(model):
    agents_states = [agent.state for agent in model.schedule.agents]
    return agents_states.count("exposed")

def get_num_infected(model):
    agents_states = [agent.state for agent in model.schedule.agents]
    return agents_states.count("infected")

def get_num_recovered(model):
    agents_states = [agent.state for agent in model.schedule.agents]
    return agents_states.count("recovered")

class EpidemicModel(Model):
    """A simple model of an epidemic otubreak where agents 
    move inside a small city at random.

    The state of the agents is either "susceptible", "exposed", "infected" or
    "recovery". All the agents begin with state "susceptible", and each time step 
    can move to somewhere inside the grid. If one infected agent is in the same 
    cell with other "susceptible", he can be infected with some probability. The
    infected agent moves to state "exposed" and stay ther for some time, then he 
    goes to state "infected" until he gets "recovered" or die. 
    """

    def __init__(self, N=100, infection_rate=0.05, first_infection_time = 10,
                 incubation_period = 20, recover_period = 100, 
                 width=10, height=10):
        self.num_agents = N
        self.infection_rate = infection_rate
        self.first_infection_time = first_infection_time
        self.incubation_period = incubation_period
        self.recover_period = recover_period
        self.grid = MultiGrid(height, width, True)
        self.schedule = RandomActivation(self)
        self.datacollector = DataCollector(
            model_reporters={
                "Susceptibles": get_num_susceptible,
                "Exposed": get_num_exposed,
                "Infected": get_num_infected,
                "Recovered": get_num_recovered}, 
            agent_reporters={"State": "state"}
        )
        # Create agents
        for i in range(self.num_agents):
            a = Person(i, self)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        # Infection is introduced
        if self.schedule.time == self.first_infection_time:
            infected_person = self.random.choice(self.schedule.agents)
            infected_person.state = "exposed"        
        self.schedule.step()
        # Do the infections between agents in the same cell
        # This part can be improved in order to be faster
        for s in self.grid.__iter__():
            if len(s) > 0:
                infecteds = []
                susceptibles = []
                for a in s:
                    if a.state == "infected":
                        infecteds.append(a)
                    if a.state == "susceptible":
                        susceptibles.append(a)
                p = self.infection_rate
                for s in susceptibles:
                    if self.random.random() < 1 - p**len(infecteds):
                        s.state = "exposed"
        # collect data
        self.datacollector.collect(self)

    def run_model(self, n):
        for i in range(n):
            self.step()

class Person(Agent):
    """An agent with some state."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "susceptible"
        self.time_since_infection = 0

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def step(self):
        if self.state != "susceptible":
            self.time_since_infection += 1
        if (self.state == "exposed") & \
                (self.time_since_infection > self.model.incubation_period):
            self.state = "infected"
        if (self.state == "infected") & \
                (self.time_since_infection > self.model.recover_period):
            self.state = "recovered"
        self.move()



class MoneyAgent(Agent):
    """ An agent with fixed initial wealth."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1

    def give_money(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if len(cellmates) > 1:
            other = self.random.choice(cellmates)
            other.wealth += 1
            self.wealth -= 1

    def step(self):
        self.move()
        if self.wealth > 0:
            self.give_money()
