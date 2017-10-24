from django.db import models


def createChoice(lists):
	foo = ()
	for str in lists:
		foo = foo + ((str, str),)
	return ((None, 'SELECT'),) + foo

class Section (models.Model):
	section = models.CharField (max_length=20)

	def __str__(self):
		return self.section

from datetime import datetime
class Index(models.Model):
	index_name = models.CharField (max_length=100)
	description = models.CharField (max_length=100,blank=True,null=True)
	update_date = models.DateTimeField(default=datetime.now)

	def __str__(self):
		return self.index_name

class Query (models.Model):
	Gender_list = ['Male', 'Female', 'All']
	Stage_list = ['Stage I', 'Stage II', 'Stage III', 'Stage IV', 'Stage X', 'Stage IA', 'Stage IIA', 'Stage IIIA',
	              'Stage IVA', 'Stage IB', 'Stage IIB', 'Stage IIIB', 'Stage IVB', 'Stage IC', 'Stage IIC',
	              'Stage IIIC', 'Stage IVC']
	Grade_list = ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade I', 'Grade II', 'Grade III', 'Grade IV']
	disease = models.CharField (max_length=100, null=True,default=None)
	age = models.CharField (max_length=3, blank=True, null=True)
	gender = models.CharField (max_length=6, choices=createChoice (Gender_list), blank=True, null=True)
	gene = models.CharField (max_length=100, blank=True, null=True,default=None)
	aas = models.CharField (max_length=100, blank=True, null=True,default=None)
	stage = models.CharField (max_length=10, choices=createChoice (Stage_list), blank=True, null=True)
	grade = models.CharField (max_length=10, choices=createChoice (Grade_list), blank=True, null=True)
	address = models.CharField (max_length=100, blank=True, null=True,default=None)
	include_keywords = models.CharField (max_length=100, blank=True, null=True,default=None)
	exclude_keywords = models.CharField (max_length=100, blank=True, null=True,default=None)

	def __str__(self):
		rs = []
		for f in self._meta.fields :
			value = getattr(self,f.name)
			if value and (value is not None) and f.name!='id' :
				rs.append(f.name+":"+str(value))
		return "    ".join(rs)


class Scenario (models.Model):

	index = models.ForeignKey(Index)
	ontology = models.BooleanField(default=False)
	withoutAAS = models.BooleanField(default=False)

	def __str__(self):
		if self.ontology:
			return self.index.index_name+" with Disease Ontology"
		elif self.withoutAAS:
			return self.index.index_name + " include non-AAS results"
		else:
			return self.index.index_name


class Trial (models.Model):
	nct = models.CharField (max_length=20)
	query = models.ForeignKey (Query)
	scenario = models.ForeignKey(Scenario)
	disease = models.CharField (max_length=800, blank=True, null=True, default=None)
	gene = models.CharField (max_length=100, blank=True, null=True, default=None)
	aas = models.CharField (max_length=100, blank=True, null=True, default=None)

	def __str__(self):
		return str(self.id)+" "+str(self.nct)


class Answer (models.Model):
	Eligibility_list = ((True, 'YES'), (False, 'NO'))
	Character_list = ['disease', 'age', 'gender', 'stage', 'grade', 'gene', 'mutation']
	trial = models.ForeignKey (Trial)
	eligibility = models.BooleanField (choices=Eligibility_list)
	section = models.ManyToManyField (Section)
	sentence = models.TextField (blank=True, null=True)
	comment = models.TextField (blank=True, null=True)
	author = models.CharField (max_length=20, blank=True, null=True)
	timer = models.IntegerField (blank=True, null=True, default=None)

	def __str__(self):
		return str(self.trial.id)+" "+self.trial.nct

class GeneSynom (models.Model):
	gene = models.CharField (max_length=150)
	synonyms = models.CharField (max_length=150, blank=True, null=True)

	def __str__(self):
		return self.synonyms

class DiseaseSynom (models.Model):
	disease = models.CharField (max_length=150)
	synonyms = models.CharField (max_length=150, blank=True, null=True)

	def __str__(self):
		return self.synonyms
