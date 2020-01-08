from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.cache import cache_control

from .new_poll import PostQuestion,PostChoices,Review
import logging

from .models import Question, Choice, User, Reviews, UserChoices

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    paginate_by = 5
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
    
def detail(request,question_id):
    question = get_object_or_404(Question, id=question_id)
    cur_user = request.user
    try:
        a = User.objects.get(username=cur_user)
    except:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        quests = UserChoices.objects.filter(user_id=a.id)
        q = []
        l = []
        for i in quests:
            q.append(Question.objects.get(id=i.question_id))
        final_set = set(q)
        for j in final_set:
            l.append(j.id)
        if question_id in l:
            return render(request,'polls/detail.html',
                          {'question':question,
                          'error_message':"You have already answered this poll."})        
        else:
            return render(request,'polls/detail.html',{'question':question})

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
        user = User.objects.get(username=request.user)
        a = UserChoices(user_id=user.id,question_id=question.id,choice_selected_id=selected_choice.id)
        num_votes = UserChoices.objects.filter(choice_selected_id=selected_choice.id)
        test = len(num_votes)
        validator = UserChoices.objects.filter(user_id=user.id,question_id=question.id)
        if len(validator) >= 1:
            return render(request,'polls/detail.html',{'question':question,'error_message':"You have already answered this poll"})
        else:
            selected_choice.votes += 1
            selected_choice.save()
            a.save()
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
    
def new_poll(request):
    if request.method == "POST":
        form = PostQuestion(request.POST)
        if form.is_valid():
            quest = form.save(commit=False)
            a = User.objects.get(username=request.user)
            quest.created_by = a.id
            quest.pub_date = timezone.now()
            question = form.cleaned_data.get('question_text')
            quest.save()
            print(question)
            return HttpResponseRedirect(reverse('polls:new_choice', args=(quest.id,)))
    else:
        form = PostQuestion()
    return render(request, 'polls/new_poll.html',{'form':form})

def new_choice(request,question_id):
    q = Question.objects.get(id=question_id)
    if request.method=="POST":
        form = PostChoices(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question_id = question_id
            choices = form.cleaned_data.get('choice_text')
            a = Choice.objects.filter(choice_text=choices,question_id=question_id)
            if len(a) >= 1:
                return render(request,'polls/new_choice.html',{'error_message':"Choice already added"})
            else:
                choice.save()
                return HttpResponseRedirect(reverse('polls:new_choice', args=(question_id,)))
            print(choices)
    else:
        form = PostChoices()
    return render(request,'polls/new_choice.html',{'form':form,'question':q})

def review(request,question_id):
    try:
        a = User.objects.get(username=request.user)
    except:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        if request.method == "POST":
            form = Review(request.POST)
            if form.is_valid():
                rev = form.save(commit=False)
                rev.questions_id_id = question_id
                rev.user_id_id = a.id
                reviews = form.cleaned_data.get('review')
                rev.save()
                print(reviews)
                return HttpResponseRedirect(reverse('polls:index'))
        else:
            form = Review()
    return render(request,'polls/new_review.html',{'form':form})

def profile(request):
    cur_user = request.user
    try:
        a = User.objects.get(username=cur_user)
    except:
        return HttpResponseRedirect(reverse('polls:login'))
    else:
        polls = Question.objects.filter(created_by=a.id)
        quests = UserChoices.objects.filter(user_id=a.id)
        q = []
        for i in quests:
            q.append(Question.objects.get(id=i.question_id))
        final_set = set(q)
        return render(request,'polls/profile.html',{'polls':polls,'quests':q})

def delete(request,question_id):
    a = Question.objects.get(id=question_id)
    a.delete()
    return HttpResponseRedirect(reverse('polls:profile'))
 
def update(request,question_id):
    a = Question.objects.get(id=question_id)
    context = {'question':a}
    return render(request,'polls/update.html',context) 
    
def update_poll(request,question_id):
    if request.method == "POST":
        form = PostQuestion(request.POST)
        if form.is_valid():
            quest = form.save(commit=False)
            question = form.cleaned_data.get('question_text')
            q = Question.objects.get(id=question_id)
            q.question_text = question
            q.pub_date = timezone.now()
            q.save()
            print(question)
            return HttpResponseRedirect(reverse('polls:update', args=(question_id,)))
    else:
        form = PostQuestion()
    return render(request, 'polls/new_poll.html',{'form':form})

def update_choice(request,choice_id):
    if request.method=="POST":
        form = PostChoices(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choices = form.cleaned_data.get('choice_text')
            a = Choice.objects.get(id=choice_id)
            a.choice_text = choices
            dup = Choice.objects.filter(choice_text=choices,question_id=a.question_id)
            if len(dup) >= 1:
                return render(request,'polls/new_choice.html',{'error_message':"Choice already added"})
            else:
                a.save()
                return HttpResponseRedirect(reverse('polls:update', args=(a.question_id,)))
            print(choices)
    else:
        form = PostChoices()
    return render(request,'polls/new_choice.html',{'form':form})

def delete_choice(request,choice_id):
    a = Choice.objects.get(id=choice_id)
    a.delete()
    return HttpResponseRedirect(reverse('polls:update', args=(a.question_id,)))

def change_response(request,question_id):
    cur_user = request.user
    a = User.objects.get(username=cur_user)
    to_del = UserChoices.objects.get(user_id=a.id,question_id=question_id)
    to_del.delete()
    b = Choice.objects.get(question_id=question_id,id=to_del.choice_selected_id)
    b.votes -= 1
    b.save()
    return HttpResponseRedirect(reverse('polls:detail', args=(question_id,)))