import apiaccess_2 as gatt 
import infofile
from matplotlib.backends.backend_pdf import PdfPages
from fpdf import FPDF
from pyPdf import PdfFileReader, PdfFileWriter
import os.path
from pudb import set_trace

PAGEVIEWS_DEFN = """
The phrase PAGE VIEWS here refers to the number of times a page has been loaded. 
If you refresh the page three times, that is 3 page views.
"""

VISITS_DEFN = """
The phrase VISITS here refers to the number of times a page has been visited at all.
This means that if you load a page on Tuesday, don't refresh it, close your computer,
then open the computer on Wednesday with the page still open, and do not refresh it then
either, this all counts as 1 view. It counts as 1, even if 
"""

def text_page_pdf(info_dict,fname, origfile, tmpfile="tmp_file_num.pdf"): # fname is the summary filename -- perhaps rename var TODO
	pdf = FPDF()
	#set_trace()
	pdf.add_page()
	pdf.set_font('Arial','',12) # adjust as appropriate
	x,y = 40,10
	pdf.cell(x,y,VISITS_DEFN) # well these long things need a lot of formatting help
	# so, should put in checks/management for every string var -- length + formatting
	pdf.ln()
	pdf.cell(x,y,PAGEVIEWS_DEFN)
	for k in info_dict:
		if k != "Across time span":
			pdf.cell(40,10, "%s: %d" % (k,info_dict[k]))
		pdf.ln()
	pdf.ln()
	# y += 10
	pdf.cell(x,y, "across time span of %s days" % (info_dict["Across time span"]))
	pdf.output(tmpfile, 'F')

	output = PdfFileWriter()
	fname = fname
	inp = PdfFileReader(file(origfile, "rb"))
	for i in range(inp.getNumPages()):
		output.addPage(inp.getPage(i))
	newf = PdfFileReader(file(tmpfile, "rb"))
	output.addPage(newf.getPage(0))
	outpStream = file(fname, "wb")
	output.write(outpStream)
	outpStream.close()



def main():
	# course views over time (input eventually for days previous + path to investigate [latter for all, infofile])
	#nd, nbdls, dlsv = 
	objs_for_plots = gatt.GoogleAnalyticsData(100), gatt.GABulkDownloads(100), gatt.GABulkDownloads_Views(100)
	plots = [x.main() for x in objs_for_plots]
	pp = PdfPages('oo_summary_1.pdf')
	throwaway = [pp.savefig(x) for x in plots]
	pp.close()

	# adding page with info ## -- should this be abstracted more? TODO
	info_obj = gatt.GA_Text_Info()
	info = info_obj.main() # returns infodict
	text_page_pdf(info, "oo_summary_4.pdf", "oo_summary_1.pdf") # no error w/ non-overwrite orig file change

	# testing stuff, view in console
	for k in info:
		print k, info[k]

# def save_pdf():
# 	return None

if __name__ == '__main__':
	main()

