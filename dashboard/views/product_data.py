from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from dashboard.models import * 
from dashboard.data_connect import DATABASE as mongo
from bson.objectid import ObjectId
from django.conf import settings
import pandas as pd, uuid
from datetime import datetime

class productDataView(View):
    
    def __init__(self, **kwargs):
        self.template_name = {
            'main': "products_data.html",
        }
        self.MONGOOBJ = mongo()

    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        page_type = 'main'
        try:
            page_no = int(self.request.GET['page'])
        except:
            page_no = 1
        try:
            node_key = int(self.request.GET['node_key'])
        except:
            node_key = None

        try:
            search_text = self.request.GET['q']
            if search_text.strip() == "":
                search_text = None
        except:
            search_text = None

        if node_key is not None:
            find_dict = {'execution_node_id': str(node_key)}
        else:
            find_dict = {}

        if search_text is not None:
            find_dict.update({
                "$text": {"$search": search_text}
            })
        if page_no == 1:
            data_results = self.MONGOOBJ.product_col.find(find_dict).limit(settings.VIEW_PAGE_LIMIT)
        else:
            skip_count = page_no*settings.VIEW_PAGE_LIMIT
            data_results = self.MONGOOBJ.product_col.find(find_dict).skip(skip_count).limit(settings.VIEW_PAGE_LIMIT)


        context_dict = {
            "results": data_results,
            "data_count": self.MONGOOBJ.product_col.find(find_dict).count(),
            "nodes_list": self.MONGOOBJ.product_col.distinct('execution_node_id'),
            "current_page": page_no, 
            "previous_page": None if page_no==1 else page_no-1,
            "next_page": page_no+1 if int(data_results.count()) > 0 else None 
        }

        return render(request, self.template_name[page_type], context_dict)
        # return HttpResponseRedirect(reverse('dashboard:opportunities'))

class productDetailView(View):
    def __init__(self, **kwargs):
        self.template_name = {
            'main': "product_details.html",
        }
        self.MONGOOBJ = mongo()

    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, request, data_id,**kwargs):
        page_type = 'main'
        data_results = {}
        res = self.MONGOOBJ.product_col.find({'_id': ObjectId(data_id)})
        if int(res.count()) > 0:
            data_results = res[0]
            csv_data = data_results['csv']
            del data_results['csv']
            data_results.update({
                "csv": csv_data
            })
        context_dict = {
            "results": data_results,
        }

        return render(request, self.template_name[page_type], context_dict)

class productExportView(View):
    def __init__(self, **kwargs):
        self.MONGOOBJ = mongo()

    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)

    def get(self, request, filter_type, **kwargs):

        try:
            filter_value = self.request.GET['q']
        except:
            filter_value = ""


        filter_dict = {}
        excluded_fields = {"csv":0,"salesRanks":0,"execution_id":0}

        if int(filter_type) == 1:
            filter_dict.update({'execution_node_id': str(filter_value)})

        if int(filter_type) == 2:
            filter_dict.update({
                "$text": {"$search": str(filter_value)}
            })

        file_name = str(datetime.now()).replace(" ","_")+"__"+str(uuid.uuid4()).replace("-","")+".csv"
        df = pd.DataFrame(list(self.MONGOOBJ.product_col.find(filter_dict, excluded_fields)))
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}'.format(file_name)
        df.to_csv(path_or_buf=response, index=False)
        return response
