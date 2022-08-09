from django.shortcuts import render
from django.utils import timezone
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import CorpusUp
from django.db.models import Q
from text_corpus.models import Page, Text, Author
import requests
import re

def home(request):
    # pulls corpus update list
    updates = list(CorpusUp.objects.order_by('-date'))
    update_paginator = Paginator(updates, 5)
    page_num = request.GET.get('page')
    disp_up = update_paginator.get_page(page_num)
    context = {
        'update': disp_up,
        'count': update_paginator.num_pages,
    }
    return render(request, 'info_corpus/home.html', context)

def about(request):
    return render(request, 'info_corpus/about.html')

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)
    
def corpus(request):
    texts = Text.objects.filter(~Q(status=1))
    txt_cnt = texts.count()
    au_cnt = Author.objects.filter(incrp=1).count()
    pg_cnt = Page.objects.all().count()

    #function to get the total words in corpus
    def getWords(texts):
        words_list = []
        for text in texts:
            words = text.word_len
            words_list.append(words)
        ttl_wrds = sum(words_list)
        return ttl_wrds
    ttl_wrds = getWords(texts)

    context = {
        'pcount': pg_cnt,
        'acount': au_cnt,
        'wcount': ttl_wrds,
        'tcount': txt_cnt,
    }
    return render(request, 'info_corpus/corpus.html', context)
