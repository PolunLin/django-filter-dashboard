from django import forms
from matplotlib import widgets
from .models import AdData,MetaData
from dal import autocomplete


class AdDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AdDataForm, self).__init__(*args, **kwargs)
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

class MetaDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MetaDataForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'easyui-combobox'
            visible.field.widget.attrs['name'] = visible.field.label
            visible.field.widget.attrs['style'] = 'width:140ch'
        for field,value in self.fields.items():
            self.fields[field].widget.attrs['id']=field
            self.fields[field].widget.attrs['name']=field
        self.fields['date_1'].widget.attrs['class'] = 'easyui-datebox'
        self.fields['date_2'].widget.attrs['class'] = 'easyui-datebox'
    product = forms.ModelChoiceField(label='關鍵字',queryset= MetaData.objects.values_list('product',flat=True).distinct())
    store_id = forms.ModelChoiceField(label='賣場ID',queryset= MetaData.objects.values_list('store_id',flat=True).distinct())
    product_id = forms.ModelChoiceField(label='商品ID',queryset= MetaData.objects.values_list('product_id',flat=True).distinct())
    date_1 = forms.DateField(label='期間1')
    date_2 = forms.DateField(label='期間2')
    status = forms.ModelChoiceField(label='狀態',queryset= MetaData.objects.values_list('status',flat=True).distinct())

    class Meta:
        model = MetaData
        fields =["product","store_id","product_id","date_1","date_2","status"]      