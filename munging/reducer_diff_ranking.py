import sys

with sys.stdin as stream:

    # Find if diffs in window were late or not, and their on-time status,
    # using CTA's algorithm. WARNING: TERMINAL DEPARTURES ARE LATE IF > 2 MIN,
    # NOT FACTORED IN YET.
    def diff_to_ontime(indexed_window):

        ontime_window = []
        for index, row in indexed_window:

            # If timepoint is route terminal, actual arrivals two minutes past
            # their scheduled time count as late.
            if row[8] != 'None':

                diff = float(row[6])
                if diff > 2:
                    ontime_status = 'late'
                    is_ontime = False
                elif diff < -1:
                    ontime_status = 'early'
                    is_ontime = False
                else:
                    ontime_status = 'on-time'
                    is_ontime = True

            # If timepoint is not terminal, diffs over 5min count as late.
            else:

                diff = float(row[6])
                if diff > 5:
                    ontime_status = 'late'
                    is_ontime = False
                elif diff < -1:
                    ontime_status = 'early'
                    is_ontime = False
                else:
                    ontime_status = 'on-time'
                    is_ontime = True

            ontime_window.append((is_ontime, ontime_status, index, row))

        return ontime_window


    # Rank each on-time boolean in window. Find average rank to break ties.
    def ontime_to_rank_with_ties(ontime_window):

        # Do a simple ranking of sorted on-time booleans.
        # Result will look like this: 1. True, 2. True, 3. False, 4. False, 5. False.
        grouped = {}
        for rank, row_bundle in enumerate(ontime_window, 1):

            # To break "ties" (more than one diff was on-time), first: 
            # Group the rankings of tied on-time booleans.
            is_ontime = row_bundle[0]
            try:
                grouped[is_ontime].append(rank)
            except KeyError:
                grouped[is_ontime] = [rank]

        # Then: calculate the average rank of each tied on-time boolean.
        average_rank = {}
        for is_ontime, rank_list in grouped.iteritems():
            average_rank[is_ontime] = float(sum(rank_list)) / float(len(rank_list))

        # return a list that is "decorated" with the rank
        ranked_window = [(average_rank[is_ontime], is_ontime, ontime_status, index, row) for (is_ontime, ontime_status, index, row) in ontime_window]

        return ranked_window


    def metric(window):

        # This is the index of the diff we want to calculate the metrics for.
        middle_index = len(window) / 2

        indexed_window = [(index, row) for index, row in enumerate(window)]

        # Find wether diff was on-time or not.
        ontime_window = diff_to_ontime(indexed_window)

        # Sort on-time booleans so they can be ranked.
        ontime_window.sort(reverse=True)

        # Find ranks of timepoints, with ties.
        ranked_window = ontime_to_rank_with_ties(ontime_window)

        # Get the rank (and on-time status) for the timepoint in question at
        # the center of the window.
        for row_bundle in ranked_window:
            index = row_bundle[3]
            if index == middle_index:
                diff_rank = row_bundle[0]
                ontime_status = row_bundle[2]
                middle_row = row_bundle[4]

        return (diff_rank, ontime_status, middle_row)


    previous_route_dir_timepoint = None
    route_dir_timepoint_data = []

    # Iterate through route-direction timepoint diffs sorted by scheduled
    # arrival date and time.
    for line in stream:
        
        current_row = line.split()

        # Remember current row's route-direction timepoint.
        current_route_dir_timepoint = (current_row[0], current_row[1], current_row[2])

        # If you reach a section of the list where rows have a new route
        # direction timepoint, calculate and print out the ranks of diff in
        # previous route-direction timepoint section.
        if current_route_dir_timepoint != previous_route_dir_timepoint:

            # Prevent this code from getting run on the first row.
            if previous_route_dir_timepoint != None:

                window = []
                window_length = 5

                # Iterate through row in previous route-direction timepoint section.
                for row in route_dir_timepoint_data:

                    # Create sliding window of diffs. 
                    # Groups each diff row's neighboring rows.
                    if len(window) < 5:
                        window.append(row)

                    elif len(window) == window_length:

                        # Find rank of diff in the middle of the window relative to neighboring diffs in the window.
                        # Also return this middle diff's on-time status and row data.
                        diff_rank, ontime_status, middle_row = metric(window)

                        # Extract middle row's data.
                        try:
                            route_id = middle_row[0] 
                            route_dir = middle_row[1]
                            timepoint_id = middle_row[2] 
                            scheduled_date = middle_row[3]
                            scheduled_arrival_time = middle_row[4]
                            actual_arrival_time = middle_row[5]
                            diff = middle_row[6]
                            operator_id = middle_row[7]
                            timepoint_pos = middle_row[8]  
                        except IndexError:
                            print >> sys.stderr, middle_row
                            raise Exception('Could not get timept data out of window!')

                        # Print out previous route-direction timepoint's rank, diff, and other data. 
                        print route_id, route_dir, timepoint_id, scheduled_date, scheduled_arrival_time, \
                            actual_arrival_time, diff, ontime_status, diff_rank, operator_id, timepoint_pos

                        # Move window to next diff.
                        window.pop(0)
                        window.append(row)

                    else:
                        raise Exception("There's a bug!")

                    # Delete previous route-direction timepoint section's data to make room for current.
                route_dir_timepoint_data = []

            # Remember route-direction timepoint of new section so you can compare
            # it to incoming rows and detect when the timepoint section changes again.
            previous_route_dir_timepoint = current_route_dir_timepoint

        # Store current route-direction timepoint's rows.
        route_dir_timepoint_data.append(current_row)


print >> sys.stderr, 'Calculated ranks for route direction timepoint diffs.'


