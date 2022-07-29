from django.contrib import admin

# Register your models here.
from .models import Text, Page, Author, Genre

admin.site.register(Text)
admin.site.register(Page)
admin.site.register(Author)
admin.site.register(Genre)
