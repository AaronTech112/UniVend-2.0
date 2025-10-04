from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import CustomUser, Campus, Department, Category, Listing, ListingImage, Message, Review, Transaction
from .forms import ListingForm, KYCForm, ProfileForm, MessageForm
from django.db.models import Q, Avg, Count
import json
from datetime import datetime
# In views.py
from django.conf import settings as django_settings 

    # Create your views here.
def landing_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request,'UnivendApp/landing.html')
        

def home(request):
    if request.user.is_authenticated:
        user = request.user
        campus = user.campus

        # Fetch Featured Listings (e.g., top 5 by views or saves)
        featured_listings = Listing.objects.filter(
            is_active=True,
            seller__campus=campus
        ).annotate(
            save_count=Count('saves')
        ).order_by('-save_count', '-views')[:5]

        # Fetch Recent Listings (e.g., latest 8 active listings)
        recent_listings = Listing.objects.filter(
            is_active=True,
            seller__campus=campus
        ).order_by('-created_at')[:8]

        context = {
            'campus': campus,
            'featured_listings': featured_listings,
            'recent_listings': recent_listings,
            'categories': Category.objects.all(),  # For category scroll
        }
        return render(request, 'UnivendApp/homepage.html', context)
    else:
        return redirect('login_user')

        
def register_user(request):
    campuses = Campus.objects.all()
    departments = Department.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        campus = request.POST.get('campus')
        department = request.POST.get('department')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        

        # Validate inputs (add more validation as needed)
        if not first_name or not last_name or not email or not password1 or not campus:
            messages.error(request, 'Please fill in all fields.')
            return render(request, 'UnivendApp/register.html', {'campuses': campuses})

        try:
            campus = Campus.objects.get(name=campus)
            department = Department.objects.get(name=department)
        except Campus.objects.get(name=campus).DoesNotExist:
            print(campus)
            messages.error(request, 'Invalid campus selected.')
            context = {"campuses":campuses, "departments":departments }
            return render(request, 'UnivendApp/register.html', context)

        # Create the user
        try:
            user = CustomUser.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                campus=campus,
                department=department,
                password=password1,
                 
            )
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Redirect to your home page
        except Exception as e:
            messages.error(request, f'Registration failed: {e}')
            context = {"campuses":campuses, "departments":departments }
            return render(request, 'UnivendApp/register.html', context)
    else:
        context = {"campuses":campuses, "departments": departments }
        return render(request, 'UnivendApp/register.html',context)
    
    
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST.get('loginEmail')
            password = request.POST.get('loginPassword')
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Logged in as {email}!')
                return redirect('home')  # Redirect to your home page
            else:
                messages.error(request, 'Invalid email or password.')
                return render(request, 'UnivendApp/index.html')
        else:
            return render(request, 'UnivendApp/index.html')


def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect('landing_page')  # Redirect to your home page

