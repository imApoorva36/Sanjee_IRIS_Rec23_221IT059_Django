from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register_poc, name = "register_poc"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),
    path("profile/", views.create_profile, name="profile"),
    path("addpoc/", views.add_poc, name = 'addpoc'),
    path("addadmin/", views.add_admin, name="addadmin"),
    path("addcomp/", views.add_company, name="addcomp"),
    path("addpost/<int:id>", views.add_post, name="addpost"),
    path("editcomp/<int:id>", views.editcomp, name="editcomp"),
    path("viewcomp/<int:id>", views.companyview, name="viewcomp"),
    path("deleting_the_selected_post/<int:id>", views.delete_post, name="deletepost"),
    path("viewpost/<int:id>", views.post_view, name="viewpost"),
    path("apply/<int:id>", views.application, name="apply"),
    path("search/", views.search_roll, name="search"),
    path("allcomp/", views.viewallcompany, name="allcomp"),
    path("viewallapplications/", views.viewallapplications, name="viewallapplications"),
    path("viewapply/<int:id>", views.viewapply, name="viewapply"),
    path("applied_posts/", views.appliedpost, name="appliedpost"),
    path("allposts/", views.allposts, name="allposts"),
    path("addpost_edit/<int:id>", views.addpost_edit, name="addpost_edit"),
    path("assignedcomp/", views.assignedcomp, name="assignedcomp" ),
    path("editpost/<int:id>", views.editpost, name="editpost"),
    path("profile_view/", views.self_profileview, name="profile_view"),
    path("public_profile_view/<str:username>", views.public_profileview, name="public_profile_view"),
]