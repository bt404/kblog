from django.contrib import admin
from ck.fields import CKEditor
from blog.models import Tag, Blog, Comment, Stats
from django.db import models

class BlogAdmin(admin.ModelAdmin):
    formfield_overrides = {     #This var overrides the widget of models.? tag in father.
        models.TextField: {'widget': CKEditor},
    }

admin.site.register(Tag)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)
admin.site.register(Stats)
