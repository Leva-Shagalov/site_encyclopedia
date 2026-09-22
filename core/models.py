from django.db import models
from tinymce.models import HTMLField

class ArticleTopic(models.Model):
    name = models.CharField(max_length=255, verbose_name="название")

    def __str__(self):
            return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="загаловок")
    topic = models.ForeignKey(ArticleTopic, verbose_name="категория", related_name='articles', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    def __str__(self):
                return self.title

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статья"

class Comments(models.Model):
    text = models.TextField()
    # user = models.ForeignKey(Users, verbose_name="создатель статьи", related_name='articleContents', on_delete=0)
    article = models.ForeignKey(Article, verbose_name="К какой статье?", related_name='comments', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    def __str__(self):
                return self.text

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

class ArticleContent(models.Model):
    content = HTMLField()
    # user = models.ForeignKey(Users, verbose_name="создатель статьи", related_name='articleContents', on_delete=0)
    article = models.ForeignKey(Article, verbose_name="К какой статье?", related_name='articlecontents', on_delete=models.CASCADE)
    date = models.DateField(auto_now=True, verbose_name="дата написание содержания статьи")

    def __str__(self):
                return self.content

    class Meta:
        verbose_name = "Контент статьи"
        verbose_name_plural = "Контент статей"

class Img(models.Model):
    name = models.FileField()
    alt = models.CharField(max_length=255, verbose_name="если картинка не отображается выводит этот текст", blank=True, null=True)
    article_content = models.ForeignKey(ArticleContent, verbose_name="К какой статье?", related_name='imgs', on_delete=models.CASCADE)

    def __str__(self):
                return str(self.name)

    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"
