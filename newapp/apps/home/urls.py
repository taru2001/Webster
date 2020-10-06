from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name="indexx"),
    path('register/',views.registerUser,name="register"),
    path('about/',views.about,name="about"),
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
    path('report/',views.report,name="report")
]