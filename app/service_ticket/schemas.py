from ..extensions import ma
from ..models import ServiceTickets

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTickets
        include_fk = True          # <-- allows customer_id
        load_instance = True
        exclude = ("customer", "mechanics")  # <-- prevents Marshmallow from expecting nested relationships

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
