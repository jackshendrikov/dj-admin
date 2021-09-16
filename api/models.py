from django.db import models


class Link(models.Model):
    link = models.URLField(max_length=1024, db_index=True, null=True)

    def __str__(self):
        return self.link


class Source(models.Model):
    source = models.CharField(max_length=128, null=True, blank=True, db_index=True)

    def __str__(self):
        return self.source


class Country(models.Model):
    country = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.country


class Brand(models.Model):
    brand = models.CharField(max_length=128, db_index=True)

    def __str__(self):
        return self.brand


class Category(models.Model):
    category = models.TextField()

    def __str__(self):
        return self.category


class Product(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    link = models.ForeignKey(Link, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '{3}: {0} ({1} [{2}])'.format(self.brand, str(self.source).capitalize(), self.country, self.category)


