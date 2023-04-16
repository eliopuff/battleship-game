import urllib.parse
import requests
import sys
import pickle
from typing import Dict
from bs4 import BeautifulSoup

# PART A

def crawl(base_url, index_file, out_file):
    '''this function is called when five arguments are entered in the command
    line containing our desired information. it essentially creates a dictionary 
    dictionaries with each key representing a page in our index, with a dictionary
    containing all the other pages in the index and the amount of times they appear
    on this page (another function employed to check this.
    in the end, it saves the dictionary of dictionaries as a pickle file.'''
    traffic_dict: Dict[str, Dict[str, int]] = {}
    page_list =  loading_index_file(index_file) #simplifies working
    for page in page_list: 
        page_dict: Dict = dict_of_linked_pages(base_url, page, page_list)
        traffic_dict[page] = page_dict
    return traffic_dict



def loading_index_file(index_file):
    '''this is a simple function that open our index file and 
    'unloads' each page in the index to a list after stripping it.'''
    with open(index_file, 'r') as index:
        page_list = [page.strip('\n') for page in index]
    return page_list            




def dict_of_linked_pages(base_url, page, page_list):
    '''this creates the singular dictionary for each key-page in the function
    crawl() (above). it employs various python libraries to read and parse html 
    pages, and allow us to access and find the links we're looking for'''
    full_url = urllib.parse.urljoin(base_url, page)
    html_request = requests.get(full_url)
    html_code = html_request.text
    all_linked_pages = {}
    parsed_page = BeautifulSoup(html_code, 'html.parser')
    for p in parsed_page.find_all('p'):
        for link in p.find_all('a', href=True):
            if link == '':
                continue
            page_link = link['href'] #a link in the page
            if page_link not in page_list:
                continue
            if page_link in all_linked_pages:
                #we have it in the dictionary, we add a counted occurrance
                all_linked_pages[page_link] += 1
            else:
                #it's not in the dictionary yet, we add a new key
                all_linked_pages[page_link] = 1
    return all_linked_pages







def pickle_load(file):
    '''to make our code cleaner with no excess code, i will
    use this function every time i unload a pickle file'''
    with open(file, 'rb') as file:
        file_content = pickle.load(file)
    return file_content




# PART B



def page_rank(iterations: int, dict_file, out_file):
    '''this function creates a dictionary that 'ranks' the pages in
    our index folder by 'popularity': how many pages point to it?
    this is found with a sum, updated in our ranking dictionary 
    that changes relative to the amount of pages each page points 
    at and dependant upon the amount of iterations fed into the input.
    finally, it will store the ranking dictionary in a pickle file'''
    r: Dict[str, float] = {} #this is the ranking table we will update
    traffic_dict = pickle_load(dict_file)
    r: Dict[str, float] = {page: 1 for page in traffic_dict}
    sum_dict: Dict[str, int] = page_pointer_sum(traffic_dict)
    if iterations == 0:
        return r
    for i in range(iterations): #num of iteration
        new_r: Dict[str,int] = {page: 0 for page in traffic_dict}
        for key1 in new_r:
            for key2 in new_r:
                if key2 not in traffic_dict[key1]:
                    continue
                new_r[key2] += r[key1] * (
                    traffic_dict[key1][key2] / sum_dict[key1])
        for key in new_r:
            r[key] = new_r[key]
    with open(out_file, 'wb') as file: #store it in a pickle file
        pickle.dump(r, file)



def page_pointer_sum(traffic_dict) -> Dict[str, float]:
    '''this function creates a dictionary of sums, summing all the links
    each page in the traffic dictionary from function crawl(), to later be 
    used in the sum employed by function page_rank()'''
    sum_dict = {}
    for key1 in traffic_dict:
        point_sum = 0
        for key2 in traffic_dict[key1]:
            point_sum += traffic_dict[key1][key2]
        sum_dict[key1] = point_sum
    return sum_dict




#PART C


def words_dict(base_url, index_file, out_file):
    '''this function creates a word dictionary that maps out all
    of the words that exists within all the pages that exist within
    the index file provided'''
    page_word_dict: Dict[str, Dict[str, int]] = {}
    page_list = loading_index_file(index_file)
    for page in page_list: 
        page_dict: Dict = dict_of_all_words(base_url, page)
        page_word_dict[page] = page_dict
    word_dict = word_dict_merging(page_word_dict)
    return word_dict




def word_dict_merging(page_word_dict):
    '''this function takes the page to word dictionary that
    the previous function created and turns it into a word to page 
    ditionary, where words are keys with values of dictionaries
    containing pages of keys where the number of appearances of 
    the word is the nested value.'''
    word_dict = {}
    for key1, val1 in page_word_dict.items():
        for key2, val2 in val1.items():
            if key2 not in word_dict:
                inner_dict = {}
            else:
                inner_dict = word_dict[key2]
            inner_dict[key1] = val2
            word_dict[key2] = inner_dict
    return word_dict


def dict_of_all_words(base_url, page) -> Dict[str, int]:
    '''this function is responsible for creating the dictionary
    for word_dict(). it is a dictionary per page of the page as key
    and words as value in a dictionary. we will change this later
    in the function word_dict_merging()'''
    full_url = urllib.parse.urljoin(base_url, page)
    html_request = requests.get(full_url)
    html_code = html_request.text
    all_words_dict: Dict[str, int] = {}
    parsed_page = BeautifulSoup(html_code, 'html.parser')
    for p in parsed_page.find_all('p'):
        paragraph: list = paragraph_cleaner(str(p.text))
        for word in paragraph:
            if word in all_words_dict:
                all_words_dict[word] += 1
            else:
                all_words_dict[word] = 1
    return all_words_dict
 

