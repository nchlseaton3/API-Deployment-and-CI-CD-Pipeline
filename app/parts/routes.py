from flask import request, jsonify
from app.extensions import db
from app.models import Inventory, Parts
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

#  Create part
@parts_bp.post("/create-part")
def create_part():
    data = request.json
    part = Parts(
        desc_id=data["desc_id"],
        ticket_id=None
    )
    db.session.add(part)
    db.session.commit()
    return part_schema.jsonify(part), 201



# GET all inventory
@parts_bp.get("/")
def get_inventory():
    items = Inventory.query.all()
    return inventories_schema.jsonify(items)


# UPDATE inventory item
@parts_bp.put("/<int:id>")
def update_inventory(id):
    item = Inventory.query.get_or_404(id)
    data = request.json

    for key, value in data.items():
        setattr(item, key, value)

    db.session.commit()
    return inventory_schema.jsonify(item)


# DELETE inventory item
@parts_bp.delete("/<int:id>")
def delete_inventory(id):
    item = Inventory.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Deleted"})
