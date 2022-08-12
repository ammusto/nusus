from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from text_corpus.models import Page, Text, Author, Genre
from django.db.models import Q
import requests
import re

# find all instances of search term in tokenized page, used in search and search results
def indices(lst, items):
    master_index = []
    for term in items:
        ind_index = [i for i, x in enumerate(lst) if x == term]
        master_index.append(ind_index)

    flat_list = [item for sublist in master_index for item in sublist]
    
    return sorted(flat_list)

# strip html tags from string. used to display text in search results
def striphtml(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

def search(request):
    sterms = request.GET.getlist('s')
    opers = request.GET.getlist('op')
    main_result_list = []
    error = ''
    getpages = None

    #grabs all the unique author ids for search results. used in filter
    authidlist = []
    textidlist = []
    def getSrFilter(result_list):
        i = 0
        while i < len(result_list):
            auth = result_list[i]['AuthID']
            text = result_list[i]['Textid']
            i += 1
            if auth in authidlist:
                pass
            else:
                authidlist.append(auth)
            if text in textidlist:
                pass
            else:
                textidlist.append(text)

    #this should only be run if there is a search result
    def getResult(pages):
        prev_len = 12
        for page in pages:
            text = striphtml(Page.getContent(page))
            i = 0

            for sterm in sterms:
                index = text.find(sterms[i])
                if index != -1:
                    prev_len = 30 - (len(sterms[i]) // 2)
                    endprev = ''
                    preview = ''
                    pr_start = 0 if index < prev_len else index - prev_len
                    pr_end = len(text)-1 if index + prev_len + len(sterms[i]) > len(text
                        )-1  else index + len(sterms[i]) + prev_len
                    startprev = '' if pr_start == 0 else '...'
                    while pr_start < index: startprev += text[pr_start]; pr_start += 1
                    while index  < pr_end-len(sterms[i]) : endprev += text[index+len(
                        sterms[i])]; index += 1;

                    endprev += '' if pr_end == range(len(text)-1) else '...'
                    preview = startprev + "<span style=\"color:red;font-weight:bold\">" + sterms[i] + "</span>" + endprev
                    sin_result = Page.getInfo(page)
                    sin_result['Term'].append(preview)
                    main_result_list.append(sin_result)
                    getSrFilter(main_result_list)
                    if opers and opers[0] != 'a':
                        i += 1
                    else:
                        break
                else:
                    i += 1

    def getSrPage(terms, operators):
        getpages = None
        if len(terms) > 0:
            tq1 = Q(pg_cont__icontains=terms[0])
        if len(terms) > 1:
            tq2 = Q(pg_cont__icontains=terms[1])
        if len(terms) > 2:
            tq3 = Q(pg_cont__icontains=terms[2])

        if len(terms) == 1:
            getpages = Page.objects.filter(tq1).order_by('text__au_id__date')
        elif len(terms) == 2:
            if operators[0] == 'a':
                getpages = Page.objects.filter(tq1 & tq2).order_by('text__au_id__date')
            else:
                getpages = Page.objects.filter(tq1 | tq2).order_by('text__au_id__date')

        elif len(terms) == 3:
            if operators[0] == 'a' and operators [1] == 'a':
                getpages = Page.objects.filter(tq1 & tq2 & tq3).order_by('text__au_id__date')
            elif operators[0] == 'a' and operators [1] == 'o':
                getpages = Page.objects.filter(tq1 & tq2 | tq3).order_by('text__au_id__date')
            elif operators[0] == 'o' and operators [1] == 'a':
                getpages = Page.objects.filter(tq1 | tq2 & tq3).order_by('text__au_id__date')
            elif operators[0] == 'o' and operators [1] == 'o':
                getpages = Page.objects.filter(tq1 | tq2 | tq3).order_by('text__au_id__date')

        return getpages



    def FilterSearch():
        au_fl = request.GET.getlist('a')
        txt_fl = request.GET.getlist('t')
        gen_fl = request.GET.getlist('g')
        getpages = ''
        if au_fl and not txt_fl and not gen_fl:
            for auth in au_fl:
                getpages = getSrPage(sterms, opers).filter(text_id__au_id=auth)
                getResult(getpages)
        elif txt_fl and not au_fl and not gen_fl:
            print("OK")
            for text in txt_fl:
                getpages = getSrPage(sterms, opers).filter(text_id=text)
                getResult(getpages)
        elif gen_fl and not au_fl and not txt_fl:
            for genre in gen_fl:
                getpages = getSrPage(sterms, opers).filter(text_id__genre=genre)
                getResult(getpages)
        else:
            getResult(getSrPage(sterms, opers))
        return getpages

    if sterms:
        FilterSearch()

    texts = Text.objects.filter(status=3).order_by('au_id__date')
    authors = Author.objects.filter(incrp=1).order_by('date')
    genres = Genre.objects.all()
    #grabs author and texts from search result to be used in the filter
    filteritems = Text.objects.filter(text_id__in=textidlist).order_by('title_ar')
    filterauth = Author.objects.filter(au_tl__in=authidlist).order_by('au_id')

    context = {
        'error': error,
        'filteritems': filteritems,
        'filterauth': filterauth,
        'getsearch': sterms,
        'opers' : opers,
        'main_result_list': main_result_list,
        'texts' : texts,
        'authors' : authors,
        'genres' : genres,
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
