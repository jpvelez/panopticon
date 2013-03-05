import csv
import sys

from django.core.management.base import BaseCommand
from main.models import Employee, Garage

class Command(BaseCommand):
    args = '<filename filename ...>'
    help = 'Drop all employees and garages from the database, and add new ones from the payroll data.'

    # Reformat dates to format django is happy with
    def format_date(self, original):
        if original == '':
            return None
        else:
            month, day, year = original.split('/')
            formatted = '%i-%02i-%02i' % (int(year), int(month), int(day))
            return formatted

    def format_name(self, original):
        return original.strip()

    def handle(self, *args, **options):

        # Drop all employees and garages from database.
        Employee.objects.all().delete()
        Garage.objects.all().delete()
        print >> sys.stderr, 'Dropping all rows from employee and garage tables.'

        # This will hold unique badge numbers. Necessary because payroll data
        # is earnings-code-payperiod level so employees show up tons of times.
        employee_dict = {}

        # Iterate through filenames.
        for filename in args:
            print >> sys.stderr, 'Reading %s' % filename

            # The payroll data is not in proper csv format. These rules 
            # clean up specific lines in 2012_Payroll_Busops.txt that are
            # causing parsing errors. WON'T CATCH PARSING ERRORS IN OTHER YEARS.
            with open(filename, 'r') as instream, open('Payroll_Busops_clean.txt', 'w') as outstream:
                for line in instream:
                    newline = line.replace('Married, but Withhold at Higher Single Rate', 'Married but Withhold at Higher Single Rate').replace('Unit 1411,', 'Unit 1411').replace('2625 w,', '2625 w.').replace('9990 84th Terrace,', '9990 84th Terrace ')
                    outstream.write(newline)

            # Parse clean payroll data to build employee table.
            stream = open('Payroll_Busops_clean.txt')
            reader = csv.DictReader(stream)

            for i, row in enumerate(reader):

                # Clean up garage names from payroll data.
                garage_name_clean = row['ORAGNIZATION'].replace(' Scheduled Transit Operations', '').replace(' Scheduled Operations', '')

                # Add current garage to the garages table, or get garage object if it already exists.
                garage, created = Garage.objects.get_or_create(name=garage_name_clean)


                # Check if lines are still being misparsed, helpful for debugging.
                # The 'ORAGNIZATION' column often ends up incorrect when this happens.
                if garage_name_clean == 'Bus Operator':
                    print >> sys.stderr, 'Row %s has a problem: %s' % (i, row)
                    raise Exception('Parsing error due to lack of proper csv encoding!')


                # Get data for unique employees.
                # This is constantly overwriting the employee info so the last instance of the
                # employee in the payroll files is actually what ends up getting stored. Employees
                # show up tons of times because the data is earnings code pay period level.
                badge_number = int(row['EMPLOYEE_NUMBER'])
                employee_dict[badge_number] = {
                    'badge_number': badge_number,
                    'last_name': self.format_name(row['LAST_NAME']),
                    'first_name': self.format_name(row['FIRST_NAME']),
                    'job_category': row['EMPLOYMENT_CATEGORY'],
                    'job_title': row['POSITION_TITLE'],
                    'start_date': self.format_date(row['DATE_START']),
                    'end_date': self.format_date(row['TERMINATION_DATE']),
                    'sex': row['SEX'],
                    'dob': self.format_date(row['DOB']),
                    'address': row['ADDRESS'],
                    'apt': row['APT'],
                    'city': row['CITY'],
                    'state': row['STATE'],
                    'zipcode': row['ZIP'],
                    'garage_name': garage_name_clean,
                    'garage': garage,

                    # The employee's total number of deviations is calculate
                    # by crunchemployeedeviation command after FAST deviation
                    # data is loaded. Defaulting to 0 so MySQL doesn't bitch.
                    'n_deviations': 0
                }

            stream.close()

        # Insert all of the unique employees.
        for attribute_dict in employee_dict.itervalues():
            print attribute_dict
            employee = Employee(**attribute_dict)
            employee.save()


            
