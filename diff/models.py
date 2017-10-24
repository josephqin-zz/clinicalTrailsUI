

# Create your models here.
from django.db import models



class Diff_case(models.Model):
	before = models.TextField()
	after = models.TextField()
	caseName = models.CharField(max_length=200,default="diff tool case")

	def __str__(self):
		return self.caseName

