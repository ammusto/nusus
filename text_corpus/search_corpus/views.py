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


# strip html tags from string. used to display text in search results
def striphtml(data):
    """ striphtml from any string """
    text = re.compile(r'<.*?>')
    return text.sub('', data)

def search(request):
    """ all functions related to search page """
    #check for search terms and operators
    osterms = request.GET.getlist('s')
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
                getpages = Page.objects.filter(tq1 & (tq2 | tq3)).order_by('text__au_id__date')
            elif operators[0] == 'o' and operators [1] == 'a':
                getpages = Page.objects.filter((tq1 | tq2) & tq3).order_by('text__au_id__date')
            elif operators[0] == 'o' and operators [1] == 'o':
                getpages = Page.objects.filter(tq1 | tq2 | tq3).order_by('text__au_id__date')

        return getpages

    main_result_list = []

    def getResult(pages):
        """ get result display for search hit """
        for page in pages:

            #strip html from page content to not interfere with display
            text = striphtml(Page.getContent(page))
            i = 0
            for sterm in sterms:
                index = text.find(sterms[i])
                if index != -1:
                    #prev_len is amount of characters on each side of the search display
                    prev_len = 30 - (len(sterms[i]) // 2)

                    #set preview start index to 0 if result index is less than prev_len away from start of text
                    pr_start = 0 if index < prev_len else index - prev_len
                    startprev = '' if pr_start == 0 else '...'

                    #set preview end index to end of text if result index is less than prev_len away from end of text
                    pr_end = len(text) if index + prev_len + len(sterms[i]) > len(text
                        )-1  else index + len(sterms[i]) + prev_len
                    endprev = ''

                    #build the preview text
                    while index > pr_start : startprev += text[pr_start]; pr_start += 1
                    while index  < pr_end-len(sterms[i]) : endprev += text[index+len(
                        sterms[i])]; index += 1;
                    #add elipsis if final word of preview is not end of text
                    endprev += '' if pr_end == len(text) else '...'

                    #build search result preview with highlighted search result
                    preview = startprev + "<span style=\"color:red;font-weight:bold\">" + sterms[i] + "</span>" + endprev

                    #get text result page metadata from model as dictionary
                    sin_result = Page.getInfo(page)

                    #add the search result to dictionary
                    sin_result['Term'].append(preview)

                    #add finalized search result to main result list for display
                    main_result_list.append(sin_result)
                    if opers and 'a' not in opers:
                        i += 1
                    else:
                        break
                else:
                    i += 1

    #run search if search terms are used
    if sterms:
        #use author filter
        if au_fl and not txt_fl and not gen_fl:
            for auth in au_fl:
                getpages = getSrPage(sterms, opers).filter(text_id__au_id=auth)
                getResult(getpages)
        #use text filter
        elif txt_fl and not au_fl and not gen_fl:
            print("OK")
            for text in txt_fl:
                getpages = getSrPage(sterms, opers).filter(text_id=text)
                getResult(getpages)
        #use genre filter
        elif gen_fl and not au_fl and not txt_fl:
            for genre in gen_fl:
                getpages = getSrPage(sterms, opers).filter(text_id__genre=genre)
                getResult(getpages)
        #run search on entire corpus
        else:
            getResult(getSrPage(sterms, opers))
        #get author and text list for search result filters
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
        'oterm' : osterms,
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
