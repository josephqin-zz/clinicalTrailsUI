from django.test import TestCase
import joseph.diff as diff
# Create your tests here.

list1="Contact: Helena Yu, MD    646-888-4274"
list2="Contact: Helena Yo,u MD 646-888-4274"


def diff_identify(before,after):
	diff_obj = diff.diff_match_patch ()


	di = diff_obj.diff_wordsToChars(before,after)
	diffs = diff_obj.diff_main(di[0],di[1],False)
	diff_obj.diff_charsToLines(diffs,di[2])
	return(diffs)

print(diff_identify(list1,list2))