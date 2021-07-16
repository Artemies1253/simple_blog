from django import views
from django.shortcuts import render


class MainView(views.View):
    def get(self, request):
        return render(request, 'main/main.html', {})
