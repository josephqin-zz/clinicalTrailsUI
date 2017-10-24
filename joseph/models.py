from django.db import models

# Create your models here.
from django.db import models


def createChoice(lists):
	foo = ()
	for str in lists:
		foo = foo + ((str, str),)
	return ((None, 'SELECT'),) + foo


class words (models.Model):
	word = models.CharField (max_length=200, db_index=True)
	frequency = models.IntegerField (default=0)

	def __str__(self):
		return self.word


class cases (models.Model):
	word = models.ForeignKey (words)
	file_num = models.CharField (max_length=100)
	original_word = models.CharField (max_length=200,blank=True)
	def __str__(self):
		rs = str(self.word) + " in " + str(self.file_num)
		return rs


class cases_validate (models.Model):
	E_list = ((True, 'YES'), (False, 'NO'))
	case = models.ForeignKey (cases)
	is_Misspelled = models.BooleanField (choices=E_list,default=False)
	gene = models.CharField (max_length=200)


class gene_in_CT (models.Model):
	gene = models.CharField (max_length=200, db_index=True)
	frequency = models.IntegerField ()

	def __str__(self):
		return self.gene


class potential_gene (models.Model):
	word = models.ForeignKey (words)
	gene = models.ForeignKey (gene_in_CT)
	score = models.FloatField ()

	def __str__(self):
		rs = str(self.word) + '=>' + str(self.gene)
		return rs

class GeneSyn (models.Model):
	gene = models.CharField (max_length=150)
	synonyms = models.CharField (max_length=150, blank=True, null=True)

	def __str__(self):
		return self.synonyms

