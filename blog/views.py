from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Post, Category, Tag
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify

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
        context['comment_form'] = CommentForm
        return context

class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    # PostCreate는 CreateView를 상속받고 있어서 form_valid()함수의 기능을 확장할 수 있다.
    # CreateView, UpdateView를 상속받으면 _form.html을 사용하도록 기본 설정 되어있다.
    model = Post
    # CreateView에서 필드명을 리스트로 작성해서 fields에 저장을 한다.
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']

    # author 필드를 자동으로 채우기 위해 CreateView에서 제공하는 form_valid()함수
    # CreateView는 form_valid()를 기본적으로 탑재

    # super() 슈퍼클래스의 메소드를 호출한다. 
    # super().form_valid(form)은 슈퍼클래스인 FormView의 메소드 form_valid 를 호출하겠다는 의미이다.

    # form_valid(form) 
    # form_valid() 함수는 유효한 폼 데이터로 처리할 로직 코딩 
    # form_valid는 django.http.HttpResponse를 반환한다. 
    # 유효한 폼데이터가 POST 요청되었을 때 form_valid 메소드가 호출된다. form_valid는 단순히 success_url로의 연결을 수행한다.
    def form_valid(self, form):
        current_user = self.request.user
        # self.request.user는 웹 사이트 방문자를 의미한다.

        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            # is_authenticated는 웹사이트에 방문자가 로그인한 상태인지 아닌지 알 수 있다.
            form.instance.author = current_user
            # current_user = 현재 접속한 방문자를 담는다.

            # 태그와 관련된 작업을 하기 전에 CreateView의 form_valid() 함수의 결과값을 respose라는 변수에 임시로 닫아둔다.
            respose = super(PostCreate, self).form_valid(form)

            # 장고가 자동으로 작성한 post_form.html의 폼을 보면 method="post"로 설정되어 있다.
            # 이 폼 안에 name = 'tag_str'인 input을 추가했으니 방문자가 <submit> 버튼을 클릭했을 때 이 값 역시 POST 방식으로 
            # PostCreate까지 전달되어 있는 상태이다.
            # 이 값은 self.request.POST.get('tag_str')로 받을 수 있다.
            # Post 방식으로 전달된 정보 중 name = 'tags_str'인 input의 값을 가져오라는 뜻이다.
            tag_str = self.request.POST.get('tag_str')

            if tag_str:
                tag_str = tag_str.strip()

                tag_str = tag_str.replace(',', ';')
                tag_list = []
                tag_list = tag_str.split(';')

                for t in tag_list:
                    t = t.strip()
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tag.add(tag)

            return respose
        else:
            # 방문자가 비로그인이라면 돌려보낸다. 
            return redirect('/blog/')

    # UserPassesTestMixin(권한관련)를 추가한 후
    # test_func()함수를 추가해 이 페이지에 접근 가능한 사용자를 최고관리자 또는 스태프로 제한한다.
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

class PostUpdate(LoginRequiredMixin, UpdateView):
    # UpdateView, CreateView를 상속받으면 _form.html을 사용하도록 기본 설정 되어있다.
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tag']

    template_name = 'blog/post_update_form.html'

    # dispatch 메소드는 요청자가 웹 사이트 서버에 GET방식으로 또는 POST방식으로 했는지 판단하는 기능을 갖는다.
    # CreateView나 UpdateView의 경우 방문자가 서버에 GET방식으로 들어오면 포스트를 작성할 수 있는 폼 페이지를 보내준다.
    # 반면 같은 경로로 POST 방식으로 들어오는 경우에는 폼의 유효성을 확인 후 문제가 없다면 데이터 베이스에 내용을 저장하도록 되어있다.
    def dispatch(self, request, *args, **kwargs):
        # request.user(방문자)
        # self.get_object().author는 UpdateView의 기본 메소드로 Post.objects.get(pk=pk)와 동일한 역할을 한다.
        # 가져온 Post 인스턴스의 author 필드가 방문자와 동일한 경우에만 dispatch()의 if참 값으로 간다.
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else: 
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()

        if self.object.tag.exists():
            tag_str_list = []
            for t in self.object.tag.all():
                tag_str_list.append(t.name)
            context['tag_str_default'] = '; '.join(tag_str_list)

        return context

    # form_valid(form) 
    # form_valid() 함수는 유효한 폼 데이터로 처리할 로직 코딩 
    # form_valid는 django.http.HttpResponse를 반환한다. 
    # 유효한 폼데이터가 POST 요청되었을 때 form_valid 메소드가 호출된다. form_valid는 단순히 success_url로의 연결을 수행한다.
    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tag.clear()

        # 장고가 자동으로 작성한 post_form.html의 폼을 보면 method="post"로 설정되어 있다.
        # 이 폼 안에 name = 'tag_str'인 input을 추가했으니 방문자가 <submit> 버튼을 클릭했을 때 이 값 역시 POST 방식으로 
        # PostCreate까지 전달되어 있는 상태이다.
        # 이 값은 self.request.POST.get('tag_str')로 받을 수 있다.
        # Post 방식으로 전달된 정보 중 name = 'tags_str'인 input의 값을 가져오라는 뜻이다.
        tag_str = self.request.POST.get('tag_str')

        if tag_str:
            tag_str = tag_str.strip()

            tag_str = tag_str.replace(',', ';')
            tag_list = []
            tag_list = tag_str.split(';')

            for t in tag_list:
                t = t.strip()
                tag, is_tag_created = Tag.objects.get_or_create(name=t)
                if is_tag_created:
                    tag.slug = slugify(t, allow_unicode=True)
                    tag.save()
                self.object.tag.add(tag)

        return response

def new_comment(request, pk):
    if request.user.is_authenticated:
        # Post.object.get(pk=pk)로 불러올 수 도 있지만 해당하는 pk가 없는 경우에는 404오류를 발생시키도록 하기 위해 장고가 제공하는
        # get_object_or_404란느 기능을 활용한다.
        post = get_object_or_404(Post, pk = pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
            else:
                return redirect(post.get_absolute_url())
        else:
            raise PermissionDenied