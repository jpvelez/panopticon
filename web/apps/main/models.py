from django.db import models


# Populated from payroll data. Garage names in FAST are matched to payroll
# names so deviations can be linked to this table. No garages in AVAS data yet.
class Garage(models.Model):

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Garage'
        verbose_name_plural = 'Garages'
        
    def __unicode__(self):
        return 'Garage: %i, %s' % (self.id, self.name)


class Employee(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    SEX = (
        (MALE, 'Male'),
        (FEMALE, 'Female')
        )

    badge_number = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    job_category = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    sex = models.CharField(choices=SEX, max_length=1)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    apt = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    garage = models.ForeignKey(Garage)

    # Added by loadpayrolldatacommand so employee_list table load quicker by
    # avoiding extra queries to garage table get garage name.
    garage_name = models.CharField(max_length=255)

    # ADded by crunchemployeedeviations command for same reason.
    n_deviations = models.IntegerField(null=True)

    # garage_stints = models.ManyToManyField('Garage', through='GarageStint')

    # This method is called whenever an employee object is printed. Object
    # values must be interpolated to a string or this function freaks out when
    # called.
    def __unicode__(self):
        return 'Employee: %i, %s %s' % (self.badge_number, self.first_name, self.last_name)


class Deviation(models.Model):

    category = models.CharField(max_length=50)
    date = models.DateField()
    employee = models.ForeignKey(Employee)
    garage = models.ForeignKey(Garage)

    class Meta:
        verbose_name = 'Deviation'
        verbose_name_plural = 'Deviations'

    def __unicode__(self):
        return 'Deviation: %s, %s, %s' % (self.category, self.date, self.employee)


class DrivingRank(models.Model):
    rank = models.FloatField()
    otp = models.FloatField()
    date = models.DateField()
    employee = models.ForeignKey(Employee)

    class Meta:
        verbose_name = 'DrivingRank'
        verbose_name_plural = 'DrivingRanks'

    def __unicode__(self):
        return 'DrivingRank: %s, %s, %s' % (self.rank, self.date, self.employee)



# Implement this once you have multiple garages per driver. Right now garages
# are being added by payroll data import command. Only the last garage showing
# up in the 2012 payroll data is being added.

# class GarageStint(models.Model):
#     employee = models.ForeignKey(Employee)
#     garage = models.ForeignKey(Garage)
#     start_date = models.DateField()
#     end_date = models.DateField()

#     class Meta:
#         verbose_name = 'GarageStint'
#         verbose_name_plural = 'GarageStints'

#     def __unicode__(self):
#         return 'GarageStint: %s, %s, %s' % (self.employee, self.garage, self.start_date)



# Not being used. Could be used to look at payment data on the employee list
# or view. loadpayroll data would need to feed this model.

# class Payment(models.Model):
#     employee = models.ForeignKey(Employee)
#     date_paid = models.DateField()
#     earnings_code = models.CharField(max_length=50)
#     hours_worked = models.FloatField()
#     hourly_rate = models.FloatField()
#     pay_period_start = models.DateField()

#     class Meta:
#         verbose_name = ('Payment')
#         verbose_name_plural = ('Payments')

#     def __unicode__(self):
#         return 'Payment: %s, %s, %s' % (self.employee, self.earnings_code, self.date_paid)

