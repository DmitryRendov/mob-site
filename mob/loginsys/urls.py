from django.conf.urls import patterns, include, url

urlpatterns = patterns('loginsys.views',

    url(r'^login/', 'login', name='login'),
    url(r'^logout/', 'logout', name='logout'),
    url(r'^register/', 'register', name='register'),
    url(r'^reactivation/', 'reactivation', name='reactivation'),
    url(r'^profile/', 'profile', name='profile'),
    url(r'^confirm/(?P<activation_key>\w+)/', 'confirm', name='confirm'),
)
