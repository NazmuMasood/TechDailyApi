from django.urls import path
from . import views

urlpatterns = [
    path('', views.contents, name='contents'),
    path('view/<str:pk>/', views.contentDetails, name='content-details'),
    path('create/', views.contentCreate, name='content-create'),
    path('update/<str:pk>/', views.contentUpdate, name='content-update'),
    path('delete/<str:pk>/', views.contentDelete, name='content-delete'),

    path('search/<str:key>/<str:value>/', views.contentByKey, name='content-by-key'),
]
