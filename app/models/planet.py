class Planet:
    def __init__(self, id, name, description, distance_from_sun):
        self.id = id
        self.name = name
        self.description = description
        self.distance_from_sun = distance_from_sun


planets = [
    Planet(1, "Mercury", "The smallest and closest planet to the Sun.", 57.9),
    Planet(2, "Venus", "Similar in size to Earth, but with a toxic atmosphere.", 108.2),
    Planet(3, "Earth", "Our home planet, the only known one with life.", 149.6),
    Planet(4, "Mars", "The Red Planet, known for its dusty, rocky surface.", 227.9),
    Planet(5, "Jupiter", "The largest planet, a gas giant with a Great Red Spot.", 778.5),
    Planet(6, "Saturn", "Famous for its beautiful ring system.", 1_433.5),
    Planet(7, "Uranus", "An ice giant with a tilted axis.", 2_872.5),
    Planet(8, "Neptune", "A distant blue planet known for its strong winds.", 4_495.1)
]