from rest_framework import fields, serializers
from .models import Profile, Project_Post

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_Post
        fields = [
            "title", 
            "img_post", 
            "description",
            "project_url",
            "posted_by",
            "posted_on",   
        ]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "user",
            "profile_pic",
            "bio",
            "email",
            "updated_on",
        ]