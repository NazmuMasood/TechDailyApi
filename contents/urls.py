from django.urls import path
from . import views

urlpatterns = [
    path('', views.contents, name='contents'),
    path('view/<str:pk>/', views.contentDetails, name='content-details'),
    path('create/', views.contentCreate, name='content-create'),
    path('update/<str:pk>/', views.contentUpdate, name='content-update'),
    path('delete/<str:pk>/', views.contentDelete, name='content-delete'),
    path('createAll/', views.contentCreateAll, name='content-create-all'),
    path('deleteAll/', views.contentDeleteAll, name='content-delete-all'),

    path('search/<str:key>/<str:value>/', views.contentByKey, name='content-by-key'),
    path('searchByOwner&Limit/<str:owner_id>/<int:limit>', views.contentByOwnerAndLimit, name='content-by-owner-and-limit'),
    path('searchUrlByOwner&Limit/<str:owner_id>/<int:limit>', views.contentUrlByOwnerAndLimit, name='content-url-by-owner-and-limit'),
]
    