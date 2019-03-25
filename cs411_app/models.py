# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Causes(models.Model):
    year = models.IntegerField(db_column='YEAR', primary_key=True)  # Field name made lowercase.
    c113_cause_name = models.TextField(db_column='C113_CAUSE_NAME')  # Field name made lowercase.
    cause_name = models.CharField(db_column='CAUSE_NAME', max_length=100)  # Field name made lowercase.
    state = models.CharField(db_column='STATE', max_length=100)  # Field name made lowercase.
    deaths = models.IntegerField(db_column='DEATHS', blank=True, null=True)  # Field name made lowercase.
    aadr = models.FloatField(db_column='AADR', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'causes'
        unique_together = (('year', 'cause_name', 'state'),)


class Pop(models.Model):
    state = models.CharField(db_column='State', primary_key=True, max_length=20)  # Field name made lowercase.
    y1999 = models.IntegerField(db_column='Y1999')  # Field name made lowercase.
    y2000 = models.IntegerField(db_column='Y2000')  # Field name made lowercase.
    y2001 = models.IntegerField(db_column='Y2001')  # Field name made lowercase.
    y2002 = models.IntegerField(db_column='Y2002')  # Field name made lowercase.
    y2003 = models.IntegerField(db_column='Y2003')  # Field name made lowercase.
    y2004 = models.IntegerField(db_column='Y2004')  # Field name made lowercase.
    y2005 = models.IntegerField(db_column='Y2005')  # Field name made lowercase.
    y2006 = models.IntegerField(db_column='Y2006')  # Field name made lowercase.
    y2007 = models.IntegerField(db_column='Y2007')  # Field name made lowercase.
    y2008 = models.IntegerField(db_column='Y2008')  # Field name made lowercase.
    y2009 = models.IntegerField(db_column='Y2009')  # Field name made lowercase.
    y2010 = models.IntegerField(db_column='Y2010')  # Field name made lowercase.
    y2011 = models.IntegerField(db_column='Y2011')  # Field name made lowercase.
    y2012 = models.IntegerField(db_column='Y2012')  # Field name made lowercase.
    y2013 = models.IntegerField(db_column='Y2013')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pop'
