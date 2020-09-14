from .models import Tasker
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework import status


class TestModel(APITestCase):

    """
    Тестирование модели.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        Tasker.objects.create(task='Hello, world')

    def test_state(self) -> None:
        get_obj = Tasker.objects.get(id=1)
        field = get_obj._meta.get_field('state').verbose_name

        self.assertEqual(field, 'state')
        self.assertTrue('to-do' in get_obj.state)


class TestView(APITestCase):

    """
    Тестирование представления.
    """

    @classmethod
    def setUpTestData(cls) -> None:
        Tasker.objects.create(task='foo')
        Tasker.objects.update(state='in-progress')

    def test_view(self) -> None:
        response = self.client.get('/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Tasker.objects.count() == 1)

    def test_update_value(self) -> None:
        get_obj = Tasker.objects.get(id=1)

        self.assertTrue('in-progress' in get_obj.state)


class TestMethods(APITestCase):

    """
    Тестирование базовых методов. Метод GET тестирован выше.
    """

    def test_post(self) -> None:
        response = self.client.post('', {'task': 'testing'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put(self) -> None:
        cli = APIRequestFactory()
        response = cli.put('/1/', {'state': 'done'})

        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.body, b'{"state":"done"}')
