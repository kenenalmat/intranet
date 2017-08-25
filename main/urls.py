from django.conf.urls import url
import views

urlpatterns = [
    url(r'^get', views.get_schedule, name="get_schedule"),
    url(r'^check', views.check, name="check")
]