@login_required(login_url='login_user')
def kyc(request):
    if request.user.is_verified:
        return redirect('home')
    departments = Department.objects.all()
    categories = Category.objects.all()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    step = request.session.get('kyc_step', 1)

    if request.method == 'POST':
        if step == 1:
            department_id = request.POST.get('department')
            phone_number = request.POST.get('phone_number')
            if department_id and phone_number:
                request.user.department = Department.objects.get(id=department_id)
                request.user.phone_number = phone_number
                request.user.save()
                request.session['kyc_step'] = 2
                step = 2
            else:
                messages.error(request, 'Please fill in all fields.')
        elif step == 2:
            if 'profile_picture' in request.FILES:
                request.user.profile_picture = request.FILES['profile_picture']
                request.user.save()
                request.session['kyc_step'] = 3
                step = 3
            else:
                messages.error(request, 'Please upload a profile picture.')
        elif step == 3:
            if 'student_id' in request.FILES:
                # Store student ID (you may want to save this to a separate field or model)
                request.session['kyc_step'] = 4
                step = 4
            else:
                messages.error(request, 'Please upload your student ID.')
        elif step == 4:
            interest_ids = request.POST.getlist('interests')
            if interest_ids:
                request.user.interests.set(interest_ids)
                request.user.is_verified = True
                request.user.save()
                del request.session['kyc_step']
                messages.success(request, 'Profile setup completed!')
                return redirect('home')
            else:
                messages.error(request, 'Please select at least one interest.')

    context = {
        'departments': departments,
        'categories': categories,
        'days': days,
        'step': step,
    }
    return render(request, 'UnivendApp/kyc.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            full_name = form.cleaned_data['full_name'].split()
            user.first_name = full_name[0] if full_name else ''
            user.last_name = ' '.join(full_name[1:]) if len(full_name) > 1 else ''
            user.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=request.user, initial={'full_name': f"{request.user.first_name} {request.user.last_name}"})
    
    # Get active listings and average rating
    active_listings = request.user.listings.filter(is_active=True).order_by('-created_at')
    average_rating = request.user.received_reviews.aggregate(Avg('rating'))['rating__avg'] or 0

    context = {
        'form': form,
        'campuses': Campus.objects.all(),
        'departments': Department.objects.all(),
        'active_listings': active_listings,
        'average_rating': average_rating,
    }
    return render(request, 'UnivendApp/profile.html', context)

@login_required
def explore(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'UnivendApp/explore.html', context)

import mimetypes
from django.core.exceptions import ValidationError
@login_required
def add_listing(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        print("Form received:", dict(request.POST), [f.name for f in request.FILES.values()])
        try:
            form = ListingForm(request.POST, request.FILES)
            if form.is_valid():
                listing = form.save(commit=False)
                listing.seller = request.user
                listing.listing_type = request.POST.get('listing_type')

                # Handle meeting preferences
                meeting_preferences = request.POST.getlist('meeting_preferences')
                if not meeting_preferences:
                    messages.error(request, 'Please select at least one meeting preference')
                    return render(request, 'UnivendApp/add-listing.html', {
                        'form': form,
                        'categories': categories
                    })
                listing.meeting_preferences = ','.join(meeting_preferences)

                listing.save()
                form.save_m2m()  # Save tags

                # Handle cover image
                cover_image = request.FILES.get('cover_image')
                if cover_image:
                    mime_type, _ = mimetypes.guess_type(cover_image.name)
                    if not mime_type or not mime_type.startswith('image'):
                        messages.error(request, 'Cover image must be a valid image file (e.g., JPEG, PNG)')
                        return render(request, 'UnivendApp/add-listing.html', {
                            'form': form,
                            'categories': categories
                        })
                    if cover_image.size > 5 * 1024 * 1024:
                        messages.error(request, 'Cover image must be smaller than 5MB')
                        return render(request, 'UnivendApp/add-listing.html', {
                            'form': form,
                            'categories': categories
                        })
                    ListingImage.objects.create(
                        listing=listing,
                        image=cover_image,
                        is_cover=True
                    )

                # Handle additional images
                for image in request.FILES.getlist('images'):
                    if image:
                        mime_type, _ = mimetypes.guess_type(image.name)
                        if not mime_type or not mime_type.startswith('image'):
                            continue
                        if image.size > 5 * 1024 * 1024:
                            continue
                        ListingImage.objects.create(
                            listing=listing,
                            image=image
                        )

                messages.success(request, 'Listing created successfully!')
                return redirect('product-detail', listing_id=listing.id)
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        except ValidationError as e:
            messages.error(request, f'Validation error: {str(e)}')
        except Exception as e:
            messages.error(request, f'An error occurred while creating the listing: {str(e)}')
        return render(request, 'UnivendApp/add-listing.html', {
            'form': form,
            'categories': categories
        })

    form = ListingForm()
    return render(request, 'UnivendApp/add-listing.html', {
        'form': form,
        'categories': categories
    })
    
@login_required
def product_detail(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, is_active=True)
    listing.views += 1
    listing.save()
    
    # Preprocess tags into a list
    tags_list = listing.tags.split(',') if listing.tags else []
    
    context = {
        'listing': listing,
        'tags_list': tags_list,
    }
    return render(request, 'UnivendApp/product-detail.html', context)

@login_required
def chat_list(request):
    # Mock chats for simplicity; replace with actual query
    chats = []
    for message in Message.objects.filter(sender=request.user) | Message.objects.filter(receiver=request.user):
        other_user = message.receiver if message.sender == request.user else message.sender
        if not any(c['other_user'] == other_user for c in chats):
            unread_count = Message.objects.filter(sender=other_user, receiver=request.user, is_read=False).count()
            chats.append({
                'id': message.id,
                'other_user': other_user,
                'last_message': message,
                'unread_count': unread_count,
                'listing': message.listing,
            })
    context = {
        'chats': chats,
    }
    return render(request, 'UnivendApp/chat-list.html', context)

@login_required
def chat_detail(request, user_id, listing_id=None):
    chat_user = get_object_or_404(CustomUser, id=user_id)
    listing = get_object_or_404(Listing, id=listing_id) if listing_id else None
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=chat_user) | Q(sender=chat_user, receiver=request.user))
    ).order_by('sent_at')
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = chat_user
            message.listing = listing
            message.save()
            return redirect('chat-detail', user_id=user_id, listing_id=listing_id)
    else:
        form = MessageForm()
    context = {
        'chat_user': chat_user,
        'listing': listing,
        'messages': messages,
        'form': form,
    }
    return render(request, 'UnivendApp/chat-detail.html', context)

