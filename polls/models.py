from django.db import models
from django.utils import timezone
from django.conf import settings
import datetime

class Question(models.Model):
    question_text = models.CharField(max_length = 200)
    created_by = models.IntegerField(null=True)
    pub_date = models.DateTimeField('Date Published')
    
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length = 200)
    votes = models.IntegerField(default = 0)
    
    def __str__(self):
        return self.choice_text
    
class User(models.Model):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=16)
    
    def __str__(self):
        return self.username
    
class Reviews(models.Model):
    questions_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    review = models.CharField(max_length=5000)
    
    def __str__(self):
        return self.review
    
class UserChoices(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_selected = models.ForeignKey(Choice, on_delete=models.CASCADE)
    
    