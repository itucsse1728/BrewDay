# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


class HelloWorld(View):
    @staticmethod
    def get(request):
        return HttpResponse("Hello World")
