from django import forms
from .models import Comment


class CommentForm(forms.Form):
    author = forms.CharField(label="Nome do autor", max_length=100)
    title = forms.CharField(label="Título", required=False)
    comment = forms.CharField(label="Comentário",
        widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        self.reference_news_id = kwargs.pop('news_id')
        super(CommentForm, self).__init__(*args, **kwargs)

    def save(self):
        data = self.cleaned_data
        instance = Comment.objects.create(
            reference_news_id=self.reference_news_id,
            author=data['author'],
            title=data.get('title') or "(Sem título)",
            comment=data['comment'])
        return instance

    def clean_comment(self):
        if len(self.cleaned_data['comment']) < 2:
            raise forms.ValidationError(
                "O Comentário deve ter no mínimo dois caracteres")
        return self.cleaned_data["comment"]

