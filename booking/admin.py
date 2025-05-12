from django.contrib import admin
from .models import Property, Booking, ExpenseCategory, Expense

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'daily_rate')
    search_fields = ('name', 'address')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('property', 'guest_name', 'start_date', 'end_date', 'total_amount', 'is_confirmed')
    list_filter = ('property', 'is_confirmed', 'start_date')
    search_fields = ('guest_name', 'guest_phone')
    date_hierarchy = 'start_date'

@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('property', 'category', 'date', 'amount', 'description')
    list_filter = ('property', 'category', 'date')
    date_hierarchy = 'date'
