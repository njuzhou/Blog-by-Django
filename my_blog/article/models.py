#coding=utf-8
from django.db import models
from django.core.urlresolvers import reverse  #用于重写get_absolute_url，实现RSS

# Create your models here.
class Article(models.Model):
    title=models.CharField(max_length=100)     #博客题目 charfield 用于存储字符串，
    category=models.CharField(max_length=50,blank=True)   #博客标签
    date_time=models.DateTimeField(auto_now_add=True)   #博客日期 datetimefield用来存储时间
    content=models.TextField(blank=True,null=True)      #博客文章正文 textfield用来存储大量文本


    def get_absolute_url(self):                     #获取URL并转换为url的表示格式
        path=reverse('detail',kwargs={'id':self.id})
        return "http://127.0.0.1:8000%s" % path



    #python2使用_unicode_,python3使用_str_
    def __str__(self):   #告诉系统使用title字段来表示这个对象  ,是双横线，不是一个
        return self.title

    class Meta: #按时间下降排序
        ordering=['-date_time']

