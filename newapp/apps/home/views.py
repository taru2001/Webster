from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import User, Post, Following, Followers, Notification, Comments
import json 
from django.conf import settings 
from django.core.mail import send_mail


def index(request):
    if "username" in request.session:
       return redirect('login')
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

        if len(passw)==0 or len(phone)==0 or len(femail)==0 or len(fname)==0 or len(fusername)==0:
             return  HttpResponse("Empty Credentials!")

        else:
            newUser = User(name=fname,username=fusername,mobile=phone,email=femail,password=passw)
            User.save(newUser)
            
            # Send Mail
            subject = 'Thank u for registering'
            message = f'Welcome to the hard core gaming world'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [femail]
            send_mail(subject,message,email_from,recipient_list)

            return redirect('indexx')


    else:
        return render(request,'home/register.html')



def about(request):
    return HttpResponse("About page")



def get_followingPost(user):

    followed_obj = Following.objects.filter(user=user)
    followed_user_posts = []
    if followed_obj:
        followed_users = followed_obj[0].followed.all()

    all_posts = Post.objects.all()

    for post in all_posts:
        if followed_obj and post.user in followed_users:
            followed_user_posts.append(post)
        if post.user==user:
            followed_user_posts.append(post)

    return followed_user_posts
    


def logout(request):
    if "username" in request.session:
        del request.session["username"]
        return redirect('indexx')
    return redirect('indexx')



def likes(request, *args):  # individually handles posts for likes by ajax but resets on refresh , so making a

# list in which a user like some posts and then sending them separetely
    id = request.GET.get("likeid","")

    userr = get_object_or_404(User, username=request.session['username'])
    print("id:"+str(id))
    p1 = Post.objects.get(pk=id)
    like = p1.likes.filter(username=userr.username)
    liked = False
    if like:
        liked = True
        print("disliked_p")
        Post.disliked_p(userr, id)
    else:
        liked = False
        print("like_p")
        Post.liked_p(userr, id)
    count = p1.likes.all().count()
    resp = {
    'liked': liked,
    'count': count
}
    response = json.dumps(resp)
    return HttpResponse(response, content_type="application/json")



def userpage(request):
    if "username" in request.session:
        username = request.session["username"]
        currUser = User.objects.filter(username=username)
        UserEmail = User.objects.filter(email=username)
        print(currUser)

        temp1 = len(currUser)
        temp2 = len(UserEmail)

        if temp1 == 1:
            currUser = currUser[0]

        if temp2 == 1:
            UserEmail = UserEmail[0]
            currUser = UserEmail

        # Fetching following users posts
        followedUser_posts = get_followingPost(currUser)

        liked_posts = []
        rated_posts = []
        reported_posts = []
        name = request.session["username"]
        for i in followedUser_posts:
            is_liked = i.likes.filter(username=name) 
            is_rated = i.raters.filter(username=name)
            is_reported = i.report.filter(username=name)
            if is_liked:
                liked_posts.append(i)

            if is_rated:
                rated_posts.append(i)

            if is_reported:
                reported_posts.append(i)

        comments = Comments.objects.all()
        # print(followedUser_posts)
        params = {'username': username, 'posts': followedUser_posts, 'liked_posts': liked_posts, 'rated_posts': rated_posts,
                'comments': comments, 'reported_posts': reported_posts}

        return render(request, 'home/userhome.html', params)

    return redirect('indexx') 


def loginUser(request):

    # User already Logged In
    if "username" in request.session:
        return redirect("user_home")
       

    # Method==POST
    elif request.method=='POST':
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
            return redirect("user_home")
            



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

            # Handle post notifications to followers
            #currUser = User.objects.get(username=request.sessiom("username"))
            follower_obj = Followers.objects.filter(user=user)

            if follower_obj:
                followers = follower_obj[0].follower.all()

                for users in followers:
                    message = str(user.username) + " uploaded a new post. Go check it out"
                    addMsg = Notification(user=users,message=message)
                    Notification.save(addMsg)
            
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


        liked_posts = []
        rated_posts = []
        
        name = request.session["username"]
        for i in mylist:
            is_liked = i.likes.filter(username=name)
            is_rated = i.raters.filter(username=name)
            
            if is_liked:
                liked_posts.append(i)

            if is_rated:
                rated_posts.append(i)

        comments = Comments.objects.all()
        
        params = {'username': name, 'posts': mylist, 'liked_posts': liked_posts, 'rated_posts': rated_posts,
                'comments': comments}

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

        
        games=user.games.split(',')
        # print(games)
        params = {'name':user.name , 'username':user.username , 'mobile':user.mobile ,
                        'email':user.email, 'games':user.games, 'country':user.country,
                        'state':user.state, 'description':user.description, 'stats':user.stats , 'profileImage':user.profileImage,
                         'followedUsers' : followedUsers , 'followers':followers, 'gamessplit':games}

        return render(request,'home/dashboard.html',params)

    else:
        return redirect('login')


