from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from .models import News, Review, Comment
from django.views.generic import CreateView
from django.urls import reverse_lazy

def home(request):
    """Главная страница с основными разделами"""
    news = News.objects.filter(is_published=True)[:3]  # Последние 3 новости
    reviews = Review.objects.filter(is_approved=True)[:5]  # Последние 5 одобренных отзывов
    return render(request, 'main/index.html', {
        'news': news,
        'reviews': reviews,
    })

def emergency_commissioner(request):
    return render(request, 'main/emergency_commissioner.html')

def independent_expertise(request):
    return render(request, 'main/independent_expertise.html')

def auto_lawyer(request):
    return render(request, 'main/auto_lawyer.html')

class NewsList(ListView):
    """Список всех опубликованных новостей"""
    model = News
    template_name = 'main/news_list.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        return News.objects.filter(is_published=True)

def news_detail(request, pk):
    news_item = News.objects.get(pk=pk, is_published=True)
    comments = news_item.comments.filter(is_approved=True)
    if request.method == 'POST':
        author_name = request.POST.get('author_name')
        content = request.POST.get('content')
        if author_name and content:
            Comment.objects.create(news=news_item, author_name=author_name, content=content, is_approved=False)
            messages.success(request, 'Спасибо за ваш комментарий! Он будет опубликован после проверки модератором.')
            return redirect('news_detail', pk=pk)
    return render(request, 'main/news_detail.html', {
        'news_item': news_item,
        'comments': comments,
    })

class ReviewCreate(CreateView):
    """Создание нового отзыва"""
    model = Review
    template_name = 'main/review_form.html'
    fields = ['author_name', 'content']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Спасибо за ваш отзыв! Он будет опубликован после проверки модератором.')
        return super().form_valid(form)
