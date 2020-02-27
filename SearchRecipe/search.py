# -*- coding: utf-8 -*-
# @Time    : 2019-10-13 20:51
# @Author  : jinhang
# @File    : search_model.py

from SearchRecipe.data_preprocess import *
import numpy as np
from SearchRecipe.models import TestModel
from array import *


def load_index(path):
    """
    fixed
    load the index file in the disk into the dict data structure:

    :param path:  the path of index file
    :return:  index: data structure {term: [(doc_id,(positions))]}
              doc_all_ids_set: all document ids set (using for NOT and computing df)
    """
    index = dict()
    doc_all_ids_set = set()  # store all document ids in a set
    # flag = 0
    with open(path, 'r') as f:
        for line in f:  # parse each line by the data features
            if line == '\n':
                continue
            if line[0] != '\t':  # the term line
                # if flag != 0:
                #     if len(index[term])>=30000:
                #         print(term + ':' + str(len(index[term])))
                # flag = 1
                term = line.strip(':\n')
            else:  # the doc_id and positions line
                doc_position = line.strip('\t\n').split(':')
                doc_id = int(doc_position[0])
                doc_all_ids_set.add(doc_id)
                position_list = doc_position[1].strip().split(',')
                position_list = array('I', [int(i) for i in position_list])
                if term not in index:  # initialization
                    index[term] = list()
                index[term].append((doc_id, tuple(position_list)))

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
        doc_ids_set = set([doc[0] for doc in index[term]])
    return doc_ids_set


def find_document_with_positions(index, term):
    """
    get the doc ids and positions list

    :param index: the index dict
    :param term: the single term
    :return: [(doc_id,(position))]
    """
    if term not in index:
        doc_ids_list = list()
    else:
        doc_ids_list = index[term]
    return doc_ids_list


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
    global input_error_flag
    terms = proximity_query.split(',')
    length = len(terms)
    if length != 2:
        input_error_flag = 1
        return doc_ids_set
    term_1 = word_preprocess(terms[0].strip())
    term_2 = word_preprocess(terms[1].strip())
    if len(term_1) == 1 and len(term_2) == 1:
        print("proximity term 1\t" + term_1[0])
        print("proximity term 2\t" + term_2[0])
        doc_ids_list_1 = find_document_with_positions(index, term_1[0])
        doc_ids_list_2 = find_document_with_positions(index, term_2[0])
        if len(doc_ids_list_1) == 0 or len(doc_ids_list_2) == 0:  # deal with the term in query but not in doc
            return doc_ids_set
        doc_ids_1 = [doc[0] for doc in doc_ids_list_1]
        doc_ids_2 = [doc[0] for doc in doc_ids_list_2]
        common_set = set(doc_ids_1).intersection(set(doc_ids_2))  # focus on the intersection
        for doc_id in common_set:
            positions_1 = doc_ids_list_1[doc_ids_1.index(doc_id)][1]
            range_1 = len(positions_1) - 1
            i = 0
            positions_2 = doc_ids_list_2[doc_ids_2.index(doc_id)][1]
            range_2 = len(positions_2) - 1
            j = 0
            while 1:
                if phrase_flag == 0:  # normal proximity search
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
                else:  # phrase search
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
    else:
        input_error_flag = 1
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