from django.db.models import Q

@login_required
def search(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')
    condition = request.GET.get('condition', '')
    listings = Listing.objects.filter(is_active=True, seller__campus=request.user.campus)
    
    if query:
        listings = listings.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(tags__icontains=query))
    if category_id:
        listings = listings.filter(category_id=category_id)
    if price_min:
        listings = listings.filter(price__gte=price_min)
    if price_max:
        listings = listings.filter(price__lte=price_max)
    if condition:
        listings = listings.filter(condition=condition)

    context = {
        'listings': listings,
        'query': query,
        'categories': Category.objects.all(),
        'selected_category': category_id,
        'price_min': price_min,
        'price_max': price_max,
        'condition': condition,
    }
    
    # ... (existing code)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        listings_data = [{
            'id': l.id,
            'title': l.title,
            'price': str(l.price),
            'image': l.images.first().image.url if l.images.exists() else None
        } for l in listings]
        return JsonResponse({'listings': listings_data})
    
    return render(request, 'UnivendApp/homepage.html', context)


def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Split full_name into first_name and last_name
            full_name = form.cleaned_data['full_name']
            name_parts = full_name.split(' ', 1)
            request.user.first_name = name_parts[0]
            request.user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            # Save the form (updates other fields)
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'UnivendApp/edit_profile.html', {'form': form})

from django.views.decorators.http import require_POST
@login_required
def settings(request):
    return render(request, 'UnivendApp/settings.html')

@login_required
@require_POST
def update_notifications(request):
    try:
        data = json.loads(request.body)
        email_notifications = data.get('email_notifications', False)
        request.user.email_notifications = email_notifications
        request.user.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)
        
@login_required
def buy_now(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id, is_active=True)
    
    # Check if the buyer is not the seller
    if request.user == listing.seller:
        return JsonResponse({'success': False, 'error': 'You cannot view contact info for your own listing'}, status=400)
    
    try:
        # Get seller contact information
        seller = listing.seller
        contact_info = {
            'name': f"{seller.first_name} {seller.last_name}",
            'phone': seller.phone_number,
            'email': seller.email
        }
        
        # Return success response with contact info
        return JsonResponse({
            'success': True, 
            'contact_info': contact_info
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)