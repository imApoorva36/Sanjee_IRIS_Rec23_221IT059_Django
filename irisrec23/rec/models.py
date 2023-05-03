from django.db import models
from django.contrib.auth.models import User
# Create your models here.

Branch_choices = (
    ("CSE", "CSE"),
    ("IT", "IT"),
    ("AI", "AI"),
    ("CDS", "CDS"),
    ("ECE", "ECE"),
    ("EEE", "EEE"),
    ("MECH", "MECH"),
    ("CIVIL", "CIVIL"),
    ("MINING", "MINING"),
    ("META", "META")
)
Sem_choices = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
)
class branch(models.Model) :
    name = models.CharField(max_length=20, choices=Branch_choices)

    def __str__(self) :
        return self.name


class profile(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name="profile")
    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    register_no = models.CharField(max_length=10, null=True, blank=True)
    profile_pic = models.ImageField( default="../media/users/user_avtar.webp", null=True, blank=True, upload_to='users/')
    choose_branch = models.ForeignKey(branch, on_delete=models.CASCADE, blank=True, null=True, related_name="students")
    resume = models.FileField(null=True, blank=True)
    student_cgpa = models.FloatField(default=0, null=True, blank=True)
    sem = models.IntegerField(null=True, blank=True, choices=Sem_choices)
   
    def __str__(self) :
        return self.student.username
    
# class posts(models.Model) :
#     role = models.CharField(max_length=50, null=True, blank=True)
#     package = models.FloatField(null=True, blank=True)
#     student = models.ManyToManyField(User, blank=True, related_name="post")

#     def __str__(self) :
#         return self.role


class company(models.Model) :
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField()
    poc = models.ForeignKey(User, on_delete=models.CASCADE, related_name="company_poc")
    branches_open = models.ManyToManyField(branch, related_name="company", blank=True )
    isactive = models.BooleanField(default=True)
    applied = models.ManyToManyField(User, blank=True ,related_name="applied_company")
    
    def __str__(self) :
        return self.name
    
class posts(models.Model) :
    role = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    package = models.FloatField(null=True, blank=True)
    student = models.ManyToManyField(User, blank=True, related_name="post")
    comp = models.ForeignKey(company, on_delete=models.CASCADE, related_name="post", null=True, blank=True)
    branch_open = models.ManyToManyField(branch, blank=True, related_name="posts")
    cgpa_cutoff = models.FloatField(null=True, blank=True, default=0)
    open_date = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) :
        return self.role
    
class cgpa(models.Model) :
    cutoff_cgpa = models.FloatField(null=True, blank=True, default=0)
    cgpa_branch = models.ForeignKey(branch, on_delete=models.CASCADE, related_name="cutoff_cgpa", null=True, blank=True )
    post = models.ForeignKey(posts, on_delete=models.CASCADE, related_name="cutoff_cgpa", null=True, blank=True)

class application_details(models.Model) :
    applied_student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    applied_post = models.ForeignKey(posts, on_delete=models.CASCADE, related_name="applications_details")
    resume = models.FileField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    student_profile = models.ForeignKey(profile, on_delete=models.CASCADE, related_name="applied_posts")

    def __str__(self) :
        return self.applied_student.username