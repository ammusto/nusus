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
    # Get query params
    page_num = request.GET.get('page', '1')
    order = request.GET.get('order')
    dr = request.GET.get('d')
    br_fl = request.GET.get('f', '0')
    br_sr = request.GET.get('s', '')

    if order == "da":
        order = "au_id__date"

    # Set ordering of corpus table through url parameters
    if dr == 'desc':
        order = f"-{order}"
    else:
        order = f"{order}"

    # Get corpus search and filter results
    text_query = Q(status=3)
    if br_sr and br_fl == '0':
        text_query &= (Q(title_tl__icontains=br_sr) |
                       Q(title_ar__icontains=br_sr) |
                       Q(au_id__au_tl__icontains=br_sr) |
                       Q(au_id__au_ar__icontains=br_sr) |
                       Q(genre_id__gen_en__icontains=br_sr) |
                       Q(genre_id__gen_ar__icontains=br_sr))
    elif br_sr and br_fl == '1':
        text_query &= (Q(title_tl__icontains=br_sr) |
                       Q(title_ar__icontains=br_sr))
    elif br_sr and br_fl == '2':
        text_query &= (Q(au_id__au_tl__icontains=br_sr) |
                       Q(au_id__au_ar__icontains=br_sr))
    elif br_sr and br_fl == '3':
        text_query &= (Q(genre_id__gen_en__icontains=br_sr) |
                       Q(genre_id__gen_ar__icontains=br_sr))

    # Run corpus metadata search
    text_list = Text.objects.filter(text_query).order_by(order)
    paginator = Paginator(text_list, 20)
    tentry = paginator.get_page(page_num)

    context = {
        'tentry': tentry,
        'direct': dr,
        'link': f"&s={br_sr}&f={br_fl}",
        'order': order,
        'br_sr': br_sr,
        'curpg': page_num,
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
