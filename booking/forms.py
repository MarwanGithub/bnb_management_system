from django import forms
from .models import Booking, Expense, Property

class DateInput(forms.DateInput):
    input_type = 'date'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['property', 'start_date', 'end_date', 'guest_name', 'guest_phone', 'is_confirmed']
        widgets = {
            'start_date': DateInput(),
            'end_date': DateInput(),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        property_obj = cleaned_data.get('property')
        
        if start_date and end_date and property_obj:
            if start_date >= end_date:
                raise forms.ValidationError("End date must be after start date.")
            
            # Check if there are overlapping bookings
            overlapping_bookings = Booking.objects.filter(
                property=property_obj,
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            
            if self.instance:
                overlapping_bookings = overlapping_bookings.exclude(id=self.instance.id)
            
            if overlapping_bookings.exists():
                raise forms.ValidationError("There is already a booking for this period.")
        
        return cleaned_data

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['property', 'date', 'amount', 'description']
        widgets = {
            'date': DateInput(),
        }

class BookingExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['booking', 'date', 'amount', 'description']
        widgets = {
            'date': DateInput(),
        }
    
    def __init__(self, *args, **kwargs):
        booking_id = kwargs.pop('booking_id', None)
        super().__init__(*args, **kwargs)
        
        if booking_id:
            booking = Booking.objects.get(id=booking_id)
            self.fields['booking'].initial = booking
            self.fields['booking'].widget = forms.HiddenInput()
            # Set the property from the booking
            if not self.instance.pk:  # Only for new expenses
                self.instance.property = booking.property

class PropertyForm(forms.ModelForm):
    address = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'cols': 40,
            'style': 'resize: vertical;'
        }),
        required=False,
        help_text="(Optional) Enter the property address"
    )
    
    class Meta:
        model = Property
        fields = ['name', 'daily_rate', 'address'] 