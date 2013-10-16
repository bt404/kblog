from blog.models import Blog, Stats
import re

def get_arch():
    arch = {}
    blogs = Blog.objects.order_by('create_time')
    for blog in blogs:
        time = str(blog.create_time).split(' ')[0][:7].replace('-',' ')
        if not arch.get(time, ''):
            arch[time] = 1
        else:
            arch[time] += 1
    return arch

def blogs_to_json(blogs):
    "Transfer tool for blogs, havn't realized string transfer"
    ret_json = '['
    for j,blog in enumerate(blogs):
        ret_json += '{'
        ret_json += '\"blog_title\":'
        ret_json += '\"'+blog.title+'\",'
        ret_json += '\"blog_contents\":'
        ret_json += '\"'+string_escape(blog.contents)+'\",'
        ret_json += '\"blog_id\":'
        ret_json += '\"'+str(blog.id)+'\",'
        ret_json += '\"blog_scan\":'
        ret_json += '\"'+str(blog.scan)+'\",'
        ret_json += '\"blog_ctime\":'
        ret_json += '\"'+str(blog.create_time)+'\",'
        ret_json += '\"blog_tags\":['
        for i,tag in enumerate(blog.tags.all()):
            ret_json += '{"tag_name\":'
            ret_json += '\"'+tag.name+'\"}'
            if i != blog.tags.count()-1:
                ret_json += ','
        ret_json += ']}'
        if j < len(blogs)-1:
            ret_json +=','
    ret_json += ']'
    return ret_json

def string_escape(contents):
    contents = re.sub(r'\"','\\"',contents)
    contents = re.sub(r'<','&lt;',contents)
    contents = re.sub(r'>','&gt;',contents)
    return contents

def get_stats(request):
    stats = {}
    stat = Stats.objects.get()
    if not 'uid' in request.session:
        request.session.set_expiry(600)
        request.session['uid']=1
        stat.total += 1
        stat.save()
    stats['total'] = stat.total
    stats['blogs'] = stat.get_blog_num()
    stats['tags'] = stat.get_tag_num()
    return stats
