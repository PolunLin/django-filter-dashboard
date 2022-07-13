import django_filters
from decimal import Decimal

from django.db.models import Q
from django.forms import TextInput
import django_filters

from shopee.models import AdData
# from . import MetaData
class AdDataFitler(django_filters.FilterSet):
    # meta_data = models.ForeignKey(MetaData, null=True, blank=True, on_delete=models.CASCADE, )
    # keyword = django_filters.CharFilter(lookup_expr='icontains')
    # status = django_filters.CharFilter(lookup_expr='icontains')
    # mode = django_filters.CharFilter(lookup_expr='icontains')
    # search_request = models.CharField(u'搜尋请求', null=True, max_length=225)
    # view = models.IntegerField(u'瀏覽數', null=True, blank=True)
    # click = models.IntegerField(u'點擊數', null=True, blank=True)
    # click_rate = models.FloatField(u'點擊率',null=True, blank=True, default=None)
    # transfer = models.IntegerField(u'轉換', null=True, blank=True)
    # dtransfer = models.IntegerField(u'直接轉換', null=True, blank=True)
    # transfer_rate = models.FloatField(u'轉換率',null=True, blank=True, default=None)
    # dtransfer_rate = models.FloatField(u'直接轉換率',null=True, blank=True, default=None)
    # cost_transfer = models.FloatField(u'每一筆轉換的成本',null=True, blank=True, default=None)
    # cost_dtransfer = models.FloatField(u'每一筆轉換的成本',null=True, blank=True, default=None)
    # sold_number = models.IntegerField(u'銷售數', null=True, blank=True)
    # dsold_number = models.IntegerField(u'直接銷售數', null=True, blank=True)
    # sold_cost = models.IntegerField(u'銷售金額', null=True, blank=True)
    # sold_dcost = models.IntegerField(u'直接銷售金額', null=True, blank=True)
    # cost = models.FloatField(u'花費',null=True, blank=True, default=None)
    # avg_rank = models.FloatField(u'平均排名',null=True, blank=True, default=None)
    # invent_rate = models.FloatField(u'投資產出比',null=True, blank=True, default=None)
    # dinvent_rate = models.FloatField(u'直接投資產出比',null=True, blank=True, default=None)
    # cost_revenue_rate = models.FloatField(u'成本收入比率',null=True, blank=True, default=None)
    # dcost_revenue_rate = models.FloatField(u'直接成本收入比率',null=True, blank=True, default=None)
        query = django_filters.CharFilter(
            method="universal_search",
            label="",
            widget=TextInput(attrs={"placeholder": "Search..."}),
        )

        class Meta:
            model = AdData
            fields = ["query"]

        def universal_search(self, queryset, name, value):
            if value.replace(".", "", 1).isdigit():
                value = Decimal(value)
                return AdData.objects.filter(Q(keyword=value) | Q(status=value))

            return AdData.objects.filter(
                Q(keyword__icontains=value) | Q(status__icontains=value)
            )
    # class Meta:
    #     verbose_name = u'商品資訊'
    #     verbose_name_plural = u'商品資訊'
        
        # ordering = ['order']

    # def __str__(self):
    #     return u"%s" % (self.title)
