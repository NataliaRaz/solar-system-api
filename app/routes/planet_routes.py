from flask import Blueprint, abort, make_response, request, Response
from ..models.planet import Planet
from ..models.moon import Moon
from ..db import db


planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")

@planets_bp.post("")
def create_planet():
    request_body = request.get_json()
    name = request_body["name"]
    description = request_body["description"]
    distance_from_sun = request_body["distance_from_sun"]

    new_planet = Planet(name=name, description=description, distance_from_sun=distance_from_sun)
    db.session.add(new_planet)
    db.session.commit()

    response = {
            "id": new_planet.id,
            "name": new_planet.name,
            "description": new_planet.description,
            "distance_from_sun": new_planet.distance_from_sun

    }

    return response, 201

@planets_bp.get("")
def get_all_planets():

    query = db.select(Planet)

    description_param = request.args.get("description")
    if description_param:
        query = query.where(
            Planet.description.ilike(f"%{description_param}%")
        )

    min_dist = request.args.get("min_distance")
    if min_dist:
        try:
            min_val = float(min_dist)
            query = query.where(Planet.distance_from_sun >= min_val)
        except ValueError:
            abort(make_response(
                {"message": f"min_distance '{min_dist}' must be a number."},
                400
            ))

    max_dist = request.args.get("max_distance")
    if max_dist:
        try:
            max_val = float(max_dist)
            query = query.where(Planet.distance_from_sun <= max_val)
        except ValueError:
            abort(make_response(
                {"message": f"max_distance '{max_dist}' must be a number."},
                400
            ))

    query = query.order_by(Planet.id) 
    planets = db.session.scalars(query) #Converts the final filtered result set into JSON

    planets_response = []
    for planet in planets:
        planets_response.append({
            "id":                planet.id,
            "name":              planet.name,
            "description":       planet.description,
            "distance_from_sun": planet.distance_from_sun
        })

    return planets_response, 200

@planets_bp.get("/<id>")
def get_one_planet(id):
    planet = validate_planet(id)

    return {
        "id": planet.id,
        "name": planet.name,
        "description": planet.description,
        "distance_from_sun": planet.distance_from_sun
    }

def validate_planet(id):
    try:
        id = int(id)
    except ValueError:
        invalid_response = {"message": f"Planet id '{id}' is invalid. Must be an integer."}
        abort(make_response(invalid_response, 400))

    planet = db.session.get(Planet, id)

    if not planet:
        not_found = {"message": f"Planet with id '{id}' not found."}
        abort(make_response(not_found, 404))

    return planet



@planets_bp.put("/<id>")
def update_planet(id):
    planet = validate_planet(id)
    request_body = request.get_json()

    planet.name = request_body["name"]
    planet.description = request_body["description"]
    planet.distance_from_sun = request_body["distance_from_sun"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@planets_bp.delete("/<id>")
def delete_planet(id):
    planet = validate_planet(id)
    db.session.delete(planet)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@planets_bp.post("/<int:planet_id>/moons")
def create_moon_for_planet(planet_id):
    planet = validate_planet(planet_id)

    data = request.get_json() or {}
    if "name" not in data or "size" not in data:
        return make_response({"details": "Invalid data"}, 400)

    moon = Moon.from_dict(data, planet_id=planet.id)
    db.session.add(moon)
    db.session.commit()

    return {"moon": moon.to_dict()}, 201

@planets_bp.get("/<int:planet_id>/moons")
def get_moons_for_planet(planet_id):
    planet = validate_planet(planet_id)
    moons = [m.to_dict() for m in planet.moons]
    return {"moons": moons}, 200
