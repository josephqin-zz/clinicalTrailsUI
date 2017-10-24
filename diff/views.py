from django.shortcuts import render

# Create your views here.
from django.shortcuts import *
from diff.forms import  diffForm_txt

import diff.diff as diff

def find_diff(before,after):
	bf = [x for x in before.split()]
	af = [x for x in after.split()]
	rs=[]
	if bf.__len__()==af.__len__():
		for i in range(0,bf.__len__()):
			if bf[i]==af[i]:
				rs.append((0,bf[i]))
			else:
				rs.append((1,af[i]))
	else:
		diff_obj = diff.diff_match_patch ()
		rs = diff_obj.diff_main (before, after)
		print(rs)
	return rs

def context_highlight(context):
	html=[]
	word=[]
	for (flag,data) in context:
		if flag==0:
			word.append(data)
		elif flag==1:
			word.append("<span class=\"before_hl\">%s</span>" % data)
		else:
			word.append ("<span class=\"after_hl\">%s</span>" % data)
	html.append("".join(word))
	return "".join(html)

def decode_fix(s):
	for encoding in "utf-8-sig", "utf-16":
		try:
			return s.decode (encoding)
		except UnicodeDecodeError:
			continue
	return s.decode ("latin-1")

from diff.models import Diff_case

def case_save(request):
	case = Diff_case(caseName=request.POST['caseName'],before=request.POST['before'],after=request.POST['after'])
	case.save()
	msg="Saved!!"
	return HttpResponse(msg)


def diff_view(request):
	before_txt = ""
	after_txt = ""
	if request.method == 'POST':
		diffform = diffForm_txt (request.POST)
		caseform = diffCaseForm (request.POST)
		before=[]
		after=[]
		diff_b= []
		diff_a = []
		if 'casebtn' in request.POST:
			c = Diff_case.objects.get (id=request.POST['case'])
			diffform = diffForm_txt ()
			before_raw = c.before
			after_raw = c.after
		else:
			caseform = diffCaseForm ()
			before_raw = request.POST['before']
			after_raw = request.POST['after']

		if diffform.is_valid () or caseform.is_valid():

			for g in before_raw.splitlines ():
				try:
					before.append(g)
				except:
					print ('no result')

			for g in after_raw.splitlines ():
				try:
					after.append (g)
				except:
					print ('no result')

			if(before.__len__()==after.__len__()):
				for i in range(0,before.__len__()):
					diff_obj = diff.diff_match_patch ()

					di = diff_obj.diff_wordsToChars ( after[i].replace('\t',' '),before[i].replace('\t',' '))
					diffs = diff_obj.diff_main (di[0], di[1], False)
					diff_obj.diff_charsToLines (diffs, di[2])
					html = str(i+1)+" "+context_highlight (diffs)
					diff_b.append (before[i])
					diff_a.append (html)
				before_txt = "</br>".join(diff_b)
				after_txt = "</br>".join(diff_a)
			else:
				before_txt = "Wrong Input!"
				after_txt = "Check the files Please!"

	else:
		diffform = diffForm_txt ()
		caseform = diffCaseForm()
	return render (request, 'difftool.html', {'caseform':caseform,'diffform': diffform, 'before':before_txt,'after':after_txt})

from diff.forms import diffCaseForm
def case_view(request):
	before_txt = ""
	after_txt = ""

	if request.method == 'POST':
		form = diffCaseForm (request.POST)
		c = Diff_case.objects.get(id=request.POST['case'])
		before = []
		after = []
		diff_b = []
		diff_a = []
		if form.is_valid ():

			for g in c.before.splitlines ():
				try:
					before.append (g)
				except:
					print ('no result')

			for g in c.after.splitlines ():
				try:
					after.append (g)
				except:
					print ('no result')

		if (before.__len__ () == after.__len__ ()):
			for i in range (0, before.__len__ ()):
				diff_obj = diff.diff_match_patch ()

				di = diff_obj.diff_wordsToChars (after[i].replace ('\t', ' '), before[i].replace ('\t', ' '))
				diffs = diff_obj.diff_main (di[0], di[1], False)
				diff_obj.diff_charsToLines (diffs, di[2])
				html = str (i + 1) + " " + context_highlight (diffs)
				diff_b.append (before[i])
				diff_a.append (html)
			before_txt = "</br>".join (diff_b)
			after_txt = "</br>".join (diff_a)
		else:
			before_txt = "Wrong Input!"
			after_txt = "Check the files Please!"

	else:
		form = diffCaseForm ()
	return render (request, 'case_list.html', {'form': form, 'before': before_txt, 'after': after_txt})