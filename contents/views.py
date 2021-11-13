from .serializers import ContentSerializer
from .models import Content
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response
from django.db.models import Q, F, Value, CharField
import re
from django.db import models
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

### ------------- 'content' end points
@api_view(['GET'])
def contents(request):
    # contents = Content.objects.order_by('-pub_date')[:40]

    # Page number/size wise pagination 
    contents = Content.objects.order_by('-pub_date')
    paginator = PageNumberPagination()
    paginator.page_size = 10 
    result_page = paginator.paginate_queryset(contents, request)
    serializer = ContentSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

    # Limit offset wise pagination
    # contents = Content.objects.order_by('pub_date')
    # paginator = LimitOffsetPagination() 
    # result_page = paginator.paginate_queryset(contents, request)
    # serializer = ContentSerializer(result_page, many=True)
    # return paginator.get_paginated_response(serializer.data)

    # serializer = ContentSerializer(contents, many=True)
    # return Response(serializer.data)

@api_view(['GET'])
def contentDetails(request, pk):
    content = Content.objects.filter(id=pk).first()
    if str(content)=='None':
        return Response([],status=200)
    serializer = ContentSerializer(content)
    return Response(serializer.data)

@api_view(['POST'])
def contentCreate(request):
    serializer = ContentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def contentUpdate(request, pk):
    content = Content.objects.get(id=pk)
    serializer = ContentSerializer(instance=content, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def contentDelete(request, pk):
    content = Content.objects.get(id=pk)
    content.delete()
    return Response(status=204)

@api_view(['POST'])
def contentCreateAll(request):
    serializer = ContentSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def contentDeleteAll(request):
    contents = Content.objects.all()
    contents.delete()
    return Response(status=204)

#------------------ content search by key
@api_view(['GET'])
def contentByKey(request, key, value):
    if key=='id':
        content = Content.objects.filter(id=value).first()
        serializer = ContentSerializer(content)
        if str(content)=='None':
            return Response([],status=200)
        return Response(serializer.data)
    
    elif key=='owner_id':
        contents = Content.objects.filter(owner_id=value).order_by('-id')[:40]
        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data)
    
    elif key=='title':
        words = re.split(r"[^A-Za-z']+", value)
        query = Q()  # empty Q object
        for word in words:
            print(word+'\n')
            # 'or' the queries together
            query |= Q(title__icontains=word) 
        contents = Content.objects.filter(query).order_by('-id')[:40]

        serializer = ContentSerializer(contents, many=True)
        return Response(serializer.data)
    
    else:
        return Response(status=400) 

@api_view(['GET'])
def contentByOwnerAndLimit(request, owner_id, limit):
    contents = Content.objects.filter(owner_id=owner_id).order_by('-id')[:limit]
    serializer = ContentSerializer(contents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def contentUrlByOwnerAndLimit(request, owner_id, limit):
    contentUrls = Content.objects.values('url').filter(owner_id=owner_id).order_by('-id')[:limit]
    print(contentUrls)
    # serializer = ContentSerializer(contents, many=True)
    return Response(contentUrls) 