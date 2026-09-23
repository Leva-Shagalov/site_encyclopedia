from django import forms
from tinymce.widgets import TinyMCE
from .models import ArticleTopic

class AddArticleForm(forms.Form):
    content = forms.CharField(label="Содержание вашей статьи", widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    # article = forms.ModelChoiceField(Article, verbose_name="К какой статье?", related_name='articlecontents', on_delete=models.CASCADE)
    article = forms.ModelChoiceField(label="К какой статье прикрепить?",queryset=ArticleTopic.objects.exclude(id=1))

    class Meta:
        widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 30})}

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     article = ArticleTopic.objects.exclude(id=1)

    #     choices = [('dhdh', 'Новая статья'), ]
    #     for art in article:
    #         choices.append((art.id, art.name))

    #     self.fields['article'].queryset = article
    #     self.fields['article'].empty_label = ''
