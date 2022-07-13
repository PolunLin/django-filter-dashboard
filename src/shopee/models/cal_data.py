

from __future__ import unicode_literals

from django.db import models
from .meta_data import MetaData

class CalData(models.Model): # 件
    meta_data = models.ForeignKey(MetaData, null=True, blank=True, on_delete=models.CASCADE, )
    total_search = models.FloatField(u'瀏覽數',null=True, blank=True, default=None)
    total_transfer = models.FloatField(u'轉換',null=True, blank=True, default=None)
    total_click = models.FloatField(u'點擊數',null=True, blank=True, default=None)
    total_dtransfer = models.FloatField(u'直接轉換',null=True, blank=True, default=None)
    total_cost = models.FloatField(u'花費',null=True, blank=True, default=None)
    total_sell = models.FloatField(u'銷售數',null=True, blank=True, default=None)
    total_tsell = models.FloatField(u'直接銷售數',null=True, blank=True, default=None)
    average_rank = models.FloatField(u'平均排名',null=True, blank=True, default=None)
    total_money = models.FloatField(u'直接銷售金額',null=True, blank=True, default=None)
    total_tmoney = models.FloatField(u'直接銷售金額',null=True, blank=True, default=None)

    class Meta:
        verbose_name = u'統計資料'
        verbose_name_plural = u'統計資料'


    # def __str__(self):
    #     return u"%s" % (self.title)