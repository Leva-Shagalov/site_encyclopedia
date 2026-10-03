from django import forms
from django.core.exceptions import ValidationError
from tinymce.widgets import TinyMCE
from .models import ArticleTopic, Article

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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     article = ArticleTopic.objects.exclude(id=1)

    #     choices = [('dhdh', 'Новая статья'), ]
    #     for art in article:
    #         choices.append((art.id, art.name))

    #     self.fields['article'].queryset = article
    #     self.fields['article'].empty_label = ''
