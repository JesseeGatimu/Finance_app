from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import IncomeSerializer
from .models import Income
from django.shortcuts import get_object_or_404
from django.db.models import Sum

class IncomeListAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        incomes=Income.objects.filter(user=request.user)
        serializer=IncomeSerializer(incomes,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class IncomeDetailAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        income=get_object_or_404(Income,pk=pk,user=request.user)
        serializer=IncomeSerializer(income)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        income=get_object_or_404(Income,pk=pk,user=request.user)
        serializer=IncomeSerializer(income,data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        income=get_object_or_404(Income,pk=pk,user=request.user)
        income.delete()
        return Response({'message':'Deleted successfully'},status=status.HTTP_200_OK)
    
class IncomeTotalAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        total=Income.objects.filter(user=request.user).aggregate(total=Sum('amount'))
        return Response({
            'total_income':total['total'] or 0
        },status=status.HTTP_200_OK)
    
class IncomeSummaryAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        data=(Income.objects.filter(user=request.user).values('category').annotate(total=Sum('amount')))
        return Response(list(data))