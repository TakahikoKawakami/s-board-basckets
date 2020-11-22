from django.forms import ModelForm
from django.shortcuts import render, get_object_or_404, redirect

from .models import Book


class BookForm(ModelForm):
    """書籍のフォーム"""
    class Meta:
        model = Book
        fields = ('name', 'publisher', 'page', )