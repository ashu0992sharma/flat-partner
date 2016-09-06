from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^flats-search/?', views.SearchApi.as_view()),
    url(r'^flats/$', views.FlatShow.as_view()),
    url(r'^search/', include('haystack.urls')),
    url(r'^save-flats-data/$', views.SaveFlatData.as_view()),
    url(r'^extra-data/$', views.ExtraData.as_view()),
    url(r'^check-availability/$', views.CheckAvailability.as_view()),
    url(r'^post-likes/$', views.SavePostLikes.as_view()),
    url(r'^get-gender/$', views.GetGender.as_view()),
    url(r'^get-flats-data/$', views.GetFlatData.as_view()),
    url(r'^comments-data/$', views.CommentsData.as_view()),
    url(r'^likes-data/$', views.LikesData.as_view()),
    url(r'^user/(?P<id>[\w-]+)/$', views.UserData.as_view()),

]
