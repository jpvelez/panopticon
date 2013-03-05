from django.core.management.base import BaseCommand

from main.models import Deviation
from main.utils import deviation_category2group

# Deviation categories are bundled into groups that share the same
# badge and calendar color on employee_profile. This script checks to
# see if known deviation categories are mapped to a group, and prints
# them if not. Useful when getting new data from FAST that might
# include deviation categories not yet added to the category2group mapping.

class Command(BaseCommand):
     args = '<None.>'
     help = ''''Check to see if all known deviation categories belong to deviation
     group, print them out if not.'''

     def handle(self, *arg, **options):

          # get all deviations
          deviations = Deviation.objects.all()

          # find unique deviations
          categories = set()

          for deviation in deviations:
               categories.add(deviation.category)

          # # check to see if deviation is in category2group mapping
          for category in categories:
               try:
                    deviation_category2group(category)

               # if not found, print
               except KeyError:
                    print category




