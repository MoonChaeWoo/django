from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

# 업데이트 시간에 대한 필드 선언과 인자값으로 auto_now=True를 넣어준다.
# 다시 저장할때 마다 그 시각이 저장되도록 한다.
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

# __str__은 관리자 페이지에서 제목과 유일키를 보여주는 기능을 함
# self.pk는 유일키 self.title은 제목을 보여준다.
    def __str__(self):
        return f'[{self.pk}번 {self.title}]'
