from flask import request, jsonify
from app.extensions import db
from app.models import Inventory, Parts, ServiceTickets
from . import parts_bp
from .schemas import inventory_schema, inventories_schema, part_schema, parts_schema

# CREATE inventory item
@parts_bp.post("/")
def create_inventory():
    data = request.json
    item = inventory_schema.load(data)
    db.session.add(item)
    db.session.commit()
    return inventory_schema.jsonify(item), 201

#  GET all inventory
@parts_bp.get("/")
def get_inventory():
    items = Inventory.query.all()
    return inventories_schema.jsonify(items)

#  Physical part instance
# POST → Create a physical part using desc_id
@parts_bp.post("/create-part")
def create_part():
    data = request.get_json()
    errors = part_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    # Ensure desc_id exists
    inventory_item = Inventory.query.get(data["desc_id"])
    if not inventory_item:
        return jsonify({"error": "Inventory item not found"}), 404

    part = Parts(
        desc_id=data["desc_id"],
        ticket_id=data.get("ticket_id")
    )
    db.session.add(part)
    db.session.commit()

    return part_schema.jsonify(part), 201


# PUT → Update a physical part instance (desc_id or ticket_id)
@parts_bp.put("/<int:id>")
def update_part(id):
    part = Parts.query.get(id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    data = request.get_json()

    # Update physical part fields
    if "desc_id" in data:
        inv = Inventory.query.get(data["desc_id"])
        if not inv:
            return jsonify({"error": "Inventory item not found"}), 404
        part.desc_id = data["desc_id"]

    if "ticket_id" in data:
        if data["ticket_id"] is not None:
            ticket = ServiceTickets.query.get(data["ticket_id"])
            if not ticket:
                return jsonify({"error": "Ticket not found"}), 404
        part.ticket_id = data["ticket_id"]

    db.session.commit()
    return part_schema.jsonify(part), 200


# DELETE → Delete physical part instance
@parts_bp.delete("/<int:id>")
def delete_part(id):
    part = Parts.query.get(id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    db.session.delete(part)
    db.session.commit()

    return jsonify({"message": "Part deleted"}), 200
