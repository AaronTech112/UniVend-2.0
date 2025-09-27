from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django.contrib.auth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Campus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('location', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('is_product', models.BooleanField(default=True)),
                ('icon', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('campus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='UnivendApp.campus')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15, null=True, unique=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('show_phone', models.BooleanField(default=False)),
                ('email_notifications', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('campus', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='UnivendApp.campus')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='UnivendApp.department')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('listing_type', models.CharField(choices=[('product', 'Product'), ('service', 'Service')], default='product', max_length=10)),
                ('title', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price_type', models.CharField(choices=[('fixed', 'Fixed Price'), ('negotiable', 'Negotiable'), ('hourly', 'Per Hour'), ('free', 'Free')], default='fixed', max_length=20)),
                ('condition', models.CharField(blank=True, choices=[('new', 'New'), ('like-new', 'Like New'), ('good', 'Good'), ('fair', 'Fair')], max_length=20)),
                ('description', models.TextField(max_length=1000)),
                ('tags', models.CharField(blank=True, max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('meeting_preferences', models.CharField(blank=True, max_length=100)),
                ('availability', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('views', models.PositiveIntegerField(default=0)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='UnivendApp.category')),
                ('saves', models.ManyToManyField(blank=True, related_name='saved_listings', to='UnivendApp.customuser')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='UnivendApp.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='completed', max_length=20)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchases', to='UnivendApp.customuser')),
                ('listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='UnivendApp.listing')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sales', to='UnivendApp.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField()),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('listing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='UnivendApp.listing')),
                ('reviewed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_reviews', to='UnivendApp.customuser')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_reviews', to='UnivendApp.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='message_images/')),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('listing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='UnivendApp.listing')),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to='UnivendApp.customuser')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to='UnivendApp.customuser')),
            ],
        ),
        migrations.CreateModel(
            name='ListingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='listing_images/')),
                ('is_cover', models.BooleanField(default=False)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='UnivendApp.listing')),
            ],
        ),
        migrations.CreateModel(
            name='KYC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.ImageField(blank=True, null=True, upload_to='student_ids/')),
                ('verification_status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('interests', models.ManyToManyField(blank=True, related_name='kyc_interests', to='UnivendApp.category')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='kyc', to='UnivendApp.customuser')),
            ],
        ),
    ]