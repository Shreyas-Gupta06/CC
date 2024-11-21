from django.urls import path
from . import views

urlpatterns =[
    
    path('', views.filter_by_query),
    path('<str:uid>/', views.id_details),

]