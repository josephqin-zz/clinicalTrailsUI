from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
import django.contrib.auth.views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.trial_list, name='trial_list'),
    url(r'search/$', views.search,name="search"),
    url(r'trialpage/$',views.trialpage,name="trialpage"),
    # Map the 'django.contrib.auth.views.login' view to the /login/ URL.
    # The additional parameters to the view are passed via the 3rd argument which is
    # a dictionary of various parameters like the name of the template to be
    # used by the view.
    url(r'^login/$', auth_views.login,
        {
            "template_name" : "trialmatch/login.html",
        },
        name="login"),
          
    # Map the 'django.contrib.auth.views.logout' view to the /logout/ URL.
    # Pass additional parameters to the view like the page to show after logout
    # via a dictionary used as the 3rd argument.
    url(r'^logout/$', auth_views.logout,
        {
            "next_page" : reverse_lazy('login')
        }, name="logout"),
]
