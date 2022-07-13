import django_tables2 as tables

from shopee.models import AdData




class AdDataTable(tables.Table):
    class Meta:
        model = AdData
        template_name = "django_tables2/bootstrap4.html"

class AdDataHTMxTable(tables.Table):
    class Meta:
        model = AdData
        template_name = "shopee/bootstrap_htmx_full.html"