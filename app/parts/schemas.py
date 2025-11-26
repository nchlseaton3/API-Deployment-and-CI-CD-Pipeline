from app.extensions import ma
from app.models import Parts, Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True

class PartsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Parts
        include_fk = True
        load_instance = True

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
part_schema = PartsSchema()
parts_schema = PartsSchema(many=True)
