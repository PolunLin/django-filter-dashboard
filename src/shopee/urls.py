from . import views
from django.urls import path ,include
from django.conf import settings
from django.conf.urls.static import static

app_name = "shopee"

urlpatterns = [
    path("", views.uploadFile, name = "uploadFile"),
    # path('export_users_csv/', views.export_users_csv,name="export_users_csv"),  
    path('Import_csv/', views.Import_csv,name="Import_csv"),  
    path('list/', views.product_list, name="product-list"),
    path('original/', views.AdDataTableView.as_view(), name='ad_data'),
    path('htmx/', views.AdDataHTMxTableView.as_view(), name='ad_data_htmx'),
]

if settings.DEBUG: 
    urlpatterns += static(
        settings.MEDIA_URL, 
        document_root = settings.MEDIA_ROOT
    )