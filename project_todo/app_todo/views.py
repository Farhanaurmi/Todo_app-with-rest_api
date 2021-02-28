from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import TodoClass
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def Todosuser(request):
    if request.method=='GET':
        return render(request,'todo/todos.html',{'form':TodoForm})
    else:
        try:
            result = TodoForm(request.POST)
            newtodo = result.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')

        except ValueError:
            return render(request,'todo/todos.html',{'form':TodoForm, 'error':'bad data passed in,try again'} )




def signupuser(request):
    if request.method=='GET':
        return render(request,'todo/signupuser.html', {'form':UserCreationForm})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user=User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')

            except IntegrityError:
                return render(request,'todo/signupuser.html', {'form':UserCreationForm,'error':'user name has been taken'})
        else:
            return render(request,'todo/signupuser.html', {'form':UserCreationForm,'error':'password did not match'})


def home(request):
    return render(request,'todo/home.html')
@login_required
def currenttodos(request):
    todos= TodoClass.objects.filter(user=request.user, dtime__isnull=True)
    return render(request,'todo/currenttodos.html',{'todos':todos})

def loginuser(request):
    if request.method=='GET':
        return render(request,'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user= authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'todo/loginuser.html', {'form':AuthenticationForm(),'error':'username and password did not match'})
        else:
            login(request,user)
            return redirect('currenttodos')
@login_required
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')
@login_required
def viewtodo(request,todo_pk):
    obj=get_object_or_404(TodoClass,pk=todo_pk,user=request.user)
    if request.method=='GET':
        newform=TodoForm(instance=obj)
        return render(request,'todo/viewtodos.html',{'newform':newform,'obj':obj})
    else:
        try:
            newform = TodoForm(request.POST,instance=obj)
            newform.save()
            return redirect('currenttodos')

        except ValueError:
            return render(request,'todo/viewtodos.html',{'newform':newform,'obj':obj,'error':'bad data passed in,try again'} )


@login_required
def completedtodo(request,todo_pk):
    obj=get_object_or_404(TodoClass,pk=todo_pk,user=request.user)
    if request.method=='POST':
        obj.dtime=timezone.now()
        obj.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request,todo_pk):
    obj=get_object_or_404(TodoClass,pk=todo_pk,user=request.user)
    if request.method=='POST':
        obj.delete()
        return redirect('currenttodos')
    
@login_required
def allcompleted(request):
    todos= TodoClass.objects.filter(user=request.user, dtime__isnull=False).order_by('-dtime')
    return render(request,'todo/allcompleted.html',{'todos':todos})

            
        
