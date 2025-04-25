from django.contrib import admin
from django.urls import path

import vaccine_app
from vaccine_app import views
from vaccine_app.views import about, index, admin_login, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', about, name='about'),
    path('', index, name='home'),  # Home page (admin dashboard)
    path('login/', admin_login, name='login'),
    path('contact/', vaccine_app.views.contact, name='contact'),
    path('logout/', logout_view, name='logout'),  # Updated the name to `logout_view`
    path('view_vaccination/', vaccine_app.views.vaccination, name='view_vaccination'),
    path('add_vaccination/', views.add_vaccination, name='add_vaccination'),
    path('delete_vaccination/<int:pid>/', views.delete_vaccination, name='delete_vaccination'),
    path('add_child/', views.add_child, name='add_child'),
    path('view_child/', views.view_child, name='view_child'),
    path('add_appointment/', views.add_appointment, name='add_appointment'),
    path('view_appointment/', views.view_appointment, name='view_appointment'),
    path('delete_child/<int:pid>/', views.delete_child, name='delete_child'),
    path('send_sms/', views.send_sms_view, name='send_sms'),
path('delete_appointment/<int:pid>/', views.delete_appointment, name='delete_appointment'),
]
