from django.urls import path
import info_corpus.views, text_corpus.views, text_corpus.search_corpus.views
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

urlpatterns = [

    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),
    path('', info_corpus.views.home, name='home'),
    path('about/', info_corpus.views.about, name='about'),
    path('corpus/', info_corpus.views.corpus, name='corpus'),


    path('results/<int:text_id>/<int:pgid>/', text_corpus.search_corpus.views.results, name='results'),
    path('search/', text_corpus.search_corpus.views.search, name='search'),

    path('browse/', text_corpus.views.browse, name='about'),
    path('text/<int:pk>/', text_corpus.views.text_detail, name='text_detail'),
    path('author/<int:pk>/', text_corpus.views.au_detail, name='au_detail'),
    path('read/<int:text_id>/', text_corpus.views.read, name='content'),

]
handler404 = "info_corpus.views.page_not_found_view"