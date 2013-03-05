#!/bin/bash

# Map actual arrival times.

# Parse raw timepoint actual arrival time data from `bus_state_hist_timept`
# table, print out subset of raw data, sort by trip_id, timepoint_id, and stop
# sequence, add a sequence number to the timepoint_id to deal with trips that
# have repeating timepoints, add tabs in awk so the columns line up the
# scheduled data and can be sorted.
cat $1 | python actual_mapper.py | sort -t$'\t' -k1n,1 -k2,2 -k3n,3 | python actual_mapper_timepoint_namer.py | awk '{print $1"\t", $2"\t", $3"\t", $4"\t", $5"\t", $6"\t"}' > actual_mappings;


# Map scheduled arrival times.

# Parse raw timepoint secheduled arrival time data from `schd_bus_timept_times`
# table, print out subset, sort by trip_id, timepoint_id, and scheduled
# arrival time, remove duplicate scheduled arrival times from previous
# schedule varions with uniq, add a sequence number to the timepoint_id and
# tab characters so columns lineup with actuals.
cat $2 | python scheduled_mapper.py | sort -t$'\t' -k3n | uniq | awk '{print $1"\t", NR"-"$2"\t", $3"\t"}' > scheduled_mappings;


# Reducer: match actual to schedule times, find the difference.

# Sort scheduled and actual arrival time mappings together on trip_id
# ordered_timepoint_id and (scheduled or actual) arrival time, pipe to reducer
# which finds the diffs.
sort -k1,1 -k2,2 -k3n,3 actual_mappings scheduled | python reducer.py;
