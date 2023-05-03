from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import profile ,branch, company, posts, cgpa, application_details
import datetime
import pytz

# Create your views here.

def index(request) :
    if not request.user.is_authenticated : 
        return render(request, "rec/index.html")
    else :
        return HttpResponseRedirect(reverse(home))
    

def register_poc(request) :
    if not request.user.is_authenticated:
        if request.method == "POST" :
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]

            if password != confirm_password :
                return render(request, "rec/register.html", {
                    "message" : "Password does not match"
                })
            
            try : 
                user = User.objects.create_user(username, email, password)
                user.groups.set("2")
                user.save()

            except IntegrityError:
                return render(request, "rec/register.html", {
                    "message" : "A user with that username already exist"
                })
            
            login(request, user)
            return HttpResponseRedirect(reverse(create_profile))

        else:
            return render(request, "rec/register.html")
    else:
        return HttpResponseRedirect(reverse(home))

def login_view(request) :
    if not request.user.is_authenticated:
        if request.method == "POST" :
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None :
                login(request, user)
                return HttpResponseRedirect(reverse(index))
            else :
                return render(request, "rec/login.html", {
                    "message" : "Invalid username and/or password."
                })
            
        else :
            return render(request, "rec/login.html")
    else :
        return HttpResponseRedirect(reverse(home))
    
def logout_view(request) :
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse(index))

def home(request) :
    if request.user.is_authenticated and profile.objects.filter(student = request.user).exists() :
        all_post = posts.objects.all()
        for post in all_post :
            if post.open_date == None or post.deadline == None :
                post.is_active = False
            elif post.open_date <= datetime.datetime.now() and post.deadline >=datetime.datetime.now() :
                post.is_active = True
            else :
                post.is_active = False
            post.save()

        get_branch = request.user.profile.choose_branch
        get_cgpa = request.user.profile.student_cgpa
        get_post = cgpa.objects.filter(cutoff_cgpa__lte =get_cgpa, cgpa_branch = get_branch)
        time_left = []
        post_available = []
        for i in get_post:
            if i.post.is_active and i.post.comp.isactive :
                post_available.append(i)
        special_access = False
        is_poc = False
        if request.user.groups.filter(name = "Admin").exists() or request.user.is_superuser :
            special_access = True 
        if request.user.groups.filter(name = "POC").exists() :
            is_poc = True
        # get_comp = company.objects.filter(branches_open = get_branch)

        # get_post = posts.objects.filter(branch_open = get_branch)
        # for each_post in get_post :
        #     cutoff_cgpa = cgpa.objects.get(cgpa_branch = get_branch, post = each_post )
        d = []
        get_profile = profile.objects.get(student = request.user)
        for i in time_left :
            d.append(i.days)
        return render(request, "rec/home.html",{
            "posts" : post_available,
            "length" : len(post_available),
            "profile" : get_profile,
            "time_left" : time_left,
            "days_left" : d,
            "special_access" : special_access,
            "is_poc" : is_poc
        })
    else :
         return HttpResponseRedirect(reverse(create_profile))
    
def create_profile(request) :
    if request.user.is_authenticated:
        if request.method == "POST" :
            user = request.user
            firstname = request.POST["firstname"]
            lastname = request.POST["lastname"]
            branch_id = request.POST["branch"]
            getbranch = branch.objects.get(id = branch_id) 
            rollno = request.POST["rollno"]
            get_cgpa = request.POST["cgpa"]
            if not rollno or not branch_id or not get_cgpa :
                return HttpResponseRedirect(reverse(create_profile))
            try :
                new_profile = profile(
                    student = user,
                    firstname = firstname,
                    lastname = lastname,
                    register_no = rollno,
                    choose_branch = getbranch,
                    student_cgpa = get_cgpa
                )
                new_profile.profile_pic = request.FILES.get('profile_pic', '../media/users/user_avtar.webp')
                new_profile.resume = request.FILES.get('resume', False) 
                new_profile.save()

            except IntegrityError :
                getprofile = profile.objects.get(student = user)
                getprofile.choose_branch = branch_id
                getprofile.firstname = firstname
                getprofile.lastname = lastname
                getprofile.register_no = rollno
                getprofile.save()
            return HttpResponseRedirect(reverse(home))
        else : 
            branches = branch.objects.all()
            return render(request, "rec/profile.html", {
                "branches" : branches,
            })
    else :
        return HttpResponseRedirect(reverse(index))

