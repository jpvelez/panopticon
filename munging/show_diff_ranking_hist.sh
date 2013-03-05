#!/bin/bash

# Plot histogram of drivers' daily (average) rank.
cat $1 | python mapper_arrival_time_diffs.py | sort | python reducer_diff_ranking.py | awk '{print $10, $4, $9, $8}' | sort | python find_driver_daily_ranks.py | python plot_driver_daily_ranks.py