from flask import request, jsonify
from ..extensions import db
from ..models import ServiceTickets, Mechanics, Parts, Customers
from . import service_ticket_bp
from .schemas import service_ticket_schema, service_tickets_schema
from datetime import datetime 

# POST '/' : create service ticket
@service_ticket_bp.post("/")
def create_ticket():
    data = request.get_json()

    # Validate required fields
    required = ("customer_id", "service_desc", "service_date", "vin")
    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    # Convert date string → Python date object
    try:
        service_date = datetime.strptime(data["service_date"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "service_date must be YYYY-MM-DD"}), 400

    ticket = ServiceTickets(
        customer_id=data["customer_id"],
        service_desc=data["service_desc"],
        service_date=service_date,  #  Real date object
        vin=data["vin"]
    )

    db.session.add(ticket)
    db.session.commit()

    return service_ticket_schema.jsonify(ticket), 201


# PUT '/<ticket_id>/assign-mechanic/<mechanic_id>'
@service_ticket_bp.put("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
def assign_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTickets.query.get_or_404(ticket_id)
    mechanic = Mechanics.query.get_or_404(mechanic_id)

    ticket.mechanics.append(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic assigned"})


# PUT '/<ticket_id>/remove-mechanic/<mechanic_id>'
@service_ticket_bp.put("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>")
def remove_mechanic(ticket_id, mechanic_id):
    ticket = ServiceTickets.query.get_or_404(ticket_id)
    mechanic = Mechanics.query.get_or_404(mechanic_id)

    ticket.mechanics.remove(mechanic)
    db.session.commit()
    return jsonify({"message": "Mechanic removed"})


# GET '/' : get all tickets
@service_ticket_bp.get("/")
def get_tickets():
    tickets = ServiceTickets.query.all()
    return service_tickets_schema.jsonify(tickets)

#  PUT /<int:ticket_id>/add-part/<part_id>
@service_ticket_bp.put("/<int:ticket_id>/add-part/<int:part_id>")
def add_part_to_ticket(ticket_id, part_id):
    
    ticket = ServiceTickets.query.get_or_404(ticket_id)
    part = Parts.query.get_or_404(part_id)
    part.ticket = ticket       # or: part.ticket_id = ticket_id
    db.session.commit()
    return {"message": "Part assigned to ticket"}

@service_ticket_bp.post("/create-customer")
def create_customer():
    data = request.get_json()

    required = ["first_name", "last_name", "email", "phone", "address"]
    for field in required:
        if field not in data:
            return {"error": f"{field} is required"}, 400

    # Create customer
    new_customer = Customers(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        phone=data["phone"],
        address=data["address"]
    )

    db.session.add(new_customer)
    db.session.commit()

    return {
        "message": "Customer created",
        "customer_id": new_customer.id
    }, 201