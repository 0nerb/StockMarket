from django.db import models

class Email(models.Model):
    address = models.EmailField()

    def __str__(self):
        return self.address

