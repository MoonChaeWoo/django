from django.db import models
from django.contrib.auth.models import User
import os

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/tag/{self.slug}'

# Create your models here.
# Category클래스를 제일 상단에 작성해야 Post에 ForeignKey(인자)로 들어갈 수 있다.
class Category(models.Model):
    # unique=True를 사용하면 동알한 name을 갖는 카테고리를 또 만들 수 없다.
    name = models.CharField(max_length=50, unique=True)
    # SlugField는 사람이 읽을 수 있는 텍스트로 고유 URL을 만들고 싶을 때 주로 사용한다.
    # Category 모델도 POST 모델처럼 pk를 활용해 URL을 만들 수 있지만, 카테고리는 포트스 만틈 개수가 많이 않으므로
    # 사람이 읽고 그 뜻을 알 수 있게 고유 URL을 사용한다. ex) URL이 /1/ 보다 /blog/ 가 좋다)
    # SlugField는 기본적으로 한글을 지원하지 않아 allow_unicode=True를 설정해 한글로도 만들 수 있게 한다.
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    # 모델의 메타 설정에서 verbose_name_plural을 추가해 복수혐임을 직접 입력가능하다.
    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
# 요약문을 나타내는 필드를 생성 글자수는 최대 100자 nullable
    hook_text = models.CharField(max_length=100, blank=True)

# 이미지 업로드 (pip intall Pillow)
# 업로드한 이미지를 년, 월, 일 별로 폴더를 나누어서 저장이 되도록 하는게 한곳에 모아서 저장하는거 보다 훨씬 성능개선에 좋다.
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)

# 파일 업로드
# FileField를 이용하여 다른 종류의 파일도 업로드 할 수 있도록 한다.
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d', blank=True)

# 업데이트 시간에 대한 필드 선언과 인자값으로 auto_now=True를 넣어준다.
# 다시 저장할때 마다 그 시각이 저장되도록 한다.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# django에서 기본적으로 제공하는 모델인 User 모델을 사용하여 저자 필드를 생성한다.
    #author = models.ForeignKey(User, on_delete=models.CASCADE) # CASECADE는 author과 관련된 데이터들을 연쇄적으로 삭제한다는 의미이다.
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # CASECADE를 SET_NULL로 수정하면 작성자가 데이터베이스에서 삭제되었을 때
                                                                           # 작성자명을 빈 칸으로 둔다는 의미이다. 
    #null=True는 default로 null일 수 없기 때문에 명시적으로 해주지 않으면 오류가 생긴다.

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # 연결된 태그가 삭제되면 해당 포스트의 tags필드는 알아서 빈칸으로 바뀐다.
    # null=True는 기본적으로 default이기 때문에 작성해주면 경고메세지가 뜬다.
    tag = models.ManyToManyField(Tag, blank=True)

# __str__은 관리자 페이지에서 제목과 유일키를 보여주는 기능을 함
# self.pk는 유일키 self.title은 제목을 보여준다.
    def __str__(self):
        return f'[{self.pk}번 {self.title}] by {self.author}'

# get_absolute_url을 정의하고 html에서 a href="{{ p.get_absolute_url }}"게 설정하여 url을 사용할 수 있다.
    def get_absolute_url(self):
        return f'/blog/{self.pk}'

# 파일의 경로를 제외하고 파일명을 나오게 하는 기능 (파이썬 os모듈을 이용한다.)
    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

# 파일의 확장자가 나오도록 하는 기능
    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]

# null=True와 blank=True의 차이점 (null과 blank는 모두 디폴트 값이 false)
# null=True 는 필드의 값이 NULL(정보 없음)로 저장되는 것을 허용한다. 결국 데이터베이스 열에 관한 설정이다.
# blank=True 는 필드가 폼(입력 양식)에서 빈 채로 저장되는 것을 허용한다. 장고 관리자(admin) 및 직접 정의한 폼에도 반영된다.