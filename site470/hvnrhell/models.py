from django.db import models

# Create your models here.
class Term(models.Model):
    term = models.CharField(max_length=500)
    index = models.PositiveIntegerField()

    def __unicode__(self):
        return "<Term:%s,Index:%d>" % (self.term,self.index)

class Page(models.Model):
    hostname = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    rating = models.CharField(max_length=10)
    def __unicode__(self):
        return "Rating:%s:%s" % (self.rating,self.url)

class TermValue(models.Model):
    term = models.ForeignKey(Term)
    value = models.FloatField()
    page  = models.ForeignKey(Page)
