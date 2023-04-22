from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from text_corpus.models import Page, Text, Author, Genre
from django.db.models import Q
from operator import or_, and_
import requests
import re


# strip html tags from string. used to display text in search results
def striphtml(data):
    """ striphtml from any string """
    text = re.compile(r'<.*?>')
    return text.sub('', data)

def search(request):
    """ all functions related to search page """
    #check for search terms and operators
    sterms = request.GET.getlist('s')
    opers = request.GET.getlist('op')
    exact = request.GET.getlist('e')
    #check for filters
    au_fl = request.GET.getlist('a')
    txt_fl = request.GET.getlist('t')
    gen_fl = request.GET.getlist('g')
    i = 0
    for x in sterms:
        if exact[i] == '1':
            sterms[i] = " " + sterms[i] + " "
        i += 1

    #grab all the unique author ids for search results. used in filter
    authidlist = []
    textidlist = []

    #error message
    error = ''
    def getSrFilter(result_list):
        """ get list of unique author and text ids for search result filter """
        i = 0
        while i < len(result_list):
            #get author id and text it from result lists
            auth = result_list[i]['AuthID']
            text = result_list[i]['Textid']
            i += 1

            #add author id and text id
            if auth in authidlist:
                pass
            else:
                authidlist.append(auth)
            if text in textidlist:
                pass
            else:
                textidlist.append(text)

    def getSrPage(terms, operators):
        queries = [Q(pg_cont__icontains=term) for term in terms]

        if len(terms) == 1:
            getpages = Page.objects.filter(*queries).order_by('text__au_id__date')
        elif len(terms) == 2:
            op = and_ if operators[0] == 'a' else or_
            getpages = Page.objects.filter(op(*queries)).order_by('text__au_id__date')
        elif len(terms) == 3:
            ops = {'a': and_, 'o': or_}
            op1 = ops[operators[0]]
            op2 = ops[operators[1]]
            getpages = Page.objects.filter(op1(queries[0], op2(queries[1], queries[2]))).order_by('text__au_id__date')
        else:
            getpages = None

        return getpages

    main_result_list = []

    def getResult(pages):
        """ get result display for search hit """
        for page in pages:
            text = striphtml(Page.getContent(page))
            for sterm in sterms:
                index = text.find(sterm)
                if index != -1:
                    prev_len = 30
                    start_index = max(0, index - prev_len)
                    end_index = min(len(text), index + len(sterm) + prev_len)
                    preview = (
                        '...' if start_index > 0 else ''
                    ) + text[start_index:index] + '<span style="color:red;font-weight:bold">' + sterm + '</span>' + text[index + len(sterm):end_index] + (
                        '...' if end_index < len(text) else ''
                    )
                    sin_result = Page.getInfo(page)
                    sin_result['Term'].append(preview)
                    main_result_list.append(sin_result)

    #run search if search terms are used
    if sterms:
        filters = {}
        if au_fl:
            filters['text_id__au_id__in'] = au_fl
            print(filters)
        elif txt_fl:
            filters['text_id__in'] = txt_fl
        elif gen_fl:
            filters['text_id__genre__in'] = gen_fl

        pages = getSrPage(sterms, opers)
        if filters:
            pages = pages.filter(**filters)

        getResult(pages)

        if main_result_list:
            getSrFilter(main_result_list)
        else:
            error = "No Results Found"


    #get corpus texts, authors, and genres for main search filter
    texts = Text.objects.filter(status=3).order_by('au_id__date')
    authors = Author.objects.filter(incrp=1).order_by('date')
    genres = Genre.objects.all()

    #grabs author and texts from search result to be used in the filter
    filteritems = texts.filter(text_id__in=textidlist).order_by('title_ar')
    filterauth = authors.filter(au_tl__in=authidlist).order_by('au_id')

    context = {
        'error' : error,
        'filteritems': filteritems,
        'filterauth': filterauth,
        'terms': sterms,
        'opers' : opers,
        'main_result_list': main_result_list,
        'texts' : texts,
        'authors' : authors,
        'genres' : genres,
        'exact' : exact,
        'txtfl' : txt_fl,
        'aufl' : au_fl,
        'genfl' : gen_fl,
    }
    return render(request, 'search_corpus/search.html', context)

def results(request, text_id, pgid):
    sterms = request.GET.getlist('s')
    exact = request.GET.getlist('e')

    #get info for Paginator controls
    page_list = list(Page.objects.filter(text_id=text_id))
    read_paginator = Paginator(page_list, 1)
    text_info = get_object_or_404(Text, text_id=text_id)
    page_num = Page.objects.get(pg_id=pgid).pg_count
    ppage = read_paginator.get_page(page_num)
    prange = list(read_paginator.get_elided_page_range(page_num, on_each_side=2, on_ends=1))

    #get the page text and replace terms
    text = Page.objects.get(pg_id=pgid).pg_cont
    for sterm in sterms:
        text = text.replace(sterm, "<span style=\"color:red;font-weight:bold\">" + striphtml(sterm) + "</span>")

    highlighted = text

    context = {
        'prange': prange,
        'highlighted': highlighted,
        'text': text_info,
        'count': read_paginator.count,
        'ppage': ppage,
    }
    return render(request, 'search_corpus/results.html', context)
