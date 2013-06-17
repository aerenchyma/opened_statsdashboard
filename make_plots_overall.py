import googleanalytics_apiaccess_timeseries_try as gatt 
import infofile
from matplotlib.backends.backend_pdf import PdfPages


def main():
	# course views over time (input eventually for days previous + path to investigate [latter for all, infofile])
	#nd, nbdls, dlsv = 
	objs_for_plots = gatt.GoogleAnalyticsData(), gatt.GABulkDownloads(), gatt.GABulkDownloads_Views()
	plots = [x.main() for x in objs_for_plots]
	pp = PdfPages('summary2.pdf')
	throwaway = [pp.savefig(x) for x in plots]
	pp.close()

# def save_pdf():
# 	return None

if __name__ == '__main__':
	main()

