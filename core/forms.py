from django import forms
from tinymce.widgets import TinyMCE

class FlatPageForm(forms.ModelForm):
    content = forms.CharField(widget={'content': TinyMCE(attrs={'cols': 80, 'rows': 30}, content_language="ru")})
    # article = forms.ModelChoiceField(Article, verbose_name="К какой статье?", related_name='articlecontents', on_delete=models.CASCADE)
    

    class Meta:
        widgets = {'content': TinyMCE(attrs={'cols': 80, 'rows': 30}, content_language="ru")}