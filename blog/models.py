# coding:utf8
from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name
    
    def get_blog_num(self):
        return Blog.objects.filter(tags=self).count()

class Blog(models.Model):
    title = models.CharField('标题',max_length=50)
    contents = models.TextField('内容')
    create_time = models.DateTimeField()
    scan = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    user_name = models.CharField(max_length=50)
    email_addr = models.CharField(max_length=50)
    content = models.TextField()
    comment_time = models.DateTimeField()
    blog = models.ForeignKey(Blog)

    def __unicode__(self):
        return u'%s %s' % (self.user_name, self.blog)

class Stats(models.Model):
    total = models.IntegerField(default=0)

    def get_blog_num(self):
        return Blog.objects.all().count()

    def get_tag_num(self):
        return Tag.objects.all().count()
