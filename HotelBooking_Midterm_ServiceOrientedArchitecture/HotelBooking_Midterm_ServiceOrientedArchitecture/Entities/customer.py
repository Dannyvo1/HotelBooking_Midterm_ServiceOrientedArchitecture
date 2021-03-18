from marshmallow_sqlalchemy import ModelSchema
from HotelBooking_Midterm_ServiceOrientedArchitecture.database import db
from marshmallow_sqlalchemy import fields

class customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True)
    cmnd = db.Column(db.String(10), unique=True)
    mail = db.Column(db.String(100), unique=True)
    phoneNum = db.Column(db.String(10), unique=True)
    id_BookingNote = db.Column(db.Integer, db.ForeignKey('bookingNote.id_BookingNote'))

    def __init__(self, name, cmnd, mail, phoneNum, id_BookingNote):
        self.name = name
        self.phoneNum = phoneNum
        self.cmnd = cmnd
        self.id_BookingNote = id_BookingNote
        self.mail = mail

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
class CustomerSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = customer
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    cmnd = fields.Integer(required=True)
    mail = fields.String(required=True)
    phoneNum = fields.String(required=True)
    id_BookingNote = fields.Integer()