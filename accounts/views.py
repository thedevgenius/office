from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, ListView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template.loader import render_to_string
from datetime import datetime


from .forms import SigninForm, UserAddForm, TeamBookForm, AssistForm
from .models import User
from .utils import generate_random_color
from .tasks import my_task
# Create your views here.

class SigninView(LoginView):
    template_name = 'accounts/sign_in.html'
    redirect_authenticated_user = True
    form_class = SigninForm


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = User.employees.filter(reporting_manager=self.request.user)
        context['booked'] = User.employees.filter(assigned_to=self.request.user)
        context['resources'] = User.employees.filter(status='AVL').exclude(reporting_manager=self.request.user)
        return context


@method_decorator(login_required, name='dispatch')
class BookView(View):
    def get(self, request):
        id = request.GET.get('id')
        form = TeamBookForm(initial={'id':id})
        html = render_to_string('accounts/team_book.html', {'form':form})

        return JsonResponse({'success':True, 'html':html})
    

    def post(self, request):
        id = request.POST.get('id')
        user = User.objects.get(id=id)
        user.status = 'WRK'
        user.assigned_till = None
        user.save()
        return JsonResponse({'success': True})    
    

@method_decorator(login_required, name='dispatch')
@method_decorator(ensure_csrf_cookie, name='dispatch')
class FreeView(View):
    def get(self, request):
        id = request.GET.get('id')
        form = TeamBookForm(initial={'id':id})
        html = render_to_string('accounts/team_free.html', {'form':form})
        return JsonResponse({'success':True, 'html':html})

    def post(self, request):
        id = request.POST.get('id')
        user = User.objects.get(id=id)
        time = request.POST.get('time')
        assigned_till = datetime.combine(datetime.today(), datetime.strptime(time, "%H:%M").time())
        if user.reporting_manager == self.request.user:
            user.status = 'AVL'
            user.assigned_till = assigned_till
            user.save()
        else:
            user.status = 'AVL'
            user.assigned_till = None
            user.assigned_to = None
            user.save()
        return JsonResponse({'success': True})


@method_decorator(login_required, name='dispatch')
class AssistView(View):
    def get(self, request):
        id = request.GET.get('id')
        form = AssistForm(initial={'id':id})
        html = render_to_string('accounts/team_assist.html', {'form':form})
        return JsonResponse({'success':True, 'html':html})
    
    def post(self, request, **kwargs):
        id = request.POST.get('id')
        user = User.objects.get(id=id)
        time = request.POST.get('time')
        assigned_to = User.objects.get(id=request.POST.get('manager'))
        assigned_till = datetime.combine(datetime.today(), datetime.strptime(time, "%H:%M").time())
        if user.reporting_manager == self.request.user:
            user.status = 'AST'
            user.assigned_to = assigned_to
            user.assigned_till = assigned_till
            user.save()
        else:
            user.status = 'AVL'
            user.assigned_till = None
            user.assigned_to = None
            user.save()
        return JsonResponse({'success': True})

@method_decorator(login_required, name='dispatch')
class UserAddView(TemplateView):
    template_name = 'accounts/user_add.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserAddForm()
        return context
    
    def post(self, request, **kwargs):
        form = UserAddForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            full_name = f"{data['first_name']}{data['last_name']}".lower()
            password = f"{full_name[:4]}{data['date_of_birth']:%d%m}"
            user = form.save(commit=False)
            user.set_password(password)
            user.profile_color = generate_random_color()
            user.save()
            return redirect('employee_list')
        else:
            return render(request, self.template_name, {'form':form})


@method_decorator(login_required, name='dispatch')
class EmployeeListView(ListView):
    template_name = 'accounts/employee_list.html'
    model = User
    context_object_name = 'users'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = User.objects.filter(is_active=True, is_staff=False).order_by('first_name')
        return queryset