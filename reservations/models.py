from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta, datetime
from django.utils import timezone


class Sport(models.Model):
    nom_sport = models.CharField(max_length=100)
    capacite_max = models.IntegerField()

    def __str__(self):
        return self.nom_sport


class Terrain(models.Model):
    TYPE_CHOICES = [
        ('gazon', 'Gazon'),
        ('synthetique', 'Synthétique'),
        ('parquet', 'Parquet'),
        ('terre', 'Terre battue'),
    ]

    nom = models.CharField(max_length=150)
    type_surface = models.CharField(max_length=20, choices=TYPE_CHOICES)
    type_sport = models.ForeignKey(Sport, on_delete=models.PROTECT, related_name='terrains')
    disponibilite = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} ({self.type_surface})"


class Joueur(models.Model):
    nom = models.CharField(max_length=150)
    telephone = models.CharField(max_length=20)

    def __str__(self):
        return self.nom


class Reservation(models.Model):
    terrain = models.ForeignKey(Terrain, on_delete=models.CASCADE, related_name='reservations')
    joueur = models.ForeignKey(Joueur, on_delete=models.CASCADE, related_name='reservations')
    date_reservation = models.DateField()
    heure_debut = models.TimeField()
    duree = models.PositiveIntegerField(help_text="Durée en minutes")

    def __str__(self):
        return f"{self.terrain} - {self.date_reservation} {self.heure_debut} ({self.joueur})"

    def clean(self):
        if self.date_reservation < timezone.localdate():
            raise ValidationError("La date de réservation ne peut pas être dans le passé.")
        if self.duree <= 0:
            raise ValidationError("La durée doit être supérieure à 0.")

        debut = datetime.combine(self.date_reservation, self.heure_debut)
        fin = debut + timedelta(minutes=self.duree)

        reservations = Reservation.objects.filter(
            terrain=self.terrain,
            date_reservation=self.date_reservation
        ).exclude(id=self.id)

        for r in reservations:
            r_debut = datetime.combine(r.date_reservation, r.heure_debut)
            r_fin = r_debut + timedelta(minutes=r.duree)

            if debut < r_fin and fin > r_debut:
                raise ValidationError("Ce terrain est deja reserve à cet horaire.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)