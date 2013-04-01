import json
import numpy as np

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from main.models import Employee, Deviation, DrivingRank
from main.utils import years_since, deviation_category2group

@login_required
def home(request):
    return render_to_response('main/home.html', 
        context_instance=RequestContext(request),
        )

@login_required
def employee_list(request):

    # Get all cta drivers for employee_list datatable.
    employee_list = Employee.objects.all()

    return render_to_response('main/employee_list.haml', {
        'employee_list': employee_list,
        },
        context_instance=RequestContext(request),
        )

@login_required
def employee_profile(request, badge_number):

    # Get the employee.
    employee = Employee.objects.get(badge_number=badge_number)

    # Crunch approx. number of years since employee started at CTA.
    employee.years_since_start = years_since(employee.start_date)


    # DEVIATION SECTION
    # Get employee's deviations.
    employee_deviations = Deviation.objects.filter(employee__badge_number=badge_number)

    # Get employee's FAST garage name from that employee's first deviation.
    # Replace this with garage data from payroll or FAST eventually.
    deviation_list = list(employee_deviations)
    if deviation_list:
        employee.deviation_garage_name = deviation_list[0].garage.name


    # Build d3 deviation calendar data.
    calendar_deviations = {}
    deviation_categories = []
    for deviation in employee_deviations:

        # Parse employee's deviations into deviation groups and categories
        # keyed on the date to display on D3 deviations calendar.
        clean_deviation_date = str(deviation.date).encode('utf8')
        calendar_deviations[clean_deviation_date] = [ deviation_category2group(deviation.category), deviation.category ]

        # Add employee's deviation categories to list to find their count below and display it on d3 badges.
        deviation_categories.append(deviation.category)

    calendar_deviations_json = json.dumps(calendar_deviations)


    # Build d3 deviation badges data.
    # Count employee's deviations by category.
    deviation_category_count = {}
    for category in deviation_categories:
        try:
            deviation_category_count[category] += 1
        except KeyError:
            deviation_category_count[category] = 1

    deviation_count_list = [(count, category) for (category, count) in deviation_category_count.items()]
    deviation_count_list.sort(reverse=True)

    deviation_badge_data = []
    for deviation_count in deviation_count_list:
        deviation_category = deviation_count[1]
        deviation_group = deviation_category2group(deviation_category)
        deviation_badge_data.append((deviation_count[0], deviation_count[1], deviation_group))

    deviation_badge_data_json = json.dumps(deviation_badge_data)


    # DRIVING PERFORMANCE SECTION
    # Get employee's daily average driving ranks.
    employee_driving_performance = DrivingRank.objects.filter(employee__badge_number=badge_number)

    # Parse employee's daily ranks into a rank dictionary keyed on the date to display on D3 driving calendar.
    calendar_driving_otp = {}
    calendar_driving_ranks = {}
    for driving_performance in employee_driving_performance:
        date = str(driving_performance.date).encode('utf8')
        calendar_driving_otp[date] = driving_performance.otp
        calendar_driving_ranks[date] = driving_performance.rank

    calendar_driving_otp_json = json.dumps(calendar_driving_otp)
    calendar_driving_ranks_json = json.dumps(calendar_driving_ranks)


    # Build data for d3 otp badges: count employee's daily otp values by quintile.
    # First, convert daily otp values to bin indexes. 
    otp_list = [opt for opt in calendar_driving_otp.itervalues()]
    x = np.array(otp_list)
    # Define the bins.
    otp_quintiles = np.array([0.0, 0.5, 0.60, 0.69, 0.78, 1.1])
    # Return the index of the quintile bin each daily otp value falls into.
    # Catch drivers with no driving data. digitize() throws an error if x is missing.
    try:
        inds = np.digitize(x, otp_quintiles)
        # Count the number of otp days per bin.
        otp_quintile_count = {}
        inds_to_otp_quintile_labels = {1: '0 - 50%', 2: '50 - 60%', 3: '60 - 69%', 4: '69 - 78%', 5: '78 - 100%'}
        for ind in inds:
            # Translate quintile bin indexes to quintile labels to display on badges.
            otp_quintile_label = inds_to_otp_quintile_labels[ind]
            try:
                otp_quintile_count[otp_quintile_label] += 1
            except KeyError:
                otp_quintile_count[otp_quintile_label] = 1
    except ValueError:
        otp_quintile_count = {'0 - 50%': 0, '50 - 60%': 0, '60 - 69%': 0, '69 - 78%': 0, '78 - 100%': 0}

    # Sort quintiles in ascending order to match css color classes.
    otp_badge_data = [(otp_quintile_label, count) for (otp_quintile_label, count) in otp_quintile_count.iteritems()]
    otp_badge_data.sort()

    otp_badge_data_json = json.dumps(otp_badge_data)


    # Build d3 rank badges data: count employee's daily rank scores by quintile.
    rank_list = [rank for rank in calendar_driving_ranks.itervalues()]
    # Convert rank days to bin indexes. 
    x = np.array(rank_list)
    # Define the bins.
    rank_quintiles = np.array([0, 2.718, 2.896, 3.06, 3.270, 5.1])
    # For each rank day, returns the index of the quintile bin it falls into.
    # Catch drivers with no driving data. digitize() throws an error if x is missing.
    try:
        inds = np.digitize(x, rank_quintiles)

        # Count number of rank days per bin.
        rank_quintile_count = {}
        # Tuples sort the quintile labels and count in the red-to-green order on the page.
        inds_to_rank_quintile_labels = {1: (5, 'Better than peers'), 2: (4, '+'), 3: (3, 'Same as peers'), 4: (2, '-'), 5: (1, 'Worse than peers') }
        for ind in inds:
            # Translate quintile bin indexes to quintile labels to display on badges.
            rank_quintile_label = inds_to_rank_quintile_labels[ind]
            try:
                rank_quintile_count[rank_quintile_label] += 1
            except KeyError:
                rank_quintile_count[rank_quintile_label] = 1
    except ValueError:
        rank_quintile_count = {(4, '+'): 0, (1, 'Worse than peers'): 0, (3, 'Same as peers'): 0, (5, 'Better than peers'): 0, (2, '-'): 0}

    # Sort quintiles in ascending order to match css color classes.
    rank_badge_data = [(rank_quintile_label, count) for (rank_quintile_label, count) in rank_quintile_count.iteritems()]
    rank_badge_data.sort()
    rank_badge_data_json = json.dumps(rank_badge_data)


    # Pass data to the template.
    return render_to_response('main/employee_profile.haml', {
            'employee': employee,
            'employee_deviations': employee_deviations,
            'calendar_deviations_json': calendar_deviations_json,
            'deviation_badge_data_json': deviation_badge_data_json,
            'calendar_driving_otp_json': calendar_driving_otp_json,
            'otp_badge_data_json': otp_badge_data_json,
            'calendar_driving_ranks_json': calendar_driving_ranks_json,
            'rank_badge_data_json': rank_badge_data_json,
            },
        context_instance=RequestContext(request),
        )
