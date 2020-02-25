from django.urls import path
from . import views

urlpatterns = [
    path('', views.index), #index page (login/register)
    path('success/<int:user_Val>', views.successDisplay), # create user success
    path('success/create', views.create_user), # go to the create page
    path('login/display', views.validate_login), # validate if the user exist
    path('logoutUser', views.logout), # successful logout
    path('notlogin', views.index), # checks if the user is login if not GETOUT 
    path('quotes/create', views.AddQuote),
    path('myaccount/<int:user_ID>', views.view_this_user),
    path('users/<int:this_user>', views.view_other_users),
    path('edit/<int:the_id>', views.editProcess),
    path('addlikes/<int:other_user_id>', views.putLikes),
    path('delete/post/<int:get_id>', views.delquote),
    path('delete/likes/<int:other_id>', views.unlikeButton),
]
