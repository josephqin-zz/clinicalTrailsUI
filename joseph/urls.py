from django.conf.urls import url
from joseph import views
from pten import views as pviews

from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', pviews.Query_view_2, name='joseph_index' ),
    url(r'^misspelling/$', views.msp_demo, name='misspelled_case'),
    url(r'^misspelling/(?P<wordID>[0-9]+)/(?P<geneID>[0-9]+)/$', views.msp_cases, name='mis_cases'),
    url(r'^misspelling/(?P<wordID>[0-9]+)/(?P<geneID>[0-9]+)/(?P<caseID>[0-9]+)/$', views.msp_file, name='mis_file'),
    url(r'^wl/$',views.words_landscape,name='word_landscape'),

]