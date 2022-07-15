from django import forms
from matplotlib import widgets
from .models import AdData,MetaData
from dal import autocomplete

 
class AdForm(forms.ModelForm):
    class Meta:
        model = AdData
        fields =["keyword","status","mode","search_request","view","click","click_rate","transfer","dtransfer","transfer_rate","dtransfer_rate","cost_transfer","cost_dtransfer","sold_number","dsold_number","sold_cost","sold_dcost","cost","avg_rank","invent_rate","dinvent_rate","cost_revenue_rate","dcost_revenue_rate"]
        widgets = {
            'keyword':autocomplete.ListSelect2(url='shopee:addata-autocomplete',forward=['keyword'],attrs={'class':"form-control"}),
            'mode':autocomplete.ListSelect2(url='shopee:addata-autocomplete',forward=['mode'],attrs={'class':"form-control"}),
        }
