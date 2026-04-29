from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()

class Expense(models.Model):
    CATEGORIES=(
        ('food','Food'),
        ('shopping','Shopping'),
        ('rent','Rent'),
        ('bills','Bills'),
        ('transport','Transport'),
        ('health','Health'),
        ('other','Other')
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="expenses")
    title=models.CharField(max_length=100)
    amount=models.IntegerField()
    category=models.CharField(max_length=50,choices=CATEGORIES)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}-{self.amount}"