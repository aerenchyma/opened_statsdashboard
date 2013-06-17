import googleanalytics_apiaccess_timeseries_try as gatt 
#from PIL import Image
import infofile
from matplotlib.backends.backend_pdf import PdfPages


def main():
	# course views over time (input eventually for days previous + path to investigate [latter for all, infofile])
	nd = gatt.GoogleAnalyticsData()
	nda = nd.main()
	# course bulk downloads over time
	nbdls = gatt.GABulkDownloads()
	nbdlsa = nbdls.main()
	# plot of course bulk downloads w/ course views
	dlsv = gatt.GABulkDownloads_Views()
	dlsva = dlsv.main()

	# next -- legend??

	pp = PdfPages('summary.pdf')
	pp.savefig(nda)
	pp.savefig(nbdlsa)
	pp.savefig(dlsva)
	pp.close()

def save_pdf():
	# assume filenames for now -- will need to make them more significant
	# img_oneplot = Image.open("test4.png")
	# img_twoplot = Image.open("test5.png")
	return None


if __name__ == '__main__':
	main()

