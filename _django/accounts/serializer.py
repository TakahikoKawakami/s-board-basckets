# coding: utf-8
from rest_framework import serializers
# from .models import Diary


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        pass
#	        model = Diary
#			        fields = ('date', 'title', 'body', 'publishing',)
