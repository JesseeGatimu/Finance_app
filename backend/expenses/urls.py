from django.urls import path
from .views import ExpenseListAPI,ExpenseDetailAPI,ExpenseTotalAPI,CategorySummaryAPI

urlpatterns=[
    path('',ExpenseListAPI.as_view(),name='expenses'),
    path('<int:pk>/',ExpenseDetailAPI.as_view(),name='expense-detail'),
    path('total/',ExpenseTotalAPI.as_view(),name='expense-total'),
    path('category-summary/',CategorySummaryAPI.as_view(),name='category-summary'),
]