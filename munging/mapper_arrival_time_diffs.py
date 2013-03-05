import sys
import csv

with sys.stdin as stream:

    misparsed_rows = 0
    no_route_id = 0
    no_operator_id = 0
    no_schd_data = 0
    no_missing_values = 0

    for timepoint_arrival in csv.DictReader(stream):

        # Check to see record lacks columns due to parsing error, throw it out
        # if it does.
        if len(timepoint_arrival) != 31:
            print >> sys.stderr, 'This row had %s columns, was misparsed: %s' %  (len(timepoint_arrival), timepoint_arrival)
            misparsed_rows += 1
        else:

            # Check to see if route id is missing, throw out record if it is.
            if timepoint_arrival['ROUTE_ID'] == '':
                no_route_id += 1
            else:

            # Check to see if scheduled arrival time data is missing, throw out
            # record if it is. This happens when drivers are in manual mode (MMODE
            # = 1).
                if timepoint_arrival['SCHD_TIME'] == '':
                    no_schd_data += 1
                else:

                    # Check to see if operator badge number is missing, throw out
                    # record if it is.
                    if timepoint_arrival['OPERATOR_ID'] == '':
                        no_operator_id += 1
                    else:

                        route_id = timepoint_arrival['ROUTE_ID']
                        route_dir = timepoint_arrival['DIRECTION']
                        timepoint_id = timepoint_arrival['PLACEID'].replace(' ', '_')
                        scheduled_date = timepoint_arrival['SCHD_TIME'].split()[0]
                        scheduled_arrival_time = timepoint_arrival['SCHD_TIME'].split()[1]
                        operator_id = timepoint_arrival['OPERATOR_ID']
                        # Time bus arrived at timepoint bubble. ACTUAL_RAW_ETIME is time it left bubble.
                        # UNCLEAR WHICH ONE CTA IS USING IN THE DIFF CALCULATION.
                        actual_arrival_time = timepoint_arrival['ACTUAL_EVENT_TIME'].split()[1]   
                        diff = timepoint_arrival['DIFF']

                        # TTPOS tells you whether timepoint is a terminal or not, which
                        # factors into on-time-percentage calculations. Non-terminal
                        # timepoints have this field blank, this check set them to None so
                        # data is piped out with right number of columns.

                        if timepoint_arrival['TPPOS'] == '':
                            timepoint_pos = 'None'
                        else:
                            timepoint_pos = timepoint_arrival['TPPOS']

                        no_missing_values +=1

                        # debugging
                        # GREP THE PROBLEM ROW IN THE DATA, AND SEE WTF IS GOING ON. EITHER CHECK FOR LENGTH OF ROW UP TOP AND SKIP ROW IF NOT RIGHT LENGTH, OR TRY TO CATCH ERROR AND FIX IT.
                        debug = True
                        if debug:
                            for index, i in enumerate([route_id, route_dir, timepoint_id, scheduled_date, scheduled_arrival_time, actual_arrival_time, diff, operator_id, timepoint_pos]):
                                if ',' in i:
                                    print >> sys.stderr, timepoint_arrival
                                    print >> sys.stderr, index, i
                                    raise ValueError('There is a comma in there (%i)' % index)

                        # Print mapping to stdout        
                        print route_id, route_dir, timepoint_id, scheduled_date, scheduled_arrival_time, actual_arrival_time, diff, operator_id, timepoint_pos        

    # Report on how many records were tossed out.
    print >> sys.stderr, 'Created route direction timepoint diff mappings.'
    print >> sys.stderr, '%s rows were badly parsed, %s rows missing scheduled_arrival_time, %s rows missing operator_id, %s rows missing route_id and %s rows missing nothing.' % (misparsed_rows, no_schd_data, no_operator_id, no_route_id, no_missing_values)


