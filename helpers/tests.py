"""
Tests helper
"""
###
# Libraries
###
from io import BytesIO
from PIL import Image

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from comments.models import Comment
from posts.models import Post
from topics.models import Topic


User = get_user_model()


###
# Test Cases
###
class CustomAPITestCase(APITestCase):
    '''
        Extend this class if you wish to use some custom validation mathods.
    '''

    def assert_list_response(self, response, status_code, count=None):
        self.assertEqual(response.status_code, status_code)
        if count is not None:
            self.assertEqual(response.data['count'], count)

    def assert_post_response(self, response, status_code, model=None, lookup=None):
        self.assertEqual(response.status_code, status_code)
        if model is not None and lookup is not None:
            result = model.objects.filter(**lookup)
            self.assertTrue(result.exists())

    def assert_get_response(self, response, status_code, entity=None):
        self.assertEqual(response.status_code, status_code)
        if entity is not None:
            self.assertEqual(response.data['id'], str(entity.id))

    def assert_update_response(self, response, status_code, entity=None, lookup=None):
        self.assertEqual(response.status_code, status_code)
        if entity is not None and lookup is not None:
            result = entity.__class__.objects.filter(**lookup).first()
            self.assertEqual(result.id, entity.id)

    def assert_delete_response(self, response, status_code, entity=None):
        self.assertEqual(response.status_code, status_code)
        if entity is not None:
            result = entity.__class__.objects.filter(id=entity.id)
            self.assertFalse(result.exists())

    @staticmethod
    def create_in_memory_image():
        in_memory_file = BytesIO()
        image = Image.new('RGBA', size=(1, 1), color=(155, 0, 0))
        image.save(in_memory_file, 'png')
        in_memory_file.name = 'image.png'
        in_memory_file.seek(0)
        return in_memory_file


class DatabaseMother():
    '''
        Class to help in db population.
    '''

    @staticmethod
    def create_user(username='testuser', password='testuser', email='testuser@example.com'):
        user = User.objects.create(username=username, email=email)
        user.set_password(password)
        user.save()
        Token.objects.create(user=user)
        return user

    @staticmethod
    def create_topic(**kwargs):
        name = kwargs['name']
        author = kwargs['author']
        title = kwargs.get('title', 'Topic')
        description = kwargs.get('description', 'Content')
        image = kwargs.get('image', 'Content')
        model = Topic.objects.create(name=name, author=author, title=title,
                                     description=description, image=image)
        model.save()
        return model

    @staticmethod
    def create_post(**kwargs):
        topic = kwargs['topic']
        author = kwargs['author']
        title = kwargs.get('title', 'Post')
        content = kwargs.get('content', 'Content')
        image = kwargs.get('image', 'Content')
        model = Post.objects.create(topic=topic, author=author, title=title,
                                    content=content, image=image)
        model.save()
        return model

    @staticmethod
    def create_comment(**kwargs):
        post = kwargs['post']
        author = kwargs['author']
        title = kwargs.get('title', 'Comment')
        content = kwargs.get('content', 'Content')
        image = kwargs.get('image', 'Content')
        model = Comment.objects.create(post=post, author=author, title=title,
                                       content=content, image=image)
        model.save()
        return model
