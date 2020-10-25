from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import User, Post, Following, Followers, Notification, Comments, Replies
import json 
from django.conf import settings 
from django.core.mail import send_mail


def index(request):
    #If user is logged in redirects to home page
    if "username" in request.session:

       return redirect('login')
       # Home Page User enters here
    return render(request,'home/index.html')

def registerUser(request):
    #Signup Here
    if request.method=='POST':
        fname = request.POST.get('name')
        fusername = request.POST.get('username')
        femail = request.POST.get('email')
        phone = request.POST.get('mobileno')
        passw = request.POST.get('password')
        confpass = request.POST.get('confirmpassword')

        # Check if confpass==passw
        if passw!=confpass:
            return  HttpResponse("passwords did not matched...!!")
        # if null return empty credentials
        if len(passw)==0 or len(phone)==0 or len(femail)==0 or len(fname)==0 or len(fusername)==0:
             return  HttpResponse("Empty Credentials!")

        else:
            # All Checks Pass
            total = len(User.objects.all())
            newUser = User(name=fname,username=fusername,mobile=phone,email=femail,password=passw,rank=total+1)
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
    # About Is empty
    return HttpResponse("About page")



def get_followingPost(user):
    # Fetches Posts of the ppl user is following
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
    # Logout user
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
        if p1.user.username != request.session["username"]:
            currUser = User.objects.get(username=request.session["username"])
            to = User.objects.get(username=p1.user.username)
            msg = str(request.session["username"]) +" just liked your post"
            newNotify = Notification(user=to,message=msg,which="post",getid=id)
            Notification.save(newNotify)

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
    # Main page shown to User after login
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
        # Fetches users post and all his followings posts
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
        replies=Replies.objects.all()
        # print(followedUser_posts)
        params = {'username': username, 'posts': followedUser_posts, 'liked_posts': liked_posts, 'rated_posts': rated_posts,
                'commentss': comments, 'reported_posts': reported_posts,'replies':replies}

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
    # User Post uploader
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
                    addMsg = Notification(user=users,message=message,which="post",getid=newPost.id)
                    Notification.save(addMsg)
            
            return redirect('login')


        else:
            return render(request,'home/uploadPost.html')

    else:
        return HttpResponse("login first")



def mypost(request):
    # Fetches users post
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
        #Comments Are fetched Here
        comments = Comments.objects.all()
        replies=Replies.objects.all()
        
        params = {'username': name, 'posts': mylist, 'liked_posts': liked_posts, 'rated_posts': rated_posts,
                'comments': comments , 'replies':replies}

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
    # Plays Video
    posts = Post.objects.filter(id=postId)
    posts=posts[0]
    params = {'posts':posts}
    return render(request,'home/playvideo.html',params)


def profile(request):
    #Profile backend for usera
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
                         'followedUsers' : followedUsers , 'followers':followers, 'gamessplit':games, 'rank':user.rank,
                          'popularity':user.popularity}

        return render(request,'home/dashboard.html',params)

    else:
        return redirect('login')


def edit(request):
    #redirects to edit profile Taking current user data
    if "username" in request.session:
        user = User.objects.get(username = request.session["username"])
        params = {'name':user.name , 'username':user.username , 'mobile':user.mobile ,
                        'email':user.email, 'games':user.games, 'country':user.country,
                        'state':user.state, 'description':user.description, 'stats':user.stats ,  'profileImage':user.profileImage, 'password':user.password}
        return render(request,'home/edit.html',params)




def manage_edit(request):
    # Profile Edit Option
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
    #Filters user based on search
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
    # Search Users
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
    # Changes Photos
    if "username" in request.session and request.method=='POST':
        profilePic = request.FILES['profilePic']

        user = User.objects.get(username=request.session["username"])
        user.profileImage = profilePic
        user.save()
        return redirect('profile')




def search_profile(request,user):
    # Filters the profile after search user is done
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
    # Follow/unfollow button
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
    # Users Notification Fetching Happens here
    if "username" in request.session:
        currUser = User.objects.get(username=request.session["username"])
        my_message = Notification.objects.filter(user = currUser)

        return render(request,'home/notifications.html',{'messages' : my_message})
    return redirect('indexx')



