import datetime
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")



    def __str__(self):
        return self.name

class Sub_Cateory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='sub_categories')

    def __str__(self):
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class Product(models.Model):
    AVAILABILITY_CHOICES = (('In Stocks', 'In Stocks'), ('Out of Stocks', 'Out of Stocks'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Cateory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)    
    image = models.ImageField(upload_to='Ecom/image')
    name = models.CharField(max_length=100)
    AVAILABILITY = models.CharField(choices=AVAILABILITY_CHOICES, max_length=100, null=True)
    price = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name



class UserCreateForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Email',
        error_messages={'exists': 'This email is already in use.'}
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")  # Correct field names

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

        # Optional: Add a CSS class to all fields
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return email




class Contact_us(models.Model):
    name= models.CharField(max_length=100)
    email= models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField()


    def __str__(self):
        return self.email
    


class Order(models.Model):
    image = models.ImageField(upload_to='Ecom/image') 
    product = models.CharField(max_length=100, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Changed to IntegerField
    price = models.IntegerField()
    address = models.TextField()
    phone = models.CharField(max_length=10)
    pincode = models.CharField(max_length=10)
    date = models.DateField(default=datetime.datetime.today)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Changed to DecimalField

    def __str__(self):
        return self.product


    
