import sys
import xlrd
import datetime

from django.core.management.base import BaseCommand
from main.models import Deviation, Garage, Employee

import crunchemployeedeviations

class Command(BaseCommand):
    args = '<filename filename ..>'
    help = 'Drop all deviations from the database, load new ones from the FAST data.'

    def handle(self, *arg, **options):

        # drop all deviations and garages from the database
        Deviation.objects.all().delete()
        print >> sys.stderr, 'Dropping all rows from deviation table.'

        # iterate over all files provided on the command line and parse them 
        for filename in arg:
            print >> sys.stderr, "Reading %s" % filename

            # read correct sheet from excel file
            book = xlrd.open_workbook(filename)
            sheet = book.sheet_by_name('Rawdata')

            # get the garage name from the filename
            garage_name = filename.split('-')[1].strip().replace('(1)', '').replace(' Revised', '').replace('.xls', '')

            missing_employees = 0

            # iterate through excel file 'Rawdata' sheet rows, parsing them and adding them to database
            for index in range(1,sheet.nrows):

                row = sheet.row(index)
                clean_row = [ cell.value for cell in row[:6] ]

                # convert weird excel date number to tuple, then to date object.
                # if it's unconvertable, skip this row for now.
                try:
                    date_tuple = xlrd.xldate_as_tuple(clean_row[0], book.datemode)
                except ValueError:
                    print >> sys.stderr, 'skipping row %i' % index
                    print >> sys.stderr, row
                clean_date = datetime.datetime(*date_tuple).date()

                # replace excel date number with cleaned date
                clean_row[0] = clean_date

                # Match garage names in FAST to those in payroll data, which
                # are being used as primary key for garage table/objects.
                fast_to_payroll_garage = {
                    '103rd': '103rd Street',
                    '74th': '74th & Wood',     
                    '77th': '77th Street',       
                    'Chicago': 'Chicago',    
                    'Forest Glen': 'Forest Glen',
                    'Kedzie': 'Kedzie',
                    'North Park': 'North Park'
                }

                # get any Garages if they exist and add if they don't
                garage, created = Garage.objects.get_or_create(name=fast_to_payroll_garage[garage_name])

                # get any Employee if they exist and add if they don't, skip ones missing badges or not found in Employee table
                try:
                    employee = Employee.objects.get(badge_number=int(clean_row[3]))
                    print >> sys.stderr, "Getting %s" % employee
                except ValueError:
                    missing_employees += 1
                    print >> sys.stderr, 'Employee %s %s missing badge number' % (clean_row[1], clean_row[2])
                    continue
                except Employee.DoesNotExist:
                    missing_employees += 1

                deviation_data = { 'category': clean_row[5], 'date': clean_row[0], 'employee': employee, 'garage': garage }

                # add the Deviation to the database, linking it with the Employee and Garage tables
                deviation = Deviation.objects.create(**deviation_data)

                print >> sys.stderr, "Adding %s" % str(deviation)

                deviation.save()

            print >> sys.stderr, "Oops! %i deviations couldn't be matched to a driver!" % missing_employees

        # Crunch deviation metrics for employees by calling crunchemployeedeviations command.
        crunchemployeedeviations.Command()
