"""
API V1: Test Topics
"""
###
# Libraries
###
from django.urls import reverse
from rest_framework import status

from topics.models import Topic

from helpers.tests import CustomAPITestCase, DatabaseMother


###
# Test Cases
###
class TopicTestCase(CustomAPITestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_helper = DatabaseMother()
        super().setUpClass()

    def setUp(self):
        self.user_0 = self.db_helper.create_user()
        self.user_1 = self.db_helper.create_user('testuser1')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_0.auth_token.key)

    def test_topic_list_with_no_register_should_return_no_register(self):
        url = reverse('topic-list')
        response = self.client.get(url)
        self.assert_list_response(response, status.HTTP_200_OK, 0)

    def test_topic_list_with_registers_in_db_should_return_some_register(self):
        self.db_helper.create_topic(name='t0', author=self.user_0)
        self.db_helper.create_topic(name='t1', author=self.user_0)
        self.db_helper.create_topic(name='t2', author=self.user_1)
        url = reverse('topic-list')
        response = self.client.get(url)
        self.assert_list_response(response, status.HTTP_200_OK, 3)

    def test_topic_post_should_create_a_new_register(self):
        url = reverse('topic-list')
        payload = {
            'name': 't1',
            'title': 't1',
            'description': 't1',
        }
        response = self.client.post(url, payload)
        self.assert_post_response(response, status.HTTP_201_CREATED, Topic, {'url_name': 't1'})

    def test_topic_post_with_image_should_save_the_image_in_s3(self):
        url = reverse('topic-list')
        payload = {
            'name': 't1',
            'title': 't1',
            'description': 't1',
            'image': self.create_in_memory_image(),
        }
        response = self.client.post(url, payload)
        self.assert_post_response(response, status.HTTP_201_CREATED, Topic, {'url_name': 't1'})

    def test_topic_get_with_no_registers_should_return_not_found(self):
        url = reverse('topic-detail', kwargs={'url_name': 't0'})
        response = self.client.get(url)
        self.assert_get_response(response, status.HTTP_404_NOT_FOUND)

    def test_topic_get_with_registers_in_db_should_return_the_correct_register(self):
        topic_0 = self.db_helper.create_topic(name='t0', author=self.user_0)
        self.db_helper.create_topic(name='t1', author=self.user_0)
        self.db_helper.create_topic(name='t2', author=self.user_1)
        url = reverse('topic-detail', kwargs={'url_name': topic_0.url_name})
        response = self.client.get(url)
        self.assert_get_response(response, status.HTTP_200_OK, topic_0)

    def test_topic_put_with_no_registers_should_return_not_found(self):
        url = reverse('topic-detail', kwargs={'url_name': 't0'})
        payload = {
            'name': 't1',
            'title': 't1',
            'description': 't1',
        }
        response = self.client.put(url, payload)
        self.assert_update_response(response, status.HTTP_404_NOT_FOUND)

    def test_topic_put_with_registers_in_db_should_return_update_the_register(self):
        topic_0 = self.db_helper.create_topic(name='t0', author=self.user_0)
        url = reverse('topic-detail', kwargs={'url_name': topic_0.url_name})
        payload = {
            'name': 't1',
            'title': 't1',
            'description': 't1',
        }
        response = self.client.put(url, payload)
        self.assert_update_response(response, status.HTTP_200_OK, topic_0, {'url_name': 't1'})

    def test_topic_put_with_registers_other_user_db_should_return_forbidden(self):
        topic_0 = self.db_helper.create_topic(name='t0', author=self.user_1)
        url = reverse('topic-detail', kwargs={'url_name': topic_0.url_name})
        payload = {
            'name': 't1',
            'title': 't1',
            'description': 't1',
        }
        response = self.client.put(url, payload)
        self.assert_update_response(response, status.HTTP_403_FORBIDDEN)

    def test_topic_patch_with_no_registers_should_return_not_found(self):
        url = reverse('topic-detail', kwargs={'url_name': 't0'})
        payload = {'name': 't1'}
        response = self.client.patch(url, payload)
        self.assert_update_response(response, status.HTTP_404_NOT_FOUND)

    def test_topic_patch_with_registers_in_db_should_return_update_the_register(self):
        topic_0 = self.db_helper.create_topic(name='t0', author=self.user_0)
        url = reverse('topic-detail', kwargs={'url_name': topic_0.url_name})
        payload = {'name': 't1'}
        response = self.client.patch(url, payload)
        self.assert_update_response(response, status.HTTP_200_OK, topic_0, {'url_name': 't1'})

    def test_topic_patch_with_registers_other_user_db_should_return_forbidden(self):
        topic_0 = self.db_helper.create_topic(name='t0', author=self.user_1)
        url = reverse('topic-detail', kwargs={'url_name': topic_0.url_name})
        payload = {'name': 't1'}
        response = self.client.patch(url, payload)
        self.assert_update_response(response, status.HTTP_403_FORBIDDEN)

    def test_topic_delete_with_no_registers_should_return_not_found(self):
        url = reverse('topic-detail', kwargs={'url_name': 't0'})
        response = self.client.delete(url)
        self.assert_delete_response(response, status.HTTP_404_NOT_FOUND)

    def test_topic_delete_with_registers_in_db_should_delete_the_register(self):
        topic_0 = self.db_helper.create_topic(name='t0', author=self.user_0)
        url = reverse('topic-detail', kwargs={'url_name': topic_0.url_name})
        response = self.client.delete(url)
        self.assert_delete_response(response, status.HTTP_204_NO_CONTENT, topic_0)

    def test_topic_delete_with_registers_other_user_db_should_return_forbidden(self):
        topic_0 = self.db_helper.create_topic(name='t0', author=self.user_1)
        url = reverse('topic-detail', kwargs={'url_name': topic_0.url_name})
        response = self.client.delete(url)
        self.assert_delete_response(response, status.HTTP_403_FORBIDDEN)

