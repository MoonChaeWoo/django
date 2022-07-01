from django.shortcuts import render
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView

# Create your views here.

# CBV 방식 (read_list)
class PostList(ListView):
    model = Post
    # ListView는 DB모델명 뒤에 _list.html파일을 기본 템플릿으로 사용하도록 설정되어있다.
    # 즉 Post모델에서 ListView모델을 상속받으면 post_list.html이 필요하다.

    # 첫번째 방법 template_name에서 직접 html을 지정할 수 있다.
    # 두번째 방법 post_list.html을 만들도록 한다.
    template_name = 'blog/index.html'
    # FBV 방식에서는 Post.objects.all()방식으로 가져와서 posts 딕셔너리로 보내주어야 했지만
    # ListView를 상속받았기에 모델 객체는 자동으로 post_list라는 이름으로 html로 넘어간다.

    # -pk를 함으로써 최신 글부터 나올 수 있도록 설정
    ordering = '-pk'

    # ListView나 DetailView와 같은 클래스는 기본적으로 get_context_data메서드를 내장하고 있다.
    # ListView를 상속받은 PostList에서 단지 model = Post라고 선언하면 get_context_data에서 자동으로 post_list = Post.objects.all()을 명령한다.
    # 즉 html에서 {% for post in post_list %}를 사용할 수 있는 이유가 이거에 있다는 것이다.
    def get_context_data(self, **kwargs):
        # get_context_data에서 기존에 제공했던 기능을 그대로 가져와 context에 저장한다.
        # 다음 원하는 쿼리셋을 만들어 딕셔너리 형태로 context에 담으면 된다.
        context = super(PostList, self).get_context_data()
        # Category.objects.all()을 가져와 categories라는 이름의 키에 담는다. 
        # 즉 html에서 {% for category in categories %} 이처럼 사용할 수 있게된다는 의미이다.
        context['categories'] = Category.objects.all()
        # 카테고리가 정해지지 않은 값을 html에서 불러온다는 의미이다. 사용은 {{ no_category_post_count }} 이렇게 사용이 가능하다.
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context

def category_page(request, slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(request, 'blog\index.html', {
        'post_list' : post_list,
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count(),
        'category' : category,
    })

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    # _set.all() 외래키로 된 필드는 _set으로 되어 있다.
    # tag_set.all()을 하게되면 외래키로 연결된 테이블의 값을 출력하게 되어있다.
    post_list = tag.post_set.all()

    return render(request, 'blog/index.html', {
        'post_list' : post_list,
        'tag' : tag,
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count()
    })

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

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context