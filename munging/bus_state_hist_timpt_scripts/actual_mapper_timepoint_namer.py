import sys

with sys.stdin as stream:

    print >> sys.stderr, 'Relabeling timepoints for actual arrival times!'

    counter = 0
    previous_trip_id = None
    previous_date = None 

    for line in stream:

        # Import actual arrival time mappings sorted by trip, timepoint, and stop sequence.
        trip_id, date, stop_sequence, timepoint_id, seconds_past_midnight, operator_id = line.split('\t')[:6]

        # Check to see if both date and trip_id are equal, if so, then just
        # increment counter. Otherwise reset the counter since it is a new
        # day/trip.
        if trip_id == previous_trip_id and date == previous_date:
            counter += 1
        else:
            counter = 1

        # Create a new timepoint_id that is numbered according to the timepoint's stop sequence on that trip.
        ordered_timepoint_id = str(counter) + '-' + timepoint_id
        
        # Print mappings to stdout
        print '%s\t%s\t%s\t%s\t%s\t%s\t' % (trip_id, ordered_timepoint_id, seconds_past_midnight, stop_sequence, date, operator_id)

        # Set trip_id and date to compare with next actual arrival time row
        previous_trip_id = trip_id
        previous_date = date


