from bson import json_util
from django.core.paginator import Paginator
from django.shortcuts import HttpResponse, render

# Create your views here.
from SearchRecipe.models import TestModel


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
    q = request.GET.get('q')
    if q:
        question_list = TestModel.objects.filter(title=q)
    else:
        question_list = TestModel.objects.all()
        question_list = question_list[:100]
    paginator = Paginator(question_list, 5)
    context = {
        'page': paginator.page(request.GET.get('page', 1)),
        'paginator': paginator,
        'query': query
    }
    return render(request, 'index.html', context)