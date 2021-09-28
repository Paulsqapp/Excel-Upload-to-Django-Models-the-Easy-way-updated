from django.urls import path
from django.views.generic.base import TemplateView
from . import views

app_name = 'core'

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/index.html'),
         name='home'),
    path('createstaff/', views.CreateStaff.as_view(), name='createstaff'),
    path('updatestaff/<int:pk>/', views.UpdateStaff.as_view(), name='updatestaff'),
    path('deletestaff/<int:pk>/', views.DeleteStaff.as_view(), name='deleteStaff'),
    path('sales/', views.ViewSales.as_view(), name='viewsales'),
    path('salesupload/', views.upload_sales, name='salesupload'),
    path('<int:year>/<str:month>/<int:day>/',
         views.ArchiveDaySales.as_view(), name='archivedDaySales'),
    path('today/',
         views.TodaySales.as_view(), name='todaySales'),
]
# DeleteStaff
# TodaySales
