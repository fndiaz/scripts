#!/usr/bin/python
from datetime import datetime
import logging
import commands
import optparse

def main(address, log):
	configurar_logs(log)
	while(True):
		re=commands.getoutput("curl -s -o /dev/null -w 'status:%{http_code} time:%{time_total}' " +"%s" %(address)) 
		logging.info('%s - %s' %(re, address))

def configurar_logs(log):
  logging.basicConfig(level=logging.INFO,
  format='%(asctime)s %(levelname)-8s %(message)s',
  datefmt='%a, %d %b %Y %H:%M:%S',
  filename='/var/log/%s.log'%(log),
  filemode='a')
  #Handler para console.
  ch = logging.StreamHandler()
  ch.setLevel(logging.INFO)
  formatter = logging.Formatter('%(asctime)s %(message)s')
  ch.setFormatter(formatter)
  logging.getLogger('').addHandler(ch)

if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option('-a', '--address', dest='address', help='region aws run scrit')
	parser.add_option('-l', '--log', dest='log', help='log name')
	(options, args) = parser.parse_args()

	if not options.address:
		raise Exception("address (--address or -a) option is mandatory")
	if not options.log:
		options.log='endpoint'
	main(options.address, options.log)
