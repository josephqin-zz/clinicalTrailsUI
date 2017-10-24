from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(words)
admin.site.register(cases)
admin.site.register(potential_gene)
admin.site.register(gene_in_CT)
admin.site.register(cases_validate)
admin.site.register(GeneSyn)
