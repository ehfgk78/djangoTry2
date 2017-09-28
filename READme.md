page 1
# ~Django~Try2
수요일, 27. 9월 2017 11:07오전 
by 조교 김기홍

### 1.  프로젝트 폴더 만들기:   djangoTry2 
~~~
# BASE_DIR
home/projects/django/djangoTry2
~~~

### 2. 기존 가상환경 불러오기 
~~~
➜  djangoTry2 pyenv local fc-djangogirls
(fc-djangogirls) ➜  djangoTry2 
~~~

### 3. git
~~~
git init
vi .gitignore
git status
git 
~~~

### 4. requirements.txt

### 5. pycharm 설정
setting interpreter
set djangoTry2 source-root
refatoring `djangoTry2` $rarr; `config`

### 6. startproject
~~~
django-admin startproject djangoTry2 .

├── __init__.py
├── settings.py
├── urls.py
└── wsgi.py
~~~

### 7. setting.py 
~~~
ALLOWED_HOSTS = [
    '*',
]
LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
~~~

### 8. make app 'blog'
~~~
./manage.py startapp blog

├── READme.md
├── blog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── djangoTry2
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   └── settings.cpython-36.pyc
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt

~~~

### models.py
~~~
from django.db import models

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
~~~
* `Ctrl` + 왼쪽 마우스 클릭 on module.함수 &rarr;  함수 내용 출력 in pyCharm

* settings.py
~~~
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # User
    'blog',
]
~~~
* makemigrations 
~~~
$ ./manage.py makemigrations
Migrations for 'blog':
  blog/migrations/0001_initial.py
    - Create model Post

├── blog
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   ├── admin.cpython-36.pyc
│   │   └── models.cpython-36.pyc
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py   !!!  makemigrations
│   │   ├── __init__.py
~~~

* `blog/migrations/0001_initial.py`
~~~
class Migration(migrations.Migration):
    initial = True
    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
~~~

~~~
./manage.py migrate blog     

Operations to perform:
  Apply all migrations: blog
Running migrations:
  Applying blog.0001_initial... OK
~~~
* migrate 취소  & delete `blog/migrations`
~~~
./manage.py migrate blog zero
Operations to perform:
  Unapply all migrations: blog
Running migrations:
  Rendering model states... DONE
  Unapplying blog.0001_initial... OK
~~~
* table 내용 보기 :  sqlbrowser에서도 확인 가능 
~~~
./manage.py showmigrations    
    
admin
 [ ] 0001_initial
 [ ] 0002_logentry_remove_auto_add
auth
 [ ] 0001_initial
 [ ] 0002_alter_permission_name_max_length
 [ ] 0003_alter_user_email_max_length
 [ ] 0004_alter_user_username_opts
 [ ] 0005_alter_user_last_login_null
 [ ] 0006_require_contenttypes_0002
 [ ] 0007_alter_validators_add_error_messages
 [ ] 0008_alter_user_username_max_length
blog
 [ ] 0001_initial
contenttypes
 [ ] 0001_initial
 [ ] 0002_remove_content_type_name
sessions
 [ ] 0001_initial
~~~
* 다시 makemigrations blog  >>  migrate

### runserver
~~~
 $ ./manage.py runserver [port 번호, 9000]
 
 url창 localhost:9000
~~~

### admin 
* createsuperuser  
    - migrations blog,  migrate이 된 이후 : DB화 되어야 log-in가능 
    - 관리자 등록 : 아래  
~~~
./manage.py createsuperuser

Username (leave blank to use 'learn'): learn
Email address: 
Password: 
Password (again): 
Superuser created successfully.
~~~

~~~
from django.contrib import admin
# Register your models here.
from .models import Post

admin.site.register(Post)
~~~
* 포스트에 글 올리기 





