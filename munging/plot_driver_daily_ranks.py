import sys
import matplotlib.pyplot as plt

with sys.stdin as stream:

    # Parse driver daily average ranks.
    driver_daily_ranks = []
    driver_daily_otp = []
    for line in stream:
        driver, date, rank, otp = line.split()
        driver_daily_ranks.append(float(rank))
        driver_daily_otp.append(float(otp))

    driver_daily_ranks.sort()
    driver_daily_otp.sort()

    # Find rank quintile values.
    rank_quintile = len(driver_daily_ranks) / 5
    print len(driver_daily_ranks), rank_quintile
    rank_values = []
    for count in range(1,6):
        offset = rank_quintile * count
        print offset
        value = driver_daily_ranks[offset]
        rank_values.append(value)

    print 'Here are your rank quintile values: %s' % rank_values

    # Find otp quintile values.
    otp_quintile = len(driver_daily_otp) / 5
    print len(driver_daily_otp), otp_quintile
    otp_values = []
    for count in range(1,6):
        offset = otp_quintile * count
        value = driver_daily_otp[offset]
        otp_values.append(value)

    print 'Here are your otp quintile values: %s' % otp_values

    # Plot drivers' daily average rank.
    f, (ax1, ax2) = plt.subplots(2, 1)
    ax1.hist(driver_daily_ranks, bins=50)
    ax2.hist(driver_daily_otp, bins=50)
    plt.show()

print >> sys.stderr, 'Plotting daily driver ranks.'
