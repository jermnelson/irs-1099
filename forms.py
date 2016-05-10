__author__ = "Jeremy Nelson"

import datetime
from flask_wtf import Form
from wtforms import BooleanField, SelectField, StringField

class MISC1099Form(Form):
    is_test = BooleanField("Is test")
    nonemployee_comp = StringField("Nonemployee compensation")
    other_income = StringField("Other income")
    payers_name = StringField("PAYER'S name")
    payers_address = StringField("PAYER'S street address")
    payers_city = StringField("PAYER'S city")
    payers_state = StringField("PAYER'S state")
    payers_telephone = StringField("PAYER'S telephone")
    payers_zip = StringField("PAYER'S zipcode")
    payers_fed_code = StringField("PAYER'S federal identification number")
    payers_tcc = StringField("PAYER'S Transmitter Control Code (TCC)")
    payment_year = StringField("Payment Year", default=datetime.datetime.utcnow().year-1)
    recipient_given_name = StringField("RECIPIENT'S given name")
    recipient_family_name = StringField("RECIPIENT'S family name")
    recipient_address = StringField("RECIPIENT'S address")
    recipient_city = StringField("RECIPIENT'S city")
    recipient_state = StringField("RECIPIENT'S state")
    recipient_zip = StringField("RECIPIENT'S zipcode")
    recipient_tin = StringField("RECIPIENT'S TIN")
    recipient_tin_type = SelectField(choices=[("1", "EIN"),
                                              ("2", "SSN"),
                                              ("2", "ITIN"),
                                              ("2", "ATIN")],
                                     label="RECIPIENT Type of TIN")

