import datetime
from datetime import timezone

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from shop.forms import CourseUploadForm
from shop.models import Comment, Course, Category
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

        response = self.client.post(reverse('shop:course-create'),
                                    {
                                        'title': 'test video',
                                        'price': 10,
                                        'description': 'tescription',
                                        'category': 'Sport',
                                        'video': test_video
                                    })

        self.assertContains(response, 'PERMISSION DENIED')
        self.assertContains(response, 'Seems like you are not a teacher')

    def test_course_creation_no_video_file(self):
        """
        Course cannot be created if the user is trying to upload
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
        self.assertContains(response, f"Files of type {content_type} are not valid, please upload an mp4.")

    def test_course_creation_invalid_category(self):
        """
        Course cannot be created if the user is trying to upload
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
        self.assertContains(response, f"Select a valid choice. {invalid_choice} is not one of the available choices.")

    def test_course_creation_invalid_price(self):
        """
        Course cannot be created if the price is a negative number or a text field
        """
        self.user = UserProfile.objects.create_user(username='testuser', password='12345', is_teacher=True)
        self.client.login(username='testuser', password='12345')

        content_type = 'video/mp4'
        test_video = SimpleUploadedFile('file.mp4', b'file_content', content_type=content_type)
        invalid_choice = 'Invalid'
        form_data = {
            'title': 'test video',
            'price': -10,
            'description': 'description test description',
            'category': 'Sport',
            'video': test_video,
        }
        form = CourseUploadForm(data=form_data)
        response = self.client.post(reverse('shop:course-create'), form.data)
        self.assertContains(response, "Ensure this value is greater than or equal to 0.1.")

        form_data['price'] = 'invalid price'
        form = CourseUploadForm(data=form_data)
        response = self.client.post(reverse('shop:course-create'), form.data)
        self.assertContains(response, 'Enter a number.')
