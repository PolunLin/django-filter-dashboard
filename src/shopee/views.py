from ast import Add, keyword
from importlib.metadata import metadata

from cv2 import ROTATE_90_CLOCKWISE
from . import models
from django.shortcuts import render

def uploadFile(request):
    if request.method == "POST":
        # Fetching the form data
        fileTitle = request.POST["fileTitle"]
        uploadedFile = request.FILES["uploadedFile"]

        # Saving the information in the database
        document = models.Document(
            title = fileTitle,
            uploadedFile = uploadedFile
        )
        document.save()

    documents = models.Document.objects.all()

    return render(request, "shopee/upload_file.html", context = {
        "files": documents
    })


from .models import AdData,MetaData,CalData
import datetime as dt
import pandas as pd
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import csv
import numpy as np
def Import_csv(request):              
    try:
        if request.method == 'POST' and request.FILES['myfile']:
          
            myfile = request.FILES['myfile']        
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            excel_file = uploaded_file_url
            # print(excel_file) 
            table_start = 0
            meta_data = {}
            with open(
                "."+excel_file, "r", encoding="utf-8-sig",
            ) as f:
                reader = csv.reader(f, delimiter=",")
                for i, line in enumerate(reader):
                    if i == 0:
                        pass
                    elif len(line) > 0 and line[0] == "順序":
                        table_start = i
                        break
                    elif len(line) >= 2 and len(line[0]) > 0:
                        line[0] = line[0].replace(" ", "")
                        line[0] = line[0].replace("：", "")
                        if line[0] == "期間":
                            line[1] = line[1].split(" - ")
                            meta_data["期間_1"] = [line[1][0].rstrip()]
                            meta_data["期間_2"] = [line[1][1].rstrip()]
                        else:
                            meta_data[line[0]] = [line[1].rstrip()]
            # print(meta_data)
            data = pd.read_csv(
                "."+excel_file,
                skiprows=table_start,
                skipinitialspace=True,
            )
            # print(data)
            ## data process
            data["平均排名"] = np.round(data["平均排名"], 3)
            data["平均排名"] = np.round(data["平均排名"], 3)
            if "順序" in data:
                data = data.drop(columns=["順序"])
            meta_data = pd.DataFrame.from_dict(meta_data)
            if not meta_data.empty:
                data["賣場ID"] = meta_data["賣場ID"][0]
                data["商品ID"] = meta_data["商品ID"][0]
                data["商品"] = meta_data["商品"][0]
                data["期間_1"] = meta_data["期間_1"][0]
                data["期間_2"] = meta_data["期間_2"][0]
            percentage_column = ['點擊率','轉換率','直接轉換率','成本收入比率','直接成本收入比率']
            data['點擊率'] = data['點擊率'].str.replace('%','')
            data['轉換率'] = data['轉換率'].str.replace('%','')
            data['直接轉換率'] = data['直接轉換率'].str.replace('%','')
            data['成本收入比率'] = data['成本收入比率'].str.replace('%','')
            data['直接成本收入比率'] = data['直接成本收入比率'].str.replace('%','')
                
            # print(123)
            # data.groupby().agg(
            # total_search = pd.NamedAgg(column="瀏覽數",aggfunc=sum),
            # total_click = pd.NamedAgg(column="點擊數",aggfunc=sum),
            # total_buy = pd.NamedAgg(column="訂單數",aggfunc=sum),
            # total_dbuy = pd.NamedAgg(column="直接訂單數",aggfunc=sum),
            # total_money = pd.NamedAgg(column="銷售金額",aggfunc=sum),
            # total_dmoney = pd.NamedAgg(column="直接銷售金額",aggfunc=sum),)
            ## create cal_data :
            # only key ,shop,product_id,product_name,peroid1,peroid2
            column_list = [
                "賣場ID",
                "商品ID",
                "期間_1",
            ]
            product_column_list = []
            import itertools
            # for i, column in enumerate(column_list):
            #     tem_list = []
            #     tem_list.append("關鍵字")
            #     tem_list.append(column)
            for L in range(0, len(column_list)+1):
                for subset in itertools.combinations(column_list, L):
                    subset = list(subset)
                    if "期間_1" in subset:
                        subset.append("期間_2")

                    subset.append("關鍵字")
                    product_column_list.append(subset)
                # for i1, column1 in enumerate(column_list):
                #     if i > i1:
                #         pass
                #     elif i == i1:

                #         if "期間_1" in tem_list:
                #             tem_list.append("期間_2")
                #         product_column_list.append(tem_list)
                #     else:
                #         tem_list.append(column1)

                #         if "期間_1" in tem_list:
                #             tem_list.append("期間_2")
                #         product_column_list.append(tem_list)
            
            
            col_dict ={}
            for i,col in enumerate(product_column_list):
                col_dict[i] =col
            # print("col_dict",col_dict)
            #         df =pd.DataFrame(columns=['total_search', 'total_transfer', 'total_click', 'total_dtransfer',
            #    'total_cost', 'total_money', 'total_dmoney'])
            # for i,x in enumerate(product_column_list):
            total_tmp_df = pd.DataFrame()
            
            for key,value in col_dict.items(): 
                tmp_df = pd.DataFrame()
                tmp_df = data.groupby(value, as_index=False).agg( #
                    total_search=pd.NamedAgg(column="瀏覽數", aggfunc=sum),
                    total_transfer=pd.NamedAgg(column="轉換", aggfunc=sum),
                    total_click=pd.NamedAgg(column="點擊數", aggfunc=sum),
                    total_dtransfer=pd.NamedAgg(column="直接轉換", aggfunc=sum),
                    total_cost=pd.NamedAgg(column="花費", aggfunc=sum),
                    total_sell=pd.NamedAgg(column="銷售數", aggfunc=sum),
                    total_tsell=pd.NamedAgg(column="直接銷售數", aggfunc=sum),
                    average_rank=pd.NamedAgg(column="平均排名", aggfunc=np.mean),
                    total_money=pd.NamedAgg(column="銷售金額", aggfunc=sum),
                    total_tmoney=pd.NamedAgg(column="直接銷售金額", aggfunc=sum),
                )
                
                def cal(num1, num2):
                    if num2 == 0:
                        return 0
                    else:
                        return num1 / num2

                tmp_df["轉換率"] = tmp_df.apply(
                    lambda x: cal(x["total_search"], x["total_transfer"]), axis=1
                )
                tmp_df["直接轉換率"] = tmp_df.apply(
                    lambda x: cal(x["total_search"], x["total_dtransfer"]), axis=1
                )
                tmp_df["成本收入比率"] = tmp_df.apply(
                    lambda x: cal(x["total_cost"], x["total_money"]), axis=1
                )
                tmp_df["直接成本收入比率"] = tmp_df.apply(
                    lambda x: cal(x["total_cost"], x["total_tmoney"]), axis=1
                )
            

                tmp_df["點擊率"] = tmp_df.apply(
                    lambda x: cal(x["total_click"], x["total_search"]), axis=1
                )
                tmp_df['cal_id'] =key
                colums = [
                    # "關鍵字",
                    # "賣場ID",
                    # "商品ID",
                    "瀏覽數",
                    "轉換",
                    "點擊數",
                    "直接轉換",
                    "花費",
                    "銷售數",
                    "直接銷售數",
                    "平均排名",
                    "銷售金額",
                    "直接銷售金額",
                    "轉換率",
                    "直接轉換率",
                    "成本收入比率",
                    "直接成本收入比率",
                    
                    "點擊率",
                    "cal_id",
                ]
                tmp_df.columns =value +colums
                tmp_df['預算'] =100
                
                tmp_df = tmp_df.reset_index(drop=True)
                for i, row in tmp_df.iterrows():
                    if row['銷售數']==0:
                        if row['點擊率']>0.05:
                            if row['點擊數']<10:
                                tmp_df.at[i,'建議出價'] = f"降低預算10% = {tmp_df.iloc[i]['預算']*0.9}"
                            else:
                                n = (row['點擊數']-5 )/5
                                tmp_df.at[i,'建議出價'] = f"提高預算{10+10*n}% {tmp_df.iloc[i]['預算']*(10+10*n)*0.01}"
                        if row['點擊率']<0.05:
                            if row['點擊數']<10:
                                tmp_df.at[i,'建議出價'] = "維持"
                            else:
                                n = (row['點擊數']-5 )/5
                                tmp_df.at[i,'建議出價'] = f"關閉"
                    else:
                        tmp_df.at[i,'建議出價']=row['銷售數']/row['點擊率']*tmp_df.iloc[i]['預算']   *row['點擊率']*5
                    tmp_df.at[i,'點擊率'] =np.round(row['點擊率']*100).astype(str)
                tmp_df['點擊率'] = tmp_df['點擊率'].astype(str) + "%"
                # print(1,tmp_df.columns)
                
                # print(tmp_df['商品ID'])
                # tmp_df['商品ID'] = tmp_df['商品ID'].astype(str) 
                # tmp_df['賣場ID'] = tmp_df['賣場ID'].astype(str) 
                if total_tmp_df.empty:
                    # tmp_df['點擊率'] = tmp_df['點擊率'] +"%"
                    total_tmp_df = tmp_df
                else:
                   total_tmp_df= pd.concat([total_tmp_df, tmp_df])

        data_records = data.to_dict('records')
        total_tmp_df_records = total_tmp_df.to_dict('records')
        meta_data_records = meta_data.to_dict('records')[0]
        
        print(meta_data_records)
        # print(len(data_records))
        model_instances = MetaData(
            store_id=meta_data_records['賣場ID'],
            product_id=meta_data_records['商品ID'],
            product=meta_data_records['商品'],
            status=meta_data_records['狀態'],
            date_1=meta_data_records['期間_1'].replace("/","-"),
            date_2=meta_data_records['期間_2'].replace("/","-"),

        ) 
        model_instances.save()
        print(model_instances)
        # meta_data_obj,created = MetaData.objects.get_or_create(model_instances)
        # print(meta_data_obj)
        ad_data_model_instances = [AdData(
            meta_data=model_instances,
            keyword=record['關鍵字'],
            status=record['狀態'],
            mode=record['比對模式'],
            search_request=record['搜尋请求'],
            view=record['瀏覽數'],
            click=record['點擊數'],
            click_rate=record['點擊率'],
            transfer=record['轉換'],
            dtransfer=record['直接轉換'],
            transfer_rate=record['轉換率'],
            dtransfer_rate=record['直接轉換率'],
            cost_transfer=record['每一筆轉換的成本'],
            cost_dtransfer=record['每一筆直接轉換的成本'],
            sold_number=record['銷售數'],
            dsold_number=record['直接銷售數'],
            sold_cost=record['銷售金額'],
            sold_dcost=record['直接銷售金額'],
            cost=record['花費'],
            avg_rank=record['平均排名'],
            invent_rate=record['投資產出比'],
            dinvent_rate=record['直接投資產出比'],
            cost_revenue_rate=record['成本收入比率'],
            dcost_revenue_rate=record['直接成本收入比率'],

        ) for record in data_records]
        cal_data_model_instances = [CalData(
            meta_data=model_instances,
            total_search=record['瀏覽數'],
            total_transfer=record['轉換'],
            total_click=record['點擊數'],
            total_dtransfer=record['直接轉換'],
            total_cost=record['花費'],
            total_sell=record['銷售數'],
            total_tsell=record['直接銷售數'],
            average_rank=record['平均排名'],
            total_money=record['直接銷售金額'],
            total_tmoney=record['直接銷售金額'],

        ) for record in total_tmp_df_records]
        CalData.objects.bulk_create(cal_data_model_instances)
        AdData.objects.bulk_create(ad_data_model_instances)
 
        # print(data, meta_data, total_tmp_df)
            # empexceldata = pd.read_csv("."+excel_file,encoding='utf-8')
            # print(1,empexceldata)
            # print(type(empexceldata))
            # dbframe = empexceldata
            #  for i, line in enumerate(reader):
            #         if i == 0:
            #             pass
            #         elif len(line) > 0 and line[0] == "順序":
            #             table_start = i
            #             break
            #         elif len(line) >= 2 and len(line[0]) > 0:
            #             line[0] = line[0].replace(" ", "")
            #             line[0] = line[0].replace("：", "")
            #             if line[0] == "期間":
            #                 line[1] = line[1].split(" - ")
            #                 meta_data["期間_1"] = [line[1][0].rstrip()]
            #                 meta_data["期間_2"] = [line[1][1].rstrip()]
            #             else:
            #                 meta_data[line[0]] = [line[1].rstrip()]
            # for dbframe in dbframe.itertuples():
            #      print(dbframe)
                # fromdate_time_obj = dt.datetime.strptime(dbframe.DOB, '%d-%m-%Y')
                # obj = tbl_Employee.objects.create(Empcode=dbframe.Empcode,firstName=dbframe.firstName, middleName=dbframe.middleName,
                #                                 lastName=dbframe.lastName, email=dbframe.email, phoneNo=dbframe.phoneNo, address=dbframe.address, 
                #                                 exprience=dbframe.exprience, gender=dbframe.gender, DOB=fromdate_time_obj,
                #                                 qualification=dbframe.qualification)
                # print(type(obj))
                # obj.save()
 
        return render(request, 'shopee/importexcel.html', {
            'shopee/uploaded_file_url': uploaded_file_url
        })    
    except Exception as identifier:            
        print("error",identifier)
     
    return render(request, 'shopee/importexcel.html',{})
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import AdDataForm, MetaDataForm,CalDataForm
class AdDataView(View):
    form_class = AdDataForm
    # initial = {'key': 'value'}
    template_name = 'shopee/ad_data.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form = AdDataForm
        data = AdData.objects.all()
        return render(request, self.template_name, {'form': form,'data':data})
