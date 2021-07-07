from os import listdir, path
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from .model import FireEvacuation
from .agent import FireExit, Wall, Furniture, Fire, Smoke, Human, Sight, Door, DeadHuman




# Creates a visual portrayal of our model in the browser interface
def fire_evacuation_portrayal(agent):
    if agent is None:
        return

    portrayal = {}
    (x, y) = agent.get_position()
    portrayal["x"] = x
    portrayal["y"] = y

    if type(agent) is Human:
        portrayal["scale"] = 1
        portrayal["Layer"] = 5

        if agent.get_mobility() == Human.Mobility.INCAPACITATED:  # Incapacitated
            portrayal["Shape"] = "evacuation_foule/images/incapable.png"
            portrayal["Layer"] = 6
        elif agent.get_mobility() == Human.Mobility.PANIC:  # Panicked
            portrayal["Shape"] = "evacuation_foule/images/panique.png"
        elif agent.is_carrying():  # Carrying someone
            portrayal["Shape"] = "evacuation_foule/images/porteur.png"
        else:  # Normal
            portrayal["Shape"] = "evacuation_foule/images/humain.png"
    elif type(agent) is Fire:
        portrayal["Shape"] = "evacuation_foule/images/feu.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 3
    elif type(agent) is Smoke:
        portrayal["Shape"] = "evacuation_foule/images/fumee.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 2
    elif type(agent) is FireExit:
        portrayal["Shape"] = "evacuation_foule/images/sortie.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1
    elif type(agent) is Door:
        portrayal["Shape"] = "evacuation_foule/images/porte.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1
    elif type(agent) is Wall:
        portrayal["Shape"] = "evacuation_foule/images/mur.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1
    elif type(agent) is Furniture:
        portrayal["Shape"] = "evacuation_foule/images/fourniture.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 1
    elif type(agent) is DeadHuman:
        portrayal["Shape"] = "evacuation_foule/images/mort.png"
        portrayal["scale"] = 1
        portrayal["Layer"] = 4
    elif type(agent) is Sight:
        portrayal["Shape"] = "evacuation_foule/images/view.png"
        portrayal["scale"] = 0.8
        portrayal["Layer"] = 7

    return portrayal


# Was hoping floorplan could dictate the size of the grid, but seems the grid needs to be specified first, so the size is fixed to 50x50
canvas_element = CanvasGrid(fire_evacuation_portrayal, 35, 35, 700, 700)

# Define the charts on our web interface visualisation
status_chart = ChartModule([{"Label": "Vivant", "Color": "blue"},
                            {"Label": "Mort", "Color": "red"},
                            {"Label": "Echappé", "Color": "green"}])

mobility_chart = ChartModule([{"Label": "Normal", "Color": "green"},
                              {"Label": "Paniqué", "Color": "red"},
                              {"Label": "Incapable", "Color": "blue"}])

collaboration_chart = ChartModule([{"Label": "Collaboration verble", "Color": "orange"},
                                   {"Label": "Collaboration physique", "Color": "red"},
                                   {"Label": "Collaboration morale", "Color": "pink"}])

# Get list of available floorplans
floor_plans = [f for f in listdir("evacuation_foule/plan_sol") if path.isfile(path.join("evacuation_foule/plan_sol", f))]

# Specify the parameters changeable by the user, in the web interface
model_params = {
    "floor_plan_file": UserSettableParameter("choice", "Les plans", value=floor_plans[0], choices=floor_plans),
    "human_count": UserSettableParameter("slider", "Nombre des Agents", value=50, min_value=0, max_value=300, step=1),
    "collaboration_percentage": UserSettableParameter("slider", "Pourcentage de collaboration", value=50, min_value=0, max_value=100, step=5),
    "fire_probability": UserSettableParameter("slider", "Probabilité du feu", value=1, min_value=0, max_value=1, step=0.01),
    "random_spawn": UserSettableParameter('checkbox', 'Mettre les agents dans des positions aleatoire', value=True),
    "visualise_vision": UserSettableParameter('checkbox', 'Afficher la vision des agents', value=False),
    "save_plots": UserSettableParameter('checkbox', 'Enregistrer les figures', value=True)
}

# Start the visual server with the model
server = ModularServer(FireEvacuation, [canvas_element, status_chart, mobility_chart, collaboration_chart], "Evacuation du Foule",
                       model_params)
