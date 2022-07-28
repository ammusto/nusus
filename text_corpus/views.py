from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Page, Text, Author
import requests
import re

# Create your views here.
def browse(request):
    order = request.GET.get('order')
    d = request.GET.get('d')

    # determines ordering of corpus table through url parameters
    if d == 'desc':
        direct = '-'
    else:
        direct = ''
    if order == 'ti':
        order = direct + 'title_tl'
    elif order == 'au':
        order = direct + 'au_id__au_sh'
    elif order == 'tid':
        order = direct + "text_id"
    else:
        order = 'text_id'
    tentry = Text.objects.order_by(order)

    context = {
            'tentry': tentry,
            'direct': d,
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
        'count': read_paginator.count,
        'ppage': ppage,
    }
    return render(request, 'text_corpus/read.html', context)
