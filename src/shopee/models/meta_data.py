from __future__ import unicode_literals

from django.db import models
# from django.utils.translation import ugettext_lazy as _
# from model_utils.models import TimeStampedModel
# from six import python_2_unicode_compatible


# 關鍵字	狀態	比對模式	搜尋请求	瀏覽數	點擊數	點擊率	轉換	直接轉換	轉換率	直接轉換率	每一筆轉換的成本	每一筆直接轉換的成本	
# #銷售數	直接銷售數	銷售金額	直接銷售金額	花費	平均排名	投資產出比	直接投資產出比	成本收入比率	直接成本收入比率
class MetaData(models.Model): # 件
    product = models.CharField(u'關鍵字', null=True, max_length=225)
    store_id = models.CharField(u'賣場ID', null=True, max_length=225)
    product_id = models.CharField(u'商品ID', null=True, max_length=225)
    date_1 = models.DateField(u'期間1')
    date_2 = models.DateField(u'期間2')
    status = models.CharField(u'狀態', null=True, max_length=225)         # 別名
    # report_time = models.DateField(u'報表匯出時間')         # 別名


    class Meta:
        verbose_name = u'詮釋資料'
        verbose_name_plural = u'詮釋資料'
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'store_id', 'product_id', 'date_1', 'date_2', 'status'], name='unique_migration_host_combination'
            )
        ]
    def __str__(self):
        return f"{self.id} {self.date_1}-{self.date_2} {self.product} {self.store_id} {self.product_id} "