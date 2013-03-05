import sys
import datetime
import csv

with sys.stdin as stream:

    print >> sys.stderr, 'Mapping actual arrival times!'

    # Skip data headers
    actuals = csv.reader(stream)
    actuals.next()

    # Iterate through actual time arrival rows, converting values and printing mappings.
    for row in actuals:

        # Convert timestamp to seconds past midnight, so actual arrivals can
        # be sorted with scheduled ones.

        timestamp = row[1]
        arrival_datetime = datetime.datetime.strptime(timestamp, "%d/%m/%Y %H:%M:%S")

        # Find midnight for the day the arrival happened on
        midnight = datetime.datetime(arrival_datetime.year, 
                                    arrival_datetime.month, 
                                    arrival_datetime.day
                                    )

        # Find time between midnight and the actual arrival time.
        time_past_midnight = arrival_datetime - midnight

        # Prep actual data for printing: add _ to timepoint_id for easier
        # parsing, find seconds since midnight.
        trip_id = row[6]
        timepoint_id = row[3].replace(' ', '_')
        seconds_past_midnight = time_past_midnight.seconds
        trip_date = midnight.date()
        stop_sequence = row[12]
        operator_id = row[5]

        # Print mapping to stdout. 
        print '%s\t%s\t%s\t%s\t%s\t%s\t' % (trip_id, trip_date, stop_sequence, timepoint_id, seconds_past_midnight, operator_id)
