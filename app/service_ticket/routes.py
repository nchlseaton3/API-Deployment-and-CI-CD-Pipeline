from flask import request, jsonify
from ..extensions import db
from ..models import ServiceTickets, Mechanics, Parts
from . import service_ticket_bp
from .schemas import service_ticket_schema, service_tickets_schema


# POST '/' : create service ticket
@service_ticket_bp.post("/")
def create_ticket():
    data = request.json
    ticket = service_ticket_schema.load(data)
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