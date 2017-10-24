from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Query)
admin.site.register(Answer)
admin.site.register(Section)

admin.site.register(GeneSynom)
admin.site.register(DiseaseSynom)
admin.site.register(Scenario)
admin.site.register(Index)
admin.site.register(Trial)