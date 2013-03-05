import sys
import csv

# Find unique dates in the avas_busstatehist_timept_sample.csv, 
# a piece of the time-point level actual arrival times data needed for
# the driving performance piece of employee_profile. 

# The connection to CTA's AVAS oracle database crapped out mid-data transfer,
# So this is a throwaway script to figure out how many days of data I got.
# Spoiler alert: the answer is 151 out of the 365 days in 2012.

with open(sys.argv[1]) as stream:

    dates = set()

    try:
        for row in csv.reader(stream):

            # Get the date from datetime fields in "MM/DD/YYYY HH:MM:SS" format.
            date = row[1].split(' ')[0]
            print date

            # Add dates to set to find unique dates in dataset
            dates.add(date)

    except csv.Error, e:

        print 'Newline up in this piece!'
        print e
        pass

    print dates