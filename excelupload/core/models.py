from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Staff(models.Model):
    choices = [
        ('junior','Junior Staff'),
        ('super', 'Supervisor'),
        ('manager', 'Manager')
    ]
    name = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=255)
    designation = models.CharField(choices=choices, max_length=10)

    def __str__(self):
        return self.display_name
    
    class Meta:
        verbose_name_plural = 'staffs'

class Sales(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    item_sold = models.CharField(max_length=255) # should be fk id to stock
    quantity = models.PositiveIntegerField()
    unit_price = models.PositiveSmallIntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_sold
    
    class Meta:
        verbose_name_plural = 'sales'
        ordering = ['-date']

