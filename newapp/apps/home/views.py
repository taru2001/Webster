from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import User,Post,Following,Followers
import json 


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
            return render(request,'home/userhome.html',params)

    return render(request,'home/login.html')



def upload(request):

    if "username" in request.session: 
        if request.method=='POST':
            user = User.objects.get(username = request.session["username"])
            tagline = request.POST.get('tagline')
            video = request.FILES['videofile']
            posttype = request.POST.get('filetype')

            newPost = Post(user=user,tagline=tagline,video=video,posttype=posttype)
            Post.save(newPost)
            print(posttype)
            
            return redirect('login')


        else:
            return render(request,'home/uploadPost.html')

    else:
        return HttpResponse("login first")



def mypost(request):

    if "username" in request.session:
        posts = Post.objects.all()
        #print(posts)

        mylist=[]
        for post in posts:
            if post.user.username==request.session["username"]:
                mylist.append(post)

        #print(mylist)
        #for i in mylist:
            #print(i.user.mobile)

        params = {'mylist':mylist}

        return render(request,'home/mypost.html',params)

    else:
        return HttpResponse("login first")


def deletePost(request,postId):
    if "username" in request.session:
        thisPost = Post.objects.filter(id=postId)
        if request.session["username"]==thisPost[0].user.username:
            #print(thisPost)
            thisPost.delete()
            return redirect('login')
        else:
            return HttpResponse("Katai Tez hor rhe ho haiiiii....chala jaa beta kuch ni hona")
    else:
        return redirect('login')


def playvideo(request,postId):
    posts = Post.objects.filter(id=postId)
    posts=posts[0]
    params = {'posts':posts}
    return render(request,'home/playvideo.html',params)


def profile(request):
    if "username" in request.session:  
        user = User.objects.get(username = request.session["username"])
        
        # count of following
        following_obj = Following.objects.filter(user=user)

        if following_obj:
            followedUsers = following_obj[0].followed.count()
        else:
            followedUsers=0

        # count of followers 
        followers_obj = Followers.objects.filter(user=user)

        if followers_obj:
            followers = followers_obj[0].follower.count()
        else:
            followers=0

        params = {'name':user.name , 'username':user.username , 'mobile':user.mobile ,
                        'email':user.email, 'games':user.games, 'country':user.country,
                        'state':user.state, 'description':user.description, 'stats':user.stats , 'profileImage':user.profileImage,
                         'followedUsers' : followedUsers , 'followers':followers}

        return render(request,'home/dashboard.html',params)

    else:
        return redirect('login')


def edit(request):
    if "username" in request.session:
        user = User.objects.get(username = request.session["username"])
        params = {'name':user.name , 'username':user.username , 'mobile':user.mobile ,
                        'email':user.email, 'games':user.games, 'country':user.country,
                        'state':user.state, 'description':user.description, 'stats':user.stats ,  'profileImage':user.profileImage}
        return render(request,'home/edit.html',params)


def manage_edit(request):
    if request.method=="POST":
        name = request.POST.get('name')
        stats = request.POST.get('stats')
        description = request.POST.get('description')
        state = request.POST.get('state')
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        game = request.POST.get('game')
        
        user = User.objects.get(username = request.session["username"])
        
        user.name=name
        user.stats=stats
        user.description = description
        user.state = state
        user.country = country
        user.phone= phone
        user.games = game
            
        user.save()
            
        return redirect('profile')



def searchuser(request):
    whichUser = request.GET.get('searchuser')
    users = User.objects.filter(username=whichUser)
    names = User.objects.filter(name=whichUser)

    if len(users)==0 and len(names)==0:
        return HttpResponse("No users found...!!")

    else:
        if len(users):
            users=users[0]
        else:
            users = names[0]
        return render(request,'home/searchuser.html',{'user':users})


def changephoto(request):
    if "username" in request.session and request.method=='POST':
        profilePic = request.FILES['profilePic']

        user = User.objects.get(username=request.session["username"])
        user.profileImage = profilePic
        user.save()
        return redirect('profile')


def search_profile(request,user):
    currUser = User.objects.get(username=request.session["username"])
    user = User.objects.get(username=user)
    
    is_following = Following.objects.filter(user=currUser , followed=user)

    same=0
    if currUser==user:
        same=1
    
    # count of following
    following_obj = Following.objects.filter(user=user)

    if following_obj:
        followedUsers = following_obj[0].followed.count()
    else:
        followedUsers=0

    # count of followers 
        followers_obj = Followers.objects.filter(user=user)

        if followers_obj:
            followers = followers_obj[0].follower.count()
        else:
            followers=0
        print(followers)
    params = {'name':user.name , 'username':user.username ,
                'games':user.games, 'country':user.country,
                'state':user.state, 'description':user.description, 'stats':user.stats , 'profileImage':user.profileImage,
                  'is_following':is_following , 'same':same , 'followedUsers': followedUsers , 'followers':followers}
    return render(request,'home/searchedProfile.html',params)



def follow(request,usern):
    if request.session["username"]==usern:
        return redirect('profile')

    if "username" in request.session:
        currUser = User.objects.get(username=request.session["username"])
        to_follow = User.objects.get(username=usern)

        is_following = Following.objects.filter(user=currUser , followed=to_follow)
        
        if is_following:
            Following.unfollow(currUser , to_follow)
            Followers.unfollow(currUser , to_follow)
            is_following = 0

        else:
            Following.follow(currUser , to_follow)
            Followers.follow(currUser , to_follow)
            is_following = 1
        
        resp={
            "following":is_following,
        }
        response=json.dumps(resp)
        return HttpResponse(response,content_type="application/json")

    else:
        return HttpResponse("login first")