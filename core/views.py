from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ArticleTopic, Article, ArticleContent, Img
from .forms import AddArticleForm

# def load_logged_in_user():
#     user_login = session.get('login')

#     if user_login is None:
#         g.user = None
#     else:
#         # Загружаем пользователя из базы данных один раз перед запросом
#         g.user = Users.get_or_none(login=user_login)

def index(request):
    return render(request, 'core/index.html')


def game_updates_page(request):
    article_updates = Article.objects.filter(topic=1).order_by('id')
    return render(request, 'core/updates_game.html',
                  {"article":article_updates})


def community(request):
    topics = ArticleTopic.objects.exclude(id=1) # exclude исключить из поиска
    articles = Article.objects.exclude(topic=1)
    
    topic = request.GET.get('topic')
    if topic:
        if topic != '1':
            articles = Article.objects.filter(topic=topic)

    return render(request, 'core/community.html',
                  {"articles":articles,
                  "topic":topics})


def page_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if article.topic.id == 1:
        return redirect('/updates')
    
    return render(request, 'core/article.html',
                  {"article":article})


def add_article(request):
    article_form = AddArticleForm()
    topic = ArticleTopic.objects.exclude(id=1)

    
    if request.method == "POST":
        article_form = AddArticleForm(request.POST)

        if article_form.is_valid():
            title = article_form.cleaned_data.get('title')
            content = article_form.cleaned_data.get('content')
            topic = article_form.cleaned_data.get('topic')

            Article.objects.create(title = title, topic = topic)
            foreign_key_article = Article.objects.get(title=title)

            # if g.user:
            ArticleContent.objects.create(content = content, article = foreign_key_article)
            # else:
                # Content_article.create(content = content, user = 0, article = id_article)

            return redirect('/community')

    return render(request, 'core/add_article.html',
                  {"article_form":article_form,
                  "topic":topic})


def edit_article_page(request):
    articles = Article.objects.exclude(topic=1).order_by('id')
    topic = ArticleTopic.objects.exclude(id=1)

    res = [{
        "arti": article.title,
        "cont": [
            content 
            for content in ArticleContent.objects.filter(article=article.id).values().order_by('id')
        ]
        }
        for article in articles
    ]
    print(res)

#     if request.form:
#         form_name = request.form.get("form")
#         if str(form_name) == "article":
        
#             arti_id = request.form.get("arti-id")
#             new_name = request.form.get("name")
#             classification = request.form.get("class")

#             print(new_name)

#             if not all([new_name, arti_id]):
#                 return 'Пропущены поля!'

#             arti = Article.get_or_none(id = arti_id)
#             if not arti:
#                 return "Вы обратились к НЕСУЩЕСТВУЮЩЕЙ статье!"

#             arti.name = new_name

#             if classification:
#                 arti.classification = classification

#             arti.save()

#             return redirect('/community')
        
#         elif str(form_name) == "content":
#             return redirect('/community')
        
#         else:
#             return "Данные отправленны не коррекстно!"
    # import json
    # base=json.dumps(res, ensure_ascii=False)
    # print(base)
    return render(request, 'core/edit_article.html',
                  {"article":articles,
                  "topic":topic,
                  "base":None})



# def get_data(request):
#     articles = Article.select().where(Article.classification != 4).order_by(Article.id).dicts()
#     clas = Class_article.select().where(Class_article.id != 4)

#     res = [{
#         "arti": arti["name"],
#         "cont":[
#             cont for cont in Content_article.select(
#             ).filter(Content_article.article_id==arti["id"]).order_by(Content_article.id).dicts()
#         ]
#         }
#         for arti in articles
#     ]
#     from flask import jsonify
#     return jsonify(res)



# def registration(request):
    
#     if request.method == 'POST':
#         login = request.form.get('login')
#         password = request.form.get('password-1')
#         confirm_password = request.form.get('password-2')

#         if not all([login, password, confirm_password]):
#             return 'Пропущены поля!'
        
#         if password != confirm_password:
#             return 'Пароли не совпадают!'
        
#         if Users.get_or_none(login = login):
#             return 'Такой логин уже есть!'
        
#         Users.create(login = login, password = password)
#         session['is_auth'] = True
#         session['login'] = login

#         return redirect('/')

#     return render('registration.html')


# def authorization(request):
    
#     if request.method == 'POST':
#         login = request.form.get('login')
#         if login == 'Аноним':
#             return 'Невозможно авторизоваться с таким именем'
#         password = request.form.get('password')

#         if not all([login, password]):
#             return 'Пропущены поля!'
        
        
#         if Users.get_or_none(login = login, password = password):
#             session['is_auth'] = True
#             session['login'] = login
#         else:
#             return 'Такого пользователя не существует!'
        
#         return redirect('/')

#     return render('authorization.html')

# # Выход из профиля
# def logout(request):
#     session['is_auth'] = False
#     session['login'] = ''

#     return redirect('/')
