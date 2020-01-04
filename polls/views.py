from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import logging

from .models import Question, Choice, User

logger = logging.getLogger(__name__)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
   
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    
class ResultView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)      
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            try:
                User.objects.create(username=username,password=raw_password)
            except:
                return render(request, 'polls/signup.html', {
            'error_message': "User already exists",
        })
            return redirect('polls:index')
    else:
        form = UserCreationForm()
    return render(request, 'polls/signup.html', {'form': form})

def login(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        a = User.objects.filter(username=username,password=password)
        if len(a) >= 1:
            user = authenticate(username=username,password=password)
            form.confirm_login_allowed(user)
            auth_login(request,user)
            print(username,password)
        else:
            return render(request,'polls/login.html',{'error_message':"User not in DB(Contact Admin)"})
        return redirect('polls:index')
    return render(request,'polls/login.html', {'form':form})
    
def logout(request):
    response = auth_logout(request)
    message = "Logged Out Successfully"
    return redirect('polls:login')
    