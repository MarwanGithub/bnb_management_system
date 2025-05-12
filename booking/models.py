from django.db import models
from django.utils import timezone
from django.db.models import Sum

class Property(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name
    
    def get_monthly_earnings(self, year, month):
        bookings = self.bookings.filter(
            start_date__year=year,
            start_date__month=month
        )
        return bookings.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    def get_monthly_expenses(self, year, month):
        expenses = self.expenses.filter(
            date__year=year,
            date__month=month
        )
        return expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    def get_monthly_profit(self, year, month):
        return self.get_monthly_earnings(year, month) - self.get_monthly_expenses(year, month)

class Booking(models.Model):
    property = models.ForeignKey(Property, related_name='bookings', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    guest_name = models.CharField(max_length=100)
    guest_phone = models.CharField(max_length=20, help_text="Guest's contact phone number")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_confirmed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.guest_name} - {self.start_date} to {self.end_date}"
    
    def save(self, *args, **kwargs):
        if not self.total_amount:
            # Calculate total amount based on daily rate
            days = (self.end_date - self.start_date).days
            self.total_amount = self.property.daily_rate * days
        super().save(*args, **kwargs)
    
    def days_count(self):
        return (self.end_date - self.start_date).days
    
    def get_expenses_total(self):
        """Get the total of all expenses linked to this booking"""
        return self.booking_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Expense(models.Model):
    property = models.ForeignKey(Property, related_name='expenses', on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, related_name='booking_expenses', on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    
    def __str__(self):
        booking_info = f" ({self.booking.guest_name})" if self.booking else ""
        category_info = f"{self.category} - " if self.category else ""
        return f"{self.date} - {category_info}EGP {self.amount}{booking_info}"
