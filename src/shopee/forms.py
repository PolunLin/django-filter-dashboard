from django import forms
from matplotlib import widgets
from .models import AdData,MetaData
from dal import autocomplete


class AdForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'easyui-combobox'
            visible.field.widget.attrs['name'] = visible.field.label
            visible.field.widget.attrs['style'] = 'width:150ch'
        for field,value in self.fields.items():
            self.fields[field].widget.attrs['id']=field
            self.fields[field].widget.attrs['name']=field
    keyword = forms.ModelChoiceField(label="關鍵字",queryset= AdData.objects.values_list('keyword',flat=True).distinct())
    mode = forms.ModelChoiceField(label="比對模式",queryset=AdData.objects.values_list('mode',flat=True).distinct())
    status = forms.ModelChoiceField(label='狀態',queryset=AdData.objects.values_list('status',flat=True).distinct())
    search_request = forms.ModelChoiceField(label='搜尋请求',queryset=AdData.objects.values_list('search_request',flat=True).distinct())
    meta_data = forms.ModelChoiceField(label='詮釋資料',queryset=MetaData.objects.all())
    class Meta:
        model = AdData
        fields =["keyword","status","mode","search_request","meta_data"]
       