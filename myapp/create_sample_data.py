#!/usr/bin/env python
"""
Django sample data creation script
Run this with: python3 create_sample_data.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myapp.settings')
django.setup()

from django.contrib.auth.models import User
from polls.models import Question, Choice, Category, Person
from django.utils import timezone
from datetime import timedelta

def create_sample_data():
    print("Creating sample data...")
    
    # Create superuser if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✓ Superuser created (admin/admin123)")
    
    # Create categories
    categories_data = [
        {'name': 'Technology', 'description': 'Questions about technology and programming', 'color': '#007bff', 'icon': 'fas fa-laptop-code'},
        {'name': 'Sports', 'description': 'Sports-related polls and surveys', 'color': '#28a745', 'icon': 'fas fa-running'},
        {'name': 'Entertainment', 'description': 'Movies, music, and entertainment', 'color': '#dc3545', 'icon': 'fas fa-film'},
        {'name': 'Food', 'description': 'Culinary preferences and food choices', 'color': '#fd7e14', 'icon': 'fas fa-utensils'},
        {'name': 'Travel', 'description': 'Travel destinations and experiences', 'color': '#20c997', 'icon': 'fas fa-plane'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'color': cat_data['color'],
                'icon': cat_data['icon'],
                'slug': cat_data['name'].lower().replace(' ', '-'),
                'is_active': True,
            }
        )
        categories.append(category)
        if created:
            print(f"✓ Category created: {category.name}")
    
    # Create admin user for questions
    admin_user = User.objects.get(username='admin')
    
    # Create sample questions with choices
    questions_data = [
        {
            'question': 'What is your favorite programming language?',
            'category': categories[0],  # Technology
            'choices': ['Python', 'JavaScript', 'Java', 'C++', 'Go'],
            'votes': [15, 12, 8, 5, 3]
        },
        {
            'question': 'Which sport do you prefer to watch?',
            'category': categories[1],  # Sports
            'choices': ['Football', 'Basketball', 'Tennis', 'Swimming'],
            'votes': [20, 15, 10, 8]
        },
        {
            'question': 'Best movie genre?',
            'category': categories[2],  # Entertainment
            'choices': ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi'],
            'votes': [25, 20, 15, 8, 12]
        },
        {
            'question': 'Your favorite cuisine?',
            'category': categories[3],  # Food
            'choices': ['Italian', 'Japanese', 'Mexican', 'Thai', 'French'],
            'votes': [18, 22, 16, 14, 10]
        },
        {
            'question': 'Dream vacation destination?',
            'category': categories[4],  # Travel
            'choices': ['Tokyo', 'Paris', 'New York', 'Bali', 'Iceland'],
            'votes': [16, 19, 13, 21, 11]
        },
        {
            'question': 'Best time to work?',
            'category': categories[0],  # Technology
            'choices': ['Morning', 'Afternoon', 'Evening', 'Night'],
            'votes': [30, 25, 20, 15]
        }
    ]
    
    for q_data in questions_data:
        # Create question
        question, created = Question.objects.get_or_create(
            question_text=q_data['question'],
            defaults={
                'author': admin_user,
                'category': q_data['category'],
                'pub_date': timezone.now() - timedelta(days=abs(hash(q_data['question'])) % 30),
                'is_active': True,
            }
        )
        
        if created:
            print(f"✓ Question created: {question.question_text}")
            
            # Create choices for this question
            for i, choice_text in enumerate(q_data['choices']):
                choice, choice_created = Choice.objects.get_or_create(
                    question=question,
                    choice_text=choice_text,
                    defaults={
                        'votes': q_data['votes'][i] if i < len(q_data['votes']) else 0,
                    }
                )
                if choice_created:
                    print(f"  ✓ Choice created: {choice_text} ({choice.votes} votes)")
    
    # Create some sample persons
    persons_data = [
        {'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com', 'gender': 'M'},
        {'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com', 'gender': 'F'},
        {'first_name': 'Bob', 'last_name': 'Johnson', 'email': 'bob@example.com', 'gender': 'M'},
        {'first_name': 'Alice', 'last_name': 'Williams', 'email': 'alice@example.com', 'gender': 'F'},
    ]
    
    for person_data in persons_data:
        person, created = Person.objects.get_or_create(
            email=person_data['email'],
            defaults=person_data
        )
        if created:
            print(f"✓ Person created: {person.full_name}")
    
    print("\n🎉 Sample data creation completed!")
    print("\nYou can now:")
    print("1. Visit http://127.0.0.1:8000/polls/ to see the polls")
    print("2. Visit http://127.0.0.1:8000/admin/ to manage data (admin/admin123)")
    print("3. Explore different URLs:")
    print("   - /polls/categories/ - View categories")
    print("   - /polls/stats/ - View statistics")
    print("   - /polls/questions/ - Class-based view")

if __name__ == '__main__':
    create_sample_data()
