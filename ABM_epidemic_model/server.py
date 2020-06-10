from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
from .model import EpidemicModel



# Green
SUSCEPTIBLE_COLOR = "#46FF33"
# Yellow
EXPOSED_COLOR = "#F3FA1E"
# Red
INFECTED_COLOR = "#FF3C33"
# Blue
RECOVERED_COLOR = "#A2A2A2"


def agent_portrayal(agent):
    portrayal = {"Shape": "circle", "Filled": "true", "r": 0.8}

    if agent.state == "susceptible":
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    elif agent.state == "exposed":
        portrayal["Color"] = "yellow"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.6
    elif agent.state == "infected":
        portrayal["Color"] = "red"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.4
    else:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 3
        portrayal["r"] = 0.2       
    return portrayal

model_params = {
    "N":  UserSettableParameter(
        "slider",
        "Number of agents",
        100,
        2,
        200,
        1,
        description="Choose how many agents to include in the model",
    ),
    "infection_rate":UserSettableParameter(
        "slider",
        "Number of agents",
        0.05,
        0,
        1,
        0.05,
        description="Choose the infection rate",
    ), 
    "first_infection_time":UserSettableParameter(
        "number",
        "First infection time", 
        value=10
    ),
    "incubation_period":UserSettableParameter(
        "number",
        "Incubation period", 
        value=2
    ), 
    "recover_period":UserSettableParameter(
        "number",
        "Recover period", 
        value=5
    ), 
    "height":UserSettableParameter(
        "number",
        "Number of rows", 
        value=10
    ),     
    "width":UserSettableParameter(
        "number",
        "Number of columns", 
        value=10
    ),  
}


# map data to chart in the ChartModule
line_chart = ChartModule(
    [
        {"Label": "Susceptibles", "Color": SUSCEPTIBLE_COLOR},
        {"Label": "Exposed", "Color": EXPOSED_COLOR},
        {"Label": "Infected", "Color": INFECTED_COLOR},
        {"Label": "Recovered", "Color": RECOVERED_COLOR},
    ]
)

grid = CanvasGrid(agent_portrayal, model_params["width"].value, 
                model_params["height"].value, 500, 500)
chart = ChartModule(
    [{"Label": "Outbreak Evolution", "Color": "#0000FF"}], data_collector_name="datacollector"
)

server = ModularServer(EpidemicModel, [grid, line_chart], 
                        "Epidemic outbreak", model_params)
server.port = 8521
