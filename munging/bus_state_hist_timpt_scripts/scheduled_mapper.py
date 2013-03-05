import csv
import sys

with sys.stdin as stream:

    print >> sys.stderr, 'Mapping scheduled arrival times!'
    
    for row in csv.reader(stream):

        # Print trip_id, timepoint_id, and scheduled arrival time (in sec
        # since midnight format) to stdout.
        print '%s\t%s\t%s\t' % (row[1], row[2].replace(' ','_'), row[7])