import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UnivendProject.settings')
django.setup()

from UnivendApp.models import Campus, Department, Category

def verify_data():
    """Verify the data in the database"""
    # Check campuses
    campuses = Campus.objects.all()
    print(f"\nCampuses ({campuses.count()}):")
    for campus in campuses:
        print(f"- {campus.name}: {campus.location}")
    
    # Check categories
    categories = Category.objects.all()
    print(f"\nCategories ({categories.count()}):")
    for category in categories:
        category_type = "Product" if category.is_product else "Service"
        print(f"- {category.name} ({category_type}): {category.icon}")
    
    # Check departments
    departments = Department.objects.all()
    print(f"\nDepartments ({departments.count()}):")
    for department in departments:
        print(f"- {department.name} at {department.campus.name}")
    
    # Count by campus
    print("\nDepartments by Campus:")
    for campus in campuses:
        dept_count = Department.objects.filter(campus=campus).count()
        print(f"- {campus.name}: {dept_count} departments")

if __name__ == '__main__':
    print("Verifying database data...")
    verify_data()
    print("\nVerification complete!")