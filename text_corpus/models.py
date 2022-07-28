from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.
class Text(models.Model):
    text_id = models.IntegerField(primary_key=True)
    title_tl = models.CharField(max_length=250)
    title_ar = models.CharField(max_length=250)
    pg_len = models.IntegerField()
    pg_rng = models.CharField(max_length=25)
    word_len = models.IntegerField()
    descr = models.TextField()
    perm = models.TextField()
    added = models.DateTimeField(default=timezone.now)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    au_id = models.ForeignKey('Author', on_delete = models.CASCADE)
    gen_id = models.ForeignKey('Genre', on_delete = models.CASCADE)
    published_date = models.DateTimeField(blank=True, null=True)
    avail_read = models.BooleanField()
    descr_ar = models.TextField()
    editions = models.TextField()
    permbib = models.TextField()
    source = models.TextField()

    def publish(self):
        self.save()

    def __str__(self):
        return self.title_tl

class Page(models.Model):
    pg_id = models.IntegerField(primary_key=True)
    pg_num = models.IntegerField()
    pg_cont = models.TextField()
    pg_count = models.IntegerField()
    text = models.ForeignKey('Text', on_delete = models.CASCADE)
    

    def __str__(self):
        return str(self.pg_id)
        
    def getContent(self):
        return str(self.pg_cont)

    def getInfo(self):
        sin_result_list = {}
        sin_result_list.update({'Text': self.text, 'Page': self.pg_num, 'Term': [], 'Textid': self.text.text_id, 'PgCount': self.pg_count, 'PgID': self.pg_id, 'AuthID': self.text.au_id,})
        return sin_result_list

class Author(models.Model):
    au_id = models.IntegerField(primary_key=True)
    au_tl = models.CharField(max_length = 250)
    au_ar = models.CharField(max_length = 250)
    au_sh = models.CharField(max_length = 50)
    sh_ar = models.CharField(max_length = 50)
    date = models.CharField(max_length = 50)
    date_ar = models.CharField(max_length = 50)
    cit = models.TextField()
    bio = models.TextField()
    bio_ar = models.TextField()
    books = models.TextField()
    books_ar = models.TextField()
    def __str__(self):
        return self.au_tl

class Genre(models.Model):
    gen_id = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length = 100)
    def __str__(self):
        return self.genre