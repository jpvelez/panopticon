from datetime import date

def years_since(start_date):

    '''Years since employee joined CTA. Years are approximate and rounded down.'''

    today_date = date.today()
    time_since_start = today_date - start_date
    years_since_start = int( time_since_start.days / 364.75 ) 

    return years_since_start

def deviation_category2group(deviation_category):

    '''Fetch the group of a deviation category. Groups are used to give similar category badges the same color on the employee_profile template.:i'''

    category2group_mapping = {

        # Missed category
        "Missed": "Missed",
        "A.W.O.L.": "Missed",

        # Health categories
        "Sick": "Sick",

        "Injured On Duty": "Injured On Duty",
        "I.O.D. Over 60 Days": "Injured On Duty",

        "F.M.L.A. - Self": "F.M.L.A.",
        "F.M.L.A. - Family": "F.M.L.A.",
        "F.M.L.A. Pending": "F.M.L.A.",

        "Sick Over 60 Days": "Out for a while",
        "Temp Med Disability": "Out for a while",
        "Discharged": "Out for a while",
        "Retired": "Out for a while",
        "L.O.A. - Military": "Out for a while",
        "L.O.A. - Personal": "Out for a while",
        "Sys  Pk Transfer-Out": "Out for a while",
        "Trnsf'd Other Area": "Out for a while",

        # Time off category
        "Vacation Week": "Vacation",
        "Vacation Random Day": "Vacation",
        "Vacation Non-Paid": "Vacation",
        "Requested Day Off": "Vacation",

        # Holidays category
        "Birthday Holiday": "Holiday",
        "Anniversary Holiday": "Holiday",
        "M.L.K. Holiday": "Holiday",
        "Veterans Holiday": "Holiday",
        "P.L.D. Holiday": "Holiday",

        # Getting in trouble categories
        "Accident/Incident": "Accident/Incident",

        "Referred To Gen Mgr": "Referred to Mgr",
        "Referred-Trans Mgr": "Referred to Mgr",

        "1 Day Suspension": "Suspension",
        "1-Day Suspension": "Suspension",
        "3 Day Suspension": "Suspension",
        "3-Day Suspension": "Suspension",
        "Susp - No License": "Suspension",

        # Trace categories (unclear)
        "Acting Clerk": "Trade",
        "Acting Instructor": "Trade",
        "Acting Supervisor": "Trade",
        "Trade Assignment": "Trade",
        "Trade SDO": "Trade",
        "Trade By Authority": "Trade",

        # Training categories
        "Referred To Instr": "Training",
        "Recertification TRNG": "Training",
        "Recertification Trng": "Training",
        "Adv Training-Clerk": "Training",
        "Adv Training-Instr": "Training",
        "B.E.C.S. Training": "Training",
        "Customer Service Tra": "Training",
        "Trans Ambassador Trg": "Training",


        # COLOR CATEGORIES END HERE

        # Family category
        "Emergency In Family": "Family",
        "Death In Family": "Family ",

        # Court/Union category
        "Jury Duty": "Court",
        "Court Time-Personal": "Court",
        "C.T.A. Court Time": "Court",
        "Union Bus. Non - CTA": "Unclear",
        "Union Business - CTA": "Unclear",
      
        # Unclear categories
        "Individual Retrng": "Unclear",
        "Transf'd Other Area": "Unclear",
        "ExBd Assignment Adj": "Unclear",
        "C.O.A. Non Roster": "Unclear",
        "C.O.A. Roster/Block": "Unclear",
        "Check PTO Hours": "Unclear",
        "Transitional RTW": "Unclear",
        "Non Rost Missed&Work": "Unclear",
        "Admin Separation": "Unclear",
        "B/O Non-Revenue Posi": "Unclear",
        "B/O Pend. Safety Inv": "Unclear",
        "F.T.A. Testing": "Unclear",
        "Referred To Medical": "Unclear",
        "Req By Med- Non Rost": "Unclear",
        "Resigned": "Unclear",
        "Rost/Blk Missed&Work": "Unclear",
        "Transition FTO - In": "Unclear",
        "Transition FTO - Out": "Unclear",
        "Transition FTP - In": "Unclear",
        "Unavail Med/Labor": "Unclear",

        "NOT QUALIFIED": "Unclear",
        "Deviation Pending": "Unclear",

        # Missing categories
        "": "Missing"
    }

    return category2group_mapping[deviation_category]

