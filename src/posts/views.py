from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import PostForm
from .models import Post, Author

def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    latest = Post.objects.order_by('-timestamp')[0:4]
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()

    context = {
        'latest': latest,
        'queryset': queryset
    }
    return render(request, 'search_results.html', context)


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:4]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 2)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'object_list': featured,
        'queryset': paginated_queryset,
        'latest': latest,
        'page_request_var': page_request_var
    }
    return render(request, 'index.html', context)

def post(request, id):
    single = Post.objects.get(id=id)

    next_post = Post.objects.filter(id__gt=single.id).order_by('id').first()
    previous_post = Post.objects.filter(id__lt=single.id).order_by('id').last()

    post = get_object_or_404(Post, id=id)

    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post
    }
    return render(request, 'post.html', context)

def information(request):
    latest = Post.objects.order_by('-timestamp')[0:4]
    context = {
        'latest': latest,
    }
    return render(request, 'information.html', context)

def contact(request):
    latest = Post.objects.order_by('-timestamp')[0:4]
    context = {
        'latest': latest,
    }
    return render(request, 'contact.html', context)

def social_media(request):
    latest = Post.objects.order_by('-timestamp')[0:4]
    context = {
        'latest': latest,
    }
    return render(request, 'social_media.html', context)


def post_create(request):
    title = 'Stwórz'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))

    context = {
        'title': title,
        'form': form
    }

    return render(request, "post_create.html", context)


def post_update(request, id):
    title = 'Edytuj'
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': form.instance.id
            }))

    context = {
        'title': title,
        'form': form
    }

    return render(request, "post_create.html", context)



def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("index"))

