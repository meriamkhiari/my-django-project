from django.db import models
from django.contrib.auth.models import AbstractUser
from conferences.models import Conference
from category.models import Category
from django.core.validators import RegexValidator, ValidationError
from django.utils import timezone


def email_validator(value):
    if not value.endswith('@esprit.tn'):
        raise ValidationError ('Email invalid, only @espirt.Tn domains are allowed')


class Participant(AbstractUser):
    cin_validator=RegexValidator(regex=r'^\d{8}$',message="This field must contain exactly 8 digits")
    cin = models.CharField(primary_key=True, max_length=8,validators=[cin_validator])
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    USERNAME_FIELD = 'username'

    CHOICES = (
        ('etudiant', 'etudiant'),
        ('chercheur', 'chercheur'),
        ('docteur', 'docteur'),
        ('enseignant', 'enseignant')
    )
    participant_category = models.CharField(max_length=255, choices=CHOICES)
    reseverations = models.ManyToManyField(Conference,through= 'Reservation',)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reservation(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    reservation_date = models.DateTimeField(auto_now_add=True)
    def clean(self):
        if self.conference.start_date < timezone.now().date():
            raise ValidationError('You can only reserve for upcoming conference.')
        reservation_count=Reservation.objects.filter(
            participant=self.participant,
            reservation_date=self.reservation_date
        )
        if reservation_count>= 3:
            raise ValidationError("You can only make up to 3 reservations per day")
class Meta:
    unique_together = ('conference', 'participant')
    verbose_name_plural = "Reservations"