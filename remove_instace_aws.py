#!/usr/bin/python
'''
Remove instances by tag running for more one hour
option -r region for aws
'''
import boto.ec2
import datetime
import logging
import optparse

def main(region):
	configurar_logs()
	logging.info('Start Script remove ami_builder')
	conn = boto.ec2.connect_to_region(region)
	res = conn.get_all_instances(filters={"tag:Name" : "*ami_builder*"})
	instances = [i for r in res for i in r.instances]
	for dado in instances:
		tm_i= calcula_time_instance(dado)
		tm_now = calcula_date_now()
		res = int(tm_now) - int(tm_i)
		final = res/3600
		if (final >=1) & (dado.state == 'running'):
			logging.info('terminate instance %s' %(dado.id))
			conn.terminate_instances(instance_ids=[dado.id])
	logging.info('End Script remove ami_builder')

def calcula_time_instance(dado):
	#print dado.id
	date_i = dado.launch_time.strip(".000Z")
	s_date_i = datetime.datetime.strptime(date_i, '%Y-%m-%dT%H:%M:%S')
	time_instace= int(s_date_i.strftime('%s')) -10800
	return time_instace

def calcula_date_now():
	utc_now = datetime.datetime.now()
	now  = utc_now.strftime("%s")
	return now

def configurar_logs():
	logging.basicConfig(level=logging.INFO,
	format='%(asctime)s %(levelname)-8s %(message)s',
  datefmt='%a, %d %b %Y %H:%M:%S',
  filename='/var/log/remove_amibuilder.log',
  filemode='a')
	#Handler para console.
	ch = logging.StreamHandler()
	ch.setLevel(logging.INFO)
	formatter = logging.Formatter('%(asctime)s %(message)s')
	ch.setFormatter(formatter)
	logging.getLogger('').addHandler(ch)

if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option('-r', '--region', dest='region', help='region aws run scrit')
	(options, args) = parser.parse_args()

	if not options.region:
		raise Exception("region (--region or -r) option is mandatory")
	main(options.region)
