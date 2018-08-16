
import csv
import argparse

def read_lecroy_csv(fname):
  raw_samples = []
	raw_times = []
	with open(fname, 'rb') as csvfile:
		c = csv.reader(csvfile)

		# Sample period: cell B2 (1,1)
		# Time: column D (3)
		# Samples: column E (4)

	csvfile.seek(0)
	for row in c:
		raw_samples.append(float(row[4]))
		raw_times.append(float(row[3]))

	return raw_samples, raw_times


def read_rigol_csv(fname, channel=1):
	sample_period = 0.0
	raw_samples = []
	raw_times = [0]
	sample_count = 0

	with open(fname, 'rb') as csvfile:
		c = csv.reader(csvfile)

		for row_num, row in enumerate(c):
			if row_num == 1:
				sample_period = float(row[1].split(':')[1])
				sample_count = int(row[3].split(':')[1])

			if len(row) > 0 and row[0] == 'X':
				break

		for row in c:
			if sample_count > 0:
				raw_samples.append(float(row[(channel-1)*2 + 1]))

			sample_count -= 1

	for i in len(raw_samples):
		raw_times.append(sample_period * i)

	return raw_samples, raw_times


def read_tek_tds2000_csv(fname):
	sample_period = 0.0
	raw_samples = []
	raw_times = [0]

	with open(fname, 'rb') as csvfile:
		c = csv.reader(csvfile)

		# Sample period is in cell B2 (1,1)

		for row_num, row in enumerate(c):
			if row_num == 1: # get the sample period
				sample_period = float(row[1])
				break

	# Sample data starts after the last header line
	# containing the firmware version.
	in_header = True
	for row in c:
		if in_header:
			if row[0] == 'Firmware Version':
				in_header = False
			else:
				raw_samples.append(float(row[4]))

	for i in len(raw_samples):
		raw_times.append(sample_period * i)

	return raw_samples, raw_times

def parse():
	global OSCIL, CHAN, IFILE, OFILE

	parser = argparse.ArgumentParser(description='https://github.com/zadewg/deside')

	parser.add_argument('-if','--infile', help='Input data filename\n', required=True)
	parser.add_argument('-of','--outfile', help='Output data filename\n', required=True)
	parser.add_argument('-o','--oscilloscope', help='Oscilloscope brand. Supported: Rigol, LeCroix, Tektronix\n', required=True)
	parser.add_argument('-c','--channel', help='Specify channel if neccesary. Default=1\n', required=False)

	args = vars(parser.parse_args())

	OSCIL = args['oscilloscope']
	CHAN = args['channel'] or 1
	IFILE = args['infile']
	OFILE = args['infile']


def main():
	
	parse()

	if OSCIL.lower() == 'rigol':
		data = read_rigol_csv(IFILE, channel=CHAN);
		times = data[1]
		values = data[0]

	elif OSCIL.lower() == 'lecroix':
		data = read_lecroy_csv(IFILE);
		times = data[1]
		values = data[0]

	elif OSCIL.lower() == 'tektronix':
		data = read_tek_tds2000_csv(IFILE);
		times = data[1]
		values = data[0]

	else:
		print('Oscilloscope not supported')
		raise SystemExit


	ofile  = open(('{}.csv'.format(OFILE)), "wb")
	writer = csv.writer(ofile, delimiter='', quotechar='"', quoting=csv.QUOTE_ALL)

	for i in len(times):
		writer.writerow(times[i], values[i])
 
	ofile.close()

if __name__ == "__main__":
	main()

