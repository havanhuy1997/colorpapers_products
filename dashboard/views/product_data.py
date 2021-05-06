from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from dashboard.models import * 
from dashboard.data_connect import DATABASE as mongo
from bson.objectid import ObjectId


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
        context_dict = {
            "results": self.MONGOOBJ.product_col.find({}),
            "data_count": self.MONGOOBJ.product_col.find({}).count(),
            "nodes_list": self.MONGOOBJ.product_col.distinct('execution_node_id')
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