def edit(request):
    if "username" in request.session:
        user = User.objects.get(username = request.session["username"])
        params = {'name':user.name , 'username':user.username , 'mobile':user.mobile ,
                        'email':user.email, 'games':user.games, 'country':user.country,
                        'state':user.state, 'description':user.description, 'stats':user.stats ,  'profileImage':user.profileImage, 'password':user.password}
        return render(request,'home/edit.html',params)




def manage_edit(request):
    if request.method=="POST" and "username" in request.session :
        name = request.POST.get('name')
        stats = request.POST.get('stats')
        description = request.POST.get('description')
        state = request.POST.get('state')
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        game = request.POST.get('game')
        password = request.POST.get('password')
        
        user = User.objects.get(username = request.session["username"])
        
        user.name=name
        user.stats=stats
        user.description = description
        user.state = state
        user.country = country
        user.phone= phone
        user.games = game
        user.password = password
            
        user.save()
            
        return redirect('profile')



def isUserMatching(str1 , str2):
    m = len(str1) 
    n = len(str2) 
      
    j = 0   
    i = 0   
      
    while j<m and i<n: 
        if str1[j] == str2[i]:     
            j = j+1    
        i = i + 1
          
    # If all characters of str1 matched, then j is equal to m 
    return j==m 




def searchuser(request):
    whichUser = request.GET.get('searchuser')
    
    all_users = User.objects.all()

    # list of matched users
    found_users = []

    # Query all usernames for checking if such related username exists or not
    for user in all_users:
        if isUserMatching(user.username , whichUser) or isUserMatching(whichUser , user.username):
            found_users.append(user.username)
    
    loggedIn=0
    followed_users = []
    if "username" in request.session:
        loggedIn=1
        currUser = User.objects.get(username=request.session["username"])
        followedObj = Following.objects.filter(user = currUser)

        if followedObj:
            x = followedObj[0].followed.all()
            for user in x:
                followed_users.append(user.username)
        

    return render(request , 'home/searchuser.html' , {'found_users':found_users , 'loggedIn':loggedIn , 'followed_users':followed_users})



def changephoto(request):
    if "username" in request.session and request.method=='POST':
        profilePic = request.FILES['profilePic']

        user = User.objects.get(username=request.session["username"])
        user.profileImage = profilePic
        user.save()
        return redirect('profile')




def search_profile(request,user):

    user = User.objects.get(username=user)
    games=user.games.split(',')
    loggedIn=0
    is_following=0
    same=0
    if "username" in request.session:
        currUser = User.objects.get(username=request.session["username"])
        
        is_following = Following.objects.filter(user=currUser , followed=user)

        same=0
        if currUser==user:
            same=1
        loggedIn = 1
    
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
    #print(followers)
        
    params = {'name':user.name , 'username':user.username ,
                'games':user.games, 'country':user.country,
                'state':user.state, 'description':user.description, 'stats':user.stats , 'profileImage':user.profileImage,
                  'is_following':is_following , 'same':same , 'followedUsers': followedUsers , 'followers':followers , 'loggedIn':loggedIn,
                  'gamesplit':games}
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

            # Handle unfollowing notifications
            message = str(currUser.username) + " just Unfollowed you"
            to_whom = to_follow
            #print(message)
            addMsg = Notification(user=to_follow , message=message)
            Notification.save(addMsg)

        else:
            Following.follow(currUser , to_follow)
            Followers.follow(currUser , to_follow)
            is_following = 1

            # Handle following notifications
            message = str(currUser.username) + " just Followed you"
            to_whom = to_follow
            #print(message)
            addMsg = Notification(user=to_follow , message=message)
            Notification.save(addMsg)
        
        resp={
            "following":is_following,
        }
        response=json.dumps(resp)
        return HttpResponse(response,content_type="application/json")

    else:
        return HttpResponse("login first")



