from . import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        # model.py에서 폼으로 만들길 원하는 클래스를 model에 작성
        model = Comment
        # 작성된 클래스의 필드 중에 content 필드를 사용한다는 의미
        fields = ('content',)