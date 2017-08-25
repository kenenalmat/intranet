from django.conf.urls import url
import views

urlpatterns = [
    url(r'^', views.get_schedule, name="get_schedule")
]