def delete_notify(request,msgId):
    # Delete notifications
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
    # Rating  Implementaion for Posts
    if "username" in request.session:
        id = request.GET.get('rateid')
        ratingValue = request.GET.get('value')
        print(id,ratingValue)

        if ratingValue:
            currUser = User.objects.get(username=request.session["username"])
            Post.rateNow(id,currUser,ratingValue)

            post=Post.objects.get(id=id)

            if post.user.username != currUser.username:
                msg = str(request.session["username"]) +" just rated your post : "+str(ratingValue)+" star"
                to = User.objects.get(username=post.user.username)
                newNotify = Notification(user=to,message=msg,which="post",getid=id)
                Notification.save(newNotify)

            currPost = Post.objects.get(id=id)
            avg = currPost.avgRating
            
            resp = {
            'avg':avg
            }
            response = json.dumps(resp)
            return HttpResponse(response, content_type="application/json")
        


def comments(request):
    # Commments are fetched here for posts
    msg=request.GET.get("comment")
    post=Post.objects.get(pk=request.GET.get("postid"))
    user=User.objects.get(username=request.session['username'])
    comment=Comments(user=user,post=post,comment=msg)
    comment.save()
    time=comment.time
    time=str(time.strftime("%b, %d-%m-%y %I:%M %p"))

    if post.user.username != user.username:
        msgs = str(request.session["username"]) +" commented on your post"
        to = User.objects.get(username=post.user.username)
        newNotify = Notification(user=to,message=msgs,which="post",getid=request.GET.get("postid"))
        Notification.save(newNotify)

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
    # reporting posts backend
    if "username" in request.session:
        id = request.GET.get('postid')
        currPost = Post.objects.get(pk=id)
        currUser = User.objects.get(username=request.session["username"])

        currPost.reported(currUser,id)

        msg = str(request.session["username"]) +" just reported your post"
        newNotify = Notification(user=currUser,message=msg,which="post",getid=id)
        Notification.save(newNotify)

        # Check if this post has crossed report threshold----if yes then delete it...!!
        report_count = currPost.report.count()

        if report_count > 3:
            print("report")
            post_user = User.objects.get(username=currPost.user.username)
            msg = "Hey "+str(currPost.user.username)+",Gamers's community had reported one of your post in huge number....so it has been deleted permanently"
            addMsg = Notification(user=post_user,message=msg)
            Notification.save(addMsg)
            currPost.delete()

        resp={

        }
        response = json.dumps(resp)
        return HttpResponse(response, content_type="application/json") 

    else:
        return redirect('indexx')


def forgot(request):
    # Fetches forgot template after main implementaion of forgot
    return render(request,'home/forgot.html')



def manage_forgot(request):
    # Main Implementaion of forgot password
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
    # Sents money from current user
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
    # Checks before sending money
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


def userposts(request,usern):

    if "username" in request.session:
        currUser = User.objects.get(username=request.session["username"])
        usern = User.objects.get(username = usern)
        followerObj = Followers.objects.filter(user=usern)

        if followerObj:
            is_follower = followerObj[0].follower.all()

            if currUser in is_follower:
                user_posts = Post.objects.filter(user=usern)

                liked_posts = []
                rated_posts = []
                reported_posts = []
                name = request.session["username"]

                for post in user_posts:
                    is_liked = post.likes.filter(username=name)
                    is_rated = post.raters.filter(username=name)
                    is_reported = post.report.filter(username=name)

                    if is_liked:
                        liked_posts.append(post)
                    if is_rated:
                        rated_posts.append(post)
                    if is_reported:
                        reported_posts.append(post)
                
                comments = Comments.objects.all()

                return render(request,'home/userpost_searched.html',{'posts': user_posts , 'profusername':usern.username, 'username':currUser.username,
                                      'liked_posts':liked_posts , 'rated_posts':rated_posts , 'reported_posts':reported_posts , 
                                        'comments':comments})

        return redirect('indexx')

    return redirect('indexx')



