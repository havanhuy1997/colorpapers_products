from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from dashboard.models import * 
from dashboard.data_connect import DATABASE as mongo
from bson.objectid import ObjectId
from django.conf import settings

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
            del data_results['csv']
        context_dict = {
            "results": data_results,
        }

        return render(request, self.template_name[page_type], context_dict)
