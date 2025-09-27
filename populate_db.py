import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UnivendProject.settings')
django.setup()

from UnivendApp.models import Campus, Department, Category

def populate_campuses():
    """Create sample campuses for the university e-commerce site"""
    campuses = [
        {
            'name': 'Main Campus',
            'location': 'University Avenue, Central City'
        },
        {
            'name': 'North Campus',
            'location': 'Northern Boulevard, North City'
        },
        {
            'name': 'South Campus',
            'location': 'Southern Street, South City'
        },
        {
            'name': 'East Campus',
            'location': 'Eastern Road, East City'
        },
        {
            'name': 'West Campus',
            'location': 'Western Drive, West City'
        }
    ]
    
    created_campuses = []
    for campus_data in campuses:
        campus, created = Campus.objects.get_or_create(
            name=campus_data['name'],
            defaults={'location': campus_data['location']}
        )
        created_campuses.append(campus)
        if created:
            print(f"Created campus: {campus.name}")
        else:
            print(f"Campus already exists: {campus.name}")
    
    return created_campuses

def populate_categories():
    """Create sample categories for products and services"""
    categories = [
        # Product categories
        {'name': 'Textbooks', 'is_product': True, 'icon': 'book'},
        {'name': 'Electronics', 'is_product': True, 'icon': 'devices'},
        {'name': 'Furniture', 'is_product': True, 'icon': 'chair'},
        {'name': 'Clothing', 'is_product': True, 'icon': 'checkroom'},
        {'name': 'School Supplies', 'is_product': True, 'icon': 'edit'},
        {'name': 'Sports Equipment', 'is_product': True, 'icon': 'sports_soccer'},
        {'name': 'Musical Instruments', 'is_product': True, 'icon': 'piano'},
        {'name': 'Vehicles', 'is_product': True, 'icon': 'directions_car'},
        
        # Service categories
        {'name': 'Tutoring', 'is_product': False, 'icon': 'school'},
        {'name': 'Cleaning', 'is_product': False, 'icon': 'cleaning_services'},
        {'name': 'Transportation', 'is_product': False, 'icon': 'local_taxi'},
        {'name': 'Repair', 'is_product': False, 'icon': 'build'},
        {'name': 'Design', 'is_product': False, 'icon': 'design_services'},
        {'name': 'Photography', 'is_product': False, 'icon': 'photo_camera'},
        {'name': 'Event Planning', 'is_product': False, 'icon': 'event'},
        {'name': 'Programming', 'is_product': False, 'icon': 'code'}
    ]
    
    created_categories = []
    for category_data in categories:
        category, created = Category.objects.get_or_create(
            name=category_data['name'],
            defaults={
                'is_product': category_data['is_product'],
                'icon': category_data['icon']
            }
        )
        created_categories.append(category)
        if created:
            print(f"Created category: {category.name} ({'Product' if category.is_product else 'Service'})")
        else:
            print(f"Category already exists: {category.name}")
    
    return created_categories

def populate_departments(campuses):
    """Create sample departments for each campus"""
    # Common departments across all campuses
    common_departments = [
        'Computer Science',
        'Engineering',
        'Business Administration',
        'Arts and Humanities',
        'Social Sciences',
        'Natural Sciences',
        'Mathematics',
        'Medicine',
        'Law',
        'Education'
    ]
    
    # Specialized departments for specific campuses
    specialized_departments = {
        'Main Campus': ['Architecture', 'Urban Planning', 'Public Policy'],
        'North Campus': ['Environmental Science', 'Agriculture', 'Forestry'],
        'South Campus': ['Marine Biology', 'Oceanography', 'Coastal Studies'],
        'East Campus': ['Film Studies', 'Digital Media', 'Performing Arts'],
        'West Campus': ['Sports Science', 'Physical Education', 'Nutrition']
    }
    
    created_departments = []
    
    # Create common departments for all campuses
    for campus in campuses:
        for dept_name in common_departments:
            dept, created = Department.objects.get_or_create(
                name=f"{dept_name} - {campus.name}",
                campus=campus
            )
            created_departments.append(dept)
            if created:
                print(f"Created department: {dept.name} at {campus.name}")
            else:
                print(f"Department already exists: {dept.name}")
        
        # Add specialized departments for specific campuses
        if campus.name in specialized_departments:
            for dept_name in specialized_departments[campus.name]:
                dept, created = Department.objects.get_or_create(
                    name=dept_name,
                    campus=campus
                )
                created_departments.append(dept)
                if created:
                    print(f"Created specialized department: {dept.name} at {campus.name}")
                else:
                    print(f"Specialized department already exists: {dept.name}")
    
    return created_departments

if __name__ == '__main__':
    print("Starting database population...")
    
    print("\nPopulating campuses...")
    campuses = populate_campuses()
    
    print("\nPopulating categories...")
    categories = populate_categories()
    
    print("\nPopulating departments...")
    departments = populate_departments(campuses)
    
    print("\nDatabase population completed!")
    print(f"Created {len(campuses)} campuses")
    print(f"Created {len(categories)} categories")
    print(f"Created {len(departments)} departments")