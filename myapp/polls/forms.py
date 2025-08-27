from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.text import slugify
from .models import Question, Choice, Category, Person, Article, Tag


class QuestionForm(forms.ModelForm):
    """Form for creating/editing questions"""
    
    class Meta:
        model = Question
        fields = ['question_text', 'category']
        widgets = {
            'question_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your question here...',
                'maxlength': 200,
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        help_texts = {
            'question_text': 'Ask a clear and concise question (max 200 characters)',
            'category': 'Select a category for your question',
        }
    
    def clean_question_text(self):
        question_text = self.cleaned_data.get('question_text')
        if len(question_text) < 5:
            raise ValidationError("Question must be at least 5 characters long.")
        return question_text


class ChoiceFormSet(forms.ModelForm):
    """Individual choice form for use in formsets"""
    
    class Meta:
        model = Choice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter choice option...',
                'maxlength': 200,
            }),
        }


# Create a formset for choices
ChoiceFormSet = forms.modelformset_factory(
    Choice,
    form=ChoiceFormSet,
    extra=2,  # Number of empty forms to display
    min_num=2,  # Minimum number of choices required
    validate_min=True,
    can_delete=True,
)


class QuestionWithChoicesForm(forms.ModelForm):
    """Combined form for question with inline choices"""
    
    choice_1 = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First choice option...',
        }),
        help_text='Enter the first choice option'
    )
    
    choice_2 = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Second choice option...',
        }),
        help_text='Enter the second choice option'
    )
    
    choice_3 = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Third choice option (optional)...',
        }),
        help_text='Enter the third choice option (optional)'
    )
    
    choice_4 = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Fourth choice option (optional)...',
        }),
        help_text='Enter the fourth choice option (optional)'
    )
    
    class Meta:
        model = Question
        fields = ['question_text', 'category']
        widgets = {
            'question_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your question here...',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        choice_1 = cleaned_data.get('choice_1')
        choice_2 = cleaned_data.get('choice_2')
        choice_3 = cleaned_data.get('choice_3')
        choice_4 = cleaned_data.get('choice_4')
        
        # Check for duplicate choices
        choices = [c for c in [choice_1, choice_2, choice_3, choice_4] if c]
        if len(choices) != len(set(choices)):
            raise ValidationError("All choices must be unique.")
        
        return cleaned_data
    
    def save(self, commit=True):
        question = super().save(commit=commit)
        
        if commit:
            # Create choices
            choices = [
                self.cleaned_data.get('choice_1'),
                self.cleaned_data.get('choice_2'),
                self.cleaned_data.get('choice_3'),
                self.cleaned_data.get('choice_4'),
            ]
            
            for choice_text in choices:
                if choice_text:
                    Choice.objects.create(
                        question=question,
                        choice_text=choice_text
                    )
        
        return question


class CategoryForm(forms.ModelForm):
    """Form for creating/editing categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'color', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category name...',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Category description...',
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
            }),
            'icon': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Font Awesome icon class (e.g., fas fa-star)...',
            }),
        }
        help_texts = {
            'name': 'Enter a unique category name',
            'description': 'Describe what this category is about',
            'color': 'Choose a color for this category',
            'icon': 'Font Awesome icon class (optional)',
        }
    
    def save(self, commit=True):
        category = super().save(commit=False)
        if not category.slug:
            category.slug = slugify(category.name)
        if commit:
            category.save()
        return category


class PersonForm(forms.ModelForm):
    """Form for creating/editing person profiles"""
    
    class Meta:
        model = Person
        fields = ['first_name', 'last_name', 'email', 'phone', 'birth_date', 
                 'gender', 'bio', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name...',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name...',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address...',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number...',
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Tell us about yourself...',
            }),
            'avatar': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Avatar URL...',
            }),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Person.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email address is already in use.")
        return email


class ArticleForm(forms.ModelForm):
    """Form for creating/editing articles"""
    
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        help_text="Select relevant tags"
    )
    
    class Meta:
        model = Article
        fields = ['title', 'content', 'category', 'tags', 'status', 'featured_image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Article title...',
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': 'Write your article content here...',
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'featured_image': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Featured image URL...',
            }),
        }
    
    def save(self, commit=True):
        article = super().save(commit=False)
        if not article.slug:
            article.slug = slugify(article.title)
        if commit:
            article.save()
            self.save_m2m()  # Save many-to-many relationships
        return article


class SearchForm(forms.Form):
    """Form for searching questions"""
    
    CATEGORY_CHOICES = [('', 'All Categories')]
    
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search questions...',
        }),
        help_text='Enter keywords to search for'
    )
    
    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        help_text='Filter by category'
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Populate category choices dynamically
        categories = Category.objects.filter(is_active=True)
        category_choices = [('', 'All Categories')]
        category_choices.extend([(cat.slug, cat.name) for cat in categories])
        self.fields['category'].choices = category_choices


class VoteForm(forms.Form):
    """Form for voting on a question"""
    
    choice = forms.ModelChoiceField(
        queryset=Choice.objects.none(),
        widget=forms.RadioSelect(attrs={
            'class': 'form-check-input',
        }),
        empty_label=None,
        help_text='Select your choice'
    )
    
    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choice'].queryset = question.choices.all()


class ContactForm(forms.Form):
    """Generic contact form"""
    
    SUBJECT_CHOICES = [
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('feedback', 'Feedback'),
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
    ]
    
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name...',
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email...',
        })
    )
    
    subject = forms.ChoiceField(
        choices=SUBJECT_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Your message...',
        }),
        help_text='Please provide as much detail as possible'
    )
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise ValidationError("Message must be at least 10 characters long.")
        return message


# Custom validation example
def validate_no_profanity(value):
    """Custom validator to check for profanity"""
    profane_words = ['badword1', 'badword2']  # Add actual words here
    for word in profane_words:
        if word.lower() in value.lower():
            raise ValidationError(f"Please avoid using inappropriate language.")
    return value


class CleanQuestionForm(forms.ModelForm):
    """Question form with custom validation"""
    
    class Meta:
        model = Question
        fields = ['question_text', 'category']
        widgets = {
            'question_text': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
    
    def clean_question_text(self):
        question_text = self.cleaned_data.get('question_text')
        
        # Use custom validator
        validate_no_profanity(question_text)
        
        # Additional custom validation
        if '?' not in question_text:
            raise ValidationError("A good question should end with a question mark.")
        
        return question_text
