from marshmallow_sqlalchemy import ModelSchema
from HotelBooking_Midterm_ServiceOrientedArchitecture.database import db
from marshmallow_sqlalchemy import fields
from datetime import datetime

class bookingNote(object):
    __tablename__ = 'bookingNote'

    id_BookingNote = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roomId = db.Column(db.String(10), unique=False)
    dateIn = db.Column(db.DateTime, nullable = False)
    dateOut = db.Column(db.DateTime, nullable = False)
    Extra_bed = db.Column(db.Integer, nullable=True)
    id_cus = db.Column(db.Integer, db.ForeignKey('customer.id'))

    def __init__(self, roomId, dateIn, dateOut, Extra_bed, id_cus):
        self.roomId = roomId
        self.dateIn = dateIn
        self.dateOut = dateOut
        self.Extra_bed = Extra_bed
        self.id_cus = id_cus

class bookingNoteSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = bookingNote
        sqla_session = db.session

    id_BookingNote = fields.Number(dump_only=True)
    roomId = fields.String(required=True)
    dateIn = fields.String(dump_only=True)
    dateOut = fields.String(dump_only=True)
    extra_bed = fields.Integer()
    id_cus = fields.Integer()
