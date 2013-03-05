from pandas.io.parsers import read_csv
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Read in first 50k sample of ridecheckmaster data
trips = read_csv('avas_ridecheckmaster_sample.csv')

# Filter out trips from September 10th, 2009
trips_9_10_09 = trips[trips['SURVEY_DATE'] == '10-SEP-09']


# Group 9/10 trips by operator
drivers = trips_9_10_09.groupby('OPERATOR_ID')

# Count the number of trips for each operator
driver_trips = drivers.size()

# Plot histogram of trips per driver
driver_trips.hist()


# Plot scatterplot of total stops per trip vs. percentage of "on time" trip timepoints 
# trips_sample = trips_9_10_09.head(200)
# plt.scatter(trips_sample.TOTAL_STOPS, trips_sample.ONTIME)

# Run OLS regression to measure relationship between total stops and OTP
# model = sm.OLS(trips_sample.ONTIME, trips_sample.TOTAL_STOPS).fit()
# print model.summary()



