from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.db.models import Sum
from django.http import JsonResponse
from datetime import datetime, date, timedelta
import calendar
import json

from .models import Property, Booking, Expense, ExpenseCategory
from .forms import BookingForm, ExpenseForm, PropertyForm, BookingExpenseForm

def dashboard(request):
    properties = Property.objects.all()
    
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    
    context = {
        'properties': properties,
        'current_month': current_month,
        'current_year': current_year,
    }
    return render(request, 'booking/dashboard.html', context)

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    today = timezone.now().date()
    current_month = today.month
    current_year = today.year
    
    # Get monthly statistics
    monthly_earnings = property_obj.get_monthly_earnings(current_year, current_month)
    monthly_expenses = property_obj.get_monthly_expenses(current_year, current_month)
    monthly_profit = property_obj.get_monthly_profit(current_year, current_month)
    
    # Get current bookings
    current_bookings = property_obj.bookings.filter(
        end_date__gte=today
    ).order_by('start_date')
    
    # Get recent expenses
    recent_expenses = property_obj.expenses.order_by('-date')[:5]
    
    context = {
        'property': property_obj,
        'current_month': calendar.month_name[current_month],
        'current_year': current_year,
        'monthly_earnings': monthly_earnings,
        'monthly_expenses': monthly_expenses,
        'monthly_profit': monthly_profit,
        'current_bookings': current_bookings,
        'recent_expenses': recent_expenses,
    }
    
    return render(request, 'booking/property_detail.html', context)

