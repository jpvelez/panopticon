# STEPS - REWRITE THIS PART IN LIGHT OF HDW_ACTUAL_MASTER DIFFS

I need to get every time-point level actual arrival time in 2012 from `cta_history.bus_state_hist_timept` table.

Then I need write an aggregate query to find every scheduled `trip_id` during that time, and use it to query the `planning_pwr.schd_bus_timepoint_times` table to get actual scheduled arrival times for those time points.

Then I need to link the scheduled time-point arrival times to the actual arrival times by joining on the `tripno` + `timepointid` columns in `schd_bus_timepoint_times`.

Then, I need to compute the difference between scheduled and actual arrival time at each time-point to get the "time diffs". Then I need to group together all similar "time diffs" - assembles all diffs in every route-direction time-point half-hour for every day.

UPDATE: what you have now is a mapper-reducer that looks at actual arrival times and outputs the diff from the schedule arrival time. The diffs in the output are grouped by time point, so the diffs of different drivers on different days appear together. It only works for trips where each time point appears only once. So you need to:

- make it work for trips where time points appear more than once
- group together diffs in the same half-hour segment of the same day, and in the same route-direction (or pattern?)
- once you have that, find z-scores
- load the z-scores into django db
- figure out how to visualize timepoint-level trip z-scores into day-level color values for the employee_profile driving performance calendar.

# Possible data problems

I'm getting actual arrival time records from hdw_actual_master.
 
IN ORACLE AVAS DATA
1. Missing data: There might be actual arrivals that happened out there that are missing from the data, due to malfunctioning GPS on the bus or records being dropped somewhere in the data workflow. (The actual arrival come from `bus_state_hist_timept`.)
2. Measurement error: Actual arrival time measurements might be inaccurate due to GPS sensor errors, or data conversion errors.
3. Matching error: To find the differences between actual and scheduled arrival times (i.e. to create `hdw_actual_master`) the actuals had to be joined to the scheduled (which live in `schd_bus_timepoint_times`.) There could have been a joining error, resulting in mismatched arrival times and thus incorrect diffs.

IN LOCAL AVAS DATA
4. Missing data - bad transfer: to get the `hdw_actual_master` data for 2012 I wrote queries and got data through the wire. Might have lost data then, wouldn't be surprised if I did. 
Original table has 45,291,552 rows. I have 45,108,118. Difference of 183,434 records, .4%.

 22535938 hdw_actual_master_april_thru_sept.csv
 22535937 rows on sql query (no header row)

 11251011 hdw_actual_master_jan_thru_march.csv
 11251010 rows on sql query (no header row)

 11321172 hdw_actual_master_oct_thru_dec.csv
 11321171 rows on sql query (no header row)

 45108119 hdw_actual_master_2012.csv
 45108118 rows in three sql queries combined (no header row)
 45291552 rows in sql query for the entire year

Not clear why there's that 100K record difference!


3. Missing data - scheduled arrival times (due to driver error): I'm removing around 1% of records that lack scheduled arrival time data because they the bus was in "manual mode" at the time, which is when the drivers can't log on to AVAS and they have to log things manually. Apparently this results in actual arrival times not being tied to scheduled arrival times. Possible to join these actuals to the schedule, but probably not worth it.
3. Missing data - operator_ids: About .1% of the records in `hdw_actual_master` lack operator_ids. I'm also dropping these.
4. Missing data - route_ids: some of the `hdw_actual_master` records also lack route_id and are being dropped. Smaller percentage that operator ids.

5. Missing data - driving performance data pipeline: the ranking step of AVAS data pipeline is losing about 1% of records. Not sure why. 
(dsa)Congo-2:munging jpv$ head -n 10000 sorted_oct | python reducer_diff_ranking.py | wc -l
Calculated ranks for route direction timepoint diffs.
9904
6. missing data - employee matching problem between AVAS and payroll: 7160 out of 841354 driver-day daily ranking and top records had AVAS badge_numbers ('operator_id') that could not be matched to employee badge_numbers in Employee model (which come from payroll) during the loadavasdata step. This is .8% of days.

