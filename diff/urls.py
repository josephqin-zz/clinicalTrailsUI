from django.conf.urls import url
from diff import views


urlpatterns = [
    url(r'^case/$',views.case_view,name='diff_compare'),
    url(r'^$',views.diff_view,name='diff_case'),
	url(r'^save/$',views.case_save,name='diff_case_save'),

]