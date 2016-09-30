"""Generates Transmitter "T" Record for form 1099 MISC

<https://www.irs.gov/pub/irs-pdf/p1220.pdf>
"""

import datetime
from __init__ import app

def __pad__(value, field_max=40):
    return value.ljust(40)




class FIREFile(object):

    def __init__(self, form):
        self.contents = []
        self.form = form
        self.today = datetime.datetime.utcnow()

    def __is_test__(self):
        if self.form.is_test.data is True:
            return "T"
        return " "

    def __prior_year_indicator__(self, tax_year):
        if str(self.today.year-1) != tax_year:
            return "A"
        return " "
            

    def end_of_payer_record(self):
        data = [
             "C", # Record Type
            "1".rjust(8,"0"), # Number of Payees
            "".ljust(6),
            "+"+self.form.nonemployee_comp.data.rjust(17, "0"), # Control Total 1
            "".rjust(270, "0"), # Control Totals 2-G
            "".ljust(196),
            str(len(self.contents)+1).rjust(8, "0"), # Record Sequence Number
            "".ljust(241)
        ]
        self.contents.append(data)

    def end_of_record(self):
        data = [
            "F", # Record Type
            "1".rjust(8, "0"), # Number of "A" records
            "".ljust(21, "0"), # Zero
            "".ljust(19),
            "1".rjust(8, "0"), # Total Number of Payees
            "".ljust(442),
            str(len(self.contents)+1).rjust(8, "0"), # Record Sequence Number
            "".ljust(241)
        ]
        self.contents.append(data)


    def payee_record(self):
        data = [
            "B", # Record Type
            self.form.payment_year.data, # Payment Year
            " ", # Corrected Return Indicator
            self.form.recipient_family_name.data[0:4].upper(), # Name Control
            self.form.recipient_tin_type.data,
            self.form.recipient_tin.data, # Payee's Taxpayer Identification Number
            "1".ljust(20), # Payer's Account Number For Payee
            "".ljust(4), # Payer's Office Code
            "".ljust(10),
            "+"+self.form.nonemployee_comp.data.rjust(11, "0"), # Payment amount 1
            "".ljust(180), # Remaining payment amounts set to blanks
            " ", # Foreign Country Indicator
            "{} {}".format(self.form.recipient_family_name.data.strip(), # First Payee Name Line
                           self.form.recipient_given_name.data.strip()).ljust(40),
            "".ljust(40), # Second Payee Name Line
            "".ljust(40),
            self.form.recipient_address.data.ljust(40),
            "".ljust(40),
            self.form.recipient_city.data.ljust(40),
            self.form.recipient_state.data.ljust(2),
            self.form.recipient_zip.data.ljust(9),
            "".ljust(1),
            str(len(self.contents)+1).rjust(8, "0"), # Record Sequence Number
            "".ljust(36),
            " ", # Second TIN Notice (optional) for Form 1099-MISC
            "".ljust(2),
            " ", # Direct Sales Indicator
            " ", # FATCA filing requirement
            "".ljust(114),
            "".ljust(60), # Special Data Entries
            "".rjust(12, "0"), # State Income Tax Withheld
            "".rjust(12, "0"), # Local Income Tax Withheld
            "".ljust(2)
        ]
        self.contents.append(data)



    def payer_record(self):
        data = [
            'A', # Record Type
            self.form.payment_year.data, # Payment Year
            " ", # Combined Federal/State Filing Program
            "".ljust(5),
            self.form.payers_fed_code.data, # Transmitter's TIN
            self.form.payers_name.data[0:4].upper(),
            " ",
            "A ", # Type of Return A - 1099-MISC
            "7", # 1099-MISC Nonemployee compensation code
            self.form.nonemployee_comp.data.rjust(15, "0")
            "".ljust(8),
            " ", # Foreign Entity Indicator
            self.form.payers_name.data.ljust(40), # First Payers Name
            "".ljust(40),
            "1", # Transfer Agent Indicator
            self.form.payers_address.data.ljust(40), # Payer Address
            self.form.payers_city.data.ljust(40), # Payer city
            self.form.payers_state.data, # Payer state
            self.form.payers_zip.data.ljust(9), # Company zip
            self.form.payers_telephone.data.ljust(15),
            "".ljust(260),
            str(len(self.contents)+1).rjust(8, "0"), # Record Sequence Number
            "".ljust(241)
        ]
        self.contents.append(data)

    def save(self):
        output = ''
        self.transmitter_record()
        self.payer_record()
        self.payee_record()
        self.end_of_payer_record()
        self.end_of_record()
        for row in self.contents:
            output += "{}\n".format(''.join(row))
        return output[:-1]

    def transmitter_record(self):
        contributor = app.config.get("CONTRIBUTOR")
        data = [
            'T', # Record Type
            self.form.payment_year.data, # Payment Year
            self.__prior_year_indicator__(self.form.payment_year.data), # Prior year indicator
            self.form.payers_fed_code.data, # Transmitter's TIN
            self.form.payers_tcc.data, # Transmitter Control Code
            "".ljust(7),
            self.__is_test__(), # Test File Indicator,
            " ", # Foreign Entity Indicator
            self.form.payers_name.data.ljust(40), # Transmitter's name
            "".ljust(40), # Transmitter's name continuation
            self.form.payers_name.data.ljust(40), # Company name
            "".ljust(40), # Company name continuation
            self.form.payers_address.data.ljust(40), # Company Address
            self.form.payers_city.data.ljust(40), # Company city
            self.form.payers_state.data, # Company state two character code
            self.form.payers_zip.data.ljust(9), # Company zip
            "".ljust(15),
            "1".rjust(8, '0'), # Number of payees, this app only supports 1
            contributor.get("name").ljust(40), 
            contributor.get("phone").ljust(15),
            contributor.get("email").ljust(50),
            "".ljust(91),
            str(len(self.contents)+1).rjust(8, "0"), # Record Sequence Number
            "".ljust(10),
            "I", # Software produced in-house
            "".ljust(40), # Vendor name blank
            "".ljust(40), # Vendor mailing address
            "".ljust(40), # Vendor city
            "".ljust(2), # Vendor state
            "".ljust(9), # Vendor zip code
            "".ljust(40), # Vendor contact name
            "".ljust(15), # Vendor telephone
            "".ljust(35),
            " ",
            "".ljust(8)
        ]
        self.contents.append(data) 
