from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete =models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile/",default = "default.jpg")
    bio = HTMLField()
    updated_on = models.DateTimeField(auto_now_add=True)

class Project_Post(models.Model):
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    img_project = models.ImageField(upload_to="project/")
    project_url = models.URLField()
    description = HTMLField()
    posted_on = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100,blank=True)
    
    
    def get_all_projects():
        projects = Project_Post.objects.all()
        return projects
    
    @classmethod
    def get_project_by_id(cls,id):
        project = Project_Post.objects.filter(id=id)
        
        return project
        

class Reviews(models.Model):
    review = HTMLField()
    posted_by = models.ForeignKey(User,on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True)
    project_id = models.ForeignKey(Project_Post,on_delete=models.CASCADE)
    
    
    
    @classmethod
    def get_review_by_project_id(cls,id):
        projects = cls.objects.filter(project_id = id)
        
        return projects
    

class Rates(models.Model):
    design = models.IntegerField(default = 1)
    rate_by = models.ForeignKey(User,on_delete=models.CASCADE)
    rate_on = models.DateTimeField(auto_now_add=True)
    project_id = models.ForeignKey(Project_Post,on_delete=models.CASCADE)
    content = models.IntegerField(default = 1)
    usability = models.IntegerField(default = 1)
    
    @classmethod
    def get_rates_by_project_id(cls,id):
        projects_rates = cls.objects.filter(project_id = id)
        
        return projects_rates