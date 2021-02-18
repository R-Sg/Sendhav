from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager 
from django.utils import timezone


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

# --------------------------------#
# Locations                       #
# --------------------------------#

class Country(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey("Country", on_delete=models.CASCADE, related_name="state_country")

    class Meta:
        verbose_name_plural = "States"

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey("Country", on_delete=models.CASCADE, related_name="location_country")
    state = models.ForeignKey(
        "State", null=True, on_delete=models.SET_NULL, related_name="location_state"
    )
    name = models.CharField(max_length=50)
  
    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class UserRole(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    CAST_CHOICES = (
        ('G', 'GENERAL'),
        ('O', 'OBC'),
        ('Sc', 'SC'),
        ('St', 'ST'),
    )
    OCCUPATION_CHOICES = (
        ('G', 'Goverment'),
        ('P', 'Private'),
        ('F', 'Farmer'),
        ('S', 'Self'),
        ('N', 'None'),
    )
    is_approved = models.BooleanField(
        ("approve status"),
        default=False,
        help_text="Designates whether the user is approved.",
        null=True,
        blank=True
    )
    is_admin = models.BooleanField(
        ("admin status"),
        default=False,
        help_text="Designates whether the user is admin.",
        null=True,
        blank=True
    )
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('First Name', max_length=30, null=True)
    last_name = models.CharField('Last Name', max_length=30, null=True)
    profile_image = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    phone = models.IntegerField(unique=True, null=True)
    language = models.CharField("language", max_length=30, blank=False, default="EN", null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)
    address = models.CharField(max_length=200, null=True)
    birthday = models.DateField(null=True)
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    bio = models.CharField("bio", max_length=150, blank=True, null=True)
    cast = models.CharField(max_length=2, choices=CAST_CHOICES, null=True)
    married = models.BooleanField(default=False)
    occupation_type = models.CharField(max_length=2, choices=OCCUPATION_CHOICES, null=True)
    occupation_detail = models.CharField(max_length=500, blank=True, null=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, blank=True, null=True)
    country_name = models.ForeignKey(
        Country, 
        on_delete=models.CASCADE,
        related_name="user_country",
        verbose_name ="country", 
        null=True
    )
    state_name = models.ForeignKey(
        State, 
        on_delete=models.CASCADE,
        related_name="user_state",
        verbose_name ="state", 
        null=True
    )
    city_name = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="user_city",
        verbose_name ="city", 
        null=True
    )
    address_detail = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return f"{self.email} - {self.first_name} {self.last_name}"