class MetaDataView(View):
    form_class = MetaDataForm
    # initial = {'key': 'value'}
    template_name = 'shopee/meta_data.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form = MetaDataForm
        data = MetaData.objects.all()
        return render(request, self.template_name, {'form': form,'data':data})
class CalDataView(View):
    form_class = CalDataForm
    # initial = {'key': 'value'}
    template_name = 'shopee/cal_data.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        form = CalDataForm
        data = CalData.objects.all()
        return render(request, self.template_name, {'form': form,'data':data})
import json
from django.core.paginator import  Paginator
from django.forms.models import model_to_dict
# @csrf_exempt
def get_data(request):
    sort=request.POST.get('sort','keyword')
    order=request.POST.get('order','asc')
    page=request.POST.get('page',1)
    rows=request.POST.get('rows',15)
    
    keyword=request.POST.get('keyword','')
    status=request.POST.get('status','')
    mode=request.POST.get('mode','')
    search_request=request.POST.get('search_request','')
    product=request.POST.get('product','')
    store_id=request.POST.get('store_id','')
    product_id=request.POST.get('product_id','')
    date_1=request.POST.get('date_1','')
    date_2=request.POST.get('date_2','')
    
    # print(keyword,mode,status,search_request)
    data_list = []
    data = AdData.objects.all()
    if keyword:
        data = data.filter(keyword=keyword)
    if status:
        data = data.filter(status=status)
    if mode:
        data = data.filter(mode=mode)
    if search_request:
        data = data.filter(search_request=search_request)

    if product:
        data = data.filter(meta_data__product=product)
    if store_id:
        data = data.filter(meta_data__store_id=store_id)
    if product_id:
        data = data.filter(meta_data__product_id=product_id)

    if date_1:
        date_1 = datetime.strptime(date_1,"%m/%d/%Y")
        data = data.filter(meta_data__date_1__gte=date_1)
    if date_2:
        date_2 = datetime.strptime(date_2,"%m/%d/%Y")
        data = data.filter(meta_data__date_2__lte=date_2)
    if order!='asc':
        sort='-'+sort
    data = data.order_by(sort)
    paginator=Paginator(data,rows)
    pages=paginator.get_page(page)
    for li in pages:
        data_list.append(model_to_dict(li))
        # data_list.append({
        #     "keyword":li.keyword,
        #     "status":li.status,
        #     "mode":li.mode,
        #     "search_request":li.search_request,
        #     "view":li.view,
        #     "click":li.click,
        #     "click_rate":li.click_rate,
        #     "transfer":li.transfer,
        #     "dtransfer":li.dtransfer,
        #     "transfer_rate":li.transfer_rate,
        #     "dtransfer_rate":li.dtransfer_rate,
        #     "cost_transfer":li.cost_transfer,
        #     "cost_dtransfer":li.cost_dtransfer,
        #     "sold_number":li.sold_number,
        #     "dsold_number":li.dsold_number,
        #     "sold_cost":li.sold_cost,
        #     "sold_dcost":li.sold_dcost,
        #     "cost":li.cost,
        #     "avg_rank":li.avg_rank,
        #     "invent_rate":li.invent_rate,
        #     "dinvent_rate":li.dinvent_rate,
        #     "cost_revenue_rate":li.cost_revenue_rate,
        #     "dcost_revenue_rate":li.dcost_revenue_rate}
        # )
    json_list = json.dumps(len(data_list))
    
    # print(data_list)
    # print(paginator.count)
    json_data_list = {'rows':data_list,'total':paginator.count}
    return HttpResponse(json.dumps(json_data_list))
