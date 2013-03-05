import sys

with sys.stdin as stream:

    # Set timepoint variables to None to start. These get reset when reducer
    # hits rows that start with a new trip-timepoint.

    trip_timepoint = None
    scheduled_arrival_time = None
    operator_arrival_times = None

    fuck_counter = 0

    for line in stream:

        # Since there are no columns headings, reading the lines into a list
        # lets check for what type of data it is - scheduled or actual arrival
        # time row - and lets you parse data for processing.

        schd_or_actual_arrival = line.split()

        # Get data out of row. Easier to use if labeled.
        if len(schd_or_actual_arrival) == 3:
            trip_id, ordered_timepoint_id, seconds_past_midnight, = line.split()
        else:
            trip_id, ordered_timepoint_id, seconds_past_midnight, stop_sequence, trip_date, operator_id = line.split()
            actual_arrival_time = int(seconds_past_midnight)

        # Short version: Is this a new (trip,timepoint) on which to compare drivers? We want
        # to do this comparison on a timepoint by timepoint basis. Only print
        # out results and reset data structures when we reach a new timepoint.

        # Long version: the following if statement runns on the first
        # iteration because trip_timepoint == None, and it skips the following
        # block for the same reason. trip_timpoint is then set to the current
        # trip-timepoint pair, and the first line is parsed, storing the
        # scheduled arrival time for the timepoint.
        # The next line probably is probably from the same trip-timepoint, so
        # now this whole section gets skipped. The script goes on and stores
        # actual arrival times by driver.
        # This continues until it hits a new batch of data with a different
        # trip-timepoint pair, which executes the following block and prints
        # the preceding trip-timepoint's data before processing the current
        # on.

        if (trip_id, ordered_timepoint_id) != trip_timepoint:

            # This only gets called once all actual arrival times (keyed on
            # the driver) have been gathered for the current timepoint. The
            # only reason it evaluates `is not None` is so this block doesn't
            # get executed on the very first iteration, only after the first
            # batch of actual arrival times have been parsed.

            if trip_timepoint is not None:

                # Iterate through drivers that have driven past the current time point.
                for operator_id in operator_arrival_times.iterkeys():

                    line_start = "%s %s %s" % (
                        trip_timepoint[0], trip_timepoint[1], operator_id,
                    )

                    # Get the actual arrival times of each driver at the timepoint.
                    for actual_arrival_time, trip_date in operator_arrival_times[operator_id]:

                        # Find the number of seconds between each actual
                        # arrival time and its scheduled arrival time, print
                        # diff to stdout.
                        if scheduled_arrival_time:

                            diff = actual_arrival_time - scheduled_arrival_time

                            print line_start, diff, trip_date, scheduled_arrival_time

                        # To match scheduled and actual timepoints, we're
                        # ordering the timepoint_ids by stop_sequence. Some
                        # trips are missing timepoint data, so these actual
                        # mappings will end up mislabeled. This means they'll
                        # be alone on the sorted list, with no neighboring
                        # scheduled arrival time and therefore no
                        # scheduled_arrival_time value. 

                        # This check prevents those records from breaking the
                        # loop, and measures how often they show up in the data.
                        else:
                            print >> sys.stderr, "OH NO! Could not match this actual arrival time to its scheduled time: %s %s" % (trip_timepoint[0], trip_timepoint[1])
                            fuck_counter += 1

                scheduled_arrival_time = None

            trip_timepoint = (trip_id, ordered_timepoint_id)
            operator_arrival_times = {}

        # Remember scheduled arrival time at timepoint.
        if len(schd_or_actual_arrival) == 3: 
            scheduled_arrival_time = int(seconds_past_midnight)

        # Remember each driver's actual arrival times at the timepoint.
        elif len(schd_or_actual_arrival) == 6:
            arrival_time_date = (actual_arrival_time, trip_date)
            try:
                operator_arrival_times[operator_id].append(arrival_time_date)
            except KeyError:
                operator_arrival_times[operator_id] = [arrival_time_date]
        else:
            raise Exception("Got a scheduled or actual timepoint arrival time row with weird fields!")

# Print final tally of misordered timepoint_ids. If there's a lot of them,
# find a better way of matching actual and scheduled arrival times than
# sorting of stop_sequence.
print >> sys.stderr, "Could not match %s actual arrival times to scheduled arrival times!" % fuck_counter