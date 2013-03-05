import sys
from collections import Counter

from django.core.management.base import BaseCommand

from main.models import Deviation, Employee

class Command(BaseCommand):
    args = '<None>'
    help = 'Find unique deviation categories, category counts, and employee with max categories in FAST deviations data.'

    def handle(self, *arg, **options):

        # get all deviations from the database
        deviations = Deviation.objects.all()

        # iterate through deviations, adding categories to a set to see unique categories 
        # and to a list to count them
        category_list = []
        unique_categories = set()

        for deviation in deviations:
            category = deviation.category

            unique_categories.add(category)
            category_list.append(category)


        # display unique categories
        print >> sys.stderr, "These are the unique deviation categories:"
        print >> sys.stderr, unique_categories

        for category in unique_categories:
            print '"%s": ""' % category

        # find and display count of deviation categories
        count = Counter(category_list)

        print >> sys.stderr, "There are %s deviation categories:" % len(count)
        print >> sys.stderr, count.most_common()

        # find the most deviation categories any employee has
        employees = Employee.objects.all()
        ndeviations = []

        for employee in employees:
            deviations = (Deviation.objects.filter(employee__badge_number = employee.badge_number))
            deviation_set = set()

            for deviation in deviations:
                deviation_set.add(deviation.category)

            ndeviations.append(len(deviation_set))

        print >> sys.stderr, "The employee with the most deviation categories has %i categories." % max(ndeviations)


