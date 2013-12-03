from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from hvnrhell.models import Term, Page, TermValue 
# Create your views here.