class PropertyCreateView(generic.CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'booking/property_form.html'
    success_url = reverse_lazy('dashboard')

class PropertyUpdateView(generic.UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'booking/property_form.html'
    
    def get_success_url(self):
        return reverse_lazy('property_detail', kwargs={'pk': self.object.pk})

class PropertyDeleteView(generic.DeleteView):
    model = Property
    template_name = 'booking/property_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

class BookingListView(generic.ListView):
    model = Booking
    template_name = 'booking/booking_list.html'
    context_object_name = 'bookings'
    
    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        if property_id:
            return Booking.objects.filter(property_id=property_id).order_by('-start_date')
        return Booking.objects.all().order_by('-start_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property_id = self.kwargs.get('property_id')
        if property_id:
            context['property'] = get_object_or_404(Property, id=property_id)
        return context

class BookingCreateView(generic.CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        property_id = self.kwargs.get('property_id')
        if property_id:
            initial['property'] = get_object_or_404(Property, id=property_id)
        return initial
    
    def get_success_url(self):
        return reverse_lazy('booking_list', kwargs={'property_id': self.object.property.id})
    
    def form_valid(self, form):
        messages.success(self.request, 'Booking created successfully!')
        return super().form_valid(form)

class BookingUpdateView(generic.UpdateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/booking_form.html'
    
    def get_success_url(self):
        return reverse_lazy('booking_list', kwargs={'property_id': self.object.property.id})
    
    def form_valid(self, form):
        messages.success(self.request, 'Booking updated successfully!')
        return super().form_valid(form)

class BookingDeleteView(generic.DeleteView):
    model = Booking
    template_name = 'booking/booking_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('booking_list', kwargs={'property_id': self.object.property.id})

class ExpenseListView(generic.ListView):
    model = Expense
    template_name = 'booking/expense_list.html'
    context_object_name = 'expenses'
    
    def get_queryset(self):
        property_id = self.kwargs.get('property_id')
        if property_id:
            return Expense.objects.filter(property_id=property_id).order_by('-date')
        return Expense.objects.all().order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property_id = self.kwargs.get('property_id')
        if property_id:
            context['property'] = get_object_or_404(Property, id=property_id)
        return context

class ExpenseCreateView(generic.CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'booking/expense_form.html'
    
    def get_initial(self):
        initial = super().get_initial()
        property_id = self.kwargs.get('property_id')
        if property_id:
            initial['property'] = get_object_or_404(Property, id=property_id)
        return initial
    
    def get_success_url(self):
        return reverse_lazy('expense_list', kwargs={'property_id': self.object.property.id})
    
    def form_valid(self, form):
        messages.success(self.request, 'Expense created successfully!')
        return super().form_valid(form)

class ExpenseUpdateView(generic.UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'booking/expense_form.html'
    
    def get_success_url(self):
        return reverse_lazy('expense_list', kwargs={'property_id': self.object.property.id})
    
    def form_valid(self, form):
        messages.success(self.request, 'Expense updated successfully!')
        return super().form_valid(form)

class ExpenseDeleteView(generic.DeleteView):
    model = Expense
    template_name = 'booking/expense_confirm_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('expense_list', kwargs={'property_id': self.object.property.id})

def calendar_view(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    bookings = property_obj.bookings.all()
    
    booking_list = []
    for booking in bookings:
        booking_list.append({
            'id': booking.id,
            'title': f"{booking.guest_name}",
            'start': booking.start_date.strftime('%Y-%m-%d'),
            'end': booking.end_date.strftime('%Y-%m-%d'),
            'url': reverse('booking_update', kwargs={'pk': booking.id}),
            'className': 'bg-success' if booking.is_confirmed else 'bg-warning'
        })
    
    context = {
        'property': property_obj,
        'bookings_json': json.dumps(booking_list)
    }
    
    return render(request, 'booking/calendar.html', context)

def api_get_monthly_stats(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    
    earnings = property_obj.get_monthly_earnings(year, month)
    expenses = property_obj.get_monthly_expenses(year, month)
    profit = earnings - expenses
    
    # Get bookings for the month
    month_bookings = property_obj.bookings.filter(
        start_date__year=year,
        start_date__month=month
    ).count()
    
    # Get total days booked
    days_booked = 0
    bookings = property_obj.bookings.filter(
        start_date__year=year, 
        start_date__month=month
    ) | property_obj.bookings.filter(
        end_date__year=year, 
        end_date__month=month
    )
    
    for booking in bookings:
        days_booked += booking.days_count()
    
    # Get days in month
    _, days_in_month = calendar.monthrange(year, month)
    
    # Calculate occupancy rate
    occupancy_rate = (days_booked / days_in_month) * 100 if days_in_month > 0 else 0
    
    return JsonResponse({
        'earnings': float(earnings),
        'expenses': float(expenses),
        'profit': float(profit),
        'bookings_count': month_bookings,
        'days_booked': days_booked,
        'occupancy_rate': round(occupancy_rate, 2)
    })

class BookingExpenseCreateView(generic.CreateView):
    model = Expense
    form_class = BookingExpenseForm
    template_name = 'booking/booking_expense_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['booking_id'] = self.kwargs.get('booking_id')
        return kwargs
    
    def form_valid(self, form):
        booking = get_object_or_404(Booking, id=self.kwargs.get('booking_id'))
        form.instance.booking = booking
        form.instance.property = booking.property
        messages.success(self.request, 'Expense added to booking successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        booking = get_object_or_404(Booking, id=self.kwargs.get('booking_id'))
        context['booking'] = booking
        return context
    
    def get_success_url(self):
        return reverse_lazy('booking_update', kwargs={'pk': self.kwargs.get('booking_id')})

def next_available_date(request, property_id):
    """API endpoint to get the next available date for a property"""
    try:
        # Start from today
        current_date = date.today()
        
        # Get all future bookings for this property
        future_bookings = Booking.objects.filter(
            property_id=property_id,
            end_date__gte=current_date
        ).order_by('start_date')
        
        # If no future bookings, today is available
        if not future_bookings.exists():
            return JsonResponse({'next_available_date': current_date.isoformat()})
        
        # Check if today is available (not in any booking)
        today_is_booked = any(
            booking.start_date <= current_date <= booking.end_date
            for booking in future_bookings
        )
        
        if not today_is_booked:
            return JsonResponse({'next_available_date': current_date.isoformat()})
        
        # Iterate through bookings to find the first available gap
        last_end_date = None
        for booking in future_bookings:
            if last_end_date and booking.start_date > (last_end_date + timedelta(days=1)):
                # Found a gap, return day after last booking ended
                next_date = last_end_date + timedelta(days=1)
                return JsonResponse({'next_available_date': next_date.isoformat()})
            
            # Update last_end_date if current booking ends later
            if not last_end_date or booking.end_date > last_end_date:
                last_end_date = booking.end_date
        
        # If no gaps found, return day after the last booking ends
        next_date = last_end_date + timedelta(days=1)
        return JsonResponse({'next_available_date': next_date.isoformat()})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
