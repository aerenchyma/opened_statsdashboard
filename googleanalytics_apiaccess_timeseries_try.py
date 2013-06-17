import sys
import infofile
from pylab import * #?
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from datetime import date, timedelta
from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError
import httplib2
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

# structural stuff, TODO
# generalization; TODO

class GoogleAnalyticsData(object):
	def __init__(self, days_back=30):
		self.days_back = days_back
		self.CLIENT_SECRETS = 'client_secrets.json'
		# helpful msg if it's missing
		self.MISSING_CLIENT_SECRETS_MSG = '%s is missing' % self.CLIENT_SECRETS
		self.paramlist = [int(infofile.profileid),infofile.pgpath] # should this be here or in overall file??
		# self.profileid = infofile.profileid
		# self.pgpath = infofile.pgpath

		# self.param_list = [profileid, pgpath]

		# flow object to be used if we need to authenticate (?)
		self.FLOW = flow_from_clientsecrets(self.CLIENT_SECRETS, scope='https://www.googleapis.com/auth/analytics.readonly', message=self.MISSING_CLIENT_SECRETS_MSG)

		# a file to store the access token
		self.TOKEN_FILE_NAME = 'analytics.dat' # should be stored in a SECURE PLACE


	def proper_start_date(self):
		"""Gets accurate date in YYYY-mm-dd format that is 30 days earlier than current day"""
		d = date.today() - timedelta(days=self.days_back)
		return str(d)


	def prepare_credentials(self):
		# get existing creds
		storage = Storage(self.TOKEN_FILE_NAME)
		credentials = storage.get()

		# if existing creds are invalid and Run Auth flow
		# run method will store any new creds

		if credentials is None or credentials.invalid:
			credentials = run(FLOW, storage)

		return credentials

	def initialize_service(self):
		http = httplib2.Http()
		credentials = self.prepare_credentials()
		http = credentials.authorize(http) # authorize the http obj
		return build('analytics', 'v3', http=http)


	def deal_with_results(self,res):
		"""Handles results gotten from API and formatted, plots them with matplotlib tools and saves plot img"""
		view_nums = [x[1] for x in res] # y axis
		date_strs = [mdates.datestr2num(x[0]) for x in res] # hmm these are strings... # x axis
		#date_strs = [mdates.strpdate2num(x[0],'%m-%d') for x in res]

		fig, ax = plt.subplots(1)
		ax.plot_date(date_strs, view_nums, fmt="g-")
		fig.autofmt_xdate()

		ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
		#plt.title('fix label test')
		total = sum(view_nums)
		plt.title("%d total Course Views over past %s days" % (total, len(date_strs)-1)) # should get title of course

		savefig('test3.png')

	def main(self):
		self.service = self.initialize_service()
		try:
			self.profile_id = self.paramlist[0]#sys.argv[1]
			#print "still in main"
			if self.profile_id:
				#print profile_id
				#query core reporting api
				results = self.get_results(self.service, self.profile_id)
				#print_results(results) # hmm formatting, also where should these go
				res = self.return_results(results)
				#print res
		except TypeError, error:
			print "There was an API error: %s " % (error)
		except HttpError, error:
			print "There was an API error: %s " % (error)
		except AccessTokenRefreshError:
			print "The credentials have been revoked or expired, please re-run app to reauthorize."
		except:
		 	print "Did you provide a profile id and a path as cli arguments? Try again."
		else: # should run if it did not hit an except clause
			self.deal_with_results(res)

	def get_results(self, service, profile_id):
		# query = service.data().ga().get(ids='ga:%s' % profile_id, start_date='2010-03-01',end_date='2013-05-15',metrics='ga:pageviews',dimensions='ga:pagePath',filters='ga:pagePath==%s' % (sys.argv[2]))
		start = self.proper_start_date() # change to change num of days back 
		end = str(date.today())
		# return query.execute()
		return self.service.data().ga().get(ids='ga:%s' % (profile_id), start_date=start,end_date=end,metrics='ga:pageviews',dimensions='ga:date',sort='ga:date',filters='ga:pagePath==%s' % (self.paramlist[1])).execute()#(sys.argv[2])).execute()


	def return_results(self, results):
		if results:
			#date_views_tup = [(str(x[0][-4:-2])+"/"+str(x[0][-2:]),int(x[1])) for x in results.get('rows')] ## altered date strs
				# should be list of tuples of form: ("mm/dd", views) where views is int
			date_views_tup = [(str(x[0]), int(x[1])) for x in results.get('rows')]
			return date_views_tup
		else:
			print "No results found."
			return None

	def print_results(self, results):
		# print data nicely for the user (may also want to pipe to a file)
		if results:
			print "Profile: %s" % results.get('profileInfo').get('profileName')
			#print 'Total Pageviews: %s' % results.get('rows')[0][1]
			for r in results.get('rows'):
				print r
		else:
			print "No results found."
		# for modularity -- poss look at Python print-results examples (e.g. by country or whatever) todo


