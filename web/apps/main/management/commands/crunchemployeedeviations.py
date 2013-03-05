import sys

from django.core.management.base import BaseCommand
from main.models import Employee, Deviation

class Command(BaseCommand):
    args = '<None.>'
    help = 'Drop all employee deviation metrics from the database, crunch and load new ones.'

    def handle(self, *arg, **options):

        # Get all employees from the database.
        employees = Employee.objects.all()
        print >> sys.stderr, 'Getting all rows from employee table.'

        for employee in employees:

            # Count employee's deviations and add them to n_deviations column
            # of employee record.

            employee_deviations = Deviation.objects.filter(employee=employee)
            employee.n_deviations = employee_deviations.count()

            print >> sys.stderr, 'Adding data to %s: %s' % (employee.badge_number, employee.n_deviations)

            employee.save()