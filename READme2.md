page 2
# ~Django~Try2

### 장고 shell 설
* 기본 쉘 내장 
* `shell_plus` 쓸 것임 
    - 기존 가상환경에 설치되지 않은 경우: 아래 &darr;
    - django-extensions 에 관한 자세한 설명: 
    [http://django-extensions.readthedocs.io](http://django-extensions.readthedocs.io) 
~~~
# 아래 
pip install django-extensions
~~~
* settings.py 
~~~
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party apps
    'django_extensions',
    # User
    'blog',
]
~~~

### 장고 veiw.py
~~~
from django.shortcuts import render

# Create your views here.
def post_list(request):
    return HttpResponse("Post List")
~~~


* url.py
~~~
from blog.views import post_list

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_list)
]
~~~


* settings.py
~~~
ROOT_URLCONF = 'config.urls'
~~~

* mkdir djangoTry2/templates/post_list.html
~~~
djangoTry2   
   ├── blog
   ├── config
   ├── db.sqlite3
   ├── manage.py
   └── templates
              └── post_list.html
~~~
* post_list.html
~~~
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
<h1>Post List</h1>

</body>
</html>
~~~

* rendering in vews.py
~~~
def post_list(request):
    # return HttpResponse("Post List")
    return render(request, 'post_list.html')
~~~

* set TEMPLATE_DIR in settings.py
~~~
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
          TEMPLATE_DIR,
        ],
~~~

* Post model과 post_list.html 연결 by views.py
~~~
from blog.models import Post 

def post_list(request):
    posts = Post.objects.all()
    context = {
        "post_list" : posts
    }
    # return HttpResponse("Post List")
    return render(request, 'post_list.html', context)
~~~

* post_list.html
~~~
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
<h1>Post List</h1>
{% for post in post_list %}
<p>{{ post.title }}</p>
<p>{{ post.content}}</p>
<p>{{post.created_date}}</p>
<p>{{post.published_date}}</p>
{% endfor %}
</body>
</html>
~~~

* Post의 title 보기 : magic method `__str__` in admin-site
~~~
class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
~~~

* published 만 올리기 + 현재 이전 것만 올리기 
~~~
from django.utils import timezone
from blog.models import Post

def post_list(request):
    # posts = Post.objects.all()
    # published 만 게시
    posts = Post.objects.filter(published_date__isnull=False).filter(published_date__lte=timezone.now())
    data = {
        "post_list": posts,
    }
    # return HttpResponse("Post List")
    return render(request, 'post_list.html', context=data)

~~~

### post_detail
* veiws.py
~~~
def post_detail(request, detail_pk):
    # post = Post.objects.filter(pk=detail_pk)[0]
    post = Post.objects.get(pk=detail_pk)
    data = {
        'post': post
    }
    return render(request, 'post_detail.html', context=data)

~~~

* urls.py
~~~
from blog.views import post_list, post_detail

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_list),
    url(r'^post/(?P<detail_pk>\d+)', post_detail),
]
~~~

* post_detail.html
~~~
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>

<h2>{{ post.title }}</h2>
<p>{{ post.title }}</p>

</body>
</html>
~~~

### ~연결하기~  post_list.html vs post_detail.html 
* urls.py
    - URL창에 입력하는 숫자 &rarr; `detail_pk`에 할당함 &darr;
    - template `{% url 'post_detail` %}을 예상하고 `name='post_detail'` 할당  &darr;
~~~
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', post_list),
    url(r'^post/(?P<detail_pk>\d+)', post_detail, name='post_detail'),
~~~

* views.py
    - filter(pk=#)에서 pk는 filter의 속성 
~~~
def post_detail(request, detail_pk):
    # post = Post.objects.filter(pk=detail_pk)[0]
    post = Post.objects.get(pk=detail_pk)
    data = {
        'post': post
    }
    return render(request, 'post_detail.html', context=data)
~~~

* post_list.html
    - `detail_pk`는 urls.py에서 정의되고 URL창에서 받아온 숫자를 할당받음
    - `post.pk`는  views.post_list에서 Post 객체에 부여된 pk 
~~~
<body>
<h1>Post List</h1>
{% for post in post_list %}
<p><a href="{% url 'post_detail' detail_pk=post.pk %}">{{ post.title }}</a></p>
<p>{{ post.content}}</p>
<p>{{post.created_date}}</p>
<p>{{post.published_date}}</p>
{% endfor %}
</body>
~~~

### ~템플릿 확장~ base.html 
* templates/base.html 작성
~~~
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
<h1><a href="{% url 'post_list' %}">Post List</a></h1>

{% block content %}
{% endblock %}

</body>
</html>
~~~

* post_list.html 수정하고 base.html로 확장시키기 
    - a태그의 `href="#"`의 값 &rarr; Server &rarr; urls.py 의 `detail_pk`
    - 따라서 `post.pk` 를 'detail_pk`에 할당해야 함  
~~~
{% extends 'base.html' %}

{% block content %}

{% for post in post_list %}
<p><a href="{% url 'post_detail' detail_pk=post.pk %}">{{ post.title }}</a></p>
<p>{{ post.content}}</p>
<p>{{post.created_date}}</p>
<p>{{post.published_date}}</p>
{% endfor %}

{% endblock %}
~~~

* post_detail.html 수정하고, base.html로 확장시키기
~~~
{% extends 'base.html' %}

{% block content %}
<h2>{{ post.title }}</h2>
<p>{{ post.content }}</p>
{% endblock %}
~~~

### CSS, javaScript ~static~
* Bootstrap
* jQuery
* static 폴더의 구성 
~~~
.
├── blog
├── config
├── db.sqlite3
├── manage.py
├── static
│   ├── Bootstrap
│   ├── css
│   ├── jQuery
│   └── javascript
└── templates
    ├── base.html
    ├── post_detail.html
    └── post_list.html
~~~
* path 설정  in settings.py 
    - static의 url은 ~~urls.py가 아니라~~ settings.py에서 설정함 
~~~
# path 연결 
STATIC_DIR = os.path.join(BASE_DIR, 'static')
# Django 가 path 인식 
STATICFILES_DIRS = [
    STATIC_DIR,
]
# static URL 확인 
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
~~~

* base.html (Template)에 연결 
~~~
{% load static %}
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">

    <!--정적파일을 참조하는 템플릿 static태그 (STATICFILES_DIRS의 path를 기준으로 상대경로)-->
	<link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.css' %}">
	<link rel="stylesheet" href="{% static 'css/blog.css' %}">
	<link rel="stylesheet" href="/static/css/blog.css">

    <title>Document</title>
</head>
<body>
<h1><a href="{% url 'post_list' %}">Post List</a></h1>

{% block content %}
{% endblock %}

</body>
</html>
~~~







