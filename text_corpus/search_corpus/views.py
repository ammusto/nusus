from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from text_corpus.models import Page, Text, Author
import requests
import re

# find all instances of search term in tokenized page, used in search and search results
def indices(lst, item):
    return [i for i, x in enumerate(lst) if x == item]

# strip html tags from string. used to display text in search results
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


def search(request):
    getsearch = request.GET.get('text_contains')
    #see if filter is applied
    getfilter = request.GET.get('f')
    main_result_list = []
    error = ''
    textidlist = []
    
    #grabs all the unique text ids for search results. used in filter
    def getTextID(sr_results):
        x = 0
        while x < len(sr_results):
            text = sr_results[x]['Textid']
            x += 1
            if text in textidlist:
                pass
            else:
                textidlist.append(text)

    #grabs all the unique author ids for search results. used in filter
    authidlist = []
    def getAuthID(sr_results):
        x = 0
        while x < len(sr_results):
            auth = sr_results[x]['AuthID']
            x += 1
            if auth in authidlist:
                pass
            else:
                authidlist.append(auth)

    #results function
    def srResults(pages):

        preview = ''
        #gets each page term is found, tokenizes the page, and grabs the term from the text
        for page in getpages:
            tokenized = Page.getContent(page).split()
            #grabs all words that contain search term, e.g. search is "ab" will get "bab" "abc" etc.
            sr_results = list(filter(lambda x: getsearch in x, tokenized))
            for sr_res in sr_results:
                tokenized = Page.getContent(page).split()
                #adds html code to identify the term
                for index in indices(tokenized, sr_res):
                    tokenized[index] = "<span style=\"color:red;font-weight:bold\">" + sr_res + "</span>"
                    startprev = []
                    endprev = []
                    preview = ''
                    #grabs the terms that precedes & antecedes the search term to display in preview
                    if int(index) - 3 > 0:
                        pr_start = int(index) - 4
                    else:
                        pr_start = 0
                    while pr_start < int(index):
                        startprev.append(tokenized[pr_start])
                        pr_start += 1
                    if int(index) + 5 > len(tokenized):
                        pr_end = len(tokenized) - 1
                    else:
                        pr_end = int(index) + 5
                        pr_end -= 1
                    while pr_end > int(index):
                        endprev.insert(0, tokenized[pr_end])
                        pr_end -= 1
                    #creates the preview
                    preview = striphtml(" ".join(startprev)) + "<span style=\"color:red;font-weight:bold\"> " + striphtml(
                        sr_res) + " </span>" + striphtml(" ".join(endprev))
            #pulls data for text in each result
            sin_result_list = Page.getInfo(page)
            sin_result_list['Term'].append(preview)
            #adds each individual result to main result list
            main_result_list.append(sin_result_list)
            getTextID(main_result_list)
            getAuthID(main_result_list)

    #runs search
    if getsearch != '' and getsearch is not None and " " not in getsearch and getfilter != '1':
        getpages = Page.objects.filter(pg_cont__icontains=getsearch
            ).order_by('text__title_ar')
        srResults(getpages)
        if len(main_result_list) < 1:
            error = "No results found."
            print(error)
    #runs search with filter activated
    elif getfilter == '1':
        filterdict = dict(request.GET)
        print("filter")
        #check if any author filters are used and filter
        if "a" in filterdict:
            for auth in filterdict['a']:
                getpages = Page.objects.filter(text_id__au_id=auth
                    ).filter(pg_cont__icontains=getsearch).order_by('text__title_ar')
                srResults(getpages)
        #check if any text filters are used and filter
        elif "t" in filterdict:
            for text in filterdict['t']:
                getpages = Page.objects.filter(text_id=text).filter(
                	pg_cont__icontains=getsearch).order_by('text__title_ar')
                srResults(getpages)
    #errors
    elif getsearch is '':
        error = "No search term provided"
    elif getsearch is None:
        error = ''
    else:
        error = "Only single word search is supported at this time"
        print(error)
        
    #grabs author and texts from search result to be used in the filter           
    filteritems = Text.objects.filter(text_id__in=textidlist).order_by('title_ar')
    filterauth = Author.objects.filter(au_tl__in=authidlist).order_by('au_id')

    context = {
        'error': error,
        'filteritems': filteritems,
        'filterauth': filterauth,
        'getsearch': getsearch,
        'main_result_list': main_result_list,
    }
    return render(request, 'search_corpus/search.html', context)

def results(request, text_id, pgid):
    term = request.GET.get('t')
    #get info for Paginator controls
    page_list = list(Page.objects.filter(text_id=text_id))
    read_paginator = Paginator(page_list, 1)
    text_info = get_object_or_404(Text, text_id=text_id)
    page_num = Page.objects.get(pg_id=pgid).pg_count
    ppage = read_paginator.get_page(page_num)
    prange = list(read_paginator.get_elided_page_range(page_num, on_each_side=2, on_ends=1))

    #tokenizes the page, finds search term, replaces it with term+html code, rejoins
    if term != '' and term is not None:
        rpage = Page.objects.get(pg_id=pgid).pg_cont.split()
        sr_results = list(filter(lambda x: term in x, rpage))
        for sr_res in sr_results:
            for index in indices(rpage, sr_res):
                rpage[index] = "<span style=\"color:red;font-weight:bold\">" + striphtml(sr_res) + "</span>"
        highlighted = " ".join(rpage)

    context = {
        'prange': prange,
        'highlighted': highlighted,
        'text': text_info,
        'count': read_paginator.count,
        'ppage': ppage,
    }
    return render(request, 'search_corpus/results.html', context)