def notify(request):
    if "username" in request.session:
        currUser = User.objects.get(username=request.session["username"])
        my_message = Notification.objects.filter(user = currUser)

        return render(request,'home/notifications.html',{'messages' : my_message})
    return redirect('indexx')



def delete_notify(request,msgId):
    if "username" in request.session:
        thisMsg = Notification.objects.filter(id=msgId)
        if request.session["username"]==thisMsg[0].user.username:
            #print(thisPost)
            thisMsg.delete()
            return redirect('notifications')
        else:
            return HttpResponse("Katai Tez hor rhe ho haiiiii....chala jaa beta kuch ni hona")
    else:
        return redirect('login')    




def rating(request,*args):
    if "username" in request.session:
        id = request.GET.get('rateid')
        ratingValue = request.GET.get('value')
        print(id,ratingValue)

        if ratingValue:
            currUser = User.objects.get(username=request.session["username"])
            Post.rateNow(id,currUser,ratingValue)

            currPost = Post.objects.get(id=id)
            avg = currPost.avgRating
            
            resp = {
            'avg':avg
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")
        


def comments(request):
    msg=request.GET.get("comment")
    post=Post.objects.get(pk=request.GET.get("postid"))
    user=User.objects.get(username=request.session['username'])
    comment=Comments(user=user,post=post,comment=msg)
    comment.save()
    time=comment.time
    time=str(time.strftime("%b, %d-%m-%y %I:%M %p"))
    print(time)
    if user.profileImage:
        pic = user.profileImage.url
    else:
        pic = "https://afribary.com/authors/anonymous-user/photo"
    rep={
        'pic':pic,
        "username":user.username,
        "comment":msg,
        "time":time,
    }
    response=json.dumps(rep)
    return HttpResponse(response,content_type='application/json')



def report(request, *args):
    id = request.GET.get('postid')
    currPost = Post.objects.get(pk=id)
    currUser = User.objects.get(username=request.session["username"])

    currPost.reported(currUser,id)
    resp={

    }
    response = json.dumps(resp)
    return HttpResponse(response, content_type="appllication/json")



def forgot(request):
    return render(request,'home/forgot.html')



def manage_forgot(request):
    if request.method=='POST':
        email=request.POST.get('email')
        UserEmail = User.objects.filter(email=email)

        temp2 = len(UserEmail)

        if(temp2==1):
            password = UserEmail[0].password
            recipient=[email]
            send_mail('Password',password,'techstartechtechstar@gmail.com',recipient,fail_silently=False)
            return redirect('login')

        else:
            return HttpResponse("Invalid Email Id")


def sendmoney(request,usern):
    if "username" in request.session:
        # check if it is the same user 
        currUser = User.objects.get(username=request.session["username"])
        send_to = User.objects.get(username=usern)

        if currUser==send_to:
            return redirect('profile')

        else:
            params = {'send_to':usern }
            return render(request,'home/sendmoney.html',params)

    return redirect('indexx')



def handlepayment(request):
    if "username" in request.session:
        if request.method=="POST":
            msg = request.POST.get('send_message')
            amount = request.POST.get('amount')

            # check if user has that much money or not
            currUsername = request.session["username"]
            currUser = User.objects.get(username=currUsername)

            if int(currUser.coins) < int(amount):
                return HttpResponse("U don't have enough coins") 
            else:
                send_to = request.POST.get('send_to')
                
                # handle coins increment of paid_user
                paid_user = User.objects.get(username=send_to)
                paid_user.coins = int(paid_user.coins) + int(amount)
                paid_user.save()

                # handle money decrement of sending_user
                currUser.coins = int(currUser.coins) - int(amount)
                currUser.save()

                # Notify paid_user about activity
                message_to_paid = "Hey " + str(send_to) + " , " + str(currUsername) + " sent u " + str(amount) + " flex coins.... \n" +"Here is a message from him : "+ str(msg)
                print(message_to_paid)
                newNotify = Notification(user=paid_user,message=message_to_paid)
                Notification.save(newNotify)
                
                return redirect('login')
                           

        return redirect('login')

    return redirect('indexx')