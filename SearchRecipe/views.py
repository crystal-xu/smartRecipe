from bson import json_util
from django.core.paginator import Paginator
from django.shortcuts import HttpResponse, render, redirect

# Create your views here.
from SearchRecipe.models import TestModel
from SearchRecipe.search import do_search
import os
from SearchRecipe.search import load_index
from django.conf import settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cw3site.settings')
index_path = os.path.join(settings.STATICFILES_DIRS[0], "index.txt")


print("load index")
index, doc_all_ids_set = load_index(index_path)

querynew = ''


def add(request):
    TestModel.objects.create(
        title="news2",
        text="xxxxxxx",
        link="http://www.baidu.com"
    )
    return HttpResponse("hello mongodb")


def query(request):
    result = TestModel.objects.all()
    return HttpResponse(json_util.dumps(result._collection_obj.find(result._query)),
                        content_type="application/json")


def search(request):
    global querynew
    if querynew != '':
        q = querynew
    else:
        q = request.GET.get('q')
    querynew = ''
    if q:
        # question_list = TestModel.objects.filter(title=q)
        print("start search")
        question_list = do_search(index, q, doc_all_ids_set)
        #print(question_list)
    else:
        question_list = TestModel.objects.all()
        #print(question_list)
        question_list = question_list[:100]

    paginator = Paginator(question_list, 5)
    context = {
        'page': paginator.page(request.GET.get('page', 1)),
        'paginator': paginator,
        'query': q
    }
    return render(request, 'index.html', context)


def load_welcome(request):

    q = request.GET.get('q')
    global querynew
    if (q != None) and (q != ''):
        querynew = q
        return redirect('search')
    else:
        return render(request, 'main_page.html')
    # return render(request, 'main_page.html')
