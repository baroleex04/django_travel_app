from django.db.models import Q
from django.db import models
from django.contrib.auth.models import User
class Dish(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField(max_length=200)
    code = models.CharField(max_length=300)
    price = models.CharField(max_length=20)
    description = models.CharField(max_length=300)
    total_like = models.IntegerField(default=0)
    likers = models.ManyToManyField(User, blank=True)
    def __str__(self):
        return self.name
    
class Address(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="address")
    number = models.CharField(max_length=20)
    street = models.CharField(max_length=50)
    district = models.CharField(max_length=20)
    ward = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    is_primary = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if self.is_primary:
            self.__class__._default_manager.filter(dish=self.dish, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['dish'],
                condition=Q(is_primary=True),
                name='unique_primary_per_dish'
            )
        ]
    def __str__(self):
        return self.dish.name
    
    