def add_poc(request) :
    if request.user.is_superuser == True or request.user.groups.filter(name = "Admin").exists() :
        if request.method == "POST" :
            user_id = request.POST["user_id"]
            poc_user = User.objects.get(id = user_id)
            if not poc_user.groups.filter(name="POC").exists() and request.user.is_superuser :
                poc_user.groups.set("1")
                poc_user.save()
            elif poc_user.groups.filter(name="POC").exists() and request.user.is_superuser :
                poc_user.groups.set("2")
                poc_user.save()

            elif request.user.groups.filter(name = "Admin").exists() and not request.user.is_superuser and poc_user.groups.filter(name="POC").exists() :
                poc_user.groups.set("2")
                poc_user.save()

            elif request.user.groups.filter(name = "Admin").exists() and not request.user.is_superuser and poc_user.groups.filter(name="student").exists() :
                poc_user.groups.set("1")
                poc_user.save()

            
            return HttpResponseRedirect(reverse(add_poc))
        
        else :
            users = User.objects.all()
            return render(request, "rec/addpoc.html", {
                "users" : users,
                "profile" : request.user.profile
            })
    
    else :
        return HttpResponseRedirect(reverse(home))
    
def add_admin(request) :
    if request.user.is_superuser == True :
        if request.method == "POST" :
            user_id = request.POST["user_id"]
            admin_user = User.objects.get(id = user_id)
            if admin_user.groups.filter(name = "student").exists() or admin_user.groups.filter(name = "POC").exists() :
                admin_user.groups.set("3")
                admin_user.save()
            else :
                admin_user.groups.set("2")
                admin_user.save()
            return HttpResponseRedirect(reverse(add_poc))
        
        else :
            users = User.objects.all()
            return render(request, "rec/addpoc.html", {
                "users" : users
            })
    
    else :
        return HttpResponseRedirect(reverse(home))
    
def add_company(request) :
    if request.user.is_authenticated :
        if request.user.is_superuser or request.user.groups.filter(name = "Admin").exists() :
            if request.method == "POST" :
                name = request.POST["name"]
                des = request.POST["description"]
                poc_id = request.POST['poc']
                isactive = request.POST.get('isactive', False)
                if isactive :
                    isactive = True
                else :
                    isactive = False
                get_poc = User.objects.get(id = poc_id, groups = "1")
                br = branch.objects.all()
                l = []
                for i in br :
                    if request.POST.get(f'{i.name}', False) :
                        l.append(i)
                if not name :
                    return HttpResponseRedirect(reverse(add_company))
                else :
                    new_comp = company(
                        name = name,
                        description = des,
                        poc = get_poc,
                        isactive = isactive
                    )
                    
                    new_comp.save()
                    
                    for i in l :
                        new_comp.branches_open.add(i)
                       

                    return HttpResponseRedirect(reverse(add_post, args=(new_comp.id, )))

            else :
                pocs = User.objects.filter(groups = "1")
                branches = branch.objects.all()
                return render(request, "rec/addcomp.html", {
                    "pocs" : pocs,
                    "branches" : branches
                })
            
