# -*- coding: utf-8 -*-
# @Time    : 2019-10-13 20:51
# @Author  : jinhang
# @File    : search_model.py

from SearchRecipe.data_preprocess import *
from collections import OrderedDict
import numpy as np
from SearchRecipe.models import TestModel


def load_index(path):
    """
    fixed
    load the index file in the disk into the dict data structure:

    :param path:  the path of index file
    :return:  index: data structure {term: OrderedDict{doc_id: [positions]}}
              doc_all_ids_set: all document ids set (using for NOT and computing df)
    """
    index = dict()
    doc_all_ids_set = set()  # store all document ids in a set
    with open(path, 'r') as f:
        for line in f:  # parse each line by the data features
            if line == '\n':
                continue
            if line[0] != '\t':  # the term line
                term = line.strip(':\n')
            else:  # the doc_id and positions line
                doc_position = line.strip('\t\n').split(':')
                doc_id = doc_position[0]
                doc_all_ids_set.add(doc_id)
                position_list = doc_position[1].strip().split(',')
                if term not in index:  # initialization
                    index[term] = OrderedDict()
                if doc_id not in index[term]:
                    index[term][doc_id] = list()
                index[term][doc_id].extend(position_list)  # get position list
    return index, doc_all_ids_set


def word_preprocess(word):
    word_list = case_folding(word).strip().split()
    term_list = stemming(stopping(word_list))
    return term_list


def find_document_for_single_term(index, term):
    """
    get the doc ids for a single term from the index

    :param index: the index dict
    :param term: the single term
    :return: the doc ids which the term in
    """
    if term not in index:
        doc_ids_set = set()
    else:
        doc_ids_set = set(index[term].keys())
    return doc_ids_set


def find_document_with_positions(index, term):
    """
    get the doc ids and positions dict

    :param index: the index dict
    :param term: the single term
    :return: {doc_id:[position]}
    """
    if term not in index:
        doc_ids_dict = dict()
    else:
        doc_ids_dict = index[term]
    return doc_ids_dict


def proximity_search(index, proximity_query, distance, phrase_flag=0):
    """
    do proximity search (phrase search also get results in this function too)

    :param index: the index dict
    :param proximity_query: the proximity query
    :param distance:  the distance of two part of the query
    :param phrase_flag:  if it is a phrase, default not
    :return:  return the doc ids set
    """
    doc_ids_set = set()
    terms = proximity_query.split(',')
    term_1 = word_preprocess(terms[0].strip())
    term_2 = word_preprocess(terms[1].strip())
    assert len(term_1) == 1 and len(term_2) == 1
    doc_ids_dict_1 = find_document_with_positions(index, term_1[0])
    doc_ids_dict_2 = find_document_with_positions(index, term_2[0])
    if len(doc_ids_dict_1) == 0 or len(doc_ids_dict_2) == 0:   # deal with the term in query but not in doc
        return doc_ids_set

    common_set = set(doc_ids_dict_1.keys()).intersection(set(doc_ids_dict_2.keys()))  # focus on the intersection
    for doc_id in common_set:
        positions_1 = doc_ids_dict_1[doc_id]
        positions_1 = list(map(int, positions_1))  # turn the position to int type for compare
        range_1 = len(positions_1) - 1
        i = 0
        positions_2 = doc_ids_dict_2[doc_id]
        positions_2 = list(map(int, positions_2))
        range_2 = len(positions_2) - 1
        j = 0
        while 1:
            if phrase_flag == 0:   # normal proximity search
                if abs(positions_1[i] - positions_2[j]) <= distance:
                    doc_ids_set.add(doc_id)
                    break
                else:
                    if positions_1[i] < positions_2[j] and i < range_1:
                        i = i + 1
                    elif positions_1[i] >= positions_2[j] and j < range_2:
                        j = j + 1
                    else:
                        break
            else:    # phrase search
                if positions_2[j] - positions_1[i] == distance:  # notice here (pos2 - pos1 == 1) will break
                    doc_ids_set.add(doc_id)
                    break
                else:
                    if positions_1[i] < positions_2[j] and i < range_1:
                        i = i + 1
                    elif positions_1[i] >= positions_2[j] and j < range_2:
                        j = j + 1
                    else:
                        break
    return doc_ids_set


def phrase_search(index, phrase_query):
    """
    phrase is a kind of proximity, distance = 1，fixed order
    so call the proximity search with fixed params

    :param index:  the index dict
    :param phrase_query:  the phrase_query (has been parsed but without preprocessing)
    :return: the document ids set
    """
    distance = 1
    phrase_flag = 1  # a flag signs fixed order
    doc_ids_set = proximity_search(index, phrase_query, distance, phrase_flag)
    return doc_ids_set


def process_boolean_basic_query(index, doc_all_ids_set, basic_query):
    """
    do boolean basic query, which means the query is split from AND/OR,
    or just a single word or a NOT with a single word

    :param index: the index dict
    :param doc_all_ids_set: the all document ids set
    :param basic_query: split query from AND/OR, single word or a NOT with a single word
    :return:
    """
    if 'NOT' in basic_query:  # process NOT
        basic_query = basic_query.split('NOT', 1)[1].strip()
        if '"' in basic_query:  # NOT + phrase_query
            query_content = basic_query.strip('"')
            phrase_query = re.sub(' ', ',', query_content)
            doc_ids_set_remove = phrase_search(index, phrase_query)
        else:  # not + single term
            term_list = word_preprocess(basic_query)
            assert len(term_list) == 1
            doc_ids_set_remove = find_document_for_single_term(index, term_list[0])
        doc_ids_set = doc_all_ids_set.difference(doc_ids_set_remove)
    elif '"' in basic_query:  # phrase_query
        query_content = basic_query.strip('"')
        phrase_query = re.sub(' ', ',', query_content)
        doc_ids_set = phrase_search(index, phrase_query)
    else:  # single term
        term_list = word_preprocess(basic_query)
        assert len(term_list) == 1
        doc_ids_set = find_document_for_single_term(index, term_list[0])

    return doc_ids_set


