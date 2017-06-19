#coding=utf-8


from article.models import Article
from datetime import datetime
from django.http import Http404

from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.syndication.views import Feed    #从Feed框架中找到RSS功能
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger   #添加分页功能所需要的包


class RSSFeed(Feed):     #创建自己的类，继承于Feed，用于实现RSS功能
    title="RSS feed - article"
    link= "feeds/posts/"
    description="RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-date_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self,item):
        return item.date_time

    def item_description(self, item):
        return item.content



# Create your views here.

def home(request):             #分页功能对home函数修改
    #return HttpResponse("Hello World,Django")
    posts=Article.objects.all()           #获取全部的Article对象
    paginator= Paginator(posts, 2)  #每页显示两篇文章
    page=request.GET.get('page')
    try:
        post_list=paginator.page(page)
    except PageNotAnInteger:
        post_list=paginator.page(1)
    except EmptyPage:
        post_list=paginator.paginator(paginator.num_pages)
    return render(request,'home.html',{'post_list':post_list})


def detail(request,id):
    #post=Article.objects.all()[int(my_args)]
    #str=("title = %s , category = %s,date_time=%s,content=%s" % (post.title,post.category,post.date_time,post.content))
    #return HttpResponse(str)
    try:
        post=Article.objects.get(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    return render(request,'post.html',{'post':post})

def archives(request): #归档函数
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'archives.html', {'post_list': post_list, 'error': False})

def about_me(request):
    return render(request,'aboutme.html')

def search_tag(request,tag):  #标签分类,点击标签，即进行对应tag的查询
    try:
        post_list=Article.objects.filter(category=tag)
    except Article.DoesNotExist:
        raise Http404
    return render(request,'tag.html',{'post_list':post_list})

def blog_search(request):     #搜索功能，可搜索文章标题或者全文内容
    if 's' in request.GET:
        s=request.GET['s']
        if not s:
            return render(request,'home.html')
        else:
            post_list=Article.objects.filter(title__icontains = s)   #title__后面是两个横线，python中带'_'的变量一般都是两个横线
            if len(post_list)==0:
                return render(request,'archives.html',{'post_list':post_list,'error':True})

            else:
                return render(request,'archives.html',{'post_list':post_list,'error':False})
    return redirect('/')




def test(request):
    return render(request, 'test.html', {'current_time': datetime.now()})