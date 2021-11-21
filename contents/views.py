from .serializers import ContentSerializer
from .models import Content
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response
from django.db.models import Q, F, Value, CharField, fields
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
    paginator = PageNumberPagination()
    paginator.page_size = 10 

    if key=='id':
        content = Content.objects.filter(id=value).first()
        serializer = ContentSerializer(content)
        if str(content)=='None':
            return Response([],status=200)
        return Response(serializer.data)
    
    elif key=='owner_id':
        # contents = Content.objects.filter(owner_id=value).order_by('-id')[:40]
        # serializer = ContentSerializer(contents, many=True)
        # return Response(serializer.data)
        contents = Content.objects.filter(owner_id=value).order_by('-id')
        result_page = paginator.paginate_queryset(contents, request)
        serializer = ContentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
     
    elif key=='title':
        contents = []
        # words = re.split(r"[^A-Za-z']+", value)
        words = value.split(" ")
        if(len(words)>0):
            query = Q()  # empty Q object
            for word in words:
                print("search keyword: '"+word+"'")
                # 'or' the queries together
                query |= Q(title__icontains=word) 
            # contents = Content.objects.filter(query).order_by('-id')[:40]
            contents = Content.objects.filter(query).order_by('-id')          

        result_page = paginator.paginate_queryset(contents, request)
        serializer = ContentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
        # serializer = ContentSerializer(contents, many=True)
        # return Response(serializer.data)
    
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


#------------------ content suggestion (builder) by key
@api_view(['GET'])
def contentSuggestionByKey(request, key, value):
    paginator = PageNumberPagination()
    paginator.page_size = 10 

    if key=='title':
        suggstnList = []
        # words = re.split(r"[^A-Za-z']+", value)
        words = value.split()
        if(len(words)>0):
            query = Q()  # empty Q object
            for word in words:
                print("search keyword: '"+word+"'")
                query |= Q(title__icontains=word) 
            titleList = Content.objects.values_list('title', flat=True).filter(query).order_by('-id')
            
            for title in titleList:
                print('full title: '+title)
                
                matchedKeyword = value
                for item in value.split():
                    if(title.lower().find(item.lower())!=-1):
                        matchedKeyword = item
                        break
                print(f"keyword: '{matchedKeyword}'")

                tokenized = re.split(r"([a-zA-Z]*(?i)"+matchedKeyword+"[a-zA-Z]*'?s?,?)",title)
                # for item in tokenized:
                #     print(f"'{item}'")
                matchedWord = tokenized[1]
                matchedWordEndIndex = title.index(matchedWord) + len(matchedWord)
                fullTrailing = title[matchedWordEndIndex:]
                print(f"full trailing: '{title[matchedWordEndIndex:]}'")
                if(len(fullTrailing.split()) > 2):
                    fullTrailingSplitted = fullTrailing.split()
                    # print(f"length of fullTrailingSplitted[]: {str(len(fullTrailingSplitted))}")
                    trailing = fullTrailingSplitted[0] +" "+ fullTrailingSplitted[1]
                    print(f"final trailing: '{trailing}'")
                    finalTitleSuggstn = matchedWord +" "+ trailing
                else:
                    finalTitleSuggstn = matchedWord +" "+ fullTrailing
                print(f"final title suggstn: '{finalTitleSuggstn}'\n")

                if finalTitleSuggstn not in suggstnList:
                    suggstnList.append(finalTitleSuggstn) 

        result_page = paginator.paginate_queryset(suggstnList, request)
        return paginator.get_paginated_response(result_page) 

    else:
        return Response(status=400)  