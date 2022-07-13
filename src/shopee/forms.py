from django import forms
 
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Row, Column, Field
 
from .models import AdData,MetaData
 
class EmployeeRegistration(forms.ModelForm):
    class Meta:
        model = AdData
        fields =["keyword","status","mode","search_request","view","click","click_rate","transfer","dtransfer","transfer_rate","dtransfer_rate","cost_transfer","cost_dtransfer","sold_number","dsold_number","sold_cost","sold_dcost","cost","avg_rank","invent_rate","dinvent_rate","cost_revenue_rate","dcost_revenue_rate"]