from datetime import datetime 
def get_meta_data(request):
    sort=request.POST.get('sort','product')
    order=request.POST.get('order','asc')
    page=request.POST.get('page',1)
    rows=request.POST.get('rows',15)
 
    product=request.POST.get('product','')
    store_id=request.POST.get('store_id','')
    product_id=request.POST.get('t','')
    date_1=request.POST.get('date_1','')
    date_2=request.POST.get('date_2','')
    status=request.POST.get('status','')

    # print(product,store_id,product_id,date_1,date_2,status)
    data_list = []
    data = MetaData.objects.all()
    if product:
        data = data.filter(product=product)
    if store_id:
        data = data.filter(store_id=store_id)
    if product_id:
        data = data.filter(product_id=product_id)
    if status:
        data = data.filter(status=status)
    if date_1:
        date_1 = datetime.strptime(date_1,"%m/%d/%Y")
        data = data.filter(date_1__gte=date_1)
    if date_2:
        date_2 = datetime.strptime(date_2,"%m/%d/%Y")
        data = data.filter(date_2__lte=date_2)
    # if search_request:
    #     data = data.filter(search_request=search_request)
    # if meta_data:
    #     meta_data = meta_data.split(" ")[0]
    #     data = data.filter(meta_data=meta_data)
    if order!='asc':
        sort='-'+sort
    data = data.order_by(sort)
    paginator=Paginator(data,rows)
    pages=paginator.get_page(page)
    for li in pages:
        data_list.append(model_to_dict(li))
    json_list = json.dumps(len(data_list))
    
    # print(data_list)
    # print(paginator.count)
    json_data_list = {'rows':data_list,'total':paginator.count}
    return HttpResponse(json.dumps(json_data_list, indent=4, sort_keys=True, default=str))