def process_boolean_basic_query(index, basic_query, doc_all_ids_set):
    """
    do boolean basic query, which means the query is split from AND/OR,
    or just a single word or a NOT with a single word

    :param index: the index dict
    :param doc_all_ids_set: the all document ids set
    :param basic_query: split query from AND/OR, single word or a NOT with a single word
    :return:
    """
    global input_error_flag
    doc_ids_set = set()
    if 'NOT' in basic_query:  # process NOT
        basic_query = basic_query.split('NOT', 1)[1].strip()
        if '"' in basic_query:  # NOT + phrase_query
            query_content = basic_query.strip('"')
            phrase_query = re.sub(' ', ',', query_content)
            doc_ids_set_remove = phrase_search(index, phrase_query)
        elif '#' in basic_query:  # NOT + proximity search
            distance = int(basic_query.strip('#').split('(')[0])
            proximity_query = basic_query.strip('#').split('(')[1].strip(')')
            doc_ids_set_remove = proximity_search(index, proximity_query, distance)
        else:  # not + single term
            term_list = word_preprocess(basic_query)
            if len(term_list) == 1:
                doc_ids_set_remove = find_document_for_single_term(index, term_list[0])
            else:
                input_error_flag = 1
                doc_ids_set_remove = set()
        doc_ids_set = doc_all_ids_set.difference(doc_ids_set_remove)

    elif '"' in basic_query:  # phrase_query
        query_content = basic_query.strip().split('"')
        if len(query_content) != 3:
            input_error_flag = 1
            return doc_ids_set
        if len(query_content[0]) != 0:
            input_error_flag = 1
            return doc_ids_set
        if len(query_content[2]) != 0:
            input_error_flag = 1
            return doc_ids_set
        phrase_query = query_content[1].strip()
        phrase_query = re.sub(' ', ',', phrase_query)
        doc_ids_set = phrase_search(index, phrase_query)

    elif '#' in basic_query:  # proximity search
        try:
            query_separate_by_bracket = basic_query.strip('#').split('(')
            if len(query_separate_by_bracket) != 2:
                input_error_flag = 1
                return doc_ids_set
            distance = int(query_separate_by_bracket[0])
            proximity_query = query_separate_by_bracket[1].split(')')
            if len(proximity_query) != 2:
                input_error_flag = 1
                return doc_ids_set
            if len(proximity_query[1]) != 0:
                input_error_flag = 1
                return doc_ids_set
        except:
            input_error_flag = 1
            return doc_ids_set

        doc_ids_set = proximity_search(index, proximity_query[0], distance)

    else:  # single term
        term_list = word_preprocess(basic_query)
        if len(term_list) == 1:
            doc_ids_set = find_document_for_single_term(index, term_list[0])
        else:
            input_error_flag = 1

    return doc_ids_set


def boolean_search(index, query_content, doc_all_ids_set):
    """
    do boolean search, divide the queries into different types by the key characters 'AND', 'OR', '#', '''
    then using the different functions to do the different search

    :param index:  the index dict
    :param query_content  the query content
    :param doc_all_ids_set:  the all document ids set
    :return: the results dict : {query_id:(doc_ids)}
    """
    global input_error_flag
    query_result = set()
    queries_doc_list = list()  # using this list if there is 'AND'/'OR' [query_part_doc_set]
    if 'OR' in query_content:  # process the queries with OR
        split_query_contents = query_content.split('OR')
        for i in range(len(split_query_contents)):
            basic_query = split_query_contents[i].strip()
            if 'AND' in basic_query:  # AND in OR expression
                queries_doc_list_with_and = list()
                split_query_contents_with_and = basic_query.split('AND')
                for j in range(len(split_query_contents_with_and)):
                    basic_query_with_and = split_query_contents_with_and[j].strip()
                    doc_ids_set_with_and = process_boolean_basic_query(index, basic_query_with_and, doc_all_ids_set)
                    queries_doc_list_with_and.append(doc_ids_set_with_and)
                doc_ids_set = doc_all_ids_set.intersection(*queries_doc_list_with_and)
            else:
                doc_ids_set = process_boolean_basic_query(index, basic_query, doc_all_ids_set)
            queries_doc_list.append(doc_ids_set)
        query_result = set().union(*queries_doc_list)   # use set.union complete OR

    elif 'AND' in query_content:  # process the queries with AND
        split_query_contents = query_content.split('AND')
        print(split_query_contents)
        for i in range(len(split_query_contents)):  # divide the query into two parts
            basic_query = split_query_contents[i].strip()  # in each part, remove whitespace
            print(basic_query)
            doc_ids_set = process_boolean_basic_query(index, basic_query, doc_all_ids_set)  # process it separated
            queries_doc_list.append(doc_ids_set)  # add results together in a list
        query_result = doc_all_ids_set.intersection(*queries_doc_list)    # use set.intersection complete AND

    elif '#' in query_content:  # process the queries with '#'
        try:
            query_separate_by_bracket = query_content.strip('#').split('(')
            if len(query_separate_by_bracket) != 2:
                input_error_flag = 1
                return query_result
            distance = int(query_separate_by_bracket[0])
            proximity_query = query_separate_by_bracket[1].split(')')
            if len(proximity_query) != 2:
                input_error_flag = 1
                return query_result
            if len(proximity_query[1]) != 0:
                input_error_flag = 1
                return query_result
        except:
            input_error_flag = 1
            return query_result

        query_result = proximity_search(index, proximity_query[0], distance)  # process the query in proximity search

    elif '"' in query_content:  # process the queries with '''
        query_content = query_content.strip().split('"')
        if len(query_content) != 3:
            input_error_flag = 1
            return query_result
        if len(query_content[0]) != 0:
            input_error_flag = 1
            return query_result
        if len(query_content[2]) != 0:
            input_error_flag = 1
            return query_result
        phrase_query = query_content[1].strip()
        phrase_query = re.sub(' ', ',', phrase_query)
        query_result = phrase_search(index, phrase_query)  # process the query in proximity search

    else:  # a single word or 'Not word'
        query_result = process_boolean_basic_query(index, query_content, doc_all_ids_set)

    return query_result


