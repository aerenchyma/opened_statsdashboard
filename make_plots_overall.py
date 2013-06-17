import googleanalytics_apiaccess_timeseries_try as gatt 
import infofile


def main():
	# course views over time (input eventually for days previous + path to investigate [latter for all, infofile])
	nd = gatt.GoogleAnalyticsData()
	nd.main()

	# other .. ADD; TODO

if __name__ == '__main__':
	main()

