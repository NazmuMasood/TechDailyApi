from django.urls import path
from . import views

urlpatterns = [
    path('', views.owners, name='owners'),
    path('view/<str:pk>/', views.ownerDetails, name='owner-details'),
    path('create/', views.ownerCreate, name='owner-create'),
    path('update/<str:pk>/', views.ownerUpdate, name='owner-update'),
    path('delete/<str:pk>/', views.ownerDelete, name='owner-delete'),

    path('createAll/', views.ownerCreateAll, name='owner-create-all'),
    path('deleteAll/', views.ownerDeleteAll, name='owner-delete-all'),
]
