import googleanalytics_apiaccess_timeseries_try as gatt 
import infofile

profileid = infofile.profileid
pgpath = infofile.pgpath
param_list = [profileid,pgpath]





def main():
	# course views over time (input eventually for days previous + path to investigate [latter for all, infofile])
	gatt.main(param_list)


if __name__ == '__main__':
	main()

