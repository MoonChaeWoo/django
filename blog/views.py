from django.shortcuts import render
from .models import Post

# Create your views here.
def index(request):
    # db를 가져오고 오름차순으로 보일 수 있도록 함
    posts = Post.objects.all().order_by('-pk')
    return render(request, 'blog\index.html', {'posts' : posts})

def single_popst_pages(request, pk):
    post = Post.objects.get(pk=pk)

    return render(request, 'blog\single_post_page.html', {'post' : post})