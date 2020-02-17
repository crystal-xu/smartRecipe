# -*- coding: utf-8 -*-
# @Time    : 2020-01-29 16:05
# @Author  : jinhang
# @File    : index.py
# @Description  : Generate index file (need to input number of data and path of index.txt)


import os
import sys
import django
from SearchRecipe.models import TestModel
from SearchRecipe.data_preprocess import *
from collections import OrderedDict
import time
from sys import stdout


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cw3site.settings')
django.setup()

stdout.write("Start build index\n")
t_start = time.time()

#doc_list = TestModel.objects.all()
t0 = time.time()
stdout.write("Get mongo objects all used %.02f seconds\n" % (t0 - t_start))

index = dict()  # {term: OrderedDict{doc_id: [positions]}}

stdout.write("\t Preprocess document           1")
doc_id = 0
for doc in TestModel.objects.all():  # len(doc_list)
    object_id = doc['idx']
    doc_title = doc['title']
    doc_text = doc['text']
    doc_content = doc_title + doc_text
    terms = stemming(stopping(tokenisation(case_folding(doc_content))))
    position = 0
    for term in terms:  # process every term occur in one doc
        position += 1
        if term not in index:  # initialization
            index[term] = dict()
        if object_id not in index[term]:
            index[term][object_id] = list()
        index[term][object_id].append(position)  # append position

    stdout.write("\b" * len(str(doc_id)))
    stdout.write("{0}".format(doc_id))
    stdout.flush()
    doc_id += 1

t1 = time.time()
stdout.write("Finish build index in %.02f seconds" % (t1 - t0))


index_path = "./index.txt"
with open(index_path, 'w') as f:
    for term in sorted(index.keys()):  # sorted alphabetically
        f.writelines(term + ':\n')     # write the file
        for doc_dict in index[term]:
            f.writelines('\t' + str(doc_dict) + ': ' + ",".join(str(i) for i in index[term][doc_dict]) + '\n')
        f.writelines('\n')


