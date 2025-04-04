from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    budget = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        """
        Meta class to define ordering for the Category model.
        This will ensure that categories are ordered by name in ascending order.
        """
        ordering = ['name']

class Source(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        """
        Meta class to define ordering for the Source model.
        This will ensure that sources are ordered by name in ascending order.
        """
        ordering = ['name']

class Transaction(models.Model):
    """
    Model representing a financial transaction.
    """
    date = models.DateField()
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)
    source = models.ForeignKey(Source, on_delete=models.SET_DEFAULT, default=None, blank=True, null=True)

    def __str__(self):
        """
        String for representing the Transaction object (in admin site etc.)
        """
        return f"{self.date} - {self.description} - ${self.amount}"
    
    class Meta:
        """
        Meta class to define ordering for the Transaction model.
        """
        ordering = ['-date']
