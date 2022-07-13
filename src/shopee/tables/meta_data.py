import django_tables2 as tables

from shopee.models import MetaData

class MetaDataTable(tables.Table):
    class Meta:
        model = MetaData
        template_name = "django_tables2/bootstrap4.html"

class MetaDataHTMxTable(tables.Table):
    class Meta:
        model = MetaData
        template_name = "bootstrap_htmx_full.html"
