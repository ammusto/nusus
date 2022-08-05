from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from django.db.models import Q
from .models import Page, Text, Author
import requests
import re

# Create your views here.
def browse(request):

    #get order direction
    dr = request.GET.get('d')

    #set default order
    order = 'text_id'

    #sets ordering of corpus table through url parameters
    def textOrder():
        order = request.GET.get('order')
        if dr == 'desc':
            direct = '-'
        else:
            direct = ''
        if order == 'ti':
            order = direct + 'title_ar'
        elif order == 'da':
            order = direct + 'au_id__date'
        elif order == 'au':
            order = direct + 'au_id__au_sh'
        elif order == 'tid':
            order = direct + "text_id"
        else:
            order = 'text_id'
        return order

    #paginate corpus list

    def crpPage(corpus):
        crp_list = list(corpus)
        crp_paginator = Paginator(crp_list, 20)
        cpage = crp_paginator.get_page(page_num)
        return cpage

    #get page num for corpus list
    if request.GET.get('page') is not None and int(request.GET.get('page')):
        page_num = request.GET.get('page')
    else:
        page_num = '1'

    #get corpus search and filter results
    br_fl = request.GET.get('f')
    br_sr = request.GET.get('s')

    #get url paramaters to pass to urls in template for table sorting
    link = ''
    def getLink():
        link = '&s=' + br_sr + '&' + 'f=' + br_fl
        return link

    #run corpus metadata search
    tentry = ''
    if br_sr is None or br_sr == '':
        order = textOrder()
        tentry = crpPage(Text.objects.order_by(textOrder()))
    #no filter
    elif br_sr != '' and br_fl == '0':
        tentry = crpPage(Text.objects.filter(
            Q(title_tl__icontains=br_sr) |
            Q(title_ar__icontains=br_sr) |
            Q(au_id__au_tl__icontains=br_sr) |
            Q(au_id__au_ar__icontains=br_sr) |
            Q(genre__icontains=br_sr)
            ).order_by(textOrder()))
        link = getLink()
    #title filter
    elif br_sr != '' and br_fl == '1':
        tentry = crpPage(Text.objects.filter(
            Q(title_tl__icontains=br_sr) |
            Q(title_ar__icontains=br_sr)
            ).order_by(textOrder()))
        link = getLink()
    #authoer filter
    elif br_sr != '' and br_fl == '2':
        tentry = crpPage(Text.objects.filter(
            Q(au_id__au_tl__icontains=br_sr) |
            Q(au_id__au_ar__icontains=br_sr)
            ).order_by(textOrder()))
        link = getLink()
    #genre filter
    elif br_sr != '' and br_fl == '3':
        tentry = crpPage(Text.objects.filter(
            Q(style__icontains=br_sr) |
            Q(genre__icontains=br_sr)
            ).order_by(textOrder()))
        link = getLink()

    context = {
            'tentry': tentry,
            'direct': dr,
            'link' : link,
            'order' : order,
            'br_sr' : br_sr,
            'curpg' : page_num,
        }

        
    return render(request, 'text_corpus/browse.html', context)

def text_detail(request, pk):
    text = get_object_or_404(Text, pk=pk)
    return render(request, 'text_corpus/text_detail.html', {'text': text})


def au_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    au_texts = Text.objects.filter(au_id=pk)

    context = {
        'author': author,
        'au_texts': au_texts,
    }
    return render(request, 'text_corpus/au_detail.html', context)

def read(request, text_id):

    #get page info for Paginator controls
    text_info = get_object_or_404(Text, text_id=text_id)
    page_list = list(Page.objects.filter(text_id=text_id))
    read_paginator = Paginator(page_list, 1)
    print(Page.objects.filter(text_id=text_id))

    #get page content
    if request.GET.get('page') is not None and int(request.GET.get('page')) <= len(page_list):
        page_num = request.GET.get('page')
    else:
        page_num = 1
    ppage = read_paginator.get_page(page_num)
    prange = list(read_paginator.get_elided_page_range(page_num, on_each_side=2, on_ends=1))

    context = {
        'prange': prange,
        'text': text_info,
        'rpag': read_paginator,
        'ppage': ppage,
    }
    return render(request, 'text_corpus/read.html', context)
