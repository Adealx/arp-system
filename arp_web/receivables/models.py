from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=100)
    invoice = models.IntegerField()
    paid = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    @property
    def balance(self):
        return self.invoice - self.paid

    def __str__(self):
        return self.name