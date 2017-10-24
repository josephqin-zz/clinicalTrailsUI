from django.conf.urls import url
from . import views


urlpatterns = [
	url (r'^$', views.summaries, name='validation'),
	url (r'^(?P<scenarioID>[0-9]+)/$', views.querySummaries, name='query_validation'),
	url (r'^admin/$', views.admin, name='validation_admin'),
	url (r'^admin/(?P<queryID>[0-9]+)/$',views.queryLists,name='query_detail'),
	url (r'^trial/(?P<trialID>[0-9]+)/$', views.TrialValidation, name='trial_content'),
    # url(r'^(?P<indexID>[0-9]+)/$', Validation_views.index_details, name='queryDemo'),
    # url(r'^(?P<indexID>[0-9]+)/(?P<queryID>[0-9]+)/$', Validation_views.vl_questionary, name='questionary'),
    # url(r'^(?P<indexID>[0-9]+)/result/(?P<queryID>[0-9]+)/$', views.vl_demo, name='result'),
    # url(r'^(?P<indexID>[0-9]+)/(?P<queryID>[0-9]+)/(?P<nct>\w+)/$', views.vl_Aws, name='submitAws'),
    # url(r'(?P<indexID>[0-9]+)/result/$', views.v_result_index, name='demoResult'),
]