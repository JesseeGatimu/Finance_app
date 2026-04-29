from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()

class Income(models.Model):
    CATEGORIES=(
        ('salary','Salary'),
        ('freelance','Freelance'),
        ('business','Business'),
        ('investments','Investments'),
        ('gifts','Gifts'),
        ('other','Other')
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE,)
    title=models.CharField(max_length=100)
    amount=models.IntegerField()
    category=models.CharField(max_length=50,choices=CATEGORIES)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}-{self.amount}"