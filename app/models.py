from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, Date, ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash


class Customers(db.Model):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    phone: Mapped[str] = mapped_column(String)
    address: Mapped[str] = mapped_column(String)

    service_tickets = relationship("ServiceTickets", back_populates="customer")


class ServiceTickets(db.Model):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    service_desc: Mapped[str] = mapped_column(String)
    service_date: Mapped[str] = mapped_column(Date)
    vin: Mapped[str] = mapped_column(String)

    
    customer = relationship("Customers", back_populates="service_tickets")
    mechanics = relationship(
        "Mechanics",
        secondary="service_assignments",
        back_populates="service_tickets"
    )

    parts = relationship("Parts", back_populates="ticket")

class Mechanics(db.Model):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    salary: Mapped[float] = mapped_column(Float)
    address: Mapped[str] = mapped_column(String)

      # For Authentication
    password: Mapped[str] = mapped_column(String)

    service_tickets = relationship(
        "ServiceTickets",
        secondary="service_assignments",
        back_populates="mechanics"
    )

    # Password helpers
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class ServiceAssignments(db.Model):
    __tablename__ = "service_assignments"

    service_ticket_id = mapped_column(
        ForeignKey("service_tickets.id"), primary_key=True
    )
    mechanic_id = mapped_column(
        ForeignKey("mechanics.id"), primary_key=True
    )


class Inventory(db.Model):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    price: Mapped[float] = mapped_column(Float)

    parts = relationship("Parts", back_populates="description")


class Parts(db.Model):
    __tablename__ = "parts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    desc_id: Mapped[int] = mapped_column(ForeignKey("inventory.id"))
    ticket_id: Mapped[int] = mapped_column(ForeignKey("service_tickets.id"), nullable=True)

    description = relationship("Inventory", back_populates="parts")
    ticket = relationship("ServiceTickets", back_populates="parts")