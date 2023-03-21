from cgitb import text
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
#####COMMMAND########### 
###For at installere det nye ''stageing area''

## python3 manage.py makemigrations main
## python3 manage.py migrate 





class ToDoList(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="todolist", null=True)
    def __str__(self) -> str:
        return self.name
    

class Item(models.Model): 
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self) -> str:
        return self.text



