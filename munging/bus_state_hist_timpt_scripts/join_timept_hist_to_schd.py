import sys
import csv

from pprint import pprint

# Map scheduled trip ids to scheduled arrival times. This mapping has two levels: it pairs trips to timepoints, then timepoints to scheduled times.
with open(sys.argv[2]) as stream:

    print "Building mapper!"

    # Parse scheduled timepoint data
    trip_to_scheduled_timepts = {}

    for scheduled_timept in csv.DictReader(stream):

        # Get keys for trip and timepoint dictionaries.
        trip_id = int(scheduled_timept['TRIPNO'])
        timepoint_id = scheduled_timept['TIMEPOINTID']

        # If schedule timepoint's trip_id key is already in dict, add timepoint data to that trip_id's timepoint dict.
        try:
            timept_list = trip_to_scheduled_timepts[trip_id]

            # Check if timepoint key has already been added to trip to prevent overwrites.
            if timepoint_id in timept_list:
                print trip_id
                print timept_list
                print timepoint_id, trip_id
                print scheduled_timept
            else:
                timept_list[timepoint_id] = scheduled_timept

        # If trip_id key is not in dict, add it, attach a dictionary to store scheduled timepoint data keyed by timepoint_id, 
        # and add first scheduled timepoint to this it.
        except KeyError:

            timept_list = {}
            timept_list[timepoint_id] = scheduled_timept

            trip_to_scheduled_timepts[trip_id] = timept_list


### NEVER FINISHED THIS PART ###

with open(sys.argv[1]) as stream:

    print 'Parsing actual arrival time data!'

    # Parse actual timepoint data 
    for actual_timept in csv.DictReader(stream):

        # Pull out the trip_id and timepoint_id of every actual timepoint arrival time.
        trip_id = actual_timept['TRIP_ID']
        timepoint_id = actual_timept['TIMEPOINT_ID']

        # Fetch the timepoint's scheduled arrival time from scheduled timepoint mapper
        if trip_id in trip_to_scheduled_timepts:
            scheduled_timept = trip_to_scheduled_timepts[trip_id][timepoint_id]

            print 'Actual timepoint:'
            pprint(actual_timept)
            print 'Scheduled timepoint:'
            pprint(scheduled_timept)

        else:
            print 'Couldnt find trip %s in schedules!' % trip_id

