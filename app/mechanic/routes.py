from flask import request, jsonify
from app.extensions import db, limiter, cache
from app.models import Mechanics, ServiceTickets
from . import mechanic_bp
from .schemas import mechanic_schema, mechanics_schema, login_schema
from app.util.auth import encode_token, token_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func 


# POST '/' : Create a new mechanic
@mechanic_bp.post("/")
@limiter.limit("5/minute")
@cache.cached(timeout=20)
def create_mechanic():
    data = request.json

    mechanic = Mechanics(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        salary=data["salary"],
        address=data["address"]
    )

    mechanic.set_password(data["password"])

    db.session.add(mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(mechanic), 201

@mechanic_bp.post("/login")
def login():
    data = login_schema.load(request.json)

    mechanic = Mechanics.query.filter_by(email=data["email"]).first()

    if not mechanic or not check_password_hash(mechanic.password, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = encode_token(mechanic.id)

    return jsonify({
        "message": f"Welcome {mechanic.first_name}",
        "token": token
    }), 200


@mechanic_bp.get("/my-tickets")
@token_required
def my_tickets():
    mechanic_id = request.logged_in_user_id
    mechanic = Mechanics.query.get_or_404(mechanic_id)

    tickets = mechanic.service_tickets

    return jsonify([
        {
            "id": t.id,
            "service_desc": t.service_desc,
            "service_date": str(t.service_date),
            "vin": t.vin
        }
        for t in tickets
    ])

# GET '/' : Get all mechanics
@mechanic_bp.get("/")
def get_mechanics():
    mechanics = Mechanics.query.all()
    return mechanics_schema.jsonify(mechanics)


# PUT '/<int:id>' : Update mechanic
@mechanic_bp.put("/<int:id>")
@token_required
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
@token_required
def delete_mechanic(id):
    mechanic = Mechanics.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted"})

#  Get '/ranking' : Mechanic ranking by numbers 
@mechanic_bp.get("/ranking")
def mechanic_ranking():
    result = db.session.query(
        Mechanics.first_name,
        Mechanics.last_name,
        func.count(ServiceTickets.id).label("ticket_count")
    ).join(Mechanics.service_tickets).group_by(Mechanics.id).order_by(func.count(ServiceTickets.id).desc()).all()

    return jsonify([
        {
            "first_name": r[0],
            "last_name": r[1],
            "ticket_count": r[2]
        } for r in result
    ])