class GABulkDownloads_Views(GoogleAnalyticsData):
	def __init__(self, days_back=30):
		self.days_back = days_back
		self.CLIENT_SECRETS = 'client_secrets.json'
		# helpful msg if it's missing
		self.MISSING_CLIENT_SECRETS_MSG = '%s is missing' % self.CLIENT_SECRETS
		self.paramlist = [int(infofile.profileid),self.get_bulk_dl_link()] # needs error checking TODO
		self.paramlist_second = [int(infofile.profileid), infofile.pgpath]
		self.FLOW = flow_from_clientsecrets(self.CLIENT_SECRETS, scope='https://www.googleapis.com/auth/analytics.readonly', message=self.MISSING_CLIENT_SECRETS_MSG)
		self.TOKEN_FILE_NAME = 'analytics.dat'
		#print self.paramlist

	def get_bulk_dl_link(self):
		try:
			import mechanize
			br = mechanize.Browser()
		except:
			print "Dependency (Mechanize) not installed. Try again."
			return None
		else:
			response = br.open("http://open.umich.edu%s" % infofile.pgpath)
			for link in br.links():
				if "Download all" in link.text: # depends on current page lang/phrasing
					response = br.follow_link(link)
					url = response.geturl()
			return url[len("http://open.umich.edu"):] # if no Download All, error -- needs checking + graceful handling

	def get_results_other(self, service, profile_id):
		# query = service.data().ga().get(ids='ga:%s' % profile_id, start_date='2010-03-01',end_date='2013-05-15',metrics='ga:pageviews',dimensions='ga:pagePath',filters='ga:pagePath==%s' % (sys.argv[2]))
		start = self.proper_start_date() # change to change num of days back 
		end = str(date.today())
		# return query.execute()
		return self.service.data().ga().get(ids='ga:%s' % (profile_id), start_date=start,end_date=end,metrics='ga:pageviews',dimensions='ga:date',sort='ga:date',filters='ga:pagePath==%s' % (self.paramlist_second[1])).execute()#(sys.argv[2])).execute()


	def deal_with_results(self, res):
		"""Handles results gotten from API and formatted, plots them with matplotlib tools and saves plot img"""
		view_nums = [x[1] for x in res] # y axis
		view_nums_orig = [x[1] for x in self.return_results(self.get_results_other(self.service,self.profile_id))] ## let's see
		date_strs = [mdates.datestr2num(x[0]) for x in res] # x axis
		fig, ax = plt.subplots(1)
		ax.plot_date(date_strs, view_nums, fmt="b-")
		ax.plot_date(date_strs, view_nums_orig, fmt="g-")
		fig.autofmt_xdate()
		ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
		total = sum(view_nums)
		plt.title("Course Views vs Bulk Material Downloads over past %s days" % (len(date_strs)-1)) # should get title of course
		savefig('test4.png')


class GABulkDownloads(GABulkDownloads_Views):
	def deal_with_results(self, res):
		"""Handles results gotten from API and formatted, plots them with matplotlib tools and saves plot img"""
		view_nums = [x[1] for x in res] # y axis
		date_strs = [mdates.datestr2num(x[0]) for x in res] # x axis
		fig, ax = plt.subplots(1)
		ax.plot_date(date_strs, view_nums, fmt="r-")
		fig.autofmt_xdate()
		ax.fmt_xdata = mdates.DateFormatter('%Y-%m-%d')
		total = sum(view_nums)
		plt.title("%d total Bulk Course Material Downloads over past %s days" % (total, len(date_strs)-1)) # should get title of course
		savefig('test5.png')



if __name__ == '__main__':

	#main(sys.argv)
	#main(param_list)
	#print "running the right file"
	a = GoogleAnalyticsData()
	#print a.paramlist[0]
	a.main()

	c = GABulkDownloads_Views()
	c.main()

	b = GABulkDownloads()
	#print b.paramlist
	b.main()