def get_cal_data(request):
    sort=request.POST.get('sort','total_search')
    order=request.POST.get('order','asc')
    page=request.POST.get('page',1)
    rows=request.POST.get('rows',15)
 
    product=request.POST.get('product','')
    store_id=request.POST.get('store_id','')
    product_id=request.POST.get('t','')
    date_1=request.POST.get('date_1','')
    date_2=request.POST.get('date_2','')
    status=request.POST.get('status','')
    avg_rank=request.POST.getlist('avg_rank[]','')
    # print(product,store_id,avg_rank,date_1,date_2,status)
    data_list = []
    data = CalData.objects.all()
    if product:
        data = data.filter(meta_data__product=product)
    if store_id:
        data = data.filter(meta_data__store_id=store_id)
    if product_id:
        data = data.filter(meta_data__product_id=product_id)

    if date_1:
        date_1 = datetime.strptime(date_1,"%m/%d/%Y")
        data = data.filter(meta_data__date_1__gte=date_1)
    if date_2:
        date_2 = datetime.strptime(date_2,"%m/%d/%Y")
        data = data.filter(meta_data__date_2__lte=date_2)
    if avg_rank:
        data = data.filter(average_rank__gte=avg_rank[0],average_rank__lte=avg_rank[1])
        # data = data.filter(meta_data__product_id=product_id)
    # print(product,store_id,product_id,date_1,date_2,status)


    if order!='asc':
        sort='-'+sort
    data = data.order_by(sort)
    paginator=Paginator(data,rows)
    pages=paginator.get_page(page)
    for li in pages:
        data_list.append(model_to_dict(li))
    json_list = json.dumps(len(data_list))
    
    # print(data_list)
    # print(paginator.count)
    json_data_list = {'rows':data_list,'total':paginator.count}
    return HttpResponse(json.dumps(json_data_list, indent=4, sort_keys=True, default=str))