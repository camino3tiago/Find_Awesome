from django import forms
from .models import Comment, Article

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = (
            'comment',   # templateで送信される項目（textarea name="comment"）であり、modelsのフィールド名
        )

class PostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            'title', 'text', 'author', 'tags', 'image', 
        )
        labels = {
            'title': 'タイトル',
            'text':'本文', 
            'author': '筆者', 
            'tags': 'タグ', 
            'image': '画像', 
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.base_fields.values():
            field.widget.attrs["class"] = "form-control"
        self.fields['author'].initial = self.user
        