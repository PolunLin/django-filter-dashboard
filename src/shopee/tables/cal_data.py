import django_tables2 as tables

from shopee.models import CalData


class CalDataTable(tables.Table):
    class Meta:
        model = CalData
        template_name = "django_tables2/bootstrap4.html"

class CalDataHTMxTable(tables.Table):
    class Meta:
        model = CalData
        template_name = "bootstrap_htmx_full.html"