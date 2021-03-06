from django.shortcuts import render,get_object_or_404
from .models import Post
from django.views.generic import ListView
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import EmailPostForm
from django.core.mail import send_mail

class PostListView(ListView):
 queryset = Post.published.all()
 context_object_name = 'posts'
 paginate_by = 3
 template_name = 'blog/list.html'

'''
def post_list(request):
    posts_object_list = Post.published.all()
    paginator = Paginator(posts_object_list,3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)        
    return render(request,'blog/list.html',{'page':page,'posts': posts})

    inside list.html:-->
         {% include "pagination.html" with page=posts %}
'''
def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug,status='published',publish__year=year,publish__month=month,publish__day=day)
    return render(request,'blog/detail.html',{'post': post})  


def post_share(request, post_id):
    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False
    if request.method == 'POST':
    # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
        # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            to=cd['to']
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'rakibulr312@gmail.com', [to])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/share.html', {'post': post,'form': form,'sent': sent})