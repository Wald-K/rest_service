from django.urls import path

from . import views

urlpatterns = [
    path('ip-tags/<str:ip_address>/', views.show_ip_tags, name='json_tags'),
    path('ip-tags-report/<str:ip_address>/', views.show_ip_tags_report,
         name='report_tags'),
]
