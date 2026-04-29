from django.urls import path
from .views import IncomeListAPI,IncomeDetailAPI,IncomeTotalAPI,IncomeSummaryAPI

urlpatterns=[
    path('',IncomeListAPI.as_view(),name="incomes"),
    path('<int:pk>/',IncomeDetailAPI.as_view(),name="income-detail"),
    path('total/',IncomeTotalAPI.as_view(),name="income-total"),
    path('category-summary/',IncomeSummaryAPI.as_view(),name="income-category-summary"),
]