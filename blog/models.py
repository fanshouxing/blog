# coding:utf-8
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import markdown
from django.utils.html import strip_tags

# Create your models here.
from django.utils.six import python_2_unicode_compatible


@python_2_unicode_compatible #兼容python2
class Category(models.Model):
    """
    Django 要求模型必须继承models.Model类。
    Category 只需要一个简单的分类名name就可以了
    CharField 指定分类名name 的数据类型 ，CharField为字符型,max_length 参数指定其最大长度
    其他Django类型的Field 日期：DateTimeField ,整数类型：IntegerField等等
    https://docs.djangoproject.com/en/1.11/ref/models/fields/#field-types
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    # 文章标题
    title = models.CharField(max_length=70)

    # 文章正文,使用TextField
    body = models.TextField()

    # 文章创建时间
    created_time = models.DateTimeField()

    # 文章修改时间
    modified_time = models.DateTimeField()

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True)

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/1.11/topics/db/models/#relationships

    category = models.ForeignKey(Category)
    tags = models.ManyToManyField(Tag,blank=True)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User)

    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @python_2_unicode_compatible
    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    class Meta:
        ordering = ['-created_time']

    def increase_views(self):
        self.views +=1
        self.save(update_fields=['views'])


    def save(self,*args,**kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post,self).save(*args,**kwargs)