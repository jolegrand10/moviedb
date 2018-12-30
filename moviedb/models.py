from django.db import models

# Create your models here.


class Director(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)

    class Meta:
        ordering=['last_name','first_name']

    def __str__(self):
        return self.first_name+" "+self.last_name

class Movie(models.Model):
    director = models.ForeignKey(Director, on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    comment=models.CharField(max_length=255)

    class Meta:
        ordering=['title']

    def __str__(self):
        return self.title

