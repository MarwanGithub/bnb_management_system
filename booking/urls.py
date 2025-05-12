from django.urls import path
from . import views

urlpatterns = [
    # Dashboard and Property
    path('', views.dashboard, name='dashboard'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('property/add/', views.PropertyCreateView.as_view(), name='property_create'),
    path('property/<int:pk>/update/', views.PropertyUpdateView.as_view(), name='property_update'),
    path('property/<int:pk>/delete/', views.PropertyDeleteView.as_view(), name='property_delete'),
    
    # Booking
    path('property/<int:property_id>/bookings/', views.BookingListView.as_view(), name='booking_list'),
    path('property/<int:property_id>/bookings/add/', views.BookingCreateView.as_view(), name='booking_create'),
    path('booking/<int:pk>/update/', views.BookingUpdateView.as_view(), name='booking_update'),
    path('booking/<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
    
    # Booking Expenses
    path('booking/<int:booking_id>/expenses/add/', views.BookingExpenseCreateView.as_view(), name='booking_expense_create'),
    
    # Expense
    path('property/<int:property_id>/expenses/', views.ExpenseListView.as_view(), name='expense_list'),
    path('property/<int:property_id>/expenses/add/', views.ExpenseCreateView.as_view(), name='expense_create'),
    path('expense/<int:pk>/update/', views.ExpenseUpdateView.as_view(), name='expense_update'),
    path('expense/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense_delete'),
    
    # Calendar
    path('property/<int:property_id>/calendar/', views.calendar_view, name='calendar'),
    
    # API
    path('api/property/<int:property_id>/monthly-stats/', views.api_get_monthly_stats, name='api_monthly_stats'),
    path('api/next-available-date/<int:property_id>/', views.next_available_date, name='next_available_date'),
] 