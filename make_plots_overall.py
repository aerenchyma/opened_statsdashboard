import googleanalytics_apiaccess_timeseries_try as gatt 
import infofile


def main():
	# course views over time (input eventually for days previous + path to investigate [latter for all, infofile])
	nd = gatt.GoogleAnalyticsData()
	nd.main()
	# course bulk downloads over time
	nbdls = gatt.GABulkDownloads()
	nbdls.main()
	# plot of course bulk downloads w/ course views
	dlsv = gatt.GABulkDownloads_Views()
	dlsv.main()

	# next == plot on same plot with legend ?

if __name__ == '__main__':
	main()

