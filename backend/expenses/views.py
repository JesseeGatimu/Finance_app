from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Expense
from .serializers import ExpenseSerializer
from django.shortcuts import get_object_or_404
from django.db.models import Sum

class ExpenseListAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        expenses=Expense.objects.filter(user=request.user)
        serializer=ExpenseSerializer(expenses,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        serializer=ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                'message':'Created Successfully',
                'data':serializer.data
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class ExpenseDetailAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pk):
        expense=get_object_or_404(Expense,pk=pk,user=request.user)
        serializer=ExpenseSerializer(expense)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,pk):
        expense=get_object_or_404(Expense,pk=pk,user=request.user)
        serializer=ExpenseSerializer(expense,data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        expense=get_object_or_404(Expense,pk=pk,user=request.user)
        expense.delete()
        return Response({'message':'deleted successfully'},status=status.HTTP_200_OK)
    
class ExpenseTotalAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        total=Expense.objects.filter(user=request.user).aggregate(total=Sum('amount'))
        return Response({'total_expense':total['total'] or 0})
    
class CategorySummaryAPI(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        data=(Expense.objects.filter(user=request.user).values('category').annotate(total=Sum('amount')))
        return Response(list(data))
    
