from django.test import TestCase
from django.urls import reverse

from forum.models import Review
from shop.models import Category, Course, Purchase
from users.models import UserProfile


class CustomTestCase(TestCase):
    def setUp(self) -> None:
        self.test_teacher = UserProfile.objects.create_user(username='testteacher',
                                                            password='12345',
                                                            email='test@teacher.com',
                                                            is_teacher=True)
        category = Category.objects.create(name='Test Category')
        self.test_course = Course.objects.create(
            teacher=self.test_teacher,
            category=category,
            description='testcription',
            title='Test Course',
            url='12345',
            price=10
        )
        self.user1 = UserProfile.objects.create_user(username='testuser',
                                                     password='12345',
                                                     email='test@user.com',
                                                     is_teacher=True)


class CommentTest(CustomTestCase):
    def test_if_comment_without_authentication(self):
        """Users cannot create comments without authentication"""
        response = self.client.get( reverse('forum:add-comment', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PERMISSION DENIED')
        self.assertContains(response, 'Sign in')

    def test_if_comment_without_purchase(self):
        """Users cannot comment a course If he hasn't bought it"""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('forum:add-comment', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PERMISSION DENIED')
        self.assertContains(response, 'You need to buy this course to comment it')

    def test_if_comment_with_purchase(self):
        """Right case"""
        self.client.login(username='testuser', password='12345')
        Purchase.objects.create(
            course_bought=self.test_course,
            buyer=self.user1,
        )

        response = self.client.get(reverse('forum:add-comment', kwargs={'pk': self.test_course.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Write down your thoughts')


class ReviewTest(CustomTestCase):
    def test_if_review_without_authentication(self):
        """Users cannot create reviews without authentication"""
        response = self.client.get(reverse('forum:add-review', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PERMISSION DENIED')
        self.assertContains(response, 'Sign in')

    def test_if_review_without_purchase(self):
        """Users cannot leave a review if he hasn't bought the course"""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('forum:add-comment', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PERMISSION DENIED')
        self.assertContains(response, 'You need to buy this course to comment it')

    def test_if_reviewed_twice(self):
        """Users cannot leave two reviews on the same course"""
        Purchase.objects.create(
            course_bought=self.test_course,
            buyer=self.user1,
        )
        Review.objects.create(
            course=self.test_course,
            author=self.user1,
            body="Test Review"
        )
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('forum:add-review', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PERMISSION DENIED')
        self.assertContains(response, "You can&#x27;t review this course twice")

    def test_if_reviewed_while_teacher(self):
        """Teachers can't review their own courses"""
        self.client.login(username='testteacher', password='12345')
        response = self.client.get(reverse('forum:add-review', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PERMISSION DENIED')
        self.assertContains(response, "You can&#x27;t review your own course")

    def test_if_review_correct(self):
        """Right case"""
        Purchase.objects.create(
            course_bought=self.test_course,
            buyer=self.user1,
        )
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('forum:add-review', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add review")
