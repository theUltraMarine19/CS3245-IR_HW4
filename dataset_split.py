import csv
import os
import re
import sys
reload(sys)
sys.setdefaultencoding('ISO-8859-1')

csv.field_size_limit(sys.maxsize)

with open('dataset.csv', 'rb') as csv_file:
	reader = csv.reader(csv_file, delimiter=',', )
	file_ctr = 1
	num_lines = 100
	output_dir = os.path.join('output/', 'dataset_%s.csv' % file_ctr)

	writer = csv.writer(open(output_dir, 'w'), delimiter = ',')
	headers = reader.next()
	writer.writerow(headers)
	
	# print(sum(1 for row in reader))
	print "Hello"

	for index, row in enumerate(reader):
		print "I'm in"
		if index+1 > num_lines:
			file_ctr += 1
			num_lines = 100 * file_ctr
			output_dir = os.path.join('output/', 'dataset_%s.csv' % file_ctr)
			writer = csv.writer(open(output_dir, 'w'), delimiter = ',')
			writer.writerow(headers)
		writer.writerow(row)
		print index


