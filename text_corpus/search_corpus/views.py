from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView
from operator import and_, or_
from text_corpus.models import Page, Text, Author, Genre
import re
import requests

def striphtml(data):
    text = re.compile(r'<.*?>')
    return text.sub('', re.sub('<p>', ' ', data))

def search(request):
    sterms = request.GET.getlist('s')
    opers = request.GET.getlist('op')
    exact = request.GET.getlist('e')
    au_fl = request.GET.getlist('a')
    txt_fl = request.GET.getlist('t')
    gen_fl = request.GET.getlist('g')
    sterms = [f" {sterm} " if exact[i] == '1' else sterm for i, sterm in enumerate(sterms)]
    authidlist, textidlist, main_result_list, error = [], [], [], ''

    def get_filter_and_result(pages):
        for page in pages:
            text = striphtml(Page.getContent(page))
            sin_result = Page.getInfo(page)
            sin_result['Term'] = []
            for sterm in sterms:
                if sterm in text:
                    start_index = max(0, text.find(sterm) - 26)
                    end_index = min(len(text), text.find(sterm) + len(sterm) + 26)
                    preview = ('...' if start_index > 0 else '') + text[start_index:end_index] + ('...' if end_index < len(text) else '')
                    
                    for term in sterms:
                        preview = preview.replace(term, f'<span style="color:red;font-weight:bold">{term}</span>')

                    sin_result['Term'].append(preview)
            
            if sin_result['Term']:
                main_result_list.append(sin_result)
                if sin_result['AuthID'] not in authidlist:
                    authidlist.append(sin_result['AuthID'])
                if sin_result['Textid'] not in textidlist:
                    textidlist.append(sin_result['Textid'])

    if sterms and (len(sterms) == len(opers) + 1):
        filters = {'text_id__au_id__in': au_fl or None, 'text_id__in': txt_fl or None, 'text_id__genre__in': gen_fl or None}
        queries = [Q(pg_cont__icontains=term) for term in sterms]
        if opers:
            pages = Page.objects.filter((and_ if opers[0] == 'a' else or_)(*queries)).order_by('text__au_id__date')
        else:
            pages = Page.objects.filter(queries[0]).order_by('text__au_id__date')
        pages = pages.filter(**{k: v for k, v in filters.items() if v is not None})
        get_filter_and_result(pages)
        error = "Search returned " + str(len(main_result_list)) + " pages."
        if not main_result_list:
            error = "No Results Found"
    else:
        error = "You must add an additional search term."


    texts = Text.objects.filter(status=3).order_by('au_id__date')
    authors = Author.objects.filter(incrp=1).order_by('date')
    genres = Genre.objects.all()
    filteritems = texts.filter(text_id__in=textidlist).order_by('title_ar')
    filterauth = authors.filter(au_tl__in=authidlist).order_by('au_id')

    return render(request, 'search_corpus/search.html', {
        'error': error,
        'filteritems': filteritems,
        'filterauth': filterauth,
        'terms': sterms,
        'opers': opers,
        'main_result_list': main_result_list,
        'texts': texts,
        'authors': authors,
        'genres': genres,
        'exact': exact,
        'txtfl': txt_fl,
        'aufl': au_fl,
        'genfl': gen_fl,
    })

def results(request, text_id, pgid):
    sterms = request.GET.getlist('s')
    exact = request.GET.getlist('e')

    page_list = list(Page.objects.filter(text_id=text_id))
    read_paginator = Paginator(page_list, 1)
    text_info = get_object_or_404(Text, text_id=text_id)
    page_num = Page.objects.get(pg_id=pgid).pg_count
    ppage = read_paginator.get_page(page_num)
    prange = list(read_paginator.get_elided_page_range(page_num, on_each_side=2, on_ends=1))

    text = Page.objects.get(pg_id=pgid).pg_cont
    highlighted = ''.join(['<span style="color:red;font-weight:bold">' + striphtml(sterm) + '</span>' if word == sterm else word for word in text.split()])

    return render(request, 'search_corpus/results.html', {
        'prange': prange,
        'highlighted': highlighted,
        'text': text_info,
        'count': read_paginator.count,
        'ppage': ppage,
    })
