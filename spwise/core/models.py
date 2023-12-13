from django.db import models



class User(models.Model):
    user_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)  
    
class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
    
class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer = models.ForeignKey(User, related_name='expenses_paid', on_delete=models.CASCADE)
    participants = models.ManyToManyField(User, related_name='expenses_participated')
    group = models.ForeignKey(Group,on_delete = models.CASCADE,default = None)
    
    
class amount(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    group = models.ForeignKey(Group,on_delete = models.CASCADE)
    value = models.DecimalField(max_digits = 10,decimal_places = 2)