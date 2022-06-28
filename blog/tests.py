from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post

# Create your tests here.
# python manage.py test 명령어를 이용하여 현재 파일에서 작성한 내용을 토대로 test 결과를 확인할 수 있다.
class TestView(TestCase):
    # TestCase 내에서 기본적으로 설정되어야 하는 내용이 있으면 setUp() 함수에서 정의를 하면 된다.
    # 현재는 setUp() 함수내에서 Client()를 사용하겠다는 내용만 담는다.
    def setUp(self):
        self.client = Client()

    def test_post_list(self):
        # 포스트 목록 페이지를 가져온다.
        response = self.client.get('/blog/')
        # 정상적으로 페이지가 로드된다.
        self.assertEqual(response.status_code, 200)
        # 페이지 타이틀은 Blog이다.
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog Home - Start Linux')

# pip install beautifulsoup4를 설치하고 TDD에 기반한 방식으로 개발을 진행한다.