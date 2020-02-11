# -*- coding: utf-8 -*-
# @Time    : 2020-02-02 13:20
# @Author  : jinhang
# @File    : test_search.py
# @Description: Use for search test

from SearchRecipe.search import *
from SearchRecipe.models import TestModel
import time
from sys import stdout
from sys import getsizeof
from django.conf import settings
from array import array
index_path = os.path.join(settings.STATICFILES_DIRS[0], "index.txt")

stdout.write("Start load index\n")
# print(getsizeof(['20','30','40']))
# print(getsizeof([20,30,40]))
# print(getsizeof(array('I',[20,30,40])))
# exit(0)
t_start = time.time()
# index_path = "./index.txt"
index, doc_all_ids_set = load_index(index_path)
# print(getsizeof(index))
print(index['0'])
# print(index)
t_end = time.time()
stdout.write("Load finished in %.02f seconds\n" % (t_end - t_start))
query = "mac"
results_list = ranked_search(index, query, doc_all_ids_set)
exit(0)
for doc_score in results_list:
    object_id = doc_score[0]
    # score = doc_score[1]
    result = TestModel.objects.filter(docId=object_id)
    # print(result)
    print(result[0]['title'])



