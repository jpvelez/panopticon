#!/bin/bash

# Output actual arrival times for each route direction timepoint, along with
# diff from scheduled arrival time and diff's rank compared with the diffs of
# neighboring arrivals.
export LC_ALL='C';
# Then sort rankings on driver and day and find each driver's daily average rankings.
cat $1 | python mapper_arrival_time_diffs.py | sort | python reducer_diff_ranking.py | awk '{print $10, $4, $9, $8}' | sort | python find_driver_daily_ranks.py

