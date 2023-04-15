from django.db import models
from django.forms import ValidationError
from django.utils.text import slugify

class Project(models.Model):
    #project = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    budget = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)


    def get_total_expenses(self):
        return sum(expense.amount for expense in self.expenses.all())

    def get_left(self):
        total_expenses = self.expenses.aggregate(models.Sum('amount'))['amount__sum'] or 0
        return self.budget - total_expenses


class Category(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    is_default = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if self.is_default:
            raise Exception("Cannot delete default category.")
        super(Category, self).delete(*args, **kwargs)


class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=30)
    #description = models.TextField(max_length=60 )
    amount = models.PositiveIntegerField(default=0.00)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
