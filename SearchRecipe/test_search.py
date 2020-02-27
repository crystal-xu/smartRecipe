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

index_path = os.path.join(settings.STATICFILES_DIRS[0], "index.txt")

stdout.write("Start load index\n")
t_start = time.time()
index, doc_all_ids_set = load_index(index_path)
# print(getsizeof(index))

t_end = time.time()
stdout.write("Load finished in %.02f seconds\n" % (t_end - t_start))
# query = "mac AND beef OR chicken OR lemon AND orange AND water"
query = '"beef noodles" OR 10(mac,chicken) AND NOT milk'
results = do_search(index, query, doc_all_ids_set)
for i in range(len(results)):
    print(results[i]['title'])


