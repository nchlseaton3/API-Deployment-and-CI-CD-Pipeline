from app.extensions import ma
from app.models import Mechanics
from marshmallow import Schema, fields


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Mechanics
        load_instance = True


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

class MechanicLoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


login_schema = MechanicLoginSchema()
