"""techdailyapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view

@api_view(['GET'])
def apiOverview(request):
    # return JsonResponse("API BASE POINT", safe=False)
    api_urls = {
        'All Contents': '/contents',
        'Content Details': '/contents/view/<str:pk>',
        'Content Create': '/contents/create',
        'Content Update': '/contents/update/<str:pk>',
        'Content Delete': '/contents/delete/<str:pk>',
        'Content Create Multiple': '/contents/createAll',
        'Content Delete All':  '/contents/deleteAll',
        '-------':'-------------------------',
        'All Owners': '/owners',
        'Owner Details': '/owners/view/<str:pk>',
        'Owner Create': '/owners/create',
        'Owner Update': '/owners/update/<str:pk>',
        'Owner Delete': '/owners/delete/<str:pk>',
        'Owner Create Multiple': '/owners/createAll',
        'Owner Delete All':  '/owners/deleteAll',
        '--------':'-------------------------',
        'Content SearchByKey - `id`, `owner_id`, `title`': 'contents/search/<str:key>/<str:value>/',
        'Content SearchByOwner&Limit': 'contents/searchByOwner&Limit/<str:owner_id>/<int:limit>/',
    }
    return Response(api_urls)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', apiOverview, name='api-overview'),
    path('owners/', include('owners.urls')),
    path('contents/', include('contents.urls')),
]
