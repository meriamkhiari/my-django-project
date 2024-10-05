from django.db import models
from category.models import Category  # Ensure the import is correct
from django.core.validators import MaxValueValidator
from django.core.validators import ValidationError
from django.utils import timezone

# Create your models here.
class Conference(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(default=timezone.now().date)
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    price = models.FloatField()
    capacity = models.IntegerField(validators=[MaxValueValidator(limit_value=900,message="capacity must be under 90")])
    program = models.FileField(upload_to='files/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="conferences")

    def clean (self):
        if self.end_date <= self.start_date:
            raise ValidationError ('End date must be greater than start date')
    
    def __str__(self):
        return self.title  # Return a string representation of the object

    class Meta:
        ordering = ['start_date']  # Order by start date by default
        constraints=[
            models.CheckConstraint(
                check=models.Q(
                    start_date__gte=timezone.now().date(),
                ), name="the date must be gretater than today"
        
            )
        ]