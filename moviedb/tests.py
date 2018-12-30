from django.test import TestCase
from django.urls import reverse
from .models import Movie, Director

# Create your tests here.


# test views
class ViewTestCase(TestCase):
    def test_view(self):
        response=self.client.get(reverse('moviedb:index'))
        self.assertEqual(response.status_code, 200)

    def test_view1(self):
        response=self.client.get(reverse('moviedb:export_csv'))
        self.assertEqual(response.status_code, 200)

    def test_view2(self):
        response=self.client.get(reverse('moviedb:movie_listing'))
        self.assertEqual(response.status_code, 200)

    def test_view3(self):
        response=self.client.get(reverse('moviedb:director_listing'))
        self.assertEqual(response.status_code, 200)

    def test_view4(self):
        dir1=Director.objects.create(first_name='Albert',last_name='Einstein')
        mov1=Movie.objects.create(title='E=mc2', comment='Film', director=dir1)
        response=self.client.get(reverse('moviedb:movie_details', args=(mov1.id,)))
        self.assertEqual(response.status_code, 200)

    def test_view5(self):
        dir1=Director.objects.create(first_name='Albert',last_name='Einstein')
        response=self.client.get(reverse('moviedb:director_details', args=(dir1.id,)))
        self.assertEqual(response.status_code, 200)
