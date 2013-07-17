import apiaccess_2 as gatt 
import infofile
import datetime
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

def create_final_filename():
	today = str(datetime.date.today())
	pg = infofile.pgpath[11:].replace("/","_")
	return "%s_%s.pdf" % (pg, today)

#TODO factor out functionality; this code is pretty gross
def text_page_pdf(info_dict,fname, origfile, tmpfile="tf_1.pdf", tmpfile2="tf_2.pdf", tmpfile3="tf_3.pdf"): # fname is the summary filename -- perhaps rename var TODO
	
	#yrlong info object(s)
	gat2 = gatt.GA_Text_Info(365)
	info_gat2 = gat2.main()
	# gatforever = gatt.GA_Text_Info(2920)
	# info_gatf = gatforever.main()

	pdf = FPDF()
	sec_pdf = FPDF()
	defns_pdf = FPDF()
	#set_trace()
	pdf.add_page()
	defns_pdf.add_page()
	sec_pdf.add_page()
	sec_pdf.set_font('Times', '', 12) # adjust as appropriate TODO
	pdf.set_font('Times','',12) # adjust as appropriate TODO
	defns_pdf.set_font('Times','',12) # adjust as appropriate TODO
	x,y = 30,10
	#pdf.cell(x,y,PAGEVIEWS_DEFN)
	pdf.cell(x,y, "Across time span of %s days:" % (info_dict["Across time span"]))
	pdf.ln()
	diff_keys = ["Across time span", "Top Nations", "Top Resources"]
	for k in info_dict:
		if k not in diff_keys:
			pdf.cell(x,y, "%s: %d" % (k,info_dict[k]))
			pdf.ln()
	pdf.ln()
	pdf.cell(x,y, "Over the past year:")
	pdf.ln()
	for k in info_gat2:
		if k not in diff_keys:
			pdf.cell(x,y, "%s: %d" % (k, info_gat2[k]))
			pdf.ln()
	pdf.ln() 

	# TODO -- 'ever' -- past-days doesn't seem to work when over a yr, need new special query w/diff start
	# pdf.cell(x,y,"Since course has been published on Open.Michigan:")
	# pdf.ln()
	# for k in info_gatf:
	# 	if k not in diff_keys:
	# 		pdf.cell(x,y,"%s: %d" % (k, info_gatf[k]))
	# 		pdf.ln()


# TODO must start new page here; information is being cut off.

	if info_dict["Top Nations"][0] == 'United States':
		sec_pdf.cell(x,y, "Top non-US countries visiting this course over past %s days:" % (info_dict["Across time span"]),0,1) # ALL time right now ## if change, add back to str: % (info_dict["Across time span"])
		for n in info_dict["Top Nations"][1:]:
			sec_pdf.cell(x,y, "* %s" % n)
			sec_pdf.ln()
	else:
		sec_pdf.cell(x,y, "Top countries visiting this course:",0,1)
		for n in info_dict["Top Nations"][:-1]:
			sec_pdf.cell(x,y, "* %s" % n)
			sec_pdf.ln()
	sec_pdf.ln()
	sec_pdf.cell(x,y,"Top 10 individual files ever downloaded from this course, and how many times:",0,1) # ALL time right now
	#pdf.ln()
	for r in info_dict["Top Resources"]:
		sec_pdf.cell(x,y, "* %s" % r)
		sec_pdf.ln()

	pdf.output(tmpfile, 'F')
	sec_pdf.output(tmpfile3,'F')

## defns etc page should have title; TODO. all of course need better formatting
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
	newf3 = PdfFileReader(file(tmpfile3,"rb"))
	newf2 = PdfFileReader(file(tmpfile2, "rb"))
	output.addPage(newf.getPage(0))
	output.addPage(newf3.getPage(0))
	output.addPage(newf2.getPage(0))
	outpStream = file(fname, "wb")
	output.write(outpStream)
	outpStream.close()

def main():
	# course views over time (input eventually for days previous + path to investigate [latter for all, infofile])
	days_back = 30
	tmp_filename = "incompletesummary.pdf"
	objs_for_plots = gatt.GoogleAnalyticsData(days_back), gatt.GABulkDownloads(days_back), gatt.GABulkDownloads_Views(days_back), gatt.GABulkDownloads_Views(365)
	plots = [x.main() for x in objs_for_plots]
	pp = PdfPages(tmp_filename) # something around here isn't working -- generating pdf without plots. why? TODO
	throwaway = [pp.savefig(x) for x in plots]
	pp.close()

	# adding page with info ## -- should this be abstracted more? TODO
	info_obj = gatt.GA_Text_Info(days_back)
	info_obj.get_more_info()
	info = info_obj.main() # returns infodict
	final_filename = create_final_filename()
	# TODO automate proper filenames
	#text_page_pdf(info, "oo_summary_4.pdf", "oo_summary_1.pdf") # no error w/ non-overwrite orig file change
	text_page_pdf(info, final_filename,tmp_filename) ## needed actually
	# testing stuff, view in console
	for k in info:
		print k, info[k]

	# return individual download nums
	#info_obj.indiv_dl_nums()

# def save_pdf():
# 	return None

if __name__ == '__main__':
	main()

