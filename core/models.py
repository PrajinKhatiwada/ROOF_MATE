from django.db import models
from django.utils.text import slugify


class Enquiry(models.Model):
    SERVICE_CHOICES = [
        ('Metal Roof Painting', 'Metal Roof Painting'),
        ('Tile Roof Painting', 'Tile Roof Painting'),
        ('Roof Repairs', 'Roof Repairs'),
        ('Roof Pressure Cleaning', 'Roof Pressure Cleaning'),
        ('Driveway Painting', 'Driveway Painting'),
        ('Driveway Cleaning', 'Driveway Cleaning'),
    ]

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField()
    suburb = models.CharField(max_length=120)
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.service}"


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('Metal Roof', 'Metal Roof'),
        ('Tile Roof', 'Tile Roof'),
        ('Driveway', 'Driveway'),
        ('Repairs', 'Repairs'),
        ('Cleaning', 'Cleaning'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    suburb = models.CharField(max_length=120)
    summary = models.TextField()
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='projects/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateField()

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class GalleryItem(models.Model):
    CATEGORY_CHOICES = [
        ('metal', 'Metal'),
        ('tile', 'Tile'),
        ('driveway', 'Driveway'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='gallery/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    read_time = models.CharField(max_length=50, default='5 min read')
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    published_at = models.DateField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Blog.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/', null=True, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    linkedin_url = models.URLField(blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name
    

class ChatConversation(models.Model):
    CHANNEL_CHOICES = [
        ('website', 'Website'),
        ('whatsapp', 'WhatsApp'),
    ]

    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES, default='website')
    session_id = models.CharField(max_length=120, blank=True, null=True, db_index=True)
    whatsapp_user_id = models.CharField(max_length=120, blank=True, null=True, db_index=True)
    user_name = models.CharField(max_length=150, blank=True)
    user_phone = models.CharField(max_length=40, blank=True)
    lead_service = models.CharField(max_length=120, blank=True)
    suburb = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    is_lead = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        ident = self.session_id or self.whatsapp_user_id or f"conv-{self.pk}"
        return f"{self.channel} - {ident}"


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('system', 'System'),
    ]

    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:40]}"