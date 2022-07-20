from . import views
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static

app_name = "shopee"

urlpatterns = [
    path("", views.uploadFile, name = "uploadFile"),
    # path('export_users_csv/', views.export_users_csv,name="export_users_csv"),  
    path('Import_csv/', views.Import_csv,name="Import_csv"),  
    path('ad_data/', views.AdDataView.as_view(),name="ad_data"),  
    path('meta_data/', views.MetaDataView.as_view(),name="meta_data"),  
    path('cal_data/', views.CalDataView.as_view(),name="cal_data"),  
    path('get_data/', views.get_data,name="get_data"),  
    path('get_meta_data/', views.get_meta_data,name="get_meta_data"),  
    path('get_cal_data/', views.get_cal_data,name="get_cal_data"),  
   
]


if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )