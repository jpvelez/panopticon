# This script extracts the raw FAST deviation data from the rawdata sheets in the spreadsheets which cover all garages from June-November 2012.
import sys
import xlrd
import csv
import datetime

# use standard out to write our csv output
writer = csv.writer(sys.stdout)
writer.writerow([
    'Date', 
    'Last Name',
    'First Name',
    'Badge Number',
    'Deviation ID',
    'Deviation Category',
    'Garage Name',
])

# get a list of excel files to extract data from
for filename in sys.argv[1:]:
    print >> sys.stderr, 'Reading %s' % filename

    # read the correct sheet from the excel file
    book = xlrd.open_workbook(filename)

    sheet = book.sheet_by_name('Rawdata')

    # get the garage name from the filename
    garage = filename.split('-')[1].strip().replace('(1)', '').replace('.xls', '')

    # print out each line with garage column added
    for index in range(1, sheet.nrows):

        # get xlrd row object and convert it to something more normal
        row = sheet.row(index)
        clean_row = [cell.value for cell in row[:6]]

        # convert weird excel date number to tuple, then to date object. if it's unconvertable, skip this row for now
        try:
            date_tuple = xlrd.xldate_as_tuple(clean_row[0], book.datemode)
        except ValueError:
            print >> sys.stderr, 'skipping row %i' % index
            print >> sys.stderr, row
        clean_date = datetime.datetime(*date_tuple).date()

        # replace date number with clean, parsed date
        clean_row[0] = clean_date

        # add the garage name at the end of the row
        clean_row.append(garage)

        # write nicely formatted csv row 
        writer.writerow(clean_row)
