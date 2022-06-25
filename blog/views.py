from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView

# Create your views here.

# CBV 방식 (read_list)
class PostList(ListView):
    model = Post
    # ListView는 모델명 뒤에 _list.html파일을 기본 템플릿으로 사용하도록 설정되어있다.
    # 즉 Post모델에서 ListView모델을 상속받으면 post_list.html이 필요하다.

    # 첫번째 방법 template_name에서 직접 html을 지정할 수 있다.
    # 두번째 방법 post_list.html을 만들도록 한다.
    template_name = 'blog/index.html'
    # FBV 방식에서는 Post.objects.all()방식으로 가져와서 posts 딕셔너리로 보내주어야 했지만
    # ListView를 상속받았기에 모델 객체는 자동으로 post_list라는 이름으로 html로 넘어간다.

    # -pk를 함으로써 최신 글부터 나올 수 있도록 설정
    ordering = '-pk'


# FBV 방식 (read_list)
# def index(request):
#     # db를 가져오고 오름차순으로 보일 수 있도록 함
#     posts = Post.objects.all().order_by('-pk')
#     return render(request, 'blog\index.html', {'posts' : posts})

#----------------------------------------------------------------------------------------

# CBV방식 (read)
# ListView가 레코드 목록 형태로 보여준다면 DetailView는 한 레코드를 자세히 보여줄 때 사용한다.
class PostDetail(DetailView):
    model = Post
    # DetailView를 상속받으면 _detail.html을 사용하도록 되어있다.
    # 즉 Post모델에서 DetailView모델을 상속받으면 post_detail.html이 필요하다.

    # 첫번째 방법 template_name에서 직접 html을 지정할 수 있다.
    # ex) template_name = 'blog/single_post_page.html'
    # 두번째 방법 post_detail.html을 만들도록 한다.

# FBV 방식 (read)
# def single_popst_pages(request, pk):
#     post = Post.objects.get(pk=pk)
#     return render(request, 'blog\single_post_page.html', {'post' : post})