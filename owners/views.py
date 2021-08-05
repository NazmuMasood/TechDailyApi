from django.shortcuts import render
from .serializers import OwnerSerializer
from .models import Owner
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import serializers, status
from rest_framework.response import Response
from django.db.models import Q, F, Value, CharField
import re
from django.db import models

###------------------ 'owner' end points
@api_view(['GET'])
def owners(request):
    owners = Owner.objects.all()
    serializer = OwnerSerializer(owners, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def ownerDetails(request, pk):
    owner = Owner.objects.filter(id=pk).first()
    if str(owner)=='None':
        return Response([],status=200)
    serializer = OwnerSerializer(owner)
    return Response(serializer.data)

@api_view(['POST'])
def ownerCreate(request):
    serializer = OwnerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def ownerUpdate(request, pk):
    owner = Owner.objects.get(id=pk)
    serializer = OwnerSerializer(instance=owner, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def ownerDelete(request, pk):
    owner = Owner.objects.get(id=pk)
    owner.delete()
    return Response(status=204)

@api_view(['POST'])
def ownerCreateAll(request):
    serializer = OwnerSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def ownerDeleteAll(request):
    owners = Owner.objects.all()
    owners.delete()
    return Response(status=204)