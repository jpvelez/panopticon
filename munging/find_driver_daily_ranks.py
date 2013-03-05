import sys
from collections import Counter

with sys.stdin as stream:

    def average(driver_date_ranks):
        return sum(driver_date_ranks) / len(driver_date_ranks)

    def otp(driver_date_ontime_status):
        count = Counter(driver_date_ontime_status)
        on_time_timepoints = float(count['on-time'])
        total_timepoints = float(sum(count.values()))
        return on_time_timepoints / total_timepoints

    # Initialize variables for the loop
    previous_driver_date = None
    driver_date_ranks = []
    driver_date_ontime_status = []

    # Counters for missing rank data.
    missing_ranks = 0
    not_missing_ranks = 0

    # Iterate through sorted timepoint rank data.
    for line in stream:

        # Parse timepoint diff ranking line.
        rank_row = line.split()

        # Remember current driver and day.
        current_driver_date = (rank_row[0], rank_row[1])

        # Check if current driver and day is the same as the previous. When
        # loop hits a new driver-day section of the sorted diff rankings, find
        # the average of the rankings in the previous section, i.e. the
        # driver's daily average rank.
        if current_driver_date != previous_driver_date:

            if previous_driver_date != None:

                # Get driver and day for printing.
                driver = previous_driver_date[0]
                day = previous_driver_date[1]

                # Find driver's daily average diff rank.
                driver_daily_rank = average(driver_date_ranks)
                driver_daily_otp = otp(driver_date_ontime_status)

                # Print daily rank to stdout.
                print driver, day, driver_daily_rank, driver_daily_otp

                # Empty driver day data for the next driver day section.
                driver_date_ranks = []
                driver_date_ontime_status = []

            previous_driver_date = current_driver_date

        # Store timepoint rankings for each driver and day.
        try:
            diff_rank = float(rank_row[2])
            driver_date_ranks.append(diff_rank)

            ontime_status = rank_row[3]
            driver_date_ontime_status.append(ontime_status)

            not_missing_ranks += 1

        except IndexError:
            print >> sys.stderr, rank_row
            print >> sys.stderr, 'Driver %s missing rank or on-time status data on %s: %s' % (current_driver_date, rank_row)

            missing_ranks += 1

print >> sys.stderr, "%s timepts missing ranks or on-time status out of %s timepts." % (missing_ranks, not_missing_ranks)
print >> sys.stderr, "Found each driver's daily average ranking."