def paragraph_cleaner(paragraph):
    '''this function receives as input a paragraph in an html page
    and splits it into words, while cleaning whitespace and 
    line breaks'''
    clean_paragraph_list = \
        paragraph.split()
    return clean_paragraph_list



# PART D


def search(query, ranking_dict_file, \
    words_dict_file, max_results):
    '''this function is the one ultimately resposible 
    for doing our moogle search. it receives as input a query
    of one word or more, and relevant files to assisst to
    reference in the search algorithm. a max_result variable
    is entered - this is the amount of results we will check
    started from the highest ranked page in the rank file 
    dictionary'''
    ranking_dict = pickle_load(ranking_dict_file)
    words_dict = pickle_load(words_dict_file)
    found_queries = queries_found(query, words_dict)
    if len(found_queries) == 0:
        return
    pages_with_queries = find_pages_queries(found_queries, 
    ranking_dict, words_dict)
    results_to_get = find_max_results(
        max_results, pages_with_queries)
    query_results: Dict[str, float] = {} #dictionary of results
    for page in results_to_get:
        page_query_score = query_score(page, found_queries, \
        ranking_dict, words_dict)
        query_results[page] = page_query_score
    results = query_result_string(query_results)
    return results

def find_pages_queries(queries, 
    ranking_dict, words_dict):
    '''this function finds which pages (that exist in both
    indexes of the ranking dict and words dict) actually
    contain all the queries. these are the only pages we 
    will be considering in out moogle search. other pages
    are irrelevant to our search.'''
    pages_with_queries = {} #dict for suitable pages
    for page in ranking_dict:
        for query in queries:
            if page not in words_dict[query]:
                break #page not suitable for search
            else:
                pages_with_queries[page] =\
                    ranking_dict[page]
    return pages_with_queries #all pages suitable for search


def queries_found(queries, words_dict):
    '''this function determines whether all the queries entered
    even exist in the pages we will be looking at, by searching
    the dictionary. all the relevant queries are entered into 
    found_queries list'''
    found_queries = []
    for query in queries.split(' '):
        if query not in words_dict:
            continue
        else:
            found_queries.append(query)
    return found_queries


def query_result_string(query_results):
    '''this function reverts the results dictionary of our
    moogle search into a string to be presented at the end
    of the search with each score'''
    sorted_results = sort_results(query_results)
    #we want oyr results sorted
    result_string = ''
    for i, result in enumerate(sorted_results):
        if i == (len(sorted_results) - 1):
            result_string += result + ' ' +\
            str(query_results[result])
        else:
            result_string += result + ' ' +\
            str(query_results[result]) + '\n'
    return result_string #clean printable results output


def sort_results(query_results):
    '''this function as part of the use of the function
    query_result_string(), sorts our query-page results
    by descending order to give our best output by order'''
    sorted_results = sorted(list(query_results.values()), 
    reverse=True) #values by descending order
    sorted_results_dict = {}
    for value in sorted_results:
        for page in query_results:
            if value == query_results[page]:
                sorted_results_dict[page] = value
    return sorted_results_dict #sorted!


def find_max_results(max_results: int, ranking_dict: Dict):
    '''this function finds amongst the dictionary depicting 
    the ranked pages in the index those to be considered in the
    moogle search, according to the int max_results'''
    max_results_dict = {}
    sorted_ranks = sorted(list(ranking_dict.values()), 
    reverse=True)
    if len(sorted_ranks) < max_results:
        max_results = len(sorted_ranks) 
        #all will be considered in this case
    max_results_ranks = sorted_ranks[:max_results]
    for page in ranking_dict:
        if ranking_dict[page] in max_results_ranks:
            max_results_dict[page] = ranking_dict[page]
    return max_results_dict



def query_score(page, queries, ranking_dict, words_dict):
    '''this function takes charge of finding the score
    for a page per query, and returns the lowest query score
    to be evaluated amongst all other page scores'''
    query_sum_dict = {} #dict of score per query
    for query in queries:
        query_sum = score_value_sum(page, 
        query, ranking_dict, words_dict)
        query_sum_dict[query] = query_sum
    min_query_sum = find_min_sum(query_sum_dict)
    return min_query_sum #we need the min


def find_min_sum(query_sum_dict):
    '''this function ensures that the sum evaluated per page
    is of the lowest score of all the queries. we want to know
    that our page is the best match possible!'''
    sorted_query_sums = sorted(list(query_sum_dict.values()))
    min_query_sum = sorted_query_sums[0]
    return min_query_sum




def score_value_sum(page, query, ranking_dict, words_dict):
    '''this function takes the information of rank and mentions
    of the specific query and calculates a score for the query 
    and the page based off of a multiplied sum of the two'''
    rank = ranking_dict[page]
    mentions = words_dict[query][page]
    score_value = rank*mentions
    return score_value





if __name__ == '__main__':
    '''main is where the arguments entered by the user are run through
    our moogle search engine, depending on the action desired'''
    if sys.argv[1] == 'crawl':
        traffic_dict = crawl(sys.argv[2], sys.argv[3], sys.argv[4])
        with open(sys.argv[4], 'wb') as file:
            pickle.dump(traffic_dict, file)
    if sys.argv[1] == 'page_rank':
        page_rank(int(sys.argv[2]), sys.argv[3], sys.argv[4])
    if sys.argv[1] == 'words_dict':
        word_dict = words_dict(sys.argv[2], sys.argv[3], sys.argv[4])
        with open(sys.argv[4], 'wb') as file:
            pickle.dump(word_dict, file)
    if sys.argv[1] == 'search':
        result = search(sys.argv[2], sys.argv[3], 
        sys.argv[4], int(sys.argv[5]))
        print(result)
