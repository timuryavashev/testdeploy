from django.test import TestCase

from library.models import Author


class ModelCase(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="Александр", last_name="Пушкин", birth_day="1799-06-06"
        )

    def test_author_str(self):
        self.assertEqual(str(self.author), "Александр Пушкин")
