"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from accounts import views as accounts_views
from boards import views
from database import views as db_views

urlpatterns = [
    url(r'^$', views.BoardListView.as_view(), name='home'),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^boards/(?P<pk>\d+)/$', views.board_topics, name='board_topics'),
    url(r'^boards/(?P<pk>\d+)/new/$', views.new_topic, name='new_topic'),
    url(r'^boards/(?P<pk>\d+)/$', views.TopicListView.as_view(), name='board_topics'),

    url(r'^admin/', admin.site.urls, name='admin'),

    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    url(r'^reset/complete/$', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    url(r'^settings/password/$', auth_views.PasswordChangeView.as_view(template_name='password_change.html'), name='password_change'),
    url(r'^settings/password/done/$', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),


    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.topic_posts, name='topic_posts'),
    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/reply/$', views.reply_topic, name='reply_topic'),

    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/posts/(?P<post_pk>\d+)/edit/$',
        views.PostUpdateView.as_view(), name='edit_post'),

    url(r'^boards/(?P<pk>\d+)/topics/(?P<topic_pk>\d+)/$', views.PostListView.as_view(), name='topic_posts'),
    url(r'^settings/account/$', accounts_views.UserUpdateView.as_view(), name='my_account'),


    url(r'^files/$', views.file_list, name='file_list'),
    url(r'^files/upload/$', views.upload_file, name='upload_file'),
    url(r'^files/(?P<pk>\d+)/', views.delete_file, name='delete_file'),

    #url(r'^database/$', db_views.db_home, name='db_home'),
    url(r'^database/$', db_views.DatabasePageView.as_view(), name='database_home'),
    url(r'database/cities/', db_views.CitySearchResultsView.as_view(), name='city_search_results'),
    url(r'database/vehicles/', db_views.VehicleSearchResultsView.as_view(), name='vehicle_search_results'),
    url(r'database/powerplant/', db_views.PowerPlantSearchResultsView.as_view(), name='powerplant_search_results'),

    url(r'^c02graph/', db_views.c02_graph, name='c02graph'),
    url(r'^vehiclepm25/', db_views.vehicle_pm25_graph, name='vehiclepm25'),

    url(r'^pieconcentration/(?P<pk>\d+)/', db_views.pollution_concentration_pie, name='pieconcentration'),
    url(r'^pm25graphline/(?P<pk>\d+)/', db_views.pm25_graph_line, name='pm25graphline'),
    url(r'^c0graphline/(?P<pk>\d+)/', db_views.c0_graph_line, name='c0graphline'),
    url(r'^c02graphline/(?P<pk>\d+)/', db_views.c02_graph_line, name='c02graphline'),
    url(r'^hcgraphline/(?P<pk>\d+)/', db_views.hc_graph_line, name='hcgraphline'),
    url(r'^nographline/(?P<pk>\d+)/', db_views.no_graph_line, name='nographline'),

    url(r'^pm25windgraph/(?P<pk>\d+)/', db_views.pm25_wind_graph, name='pm25windgraph'),
    url(r'^c0windgraph/(?P<pk>\d+)/', db_views.c0_wind_graph, name='c0windgraph'),
    url(r'^c02windgraph/(?P<pk>\d+)/', db_views.c02_wind_graph, name='c02windgraph'),
    url(r'^hcwindgraph/(?P<pk>\d+)/', db_views.hc_wind_graph, name='hcwindgraph'),
    url(r'^nowindgraph/(?P<pk>\d+)/', db_views.no_wind_graph, name='nowindgraph'),
    url(r'^allconcentration/(?P<pk>\d+)/', db_views.all_pollution, name='allconcentration'),

    url(r'^bargraph/(?P<pk>\d+)/', db_views.bar_graph, name='bargraph'),

    #url(r'^dbupload/$', db_views.db_upload, name='db_upload')

    #WIP
#    url(r'^boards/(?P<board_pk>\d+)/topics/(?P<pk>\d+)', views.delete_topic, name='delete_topic'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