def add_post(request, id) :
    if request.user.is_authenticated :
        if request.user.is_superuser or request.user.groups.filter(name = "Admin").exists() :
            if request.method == "POST" :
                get_post = request.POST['post']
                package = request.POST['package']
                comp = company.objects.get(id = id)
                open_date = request.POST['open_date']
                open_time = request.POST['open_time']
                deadline_date = request.POST['deadline_date']
                deadline_time = request.POST['deadline_time']
                description = request.POST['description']
                # open_date_time = datetime(open_date, open_time)
                br = branch.objects.all()
                l = []
                for i in br :
                    if request.POST.get(f'{i.name}', False) :
                        l.append(i)

                if not get_post or not package or len(l) == 0 :
                    return HttpResponseRedirect(reverse(add_post, args=(id, )))
                
                new_post = posts(
                    role = get_post,
                    package = package,
                    comp = comp,
                    description = description
                )
                if open_date :
                    new_post.open_date = open_date + " "+open_time
                if deadline_date :
                    new_post.deadline = deadline_date + " " + deadline_time

                new_post.save()
                for i in l :
                        new_post.branch_open.add(i)

                for i in l :
                    if request.POST.get(f'{i.name}branch', False) :
                        get_cgpa = request.POST.get(f'{i.name}branch', False)
                    else :
                        get_cgpa = 0

                    new_cgpa = cgpa(
                        cutoff_cgpa = get_cgpa,
                        cgpa_branch = i,
                        post = new_post
                    )
                    new_cgpa.save()
                    

                return HttpResponseRedirect(reverse(add_post, args=(id, )))
            else :
                branches = branch.objects.all()
                comp = company.objects.get(id = id)
                return render(request, "rec/addpost.html", {
                    "ids" : id,
                    "comp" : comp,
                    "branches" : branches,
                    "currenttime" : datetime.datetime.now(),
                    "profile" : request.user.profile
                })
            
def editcomp(request, id) :
    if request.user.is_authenticated :
        get_comp = company.objects.get(id = id)
        if request.user.is_superuser or request.user.groups.filter(name = "Admin").exists() or get_comp.poc == request.user :
            if request.method == "POST" :
                name = request.POST['name']
                des = request.POST['description']
                poc_id = request.POST['poc']
                activate = request.POST.get('activate', False)
                deactivate = request.POST.get('deactivate', False)

                poc = User.objects.get(id = poc_id, groups = "1")
                if name :
                    get_comp.name = name
                if des :
                    get_comp.description = des
                if poc :
                    get_comp.poc = poc
                if activate :
                    get_comp.isactive = True
                if deactivate :
                    get_comp.isactive = False
                get_comp.save()
                return HttpResponseRedirect(reverse(companyview, args=(id, )))

            else :
                get_comp = company.objects.get(id = id)
                pocs = User.objects.filter(groups = "1")
                branches = branch.objects.all()
                return render(request, "rec/editcomp.html",{
                    "comp" : get_comp,
                    "ids" : get_comp.id,
                    "pocs" : pocs,
                    "branches" : branches,
                    "profile" : request.user.profile
                })
            
def companyview(request, id) :
    if request.user.is_authenticated :
        get_comp = company.objects.get(id = id) 
        can_edit = False
        if request.user.is_superuser or  request.user.groups.filter(name = "Admin").exists() or get_comp.poc == request.user :
            can_edit = True
        return render(request, "rec/viewcompany.html",{
            "comp" : get_comp,
            "profile" : request.user.profile,
            "canedit" : can_edit
        })
    
def delete_post(request, id) :
    if request.user.is_authenticated :
        if request.user.is_superuser or request.user.groups.filter(name = "Admin").exists() or request.user.groups.filter(name = "POC").exists() :
            get_post = posts.objects.get(id = id)
            comp_id = get_post.comp.id
            get_post.delete()
            return HttpResponseRedirect(reverse(add_post, args=(comp_id, )))
        
def post_view(request, id) :
    if request.user.is_authenticated :
        get_post = posts.objects.get(id = id)
        get_branch = request.user.profile.choose_branch
        eligible = False
        can_edit = False
        if get_post.comp.isactive :
            if get_branch in get_post.branch_open.all() :
                get_cgpa = get_post.cutoff_cgpa.get(cgpa_branch = get_branch)
                if get_cgpa.cutoff_cgpa <= request.user.profile.student_cgpa :
                    eligible = True
        if request.user.is_superuser or  request.user.groups.filter(name = "Admin").exists() or get_post.comp.poc == request.user :
            can_edit = True
        
        return render(request, "rec/viewpost.html",{
            "post" : get_post,
            "eligible" : eligible,
            "profile" : request.user.profile,
            "canedit" : can_edit
        })
    
