from django.db import models

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Easy(models.Model):
    first = models.IntegerField(default=0)

# +-----------------+--------------+------+-----+---------+-------+
# | Field           | Type         | Null | Key | Default | Extra |
# +-----------------+--------------+------+-----+---------+-------+
# | YEAR            | int(11)      | NO   | PRI | NULL    |       |
# | C113_CAUSE_NAME | text         | NO   |     | NULL    |       |
# | CAUSE_NAME      | varchar(100) | NO   | PRI | NULL    |       |
# | STATE           | varchar(100) | NO   | PRI | NULL    |       |
# | DEATHS          | int(11)      | YES  |     | NULL    |       |
# | AADR            | double       | YES  |     | NULL    |       |
# +-----------------+--------------+------+-----+---------+-------+

# class Cause(models.Model):
#     YEAR = models.IntegerField(default=0)
#     C113_CAUSE_NAME = models.CharField(max_length=200)
#     CAUSE_NAME = models.CharField(max_length=200)
#     STATE = models.CharField(max_length=200)
#     DEATH = models.IntegerField(default=0)
#     AADR = models.DoubleFIeld(default=0)