def boolean_search(index, queries, doc_all_ids_set):
    """
    do boolean search, divide the queries into different types by the key characters 'AND', 'OR', '#', '''
    then using the different functions to do the different search

    :param index:  the index dict
    :param queries:  the query dict
    :param doc_all_ids_set:  the all document ids set
    :return: the results dict : {query_id:(doc_ids)}
    """
    search_results = OrderedDict()  # get results in this dict {query_id:(doc_ids)}
    for query_id, query_content in queries.items():  # deal with every query
        queries_doc_list = list()  # using this list if there is 'AND'/'OR' [query_part_1_doc_set, query_part_2_doc_set]
        if 'AND' in query_content:  # process the queries with AND
            split_query_contents = query_content.split('AND', 1)
            for i in range(len(split_query_contents)):  # divide the query into two parts
                basic_query = split_query_contents[i].strip()  # in each part, remove whitespace
                doc_ids_set = process_boolean_basic_query(index, doc_all_ids_set, basic_query)  # process it separated
                queries_doc_list.append(doc_ids_set)  # add results together in a list
            assert len(queries_doc_list) == 2
            query_result = queries_doc_list[0].intersection(queries_doc_list[1])  # use set.intersection complete AND
        elif 'OR' in query_content:  # process the queries with OR
            split_query_contents = query_content.split('OR', 1)
            for i in range(len(split_query_contents)):
                basic_query = split_query_contents[i].strip()
                doc_ids_set = process_boolean_basic_query(index, doc_all_ids_set, basic_query)
                queries_doc_list.append(doc_ids_set)
            assert len(queries_doc_list) == 2
            query_result = queries_doc_list[0].union(queries_doc_list[1])  # use set.union complete OR
        elif '#' in query_content:  # process the queries with '#'
            distance = int(query_content.strip('#').split('(')[0])
            proximity_query = query_content.strip('#').split('(')[1].strip(')')
            query_result = proximity_search(index, proximity_query, distance)  # process the query in proximity search
        elif '"' in query_content:  # process the queries with '''
            query_content = query_content.strip('"')
            phrase_query = re.sub(' ', ',', query_content)
            query_result = phrase_search(index, phrase_query)  # process the query in proximity search
        else:  # a single word or 'Not word'
            query_result = process_boolean_basic_query(index, doc_all_ids_set, query_content)

        search_results[query_id] = query_result

    return search_results


def ranked_search(index, query_content, doc_all_ids_set):
    """
    fixed
    do ranked search for each query

    :param index: the index dict
    :param query_content: the ranked queries
    :param doc_all_ids_set: the all document ids
    :return: the search results {doc_id: score}
    """
    print("rank search")
    n = len(doc_all_ids_set)  # number of documents in a collection
    print(n)
    scores_dict = {}   # {doc_id: score}
    terms = stemming(stopping(tokenisation(case_folding(query_content))))  # preprocessing
    print(terms)
    for term in terms:
        print(term)
        doc_ids_dict = find_document_with_positions(index, term)
        df = len(doc_ids_dict)
        if df == 0:
            continue
        else:
            for doc_id in doc_ids_dict:
                tf = len(doc_ids_dict[doc_id])
                if doc_id not in scores_dict:
                    scores_dict[doc_id] = (1.0 + np.log10(tf)) * (np.log10(n/float(df)))
                else:
                    scores_dict[doc_id] += (1.0 + np.log10(tf)) * (np.log10(n/float(df)))
        print("one step")
    print("finished search")
    scores_list = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)  # reverse list
    return scores_list


def write_results_to_file(search_results, path, query_type):
    """
    write results for both boolean and ranked queries

    :param search_results: {query_id: [doc_id, score]}
    :param path:  the path in the disk
    :param query_type:  boolean or ranked
    :return:
    """
    f = open(path, 'w')
    if query_type == 'ranked':  # for ranked
        max_num = 1000  # if equal max_num stop
        for query_id in search_results:
            count = 0
            scores_list = search_results[query_id]
            for doc_score in scores_list:
                count += 1
                doc_id = doc_score[0]
                score = doc_score[1]
                score = format(score, '.4f')
                f.write(query_id + ' 0 ' + doc_id + ' 0 ' + str(score) + ' 0\n')
                if count == max_num:
                    break

    if query_type == 'boolean':  # for boolean
        for query_id in search_results:
            docs_list = sorted(list(map(int, list(search_results[query_id]))), reverse=True)  # bigger doc id first
            for doc_id in docs_list:
                f.write(query_id + ' 0 ' + str(doc_id) + ' 0 1 0\n')
    f.close()
    return None


def do_search(query, index, doc_all_ids_set):
    # index_path = "./index.txt"

    # index_path = index_file
    # index, doc_all_ids_set = load_index(index_path)
    print("enter do search")
    results_list = ranked_search(index, query, doc_all_ids_set)
    results = list()

    #todo: merge the boolean search

    # one by one
    # for doc_score in results_list:
    #     object_id = doc_score[0]
    #     result = TestModel.objects.filter(docId=object_id)
    #     # break
    #     results.append(result[0])
    #     # print(result[0]['title'])

    object_list = list()
    for doc_score in results_list:
        object_id = doc_score[0]
        object_list.append(object_id)

    results = TestModel.objects.filter(docId__in=object_list)
    results = list(results)
    results.sort(key=lambda t: object_list.index(t.docId))
    # test output
    # for i in range(len(results)):
    #     print(results[i]['title'])
    return results

