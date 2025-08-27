from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import F, Q, Count, Sum
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import Http404
import json

from .models import Question, Choice, Category, Article, Tag, Person

# Create your views here.

# Function-based Views
def index(request):
    """Display latest poll questions with pagination and search"""
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category', '')
    
    # Base queryset
    questions = Question.objects.filter(is_active=True).select_related('author', 'category')
    
    # Apply search filter
    if search_query:
        questions = questions.filter(
            Q(question_text__icontains=search_query) |
            Q(choices__choice_text__icontains=search_query)
        ).distinct()
    
    # Apply category filter
    if category_filter:
        questions = questions.filter(category__slug=category_filter)
    
    # Order by publication date
    questions = questions.order_by('-pub_date')
    
    # Pagination
    paginator = Paginator(questions, 5)  # Show 5 questions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter dropdown
    categories = Category.objects.filter(is_active=True)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'total_questions': paginator.count,
    }
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """Display a specific question and its choices"""
    question = get_object_or_404(Question, pk=question_id, is_active=True)
    
    # Increment views count (if you add a views field)
    # Question.objects.filter(pk=question_id).update(views=F('views') + 1)
    
    context = {
        'question': question,
        'choices': question.choices.all(),
        'total_votes': question.total_votes(),
    }
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    """Display voting results for a question"""
    question = get_object_or_404(Question, pk=question_id)
    
    # Get choices with vote percentages
    choices_with_percentages = []
    total_votes = question.total_votes()
    
    for choice in question.choices.all():
        percentage = choice.vote_percentage()
        choices_with_percentages.append({
            'choice': choice,
            'percentage': percentage,
        })
    
    context = {
        'question': question,
        'choices_with_percentages': choices_with_percentages,
        'total_votes': total_votes,
    }
    return render(request, 'polls/results.html', context)


@require_POST
def vote(request, question_id):
    """Handle voting for a question"""
    question = get_object_or_404(Question, pk=question_id)
    
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form with error message
        context = {
            'question': question,
            'error_message': "You didn't select a choice.",
        }
        return render(request, 'polls/detail.html', context)
    else:
        # Increment vote count using F() to avoid race conditions
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        selected_choice.refresh_from_db()  # Get updated value
        
        messages.success(request, f'Your vote for "{selected_choice.choice_text}" has been recorded!')
        
        # Always return an HttpResponseRedirect after successfully dealing with POST data
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


# AJAX vote endpoint
@csrf_exempt
@require_POST
def vote_ajax(request, question_id):
    """Handle AJAX voting"""
    if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    try:
        data = json.loads(request.body)
        choice_id = data.get('choice_id')
        
        question = get_object_or_404(Question, pk=question_id)
        choice = get_object_or_404(Choice, pk=choice_id, question=question)
        
        # Update vote count
        choice.votes = F('votes') + 1
        choice.save()
        choice.refresh_from_db()
        
        # Return updated vote counts
        choices_data = []
        total_votes = question.total_votes()
        
        for c in question.choices.all():
            choices_data.append({
                'id': c.id,
                'text': c.choice_text,
                'votes': c.votes,
                'percentage': c.vote_percentage(),
            })
        
        return JsonResponse({
            'success': True,
            'message': f'Vote recorded for "{choice.choice_text}"',
            'choices': choices_data,
            'total_votes': total_votes,
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


# Class-based Views
class QuestionListView(generic.ListView):
    """Class-based view for listing questions"""
    model = Question
    template_name = 'polls/question_list.html'
    context_object_name = 'questions'
    paginate_by = 10
    
    def get_queryset(self):
        return Question.objects.filter(is_active=True).select_related('author', 'category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        return context


class QuestionDetailView(generic.DetailView):
    """Class-based view for question detail"""
    model = Question
    template_name = 'polls/question_detail.html'
    context_object_name = 'question'
    
    def get_queryset(self):
        return Question.objects.filter(is_active=True)


class CategoryListView(generic.ListView):
    """List all categories"""
    model = Category
    template_name = 'polls/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.filter(is_active=True).annotate(
            question_count=Count('question', filter=Q(question__is_active=True))
        )


class CategoryDetailView(generic.DetailView):
    """Show questions in a specific category"""
    model = Category
    template_name = 'polls/category_detail.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        questions = Question.objects.filter(
            category=category,
            is_active=True
        ).select_related('author').order_by('-pub_date')
        
        # Pagination
        paginator = Paginator(questions, 10)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['page_obj'] = page_obj
        return context


# Advanced Views with Mixins
class QuestionCreateView(LoginRequiredMixin, generic.CreateView):
    """Create new question (requires login)"""
    model = Question
    fields = ['question_text', 'category']
    template_name = 'polls/question_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        messages.success(self.request, 'Question created successfully!')
        return reverse('polls:detail', kwargs={'question_id': self.object.pk})


class QuestionUpdateView(LoginRequiredMixin, generic.UpdateView):
    """Update existing question (requires login and ownership)"""
    model = Question
    fields = ['question_text', 'category', 'is_active']
    template_name = 'polls/question_form.html'
    
    def get_queryset(self):
        # Only allow users to edit their own questions
        return Question.objects.filter(author=self.request.user)
    
    def get_success_url(self):
        messages.success(self.request, 'Question updated successfully!')
        return reverse('polls:detail', kwargs={'question_id': self.object.pk})


class QuestionDeleteView(LoginRequiredMixin, generic.DeleteView):
    """Delete question (requires login and ownership)"""
    model = Question
    template_name = 'polls/question_confirm_delete.html'
    success_url = reverse_lazy('polls:index')
    
    def get_queryset(self):
        return Question.objects.filter(author=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Question deleted successfully!')
        return super().delete(request, *args, **kwargs)


# API-like Views
def api_questions(request):
    """Return questions as JSON"""
    questions = Question.objects.filter(is_active=True).select_related('author', 'category')
    
    data = []
    for question in questions[:20]:  # Limit to 20 questions
        data.append({
            'id': question.id,
            'text': question.question_text,
            'pub_date': question.pub_date.isoformat(),
            'author': question.author.username if question.author else None,
            'category': question.category.name if question.category else None,
            'total_votes': question.total_votes(),
            'choices': [
                {
                    'id': choice.id,
                    'text': choice.choice_text,
                    'votes': choice.votes,
                } for choice in question.choices.all()
            ]
        })
    
    return JsonResponse({'questions': data})


# Statistics View
def stats(request):
    """Display polling statistics"""
    total_questions = Question.objects.filter(is_active=True).count()
    total_votes = Choice.objects.aggregate(total=Sum('votes'))['total'] or 0
    total_categories = Category.objects.filter(is_active=True).count()
    
    # Recent activity
    recent_questions = Question.objects.filter(is_active=True).order_by('-pub_date')[:5]
    
    # Category statistics
    category_stats = Category.objects.filter(is_active=True).annotate(
        question_count=Count('question', filter=Q(question__is_active=True)),
        total_votes=Sum('question__choices__votes', filter=Q(question__is_active=True))
    ).order_by('-question_count')
    
    context = {
        'total_questions': total_questions,
        'total_votes': total_votes,
        'total_categories': total_categories,
        'recent_questions': recent_questions,
        'category_stats': category_stats,
    }
    
    return render(request, 'polls/stats.html', context)