def application(request, id) :
    if request.user.is_authenticated :
        if request.method == "POST" :
            get_post = posts.objects.get(id = id)
            
            if get_post.is_active == False or get_post.comp.isactive == False:
                return HttpResponseRedirect(reverse(home))
            if get_post.open_date >= datetime.datetime.now() or get_post.deadline <= datetime.datetime.now() :
                return HttpResponseRedirect(reverse(home))
            eligible_post = cgpa.objects.filter(cutoff_cgpa__lte =request.user.profile.student_cgpa, cgpa_branch = request.user.profile.choose_branch, post = get_post)
            if not eligible_post :
                return HttpResponseRedirect(reverse(home))
            get_application = application_details.objects.filter(applied_student = request.user, applied_post = get_post).exists()
            if get_application :
                return HttpResponseRedirect(reverse(home))

            get_description = request.POST['description']
            new_application = application_details(
                applied_student = request.user,
                applied_post = get_post,
                description = get_description,
                student_profile = request.user.profile
            )
            get_stu = User.objects.get(id = request.user.id)
            get_post.student.add(get_stu)
            new_application.save()
            return HttpResponseRedirect(reverse(home))

        else :
            get_post = posts.objects.get(id = id)
            if get_post.is_active == False or get_post.comp.isactive == False:
                return HttpResponseRedirect(reverse(home))
            if get_post.open_date >= datetime.datetime.now() or get_post.deadline <= datetime.datetime.now() :
                return HttpResponseRedirect(reverse(home))
            eligible_post = cgpa.objects.filter(cutoff_cgpa__lte =request.user.profile.student_cgpa, cgpa_branch = request.user.profile.choose_branch, post = get_post)
            if not eligible_post :
                return HttpResponseRedirect(reverse(home))
            get_application = application_details.objects.filter(applied_student = request.user, applied_post = get_post).exists()
            if get_application :
                return HttpResponseRedirect(reverse(home))
            return render(request, "rec/apply.html", {
                "post" : get_post,
                "profile" : request.user.profile
            })

def search_roll(request) :
    if request.method == "POST" :
        get_rollno = request.POST['roll']
        get_profile = profile.objects.filter(register_no = get_rollno)
        users = User.objects.all()
        return render(request, "rec/addpoc.html", {
            "users" : users,
            "profile" : request.user.profile,
            "get_user" : get_profile
        })
    
def viewallcompany(request) :

    get_allcompany = company.objects.all()
    special_access = False
    if request.user.groups.filter(name = "Admin").exists() or request.user.is_superuser :
        special_access = True
    return render(request, "rec/allcomp.html",{
        "companys" : get_allcompany,
        "profile" : request.user.profile,
        "special_access" : special_access
    })

def viewallapplications(request) :
    if request.user.is_superuser or request.user.groups.filter(name = "Admin").exists() :
        get_application = application_details.objects.all()
        return render(request, "rec/viewallapply.html", {
            "profile" : request.user.profile,
            "applications" : get_application,
            "special_access" : True
        })
    
def viewapply(request, id) :
    if request.user.is_authenticated :
        get_application = application_details.objects.get(id = id)
        if request.user == get_application.applied_student or request.user.is_superuser or request.user.groups.filter(name = "Admin").exists() or request.user == get_application.applied_post.comp.poc :
            return render(request, 'rec/vieweachapply.html', {
                "profile" : request.user.profile,
                "application" : get_application
            })
        else :
            return HttpResponseRedirect(reverse(home))

def appliedpost(request) :
    if request.user.is_authenticated :
        get_apply = application_details.objects.filter(applied_student = request.user)
        return render(request, "rec/appliedpost.html", {
            "appliedposts" : get_apply,
            "profile" : request.user.profile
        })
    
def allposts(request) :
    if request.user.is_authenticated :
        get_all_posts = posts.objects.all()
        return render(request, "rec/allposts.html", {
            "profile" : request.user.profile,
            "posts" : get_all_posts
        })
    

