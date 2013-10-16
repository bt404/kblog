# coding:utf8
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import Http404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from blog.models import Tag, Blog, Comment
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
import re
import mytools

@csrf_exempt
def show_blog(request, blog_id):
    stats = mytools.get_stats(request)
    try:
        this_blog = Blog.objects.get(pk = blog_id)
    except Blog.DoesNotExist:
        raise Http404
    if request.POST:    #Save and refresh the comments.
        response = HttpResponse()
        response['Content-Type'] = 'text/plain'
        user = request.POST.get('user')
        email = request.POST.get('email')
        this_content = request.POST.get('content')
        ctime = datetime.now()
        comment = Comment(user_name=user, email_addr=email, content=this_content, blog=this_blog, comment_time=ctime)
        comment.save()
        str_ctime = str(ctime).split('.')[0][:16]
        response.write(str_ctime)
        return response

    this_blog.scan += 1
    this_blog.save()
    comments = Comment.objects.filter(blog__exact=this_blog)
    tags = Tag.objects.all()
    arch = mytools.get_arch()
    return render_to_response('blog.html',
                              {'blog':this_blog, 'comments':comments, 'show_tags':tags, 'arch':arch, 'stats':stats}
                             )

@csrf_exempt
def home_blogs(request):
    stats = mytools.get_stats(request)
    if request.GET.get('more_data'):    #Show more blogs on aMore click.
        times = request.GET.get("times","")
        begin_num = 5*int(times)    #5 blogs each time
        total_num = Blog.objects.all().count()
        if begin_num+5 <= total_num:
            blogs = Blog.objects.all().order_by('-create_time')[begin_num:begin_num+5]
        else:
            blogs = Blog.objects.all().order_by('-create_time')[begin_num:total_num]
        for blog in blogs:
            blog.contents = blog.contents[:190] + '......'
            blog.contents = re.sub(r'<.*?>',' ',blog.contents)  #Replace tags with spaces.
            blog.contents = re.sub(r'\r\n','  ',blog.contents)
            blog.contents = re.sub(r'\n','  ',blog.contents)
        response = HttpResponse()
        response['Content-Type'] = 'text/plain'
        if blogs:
            ret_json = mytools.blogs_to_json(blogs)
        else:
            ret_json = "1" 
        response.write(ret_json)
        return response

    blogs = Blog.objects.all().order_by('-create_time')[:6] #Initiate the blogs.
    arch = mytools.get_arch()
    for blog in blogs:
        blog.contents = blog.contents[:190] + '......'    #Only show the first 190 chars.
        blog.contents = re.sub(r'<.*?>',' ',blog.contents)  #Replace tags with spaces.
        blog.contents = re.sub(r'\r\n','  ',blog.contents)
        blog.contents = re.sub(r'\n','  ',blog.contents)
        blog.contents = re.sub(r'\"','\\"',blog.contents)
    tags = Tag.objects.all()
    return render_to_response('index_blogs.html',
                              {'blogs':blogs, 'show_tags':tags, 'arch':arch, 'stats':stats}
                             )

@csrf_exempt
def show_menu(request, menuname='', year='', month=''):
    stats = mytools.get_stats(request)
    titles = []
    title = {}
    if menuname:    #Show titles with tag's name given.
        find_blogs = Blog.objects.filter(tags__name=menuname).order_by('-create_time')
        if not find_blogs:
            raise Http404
        for this_blog in find_blogs:
            title['id'] = this_blog.id
            title['name'] = this_blog.title
            title['scan'] = this_blog.scan
            title['comment_count'] = Comment.objects.filter(blog=this_blog).count()
            title['ctime'] = this_blog.create_time
            titles.append(title.copy())
    elif year and month:    #Show titles with year and month given.
        find_blogs = Blog.objects.filter(create_time__year=year,
                                         create_time__month=month).order_by('-create_time')
        if not find_blogs:
            raise Http404
        for this_blog in find_blogs:
            title['id'] = this_blog.id
            title['name'] = this_blog.title
            title['scan'] = this_blog.scan
            title['comment_count'] = Comment.objects.filter(blog=this_blog).count()
            title['ctime'] = this_blog.create_time
            titles.append(title.copy())
    else:   #Show titles with menu page default.
        find_blogs = Blog.objects.all().order_by('-create_time')[:15]
        for this_blog in find_blogs:
            title['id'] = this_blog.id
            title['name'] = this_blog.title
            title['scan'] = this_blog.scan
            title['comment_count'] = Comment.objects.filter(blog=this_blog).count()
            title['ctime'] = this_blog.create_time
            titles.append(title.copy())
    tags = Tag.objects.all()
    arch = mytools.get_arch()
    return render_to_response('menu.html',
                              {'titles':titles, 'menuname':menuname, 'show_tags':tags,
                              'arch':arch, 'year':year, 'month':month, 'stats':stats}
                             )

