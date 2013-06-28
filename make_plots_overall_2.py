import apiaccess_2 as gatt 
import infofile
from matplotlib.backends.backend_pdf import PdfPages
from fpdf import FPDF
from pyPdf import PdfFileReader, PdfFileWriter
import os.path
from pudb import set_trace

PAGEVIEWS_DEFN = """
The word (PAGE)VIEWS here refers to the number of times a page has been loaded. 
If you refresh the page three times, that is 3 page views.
"""

VISITS_DEFN = """
The word VISITS here refers to the number of times a page has been visited at all.
This means that if you load a page on Tuesday, don't refresh it, close your computer,
then open the computer on Wednesday with the page still open and click around on it,
this all counts as only one view.
"""

def text_page_pdf(info_dict,fname, origfile, tmpfile="tmp_file_num.pdf", tmpfile2="tmp_file_2.pdf"): # fname is the summary filename -- perhaps rename var TODO
	pdf = FPDF()
	defns_pdf = FPDF()
	#set_trace()
	pdf.add_page()
	defns_pdf.add_page()
	pdf.set_font('Times','',12) # adjust as appropriate
	defns_pdf.set_font('Times','',12)
	x,y = 30,10
	#pdf.cell(x,y,PAGEVIEWS_DEFN)
	pdf.cell(x,y, "Across time span of %s days:" % (info_dict["Across time span"]))
	pdf.ln()
	for k in info_dict:
		if k != "Across time span":
			pdf.cell(x,y, "%s: %d" % (k,info_dict[k]))
			pdf.ln()
	pdf.output(tmpfile, 'F')

## second page should have title; TODO. all of course need better formatting
	visits_list = VISITS_DEFN.split("\n")
	pageviews_list = PAGEVIEWS_DEFN.split("\n")
	for l in visits_list:
		defns_pdf.cell(x,y,l)
		defns_pdf.ln()
	#pdf.ln()
	for l in pageviews_list:
		defns_pdf.cell(x,y,l)
		defns_pdf.ln()

	defns_pdf.output(tmpfile2,'F')

	output = PdfFileWriter()
	fname = fname
	inp = PdfFileReader(file(origfile, "rb"))
	for i in range(inp.getNumPages()):
		output.addPage(inp.getPage(i))
	newf = PdfFileReader(file(tmpfile, "rb"))
	newf2 = PdfFileReader(file(tmpfile2, "rb"))
	output.addPage(newf.getPage(0))
	output.addPage(newf2.getPage(0))
	outpStream = file(fname, "wb")
	output.write(outpStream)
	outpStream.close()



def main():
	# summary numbers and chart numbers are not the same -- diff timespans -- where is that determined 
	## TODO sync!


	# course views over time (input eventually for days previous + path to investigate [latter for all, infofile])
	#nd, nbdls, dlsv = 
	days_back = 100
	objs_for_plots = gatt.GoogleAnalyticsData(days_back), gatt.GABulkDownloads(days_back), gatt.GABulkDownloads_Views(days_back)
	plots = [x.main() for x in objs_for_plots]
	pp = PdfPages('oo_summary_1.pdf')
	throwaway = [pp.savefig(x) for x in plots]
	pp.close()

	# adding page with info ## -- should this be abstracted more? TODO
	info_obj = gatt.GA_Text_Info(days_back)
	info = info_obj.main() # returns infodict
	text_page_pdf(info, "oo_summary_4.pdf", "oo_summary_1.pdf") # no error w/ non-overwrite orig file change

	# testing stuff, view in console
	for k in info:
		print k, info[k]

# def save_pdf():
# 	return None

if __name__ == '__main__':
	main()

