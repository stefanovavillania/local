from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
from .forms import UserForm, PermissionForm

base_url = 'http://127.0.0.1:8000/nube/{}'
def send_request(method, url, params):
    if method == 'GET':
        response = requests.get(url, params=params)
        try:
            response = response.json()
        except:
            response = {}
    elif method == 'POST':
        response = requests.post(url, data=params)
        try:
            response = response.json()
        except:
            response = {}
    elif method == 'PUT':
        response = requests.put(url, data=params)
        try:
            response = response.json()
        except:
            response = {}
    elif method == 'DELETE':
        response = requests.delete(url, params=params)
        try:
            response = response.json()
        except:
            response = {}
    return response

class IndexView(LoginRequiredMixin, View):
    template = 'base.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template, {})

class UserListView(LoginRequiredMixin, View):
    template = 'list_users.html'
    def get(self, request, *args, **kwargs):
        data = send_request('GET', base_url.format('users/list'),{})
        return render(request, self.template, {'users': data})

class UserCreateView(LoginRequiredMixin, View):
    template = 'create_user.html'
    def get(self, request, *args, **kwargs):
        form = UserForm()
        return render(request, self.template, {'form': form, 'initial': False})

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            dict_req = {
                'username': request.POST.get('username'),
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'email': request.POST.get('email'),
                'password': request.POST.get('password'),
                'is_superuser': request.POST.get('is_superuser')}
            data = send_request('POST', base_url.format('users/create/'), dict_req)
            return HttpResponseRedirect(reverse('user_list'))
        else:
            return render(request, template, {'form': form, 'initial': False})


class UserUpdateView(LoginRequiredMixin, View):
    template = 'create_user.html'
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        data = send_request('GET', base_url.format('users/update/{}'.format(id)), {})
        form = UserForm(initial=data)
        return render(request, self.template, {'form': form, 'initial': True, 'id': id})

    def post(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        data = send_request('GET', base_url.format('users/update/{}'.format(id)), {})
        form = UserForm(request.POST)
        if form.is_valid():
            dict_req = {
                'username': request.POST.get('username'),
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name'),
                'email': request.POST.get('email'),
                'password': request.POST.get('password'),
                'is_superuser': request.POST.get('is_superuser')}
            data = send_request('POST', base_url.format('users/update/{}/'.format(id)), dict_req)
            # messages.success(request, 'propietario actualizado correctamente')
            return HttpResponseRedirect(reverse('user_list'))
        else:
            return render(request, template, {'form': form, 'initial': True})

class UserDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')
        data = send_request('DELETE', base_url.format('users/delete/{}/'.format(id)), {})
        return HttpResponseRedirect(reverse('user_list'))
