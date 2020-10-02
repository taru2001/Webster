from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Post


def index(request):
    return render(request,'home/index.html')

def registerUser(request):
    if request.method=='POST':
        fname = request.POST.get('name')
        fusername = request.POST.get('username')
        femail = request.POST.get('email')
        phone = request.POST.get('mobileno')
        passw = request.POST.get('password')
        confpass = request.POST.get('confirmpassword')

        
        if passw!=confpass:
            return  HttpResponse("passwords did not matched...!!")

        else:
            newUser = User(name=fname,username=fusername,mobile=phone,email=femail,password=passw)
            User.save(newUser)
            return redirect('/home/login/')


    else:
        return render(request,'home/register.html')



def about(request):
    return HttpResponse("About page")


def logout(request):
    del request.session["username"]
    return redirect('index')



def loginUser(request):

    # User already Logged In
    if "username" in request.session:
        username = request.session["username"]
        currUser = User.objects.filter(username=username)
        UserEmail = User.objects.filter(email=username)

        temp1 = len(currUser)
        temp2 = len(UserEmail)
        
        if temp1==1:
            currUser = currUser[0]

        if temp2==1:
            UserEmail = UserEmail[0]
            currUser = UserEmail

        params = {'name':currUser.name , 'username':currUser.username , 'mobile':currUser.mobile ,
                        'email':currUser.email}
        return render(request,'home/userhome.html',params) 
        

    # Method==POST
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        currUser = User.objects.filter(username=username)
        UserEmail = User.objects.filter(email=username)

        temp1 = len(currUser)
        temp2 = len(UserEmail)
        
        if temp1==1:
            currUser = currUser[0]

        if temp2==1:
            UserEmail = UserEmail[0]
            currUser = UserEmail

        if temp1==0 and temp2==0:
            return HttpResponse("Invalid username or such user does not exist")

        elif(password!=currUser.password):
            return HttpResponse("Incorrect password")

        else:
            # Created Session
            request.session["username"] = currUser.username
            
            params = {'name':currUser.name , 'username':currUser.username , 'mobile':currUser.mobile ,
                        'email':currUser.email}
            return render(request,'home/userhome.html')

    return render(request,'home/login.html')



def upload(request):

    if "username" in request.session:
        if request.method=='POST':
            user = User.objects.get(username = request.session["username"])
            tagline = request.POST.get('tagline')
            video = request.FILES['videofile']

            newPost = Post(user=user,tagline=tagline,video=video)
            Post.save(newPost)
            #print(tagline,video,user)
            print(video)
            return redirect('login')


        else:
            return render(request,'home/uploadPost.html')

    else:
        return HttpResponse("login first")

def profile(request):
    if "username" in request.session:
        # username = request.session["username"]
        # user = User.objects.filter(username=username)
        user = User.objects.get(username = request.session["username"])
        params = {'name':user.name , 'username':user.username , 'mobile':user.mobile ,
                        'email':user.email}
        return render(request,'home/dashboard.html',params)

    else:
        return redirect('login')

def edit(request):
    return render(request,'home/edit.html')

def manage_edit(request):
    if request.method=="POST":
        name = request.POST.get('name')
        if "username" in request.session:
            user = User.objects.get(username = request.session["username"])
            del request.session["username"]
            user.name=name
            user.username="hacker"
            # newdata = User(name=user.name,username=user.username,mobile=user.mobile,email=user.email,password=user.password)
            # newUser = User(name=name)
            user.save()
            request.session["username"] = user.username
            return redirect('profile')

