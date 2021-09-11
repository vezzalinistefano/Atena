from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from shop.forms import CourseUploadForm
from shop.models import Course, Category, Purchase, Review
from users.models import UserProfile


class CourseTests(TestCase):
    def test_course_creation_without_login(self):
        """Courses cannot be created by unauthenticated users"""
        response = self.client.get(reverse('shop:course-create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PERMISSION DENIED')

    def test_course_creation_if_not_teacher(self):
        """Courses cannot be created by users that aren't teacher"""
        self.user = UserProfile.objects.create_user(username='testuser', password='12345', is_teacher=False)
        self.client.login(username='testuser', password='12345')

        test_video = SimpleUploadedFile('file.mp4', b'file_content', content_type='video/mp4')
        form_data = {
            'title': 'test video',
            'price': 10,
            'description': 'tescription',
            'category': 'Sport',
            'video': test_video
        }
        form = CourseUploadForm(data=form_data)
        response = self.client.post(reverse('shop:course-create'), form.data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PERMISSION DENIED')
        self.assertContains(response, 'Seems like you are not a teacher')

    def test_course_creation_no_video_file(self):
        """
        Courses cannot be created if the user is trying to upload
        a file that is not a video/mp4 file
        """
        self.user = UserProfile.objects.create_user(username='testuser', password='12345', is_teacher=True)
        self.client.login(username='testuser', password='12345')

        content_type = 'text/plain'
        test_video = SimpleUploadedFile('file.txt', b'file_content', content_type=content_type)

        form_data = {
            'title': 'test video',
            'price': 10,
            'description': 'description test description',
            'category': 'Sport',
            'video': test_video,
        }
        form = CourseUploadForm(data=form_data)
        response = self.client.post(reverse('shop:course-create'), form.data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Files of type {content_type} are not valid, please upload an mp4.")

    def test_course_creation_invalid_category(self):
        """
        Courses cannot be created if the user is trying to upload
        a course of an invalid category
        """
        self.user = UserProfile.objects.create_user(username='testuser', password='12345', is_teacher=True)
        self.client.login(username='testuser', password='12345')

        content_type = 'video/mp4'
        test_video = SimpleUploadedFile('file.mp4', b'file_content', content_type=content_type)
        invalid_choice = 'Invalid'
        form_data = {
            'title': 'test video',
            'price': 10,
            'description': 'description test description',
            'category': 'Invalid',
            'video': test_video,
        }
        form = CourseUploadForm(data=form_data)
        response = self.client.post(reverse('shop:course-create'), form.data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f"Select a valid choice. {invalid_choice} is not one of the available choices.")

    def test_course_creation_invalid_price(self):
        """
        Courses cannot be created if the price is a negative number or a text field
        """
        self.user = UserProfile.objects.create_user(username='testuser', password='12345', is_teacher=True)
        self.client.login(username='testuser', password='12345')

        content_type = 'video/mp4'
        test_video = SimpleUploadedFile('file.mp4', b'file_content', content_type=content_type)
        form_data = {
            'title': 'test video',
            'price': -10,
            'description': 'description test description',
            'category': 'Sport',
            'video': test_video,
        }
        form = CourseUploadForm(data=form_data)
        response = self.client.post(reverse('shop:course-create'), form.data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ensure this value is greater than or equal to 0.1.")

        form_data['price'] = 'invalid price'
        form = CourseUploadForm(data=form_data)
        response = self.client.post(reverse('shop:course-create'), form.data)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Enter a number.')


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
        response = self.client.get(reverse('shop:add-comment', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PERMISSION DENIED')
        self.assertContains(response, 'Sign in')

    def test_if_comment_without_purchase(self):
        """Users cannot comment a course If he hasn't bought it"""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('shop:add-comment', kwargs={'pk': self.test_course.pk}))

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

        response = self.client.get(reverse('shop:add-comment', kwargs={'pk': self.test_course.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Write down your thoughts')


class ReviewTest(CustomTestCase):
    def test_if_review_without_authentication(self):
        """Users cannot create reviews without authentication"""
        response = self.client.get(reverse('shop:add-review', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PERMISSION DENIED')
        self.assertContains(response, 'Sign in')

    def test_if_review_without_purchase(self):
        """Users cannot leave a review if he hasn't bought the course"""
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('shop:add-comment', kwargs={'pk': self.test_course.pk}))

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
        response = self.client.get(reverse('shop:add-review', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'PERMISSION DENIED')
        self.assertContains(response, "You can&#x27;t review this course twice")

    def test_if_reviewed_while_teacher(self):
        """Teachers can't review their own courses"""
        self.client.login(username='testteacher', password='12345')
        response = self.client.get(reverse('shop:add-review', kwargs={'pk': self.test_course.pk}))

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
        response = self.client.get(reverse('shop:add-review', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Add review")


class PurchaseTest(CustomTestCase):
    def test_if_purchase_twice(self):
        """User can't purchase a course twice"""
        Purchase.objects.create(
            course_bought=self.test_course,
            buyer=self.user1,
        )
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('shop:course-purchase', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Seems like you have already bought this course")

    def test_teacher_purchase_own_course(self):
        """Teachers can't purchase their own course"""
        self.client.login(username='testteacher', password='12345')
        response = self.client.get(reverse('shop:course-purchase', kwargs={'pk': self.test_course.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You can't purchase your own course")