def ranked_search(index, query_content, doc_all_ids_set):
    """
    fixed
    do ranked search for each query

    :param index: the index dict
    :param query_content: the ranked queries
    :param doc_all_ids_set: the all document ids
    :return: the search results {doc_id: score}
    """
    print("begin rank search")
    n = len(doc_all_ids_set)  # number of documents in a collection
    print("number of docs: " + str(n))
    scores_dict = {}  # {doc_id: score}
    terms = stemming(stopping(tokenisation(case_folding(query_content))))  # preprocessing
    print(terms)
    for term in terms:
        doc_ids_list = find_document_with_positions(index, term)
        df = len(doc_ids_list)
        if df == 0:
            continue
        else:
            for doc in doc_ids_list:
                tf = len(doc[1])
                if doc[0] not in scores_dict:
                    scores_dict[doc[0]] = (1.0 + np.log10(tf)) * (np.log10(n / float(df)))
                else:
                    scores_dict[doc[0]] += (1.0 + np.log10(tf)) * (np.log10(n / float(df)))
        print(term + "\t search finished")
    print("whole search finished")
    scores_list = sorted(scores_dict.items(), key=lambda x: x[1], reverse=True)  # reverse list
    return scores_list


def do_search(index, query, doc_all_ids_set):
    global input_error_flag
    input_error_flag = 0
    boolean_flag = 0
    results = []
    print("Determine search type: ")
    boolean_words = ['OR', 'AND', '#', '"']
    for word in boolean_words:
        if word in query:
            print("do boolean search")
            print("contain word: " + word)
            boolean_flag = 1
            results_list = boolean_search(index, query, doc_all_ids_set)
            if input_error_flag == 1:
                print("input not valid in boolean, treat as ranked search")
                boolean_flag = 0
                break
            object_list = list()
            max_num = 100  # display the max_num pages
            num = 0
            for object_id in results_list:
                object_list.append(object_id)
                num += 1
                if num == max_num:
                    break
            results = TestModel.objects.filter(idx__in=object_list)
            results = list(results)
            results.sort(key=lambda t: object_list.index(t.idx))
            break

    if boolean_flag == 0:
        print("do ranked search")
        results_list = ranked_search(index, query, doc_all_ids_set)
        object_list = list()
        max_num = 100  # display the max_num pages
        num = 0
        for doc_score in results_list:
            object_id = doc_score[0]
            object_list.append(object_id)
            num += 1
            if num == max_num:
                break
        print("idx found")
        results = TestModel.objects.filter(idx__in=object_list)
        results = list(results)
        results.sort(key=lambda t: object_list.index(t.idx))

    return results
