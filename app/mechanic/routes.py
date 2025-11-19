from flask import request, jsonify
from app.extensions import db
from app.models import Mechanics
from . import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema


# POST '/' : Create a new mechanic
@mechanic_bp.post("/")
def create_mechanic():
    data = request.json
    mechanic = mechanic_schema.load(data)
    db.session.add(mechanic)
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 201


# GET '/' : Get all mechanics
@mechanic_bp.get("/")
def get_mechanics():
    mechanics = Mechanics.query.all()
    return mechanics_schema.jsonify(mechanics)


# PUT '/<int:id>' : Update mechanic
@mechanic_bp.put("/<int:id>")
def update_mechanic(id):
    mechanic = Mechanics.query.get_or_404(id)
    data = request.json

    for key, value in data.items():
        if hasattr(mechanic, key):
            setattr(mechanic, key, value)

    db.session.commit()
    return mechanic_schema.jsonify(mechanic)


# DELETE '/<int:id>' : Delete mechanic
@mechanic_bp.delete("/<int:id>")
def delete_mechanic(id):
    mechanic = Mechanics.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted"})
