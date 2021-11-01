from django.http.response import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import Post_projectform,ReveiwForm,UpdateProfile,UserUpdateform
from django.contrib import messages
from .models import Project_Post,Profile,Reviews,Rates
from rest_framework.response import Response
from rest_framework.views import APIView
from .serialiers import ProfileSerializer,ProjectSerializer
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse


# @login_required(login_url='/accounts/login/')
def home(request):
    project = Project_Post.get_all_projects()
    return render(request,"home.html",{"project":project})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def post_project_view(request):
    if request.method =='POST':
        form = Post_projectform(request.POST,request.FILES)
        
        if form.is_valid():
            new_project = form.save(commit=False)
            new_project.posted_by = request.user
            new_project.save()
            return redirect('home')
        else:
            messages.info(request,'all fields are required')
            return redirect('post-project')
    
    else:
        form = Post_projectform()
    return render(request,'new_post.html',{"form":form})
    
@login_required
def post_review_view(request,id):
    
    form = ReveiwForm()
    reviews = Reviews.get_review_by_project_id(id)
    project = Project_Post.get_project_by_id(id)
    rates = Rates.get_rates_by_project_id(id)
    desrate = []
    usarate=[]
    conrate=[]
    if rates:
        for rate in rates:
            desrate.append(rate.design)
            usarate.append(rate.usability)
            conrate.append(rate.content)
        total = len(desrate)*9
        design =round(sum(desrate)/total *100,2)
        usability = round(sum(usarate)/total *100,2)
        content = round(sum(conrate),2)
        return render(request,'single_project.html',{"form":form,"reviews":reviews,"project":project,"project_id":id,"design":design,"usability":usability,"content":content})
    else:
        usability=0
        design = 0
        content = 0
        return render(request,'single_project.html',{"form":form,"reviews":reviews,"project":project,"project_id":id,"design":design,"usability":usability,"content":content})

        
@login_required   
def review_post(request,id):
    if request.method=='POST':
        form = ReveiwForm(request.POST)
        
        if form.is_valid():
            new_review=form.save(commit=False)
            new_review.posted_by = request.user
            project = Project_Post.objects.get(id=id)
            new_review.project_id = project
            new_review.save()
            return redirect('post-review',id)


@login_required
def post_rate_view(request,id):
    if request.method=='POST':
        rates = Rates.get_rates_by_project_id(id)
        for rate in rates:
            if rate.rate_by ==request.user:
                messages.info(request,'You have alraedy rated the project')
                return redirect('post-review', id)
        design = request.POST.get('design')
        usability = request.POST.get('usability')
        content = request.POST.get('content')
        
        if design and usability and content:
            project = Project_Post.objects.get(id=id)
            rate = Rates(design = design,usability = usability,content=content,project_id = project,rate_by=request.user)
            
            rate.save()
            return redirect('post-review',id)
    else:
        messages.info(request,'all fields are required')
        return redirect('post-review',id)
        
@login_required
def update_profile_view(request):
    if request.method =='POST':
        form = UpdateProfile(request.POST,request.FILES,instance=request.user.profile)
        userform = UserUpdateform(request.POST,instance=request.user)
        
        if form.is_valid() and userform.is_valid():
            form.save()
            userform.save()
            return redirect('profile')
    else:
        form = UpdateProfile(instance=request.user.profile)
        userform = UserUpdateform(instance=request.user)
    return render(request,"update_profile.html",{"form":form,"userform":userform})
        
@login_required
def profile(request):
    profile = Profile.objects.filter(user = request.user)
    projects = Project_Post.objects.filter(posted_by = request.user)
    
    return render(request,'profile.html',{"profile":profile,"projects":projects})

@login_required
def search_view(request):
    if request.method =='POST':
        title = request.POST['search']
        if Project_Post.objects.filter(title = title).first() is None:
            messages.info(request,'There is no project with that name')
            return redirect('home')
        else:
            proj = get_object_or_404(Project_Post, title = title)
            return redirect('post-rate',proj.id)
    else:
        messages.info(request,'Filling the input field')
        return redirect('home')
        
def nav(request):
    current_user = request.user
    return render(request,'navbar.html',{"current_user":current_user})

class ProfileList(APIView):
    def get(self,request,format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many = True)
        return Response(serializers.data)
    
    
class ProjectList(APIView):
    def get(self,request,format = None):
        all_projects = Project_Post.objects.all()
        serializers = ProjectSerializer(all_projects,many = True)
        return Response(serializers.data)
        


# @csrf_exempt
# def ProjectList(request,id=0):
#     if request.method=='GET':
#         projects = Project_Post.objects.all()
#         project_serializer = ProjectSerializer(projects, many=True)
#         return JsonResponse(project_serializer.data, safe=False)

#     elif request.method=='POST':
#         project_data=JSONParser().parse(request)
#         project_serializer = ProjectSerializer(data=project_data)
#         if project_serializer.is_valid():
#             project_serializer.save()
#             return JsonResponse("Added Successfully!!" , safe=False)
#         return JsonResponse("Failed to Add.",safe=False)
    
#     elif request.method=='PUT':
#         project_data = JSONParser().parse(request)
#         project=Project_Post.objects.get(ProjectId=project_data['ProjectId'])
#         project_serializer=ProjectSerializer(project,data=project_data)
#         if project_serializer.is_valid():
#             project_serializer.save()
#             return JsonResponse("Updated Successfully!!", safe=False)
#         return JsonResponse("Failed to Update.", safe=False)

#     elif request.method=='DELETE':
#         project=Project_Post.objects.get(ProjectId=id)
#         project.delete()
#         return JsonResponse("Deleted Succeffully!!", safe=False)