def addpost_edit(request, id) :
    if request.user.is_authenticated :
        if request.user.is_superuser or request.user.groups.filter(name = "Admin").exists() :
            if request.method == "POST" :
                get_post = request.POST['post']
                package = request.POST['package']
                comp = company.objects.get(id = id)
                open_date = request.POST['open_date']
                open_time = request.POST['open_time']
                deadline_date = request.POST['deadline_date']
                deadline_time = request.POST['deadline_time']
                # open_date_time = datetime(open_date, open_time)
                br = branch.objects.all()
                l = []
                for i in br :
                    if request.POST.get(f'{i.name}', False) :
                        l.append(i)

                if not get_post or not package or len(l) == 0 :
                    return HttpResponseRedirect(reverse(editcomp, args=(id, )))
                
                new_post = posts(
                    role = get_post,
                    package = package,
                    comp = comp
                )
                if open_date :
                    new_post.open_date = open_date + " "+open_time
                if deadline_date :
                    new_post.deadline = deadline_date + " " + deadline_time

                new_post.save()
                for i in l :
                        new_post.branch_open.add(i)

                for i in l :
                    if request.POST.get(f'{i.name}branch', False) :
                        get_cgpa = request.POST.get(f'{i.name}branch', False)
                    else :
                        get_cgpa = 0

                    new_cgpa = cgpa(
                        cutoff_cgpa = get_cgpa,
                        cgpa_branch = i,
                        post = new_post
                    )
                    new_cgpa.save()
                    

                return HttpResponseRedirect(reverse(editcomp, args=(id, )))
    

def assignedcomp(request) :
    if request.user.groups.filter(name = "POC").exists() :
        get_comp = company.objects.filter(poc = request.user)
        return render(request, "rec/assignedcomp.html",{
            "comps" : get_comp,
            "profile" : request.user.profile
        })

             
def editpost(request, id) :
    get_post = posts.objects.get(id = id)
    if request.user.is_superuser or request.user.groups.filter(name = "Admin").exists() or get_post.comp.poc == request.user :
        if request.method == "POST" :
            get_post_name = request.POST['name']
            # des = request.POST['des']
            open_date = request.POST['opendate']
            open_time = request.POST['opentime']
            deadline_date = request.POST['dead_date']
            deadline_time = request.POST['dead_time']
            package = request.POST['package']
            # is_active = request.POST['active']
            br = branch.objects.all()
            l = []
            for i in br :
                if request.POST.get(f'{i.name}', False) :
                    l.append(i)
            if get_post_name :
                get_post.role = get_post_name
                get_post.save()
            # if des :
            #     get_post.description = des
            if open_date and open_time:
                get_post.open_date = open_date+" "+open_time
                get_post.save()
            if open_date and not open_time :
                get_post.open_date = open_date+" "+"23:59"
                get_post.save()
            if deadline_date and deadline_time:
                get_post.deadline = deadline_date+" "+deadline_time
                get_post.save()

            if deadline_date and not deadline_time :
                get_post.deadline = deadline_date+" "+"23:59"
                get_post.save()

            if package :
                get_post.package = package
                get_post.save()

            if len(l) > 0 :
                get_post.branch_open.clear()
                get_cgpa_t = cgpa.objects.filter(post = get_post)
                get_cgpa_t.delete()
                for i in l :
                    get_post.branch_open.add(i)
                get_post.save()
        
                for i in l :
                    if request.POST.get(f'{i.name}branch', False) :
                        get_cgpa = request.POST.get(f'{i.name}branch', False)
                    else :
                        get_cgpa = 0

                    new_cgpa = cgpa(
                        cutoff_cgpa = get_cgpa,
                        cgpa_branch = i,
                        post = get_post
                    )
                    new_cgpa.save()
            return HttpResponseRedirect(reverse(post_view, args=(id, )))
        else :
            br = branch.objects.all()
            get_cgpa = cgpa.objects.filter(post = get_post)
            return render(request, "rec/editpost.html", {
                "post" : get_post,
                "profile" : request.user.profile,
                "branches" : br,
                "cgpa" : get_cgpa
            })
        
def self_profileview(request) :
    if request.user.is_authenticated :
        get_profile = request.user.profile
        return render(request, "rec/selfprofile.html", {
            "profile" : get_profile
        })
    
def public_profileview(request, username) :
    if request.user.is_authenticated :
        get_user = User.objects.get(username = username)
        return render(request, "rec/selfprofile.html", {
            "profile" : get_user.profile
        })