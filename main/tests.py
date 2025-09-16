from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from goods.models import Product
from main.models import Info, News, Review

User = get_user_model()


class InfoModelTest(TestCase):
    def setUp(self):
        self.info = Info.objects.create(
            name="О компании",
            description="Информация о компании",
            slug="about"
        )

    def test_info_creation(self):
        """Тест создания объекта Info"""
        self.assertTrue(isinstance(self.info, Info))
        self.assertEqual(str(self.info), "О компании")

    def test_info_unique_name(self):
        """Тест уникальности названия"""
        with self.assertRaises(Exception):
            Info.objects.create(
                name="О компании",  # Такое имя уже существует
                description="Другая информация",
                slug="about-new"
            )

    def test_info_slug_unique(self):
        """Тест уникальности slug"""
        with self.assertRaises(Exception):
            Info.objects.create(
                name="Новая информация",
                description="Описание",
                slug="about"  # Такой slug уже существует
            )


class NewsModelTest(TestCase):
    def setUp(self):
        self.news = News.objects.create(
            name="Новость 1",
            description="Описание новости",
            image="news/test.jpg"
        )

    def test_news_creation(self):
        """Тест создания объекта News"""
        self.assertTrue(isinstance(self.news, News))
        self.assertEqual(str(self.news), "Новость 1")

    def test_news_ordering(self):
        """Тест порядка сортировки новостей"""
        news2 = News.objects.create(
            name="Новость 2",
            description="Описание новости 2",
            image="news/test2.jpg"
        )

        all_news = News.objects.all()
        # Последняя созданная новость должна быть первой (сортировка по -id)
        self.assertEqual(all_news.first().name, "Новость 2")


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        self.review = Review.objects.create(
            user=self.user,
            text="Отличный товар!",
            rating=5,
            status="Модерация"
        )

    def test_review_creation(self):
        """Тест создания объекта Review"""
        self.assertTrue(isinstance(self.review, Review))
        self.assertEqual(str(self.review), f"{self.user} | {self.review.rating}")

    def test_review_default_status(self):
        """Тест значения по умолчанию для статуса"""
        self.assertEqual(self.review.status, "Модерация")

    def test_review_status_choices(self):
        """Тест допустимых значений статуса"""
        self.review.status = "Опубликован"
        self.review.save()
        self.assertEqual(self.review.status, "Опубликован")



class IndexViewTest(TestCase):

    def test_index_view_status_code(self):
        """Тест статуса ответа главной страницы"""
        response = self.client.get(reverse('main:home'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        """Тест использования правильного шаблона"""
        response = self.client.get(reverse('main:home'))
        self.assertTemplateUsed(response, 'main/index.html')




class NewsViewTest(TestCase):
    def setUp(self):
        # Создаем тестовые новости
        for i in range(3):
            News.objects.create(
                name=f"Новость {i}",
                description=f"Описание новости {i}",
                image="news/test.jpg"
            )

    def test_news_view_status_code(self):
        """Тест статуса ответа страницы новостей"""
        response = self.client.get(reverse('main:news'))
        self.assertEqual(response.status_code, 200)

    def test_news_view_template(self):
        """Тест использования правильного шаблона"""
        response = self.client.get(reverse('main:news'))
        self.assertTemplateUsed(response, 'main/news.html')

    def test_news_view_context(self):
        """Тест наличия контекста с новостями"""
        response = self.client.get(reverse('main:news'))
        self.assertIn('news', response.context)


class InfoDetailViewTest(TestCase):
    def setUp(self):
        self.info = Info.objects.create(
            name="Контакты",
            description="Наши контакты",
            slug="contacts"
        )

    def test_info_detail_view_status_code(self):
        """Тест статуса ответа страницы информации"""
        response = self.client.get(reverse('main:info', kwargs={'info_slug': 'contacts'}))
        self.assertEqual(response.status_code, 200)

    def test_info_detail_view_template(self):
        """Тест использования правильного шаблона"""
        response = self.client.get(reverse('main:info', kwargs={'info_slug': 'contacts'}))
        self.assertTemplateUsed(response, 'main/info.html')

    def test_info_detail_view_context(self):
        """Тест наличия контекста с информацией"""
        response = self.client.get(reverse('main:info', kwargs={'info_slug': 'contacts'}))
        self.assertIn('info', response.context)
        self.assertEqual(response.context['info'], self.info)


class ReviewViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        # Создаем опубликованные отзывы
        for i in range(2):
            Review.objects.create(
                user=self.user,
                text=f"Отзыв {i}",
                rating=5,
                status="Опубликован"
            )
        # Создаем отзыв в модерации
        Review.objects.create(
            user=self.user,
            text="Отзыв в модерации",
            rating=3,
            status="Модерация"
        )

    def test_review_view_status_code(self):
        """Тест статуса ответа страницы отзывов"""
        response = self.client.get(reverse('main:review'))
        self.assertEqual(response.status_code, 200)

    def test_review_view_template(self):
        """Тест использования правильного шаблона"""
        response = self.client.get(reverse('main:review'))
        self.assertTemplateUsed(response, 'main/review.html')

    def test_review_view_context(self):
        """Тест наличия контекста с опубликованными отзывами"""
        response = self.client.get(reverse('main:review'))
        self.assertIn('review_pub_all', response.context)
        # Проверяем, что отображаются только опубликованные отзывы
        published_reviews = response.context['review_pub_all']
        for review in published_reviews:
            self.assertEqual(review.status, "Опубликован")

    def test_review_post_authorized(self):
        """Тест отправки отзыва авторизованным пользователем"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post(reverse('main:review'), {
            'rating': 4,
            'text': 'Хороший сервис!'
        }, follow=True)

        # Проверяем редирект
        self.assertEqual(response.status_code, 200)

        # Проверяем, что отзыв был создан
        reviews = Review.objects.filter(user=self.user, text='Хороший сервис!', rating=4)
        self.assertTrue(reviews.exists())

        # Проверяем наличие сообщения об успехе
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Ваш отзыв будет опубликован после модерации!")
