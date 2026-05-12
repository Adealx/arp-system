from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    invoice = models.IntegerField()
    paid = models.IntegerField(default=0)

    @property
    def balance(self):
        return self.invoice - self.paid

    def __str__(self):
        return self.name