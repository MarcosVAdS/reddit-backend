"""
API V1: Test Posts
"""
###
# Libraries
###
from django.urls import reverse
from rest_framework import status

from posts.models import Post

from helpers.tests import CustomAPITestCase, DatabaseMother


###
# Test Cases
###
class PostTestCase(CustomAPITestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_helper = DatabaseMother()
        super().setUpClass()

    def setUp(self):
        self.user_0 = self.db_helper.create_user()
        self.user_1 = self.db_helper.create_user('testuser1')
        self.topic_0 = self.db_helper.create_topic(name='t0', author=self.user_0)
        self.topic_1 = self.db_helper.create_topic(name='t1', author=self.user_1)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_0.auth_token.key)

    def test_post_list_with_no_register_should_return_no_register(self):
        url = reverse('topic-post-list', kwargs={'topics_url_name': self.topic_0.url_name})
        response = self.client.get(url)
        self.assert_list_response(response, status.HTTP_200_OK, 0)

    def test_post_list_with_registers_in_db_should_return_some_register(self):
        self.db_helper.create_post(topic=self.topic_0, author=self.user_0)
        self.db_helper.create_post(topic=self.topic_1, author=self.user_0)
        self.db_helper.create_post(topic=self.topic_0, author=self.user_1)
        url = reverse('topic-post-list', kwargs={'topics_url_name': self.topic_0.url_name})
        response = self.client.get(url)
        self.assert_list_response(response, status.HTTP_200_OK, 2)

    def test_post_post_should_create_a_new_register(self):
        url = reverse('topic-post-list', kwargs={'topics_url_name': self.topic_0.url_name})
        payload = {
            'title': 't1',
            'content': 't1',
        }
        response = self.client.post(url, payload)
        self.assert_post_response(response, status.HTTP_201_CREATED, Post, {'title': 't1'})

    def test_post_post_with_image_should_save_the_image_in_s3(self):
        url = reverse('topic-post-list', kwargs={'topics_url_name': self.topic_0.url_name})
        payload = {
            'title': 't1',
            'content': 't1',
            'image': self.create_in_memory_image(),
        }
        response = self.client.post(url, payload)
        self.assert_post_response(response, status.HTTP_201_CREATED, Post, {'title': 't1'})

    def test_post_get_with_no_registers_should_return_not_found(self):
        url = reverse('topic-post-detail',
                      kwargs={'topics_url_name': self.topic_0.url_name, 'pk': '0'})
        response = self.client.get(url)
        self.assert_get_response(response, status.HTTP_404_NOT_FOUND)

    def test_post_get_with_registers_in_db_should_return_the_correct_register(self):
        post_0 = self.db_helper.create_post(topic=self.topic_0, author=self.user_0)
        self.db_helper.create_post(topic=self.topic_1, author=self.user_0)
        self.db_helper.create_post(topic=self.topic_0, author=self.user_1)
        url = reverse('topic-post-detail',
                      kwargs={'topics_url_name': self.topic_0.url_name, 'pk': str(post_0.id)})
        response = self.client.get(url)
        self.assert_get_response(response, status.HTTP_200_OK, post_0)

    def test_post_put_with_no_registers_should_return_not_found(self):
        url = reverse('topic-post-detail',
                      kwargs={'topics_url_name': self.topic_0.url_name, 'pk': '0'})
        payload = {
            'title': 't1',
            'content': 't1',
        }
        response = self.client.put(url, payload)
        self.assert_update_response(response, status.HTTP_404_NOT_FOUND)

    def test_post_put_with_registers_in_db_should_return_update_the_register(self):
        post_0 = self.db_helper.create_post(topic=self.topic_0, author=self.user_0)
        url = reverse('topic-post-detail',
                      kwargs={'topics_url_name': self.topic_0.url_name, 'pk': str(post_0.id)})
        payload = {
            'title': 't1',
            'content': 't1',
        }
        response = self.client.put(url, payload)
        self.assert_update_response(response, status.HTTP_200_OK, post_0, {'title': 't1'})

    def test_post_put_with_registers_other_user_db_should_return_forbidden(self):
        post_0 = self.db_helper.create_post(topic=self.topic_0, author=self.user_1)
        url = reverse('topic-post-detail',
                      kwargs={'topics_url_name': self.topic_0.url_name, 'pk': str(post_0.id)})
        payload = {
            'title': 't1',
            'content': 't1',
        }
        response = self.client.put(url, payload)
        self.assert_update_response(response, status.HTTP_403_FORBIDDEN)

    def test_post_patch_with_no_registers_should_return_not_found(self):
        url = reverse('topic-post-detail',
                      kwargs={'topics_url_name': self.topic_0.url_name, 'pk': '0'})
        payload = {'title': 't1'}
        response = self.client.patch(url, payload)
        self.assert_update_response(response, status.HTTP_404_NOT_FOUND)

    def test_post_patch_with_registers_in_db_should_return_update_the_register(self):
        post_0 = self.db_helper.create_post(topic=self.topic_0, author=self.user_0)
        url = reverse('topic-post-detail',
                      kwargs={'topics_url_name': self.topic_0.url_name, 'pk': str(post_0.id)})
        payload = {'title': 't1'}
        response = self.client.patch(url, payload)
        self.assert_update_response(response, status.HTTP_200_OK, post_0, {'title': 't1'})

    def test_post_patch_with_registers_other_user_db_should_return_forbidden(self):
        post_0 = self.db_helper.create_post(topic=self.topic_0, author=self.user_1)
        url = reverse('topic-post-detail',
                      kwargs={'topics_url_name': self.topic_0.url_name, 'pk': str(post_0.id)})
        payload = {'title': 't1'}
        response = self.client.patch(url, payload)
        self.assert_update_response(response, status.HTTP_403_FORBIDDEN)

    def test_post_delete_with_no_registers_should_return_not_found(self):
        url = reverse('topic-post-detail',
                      kwargs={'topics_url_name': self.topic_0.url_name, 'pk': '0'})
        response = self.client.delete(url)
        self.assert_delete_response(response, status.HTTP_404_NOT_FOUND)

    def test_post_delete_with_registers_in_db_should_delete_the_register(self):
        post_0 = self.db_helper.create_post(topic=self.topic_0, author=self.user_0)
        url = reverse('topic-post-detail',
                      kwargs={'topics_url_name': self.topic_0.url_name, 'pk': str(post_0.id)})
        response = self.client.delete(url)
        self.assert_delete_response(response, status.HTTP_204_NO_CONTENT, post_0)

    def test_post_delete_with_registers_other_user_db_should_return_forbidden(self):
        post_0 = self.db_helper.create_post(topic=self.topic_0, author=self.user_1)
        url = reverse('topic-post-detail',
                      kwargs={'topics_url_name': self.topic_0.url_name, 'pk': str(post_0.id)})
        response = self.client.delete(url)
        self.assert_delete_response(response, status.HTTP_403_FORBIDDEN)