def topPost(request):
    # fetches Trending Post
    posts = Post.objects.all()
    all_posts = list(posts)
    total = len(all_posts)
    #print(total)

    loggedIn = 0

    if "username" in request.session:
        loggedIn = 1

    for i in range(0,total-1):
        
        for j in range(i+1,total):

            rating1 = int(all_posts[i].likes.count() + 1) * float(all_posts[i].avgRating + 1)
            rating2 = int(all_posts[j].likes.count() + 1) * float(all_posts[j].avgRating + 1)
            print(rating1," ",rating2)
            if rating1 < rating2:
                all_posts[i] , all_posts[j] = all_posts[j] , all_posts[i]

    return render(request,'home/topPosts.html' , {'posts': all_posts , 'loggedIn':loggedIn})




def seePost(request,postid):

    f = Post.objects.filter(id=postid)
    if not f:
        return HttpResponse("this post no longer exists")
    # See posts in notifications
    currPost = Post.objects.get(id=postid)    

    is_liked = 0 
    loggedIn = 0
    is_rated = 0
    is_reported = 0
    same = 0
    if "username" in request.session:
        name=request.session["username"]
        loggedIn = 1
        liked = currPost.likes.filter(username=name)
        rated = currPost.raters.filter(username=name)
        reported = currPost.report.filter(username=name)

        if liked:
            is_liked=1
        if rated:
            is_rated=1
        if reported:
            is_reported=1
        if currPost.user.username==name:
            same=1
    comments = Comments.objects.all()

    return render(request,'home/seePost.html',{'post':currPost , 'is_liked':is_liked , 'is_rated':is_rated , 'is_reported':is_reported,
                            'same':same , 'comments':comments , 'loggedIn':loggedIn})



def popularity(request):
    # Users Popularity
    if request.method=='POST':
        to_whom = request.POST.get('to_whom')
        popularity_val = request.POST.get('popularity')

        currName = request.session["username"]
        currUser_obj = User.objects.get(username=currName)

        toUser_obj = User.objects.get(username=to_whom)

        if int(currUser_obj.coins) < int(popularity_val)*2:
            return HttpResponse("<h1>Action Failed as u do not have enough coins</h1>")

        else:
            toUser_obj.popularity = int(toUser_obj.popularity) + int(popularity_val)
            toUser_obj.save()

            currUser_obj.coins = int(currUser_obj.coins) - int(popularity_val)*2
            currUser_obj.save()

            # Send notification to user
            msg = "Hey "+str(to_whom)+" , "+str(currName)+" just gave you "+str(popularity_val)+" popularity...!!"
            addMsg = Notification(user=toUser_obj,message=msg)
            Notification.save(addMsg)

            return redirect(request.META['HTTP_REFERER'])

    else:
        return redirect('indexx')



def getUserRating(user):
    #Gets User Rating
    rating = 0.000
    user_posts = Post.objects.filter(user=user)
    total = len(user_posts)

    avg=0.000

    for post in user_posts:
        avg = avg + float(post.avgRating)
    
    if total:
        avg = round( (float(avg)/total) , 3)


    rating = ( (avg*5+1) *  int(user.popularity+1) )
    print(user.username," ",rating)
    return rating



def topGamers(request):
    # Fetches top Gamers based on rating
    all_users = list(User.objects.all())
    lenUsers = len(all_users)

    for i in range(0,lenUsers-1):
        for j in range(i+1,lenUsers):
            
            if getUserRating(all_users[i]) < getUserRating(all_users[j]):
                all_users[i] , all_users[j] = all_users[j] , all_users[i]

    loggedIn = 0

    if "username" in request.session:
        loggedIn = 1


    count = 1
    for i in all_users:
        # Update rank of users
        i.rank = count
        i.save()
        count+=1

    return render(request,'home/topGamer.html',{'rankers':all_users , 'loggedIn':loggedIn})




    

