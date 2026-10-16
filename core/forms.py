from django import forms
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE
from .models import ArticleTopic, Article, ArticleContent

class AddArticleForm(forms.Form):
    title = forms.CharField(max_length=255, label="Введите название статьи")
    content = forms.CharField(label="Содержание вашей статьи", widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    topic = forms.ModelChoiceField(label="Какая тема статьи", queryset=ArticleTopic.objects.exclude(id=1))

    class Meta:
        widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 30})}

    def clean_title(self):
        title = self.cleaned_data.get("title")

        same_articles = Article.objects.filter(title=title).exists()
        if same_articles:
            raise ValidationError('Такая статья уже есть! Используйте другое название статьи.')
                
        return title

class AddArticleContentForm(forms.Form):
    content = forms.CharField(label="Содержание вашей статьи", widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 30})}

class EditArticleForm(forms.Form):
    title = forms.CharField(max_length=255, label="Введите название статьи", required=False)
    content = forms.CharField(label="Содержание вашей статьи", widget=TinyMCE(attrs={'cols': 80, 'rows': 30}), required=False)
    topic = forms.ModelChoiceField(label="Какая тема статьи", queryset=ArticleTopic.objects.all(), required=False)
    status = forms.MultipleChoiceField(label='Статус статьи', choices=ArticleContent.StatusArticle.choices, required=False)
    
    class Meta:
        widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 30})}

    def __init__(self, *args, **kwargs):
        self.id = kwargs.pop('content_id', None)
        super().__init__(*args, **kwargs)
    
    def clean_title(self):
        title = self.cleaned_data.get("title")
    
        same_articles = Article.objects.exclude(id=self.id).filter(title=title).exists()
        if same_articles:
            raise ValidationError('Используйте другое название статьи. Нельзя иметь две статьи с одинаковыми названиями')
                    
        return title

    def clean_status(self):
        status = self.cleaned_data.get("status")

        if status == "NC":
            return ""
        return status