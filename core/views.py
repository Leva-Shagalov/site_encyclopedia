from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import ArticleTopic, Article, ArticleContent, Img
from .forms import AddArticleForm, AddArticleContentForm, EditArticleForm
from django.core.exceptions import ValidationError


def index(request):
    return render(request, 'core/index.html')


def game_updates_page(request):
    article_updates = Article.objects.filter(topic=1)
    return render(request, 'core/updates_game.html',
                  {"article":article_updates})


def community(request):
    topics = ArticleTopic.objects.exclude(id=1) # exclude исключить из поиска
    articles = Article.objects.exclude(topic=1)
    
    topic = request.GET.get('topic')
    text = request.GET.get('text')
    
    if topic:
        articles = articles.filter(topic=topic)
    if text:
        articles = articles.filter(title__icontains=text.lower())

    return render(request, 'core/community.html',
                  {"articles":articles,
                  "topic":topics})


def page_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if article.topic.id == 1:
        return redirect('/updates')
    content = ArticleContent.objects.filter(article=article).exclude(status="NC").order_by('-version')

    try:
        return render(request, 'core/article.html',
                            {"article":article,
                            "content":content[0],
                            "history":content[1:],
                             })
    except IndexError:
        return HttpResponse("Извините, но у этой статьи нет провереного контента для просмотра.")


def add_article(request):
    article_form = AddArticleForm()

    if request.method == "POST":
        article_form = AddArticleForm(request.POST)

        if article_form.is_valid():
            title = article_form.cleaned_data.get('title')
            content = article_form.cleaned_data.get('content')
            topic = article_form.cleaned_data.get('topic')

            Article.objects.create(title = title, topic = topic)
            foreign_key_article = Article.objects.get(title=title)
            
            article_content = ArticleContent.objects.create(content = content, article = foreign_key_article)

            if request.user.is_authenticated:
                article_content.author = request.user.profile
                if request.user.is_staff:
                    article_content.status = ArticleContent.StatusArticle.CREATE_ADMIN
                else:
                    article_content.status = ArticleContent.StatusArticle.AUTHOR_USER
                article_content.save()

            article_content_version = ArticleContent.objects.filter(article=foreign_key_article).order_by('-version')[0]
            article_content.version = article_content_version + 1
            article_content.save()

            return redirect('/community')

    return render(request, 'core/add_article.html',
                  {"article_form":article_form})

def add_article_content(request, article_id):
    article_form = AddArticleContentForm()
    
    if request.method == "POST":
        article_form = AddArticleContentForm(request.POST)

        if article_form.is_valid():
            content = article_form.cleaned_data.get('content')

            foreign_key_article = Article.objects.get(id=article_id)
            
            article_content = ArticleContent.objects.create(content = content, article = foreign_key_article)

            if request.user.is_authenticated:
                article_content.author = request.user.profile
                article_content.save()

            article_content_version = ArticleContent.objects.filter(article=foreign_key_article).order_by('-version')[0]
            article_content.version = article_content_version.version + 1
            article_content.save()

            return redirect(f'/article/{article_id}')

    return render(request, 'core/add_article.html',
                            {"article_form":article_form})



def reserch_article_not_checked(request, article_id):
    if article_id == 0:
        article_content = ArticleContent.objects.filter(status="NC")
        articles = []

        for article in article_content:
            if article.article not in articles:
                articles.append(article.article)

        return render(request, 'core/reserch_article_not_checked.html',
                                {"articles": articles,
                                 "flag": False})

    else:
        article_content = ArticleContent.objects.filter(article=article_id, status="NC")
        article = Article.objects.get(id=article_id)

        return render(request, 'core/reserch_article_not_checked.html',
                                {"articles": article_content,
                                 "article": article,
                                 "flag": True})

def edit_article(request, content_id):
    if not request.user.is_staff:
        return redirect('/')
    article_edit_form = EditArticleForm()

    if request.method == "POST":
            article_edit_form = EditArticleForm(request.POST, content_id=content_id)
    
            if article_edit_form.is_valid():
                title = article_edit_form.cleaned_data.get('title')
                content = article_edit_form.cleaned_data.get('content')
                topic = article_edit_form.cleaned_data.get('topic')
                status = article_edit_form.cleaned_data.get('status')

                print(f"DEBUG: title={repr(title)}, content={repr(content)}, topic={repr(topic)}, status={repr(status)}")
                print(f"DEBUG: bool(title)={bool(title)}, bool(content)={bool(content)}, bool(topic)={bool(topic)}, bool(status)={bool(status)}")

                if not any([title, content, topic, status]):
                    ArticleContent.objects.get(id=content_id).delete()
                elif not all([title, content, topic, status]):
                    raise ValidationError('Либо должны быть все поля для измения статьи, либо отсутвовать все поля для удаления.')
                
                else:
                    content = ArticleContent.objects.get(id=content_id)

                    content.article.title = title
                    content.content = f"{content}"
                    content.article.topic = topic
                    content.status = ArticleContent.StatusArticle(status[0])
                    content.save()
    
                return redirect('/reserch_article_not_checked/0')
   
    return render(request, 'core/edit_article.html',
                  {"edit_form":article_edit_form})


def get_data_form(request, content_id):
    content = ArticleContent.objects.get(id=content_id)
    data = {
            "title": content.article.title,
            "content": content.content,
            "topic": content.article.topic.id,
            "status": content.status
        }
    return JsonResponse(data)