# hdw_actual_master data (data/AVAS data/)

- `hdw_actual_master_2012.csv`: dump of `hdw_actual_master` table for year 2012. Composed of following three tables:

`hdw_actual_master_jan_thru_march.csv`
`hdw_actual_master_april_thru_sept.csv`
`hdw_actual_master_oct_thru_dec.csv`

Might be missing data from oracle table, see above.

- `get_hdw_actual_master.sql`: sql query to get above dump of `hdw_actual_master` table.

- `hdw_actual_master_01_02_2012.csv`: single day sample of `hdw_actual_master_2012.csv` data for use when testing and writing out munging scripts.

- `daily_average_ranks_otp_2012`: daily rank/otp by driver output of munging scripts, ready to be ingested into django. Currently using this on the site, might be missing data for all reasons stated above.

# bus_state_hist_timept data - DEPRECATED 
# (data/AVAS data/actual_and_scheduled_timept_arrivals)
- schd_bus_timepoint_times.csv: full download of scheduled time point arrival times from `planning_pwr.schd_bus_timepoint_times' table. Downloaded 1/30/2013.

- get_bus_state_hist_timept.sql: contains the query to get relevant and properly formatted fields from `cta_history.bus_state_hist_timept`.

- bus_state_hist_timept.sample: partial actual time point arrival data from the `cta_history.bus_state_hist_timept` table.

Connection to AVAS database dropped with an IO error after ~4GB downloaded. It got about half of the 2012 data in the table:

Total rows in .biggersample: 21,341,851
Total rows in 2012: 47,605,014
Total rows in table: 363,276,397

It took 4 minutes to return table count, 38 minutes to return 2012 count.

- find_dates_in_bus_state_hist_timept.py: throwaway script to figure out how many days of data are in the above.

- non_project_avas_date_samples: dir containing mostly samples of other major AVAS tables (busstatehist, hdw stuff, etc.)

# hdw_actual_master scripts (munging/)

- `find_diff_ranking.sh`: chains the following scripts into a data pipeline that ingests raw `hdw_actual_master` data and spits out daily average ranks and on-time percentage for drivers to be ingested by `loadavasdata` management command.

- `mapper_arrival_time_diffs.py`: ingests `hdw_actual_master` data and prints out following mapping:

route_id, route_dir, timepoint_id, scheduled_date, scheduled_arrival_time, actual_arrival_time, diff, operator_id, timepoint_pos 

- `reducer_diff_ranking.py`: takes arrival_time_diff mappings and spits out each actual arrival time diff's on-time status as well as its rank relative to neighboring arrival times diffs.

- `find_driver_daily_ranks.py`: takes timepoint rankings and onetime status sorted by driver and day and find daily average ranks and one-time percentage for each driver. This is the data needed for the rank and otp driving performance maps.

- `show_diff_ranking_hist.sh`: runs every script like `find_diff_ranking.sh` and plots histograms of the daily rank/otp output of find_driver_daily_ranks.py. Useful for seeing the distribution of driver-day rank/otp values. Also calculate quintile percentages for each distribution to correctly map rank/otp values to 5-color diverging color ramp in D3 calendars.

# bus_state_hist_timept scripts - DEPRECATED 
# (munging/bus_state_hist_timept_scripts/)

- 54096883_actuals: actual ride arrival time data for trip 54096883. Got this by picking trip_ids from the tail of `schd_bus_timepoint_times` and greping `bus_state_hist_timept.bigsample` to see if there were any corresponding actual trips in the hist sample. This trip turned up a lot of rows. 

- 54096883_scheduled: actual ride arrival time data for the same trip.

- actual_mapper.py: prints out only important fields from `bus_state_hist_timept`, starting with trip_id and timepoint_id so you can quickly sort the output on that. The idea is to do the same thing to the scheduled and then sort them together. This will work for the whole dataset, but here's how to do it for the 54096883_actuals example:

`p actual_mapper.py < 54096883_actuals > 54096883_actuals_mapping`
`p scheduled_mapper.py < 54096883_scheduled > 54096883_scheduled_mapping`

- scheduled_mapper.py: prints out only important fields from schd_bus_timepoint_times. The actuals mapper outputs 5 fields, and the scheduled mapper only 3. This makes it easy to parse the combined results when you sort aa and bb together. Because of the order of the fields you're sorting on, early actual arrival times will show up before the scheduled arrival times, and late after. 

`sort aa bb | uniq | p reducer.py`

Because a trip will show up in multiple versions of the schedule (you'll see this in the version number on the original scheduled timepoint_rows), the duplicate scheduled rows will show up in the sorted results. Get rid of them using uniq, and then pipe things to the reducer.

- reducer.py: a hadoop-style reducer for the sorted mappings. This is hadoop style because you sort the data (sort is fast), the sequence of fields in the sort matters, and the code only processes a batch of records sorted to start with the same key (i.e. 'mapped'), so you keep less in memory and the code is fast. Read the script for the particulars on how to do this.

- To print cumulative distribution diffs between actual and scheduled arrival for a for a single time point, grep out a single time point and pipe it to xmgrace with the following transformation. 

This is better than a histogram with empirical data, especially when its sparse, because if you don't have a lot of data points the bins can look messed up. 

`sort aa bb | uniq | p reducer.py | grep 35_Org | sort -nk4 | awk '{print $4, 1.0-(NR-1)/23}' | xmgrace`

`1.0-(NR-1)/23` applies a cumulative distribution function to the diff values in $4, which will be plotted on the x avis.

- 54096883_actuals_mapping: outputted actual arrival time mappings.
- 54096883_scheduled_mapping: outputted scheduled arrival time mappings.

- join_timept_hist_to_schd.py: DEPRECATED. my attempt to join actual to scheduled arrival times through map reduce pattern. Abandoned in favor of scripts written with Dean above.s

# Datapoints I need to get
In the end, each record needs: 

- timepointid (both)
- a route-direction (hist has route_id and pattern, but it also has trip_id, maybe you can get route-direction from some trip lookup table) 
- an operator_id (hist)
- a date (hist)
- scheduled arrival time (schd, needs to be reformatted with to_char function) 
- actual arrival time (EVENT_TIME in hist, ditto)
- Also good to have trip_id/tripno (hist, schd) and run_id (hist, schd)


# TEST QUERY FOR 2012 ACTUAL TIME-POINT ARRIVAL TIMES

select * from (
select 
"BUS_STATE_ID",
to_char(EVENT_TIME,'DD/MM/YYYY HH24:MI:SS') ACTUAL_EVENT_TIME,
"EVENT_TYPE",
"TIMEPOINT_ID",
"BUS_ID",
"OPERATOR_ID",
"TRIP_ID",
"TRIP_TYPE",
to_char(TRIP_START_TIME,'DD/MM/YYYY HH24:MI:SS') ACTUAL_TRIPSTART_TIME,
to_char(DEPARTURE_TIME,'DD/MM/YYYY HH24:MI:SS') ACTUAL_DEPARTURE_TIME,
"ROUTE_ID",
"PATTERN",
"STOP_SEQUENCE",
"RUN_ID",
"LATITUDE",
"LONGITUDE",
"BLOCK_ID",
"DELTA_TIME",
"TIMEPOINT_TYPE",
"TIMEPOINT_DWELL",
"TIMEPOINT_STATUS"
"WORKID2",
"WORK_STATUS",
"WORK_VERSION"
from cta_history.bus_state_hist_timept
where event_time like '%-12'
) 
where ROWNUM <= 5;

# TEST QUERY FOR 2012 ACTUAL TIME-POINT ARRIVAL TIMES INTO CSV

select /*csv*/ * from (
select 
"BUS_STATE_ID",
to_char(EVENT_TIME,'DD/MM/YYYY HH24:MI:SS') ACTUAL_EVENT_TIME,
"EVENT_TYPE",
"TIMEPOINT_ID",
"BUS_ID",
"OPERATOR_ID",
"TRIP_ID",
"TRIP_TYPE",
to_char(TRIP_START_TIME,'DD/MM/YYYY HH24:MI:SS') ACTUAL_TRIPSTART_TIME,
to_char(DEPARTURE_TIME,'DD/MM/YYYY HH24:MI:SS') ACTUAL_DEPARTURE_TIME,
"ROUTE_ID",
"PATTERN",
"STOP_SEQUENCE",
"RUN_ID",
"LATITUDE",
"LONGITUDE",
"BLOCK_ID",
"DELTA_TIME",
"TIMEPOINT_TYPE",
"TIMEPOINT_DWELL",
"TIMEPOINT_STATUS"
"WORKID2",
"WORK_STATUS",
"WORK_VERSION"
from cta_history.bus_state_hist_timept
where event_time like '%-12'
) 
where ROWNUM <= 5
spool ~/dsa/CTA_Profiles/data/avas_busstatehist_timept.csv;


# REAL QUERY FOR 2012 ACTUAL TIME-POINT ARRIVAL TIMES

select 
"BUS_STATE_ID",
to_char(EVENT_TIME,'DD/MM/YYYY HH24:MI:SS') ACTUAL_EVENT_TIME,
"EVENT_TYPE",
"TIMEPOINT_ID",
"BUS_ID",
"OPERATOR_ID",
"TRIP_ID",
"TRIP_TYPE",
to_char(TRIP_START_TIME,'DD/MM/YYYY HH24:MI:SS') ACTUAL_TRIPSTART_TIME,
to_char(DEPARTURE_TIME,'DD/MM/YYYY HH24:MI:SS') ACTUAL_DEPARTURE_TIME,
"ROUTE_ID",
"PATTERN",
"STOP_SEQUENCE",
"RUN_ID",
"LATITUDE",
"LONGITUDE",
"BLOCK_ID",
"DELTA_TIME",
"TIMEPOINT_TYPE",
"TIMEPOINT_DWELL",
"TIMEPOINT_STATUS"
"WORKID2",
"WORK_STATUS",
"WORK_VERSION"
from cta_history.bus_state_hist_timept
where event_time like '%-12';

# REAL QUERY FOR 2012 ACTUAL TIME-POINT ARRIVAL TIMES TO CSV


spool avas_bustatehist_timept.csv
select /*csv*/ 
"BUS_STATE_ID",
to_char(EVENT_TIME,'DD/MM/YYYY HH24:MI:SS') ACTUAL_EVENT_TIME,
"EVENT_TYPE",
"TIMEPOINT_ID",
"BUS_ID",
"OPERATOR_ID",
"TRIP_ID",
"TRIP_TYPE",
to_char(TRIP_START_TIME,'DD/MM/YYYY HH24:MI:SS') ACTUAL_TRIPSTART_TIME,
to_char(DEPARTURE_TIME,'DD/MM/YYYY HH24:MI:SS') ACTUAL_DEPARTURE_TIME,
"ROUTE_ID",
"PATTERN",
"STOP_SEQUENCE",
"RUN_ID",
"LATITUDE",
"LONGITUDE",
"BLOCK_ID",
"DELTA_TIME",
"TIMEPOINT_TYPE",
"TIMEPOINT_DWELL",
"TIMEPOINT_STATUS"
"WORKID2",
"WORK_STATUS",
"WORK_VERSION"
from cta_history.bus_state_hist_timept
where event_time like '%-12';
spool off;

# REAL QUERY FOR SCHD_BUS_TIMEPOINT_TIME
select *
from planning_pwr.schd_bus_timepoint_times;