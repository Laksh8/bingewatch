from django.shortcuts import render,redirect
from .models import Videos,Comments,CommentLike,Category,profile,Reply
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.views import login_required

# Create your views here.
def home(request):
    videos = Videos.objects.all()
    if request.GET.get('search') is not None:
        search = request.GET.get('search')
        a = Videos.objects.all()
        videos = []
        for i in a:
            for j in search.lower().split():
                if j in i.title.lower():
                    if i not in videos:
                        videos.append(i)

        category = Category.objects.all()
        for i in category:
            for word in search.lower().split():
                if word in i.title.lower():
                    videos.append(Videos.objects.get(id=i.video.id))
        videos1 = videos
        try :
            for i in Videos.objects.filter(user=User.objects.get(username=request.GET.get('search'))):
                if i not in videos:
                    videos.append(i)
        except:
            videos = videos1
    return render(request,'blogapp/home.html',{'videos':videos,"error2" : "No result Found",})

def watch(request,id):
    video = Videos.objects.get(id=id)
    if request.user.is_authenticated:
        if request.method == 'POST':
            comment = Comments()
            comment.video = video
            comment.comment = request.POST['comment']
            comment.user = request.user
            comment.save()

    return render(request, 'blogapp/watch.html', {'video': video})


def comments(request,title):
    title = title.split('/')[-1]
    video = Videos.objects.get(id=int(title))
    comments = Comments.objects.filter(video=video.id)
    likes = []
    replys = []
    try:
        for comment in comments:

            if Reply.objects.filter(comment=comment):
                replys.append(Reply.objects.filter(comment=comment))
    except:
        pass
    if comments == None:
       return render(request,'blogapp/comments.html')

    #return render(request, 'blogapp/comments.html', {'video': video,'comments':comments})

    return render(request, 'blogapp/comments.html', {'video': video, 'comments': comments,'replys':replys,'likes':likes})



@login_required
def like(request,id):
    video = Videos.objects.get(id=id)
    comment = Comments.objects.get(video=video)
    comment_likes = CommentLike.objects.get(comment=comment)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def add_video(request):
    if request.method == 'POST':
        video = Videos()
        video.title,video.discreption,video.thumbnail,video.video = request.POST['title'],request.POST["discreption"],request.FILES['thumbnail'],request.POST['video']
        video.user = request.user
        video.save()
        return redirect('home')
    return render(request,'blogapp/add_video.html')

@login_required
def update_profile(request,id):
    if request.method == 'POST':

        try:
            pro = profile.objects.get(id=User.objects.get(id=id).profile.id)
            pro.delete()
            user = User()
            user.id = request.user.id
            user.first_name,user.last_name,user.profile.profile_discreption,user.profile.image = request.POST['first_name'],request.POST['last_name'],request.POST['profile_discreption'],request.FILES['image']
            user.profile.user=request.user
            user.save()
        except:
            pro = profile()
            pro.user = request.user
            pro.profile_discreption = request.POST['profile_discreption']
            pro.image = request.FILES['image']
            pro.save()

            user = User.objects.get(id=id)

            user.first_name, user.last_name = request.POST['first_name'], request.POST['last_name']
            user.save()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def reply(request,id):
    if request.method == 'POST':
        comment = Comments.objects.get(id=id)
        reply =Reply()
        reply.comment = comment
        reply.reply = request.POST['reply']
        reply.user = request.user
        reply.save()

    return redirect("/watch/"+str(comment.video.id))

@login_required
def commentlike(request,id):
    like = CommentLike.objects.get(like=request.user)
    if like:
        like.delete()
    else:
        like.comment = Comments.objects.get(id=id)
        like.like = request.user
        like.save()
    return redirect(request.META.get('HTTP_REFERER'))