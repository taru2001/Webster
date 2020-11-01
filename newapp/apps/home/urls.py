from django.urls import path
from . import views,replies,streaming

urlpatterns = [
    path('index/',views.index,name="indexx"),
    path('register/',views.registerUser,name="register"),
    path('live_stream/',views.about,name="about"),
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logout,name="logout"),
    path('login/upload/',views.upload,name="upload"),
    path('login/mypost/',views.mypost,name="mypost"),
    path('login/mypost/delete/<int:postId>/',views.deletePost,name="delete"),
    path('playvideo/<int:postId>/',views.playvideo,name="playvideo"),
    path('profile/',views.profile,name="profile"),
    path('profile/edit',views.edit,name="edit"),
    path('profile/manage_edit',views.manage_edit,name="manage_edit"),
    path('search/',views.searchuser,name="searchuser"),
    path('changephoto/',views.changephoto,name="profilePic"),
    path('search/<str:user>/',views.search_profile,name="searchProfile"),
    path('handlefollow/<str:usern>/',views.follow,name="follow"),
    path('notify/',views.notify,name="notifications"),
    path('delNotify/<int:msgId>/',views.delete_notify,name="deleteMsg"),
    path('login/mypost/follow',views.likes,name="like_post"),
    path('rating/',views.rating,name="rating"),
    path('comments',views.comments,name="comment_post"),
    path('report/',views.report,name="report"),
    path('user/',views.userpage,name="user_home"),
    path('login/forgot/',views.forgot,name="forgot"),
    path('login/forgot/manage_forgot',views.manage_forgot,name='manage_forgot'),
    path('sendmoney/<str:usern>',views.sendmoney,name="sendmoney"),
    path('event/',views.events,name="event"),
    path('handlepayment/',views.handlepayment,name="handlepayment"),
    path('posts/<str:usern>/',views.userposts,name="userposts"),

    path('topPost/',views.topPost,name="topPost"),
    path('seepost/<int:postid>/',views.seePost,name="seePost"),

    path('givePopularity/',views.popularity,name="popularity"),

    path('topGamers/',views.topGamers,name="topGamers"),
    path('Comments/replies',replies.replies,name='replies'),
    path('deletereply/',replies.delete_reply,name="deletereply"),
    path('closeall/',views.closeall,name="closeall"),

    path('check/',streaming.check,name="check"),
    path('render/',streaming.renders,name="render"),
    path('getstream/',streaming.getstream,name="getstream"),

    path('checkUsername/',views.check_unique,name="checkUsername")
    
]