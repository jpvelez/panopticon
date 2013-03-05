import sys

from django.core.management.base import BaseCommand
from main.models import DrivingRank, Employee

class Command(BaseCommand):
    args = '<filename filename..>'
    help = 'Drop all daily driving ranks from the database, load new ones from AVAS data.'

    def format_date(self, original):
        if original == '':
            return None
        else:
            month, day, year = original.split('/')
            formatted = '%i-%i-%i' % (int(year), int(month), int(day))
            return formatted

    def handle(self, *arg, **options):

        # Drop all daily driving ranks from the database.
        DrivingRank.objects.all().delete()
        print >> sys.stderr, 'Dropping all rows from drivingrank table.'

        # Iterate through files.
        for filename in arg:
            print >> sys.stderr, 'Reading %s' % filename

            with open(filename) as stream:

                # Iterate through driver-day average rank and otp data.
                missing_employees = 0
                for line in stream:

                    rank_row = line.split()

                    # Get current driver from the employee table.
                    badge_number = rank_row[0]
                    try:
                        employee = Employee.objects.get(badge_number=int(badge_number))

                        # Prepare driving rank row by extracting date, daily average
                        # rank, daily otp, and pairing them with employee object.
                        rank_data = { 'employee': employee, 'date': self.format_date(rank_row[1]), 'rank': rank_row[2], 'otp': rank_row[3] }

                        # Add daily driving rank to the database, linking it to the employee table.
                        driving_rank = DrivingRank(**rank_data)
                        driving_rank.save()

                    except Employee.DoesNotExist:
                        print >> sys.stderr, 'Could not find employee %s' % badge_number
                        missing_employees += 1

                # Report number of missing employees.
                print >> sys.stderr, 'Could not match %i daily rank/top records to employees in payroll employee table!' % missing_employees