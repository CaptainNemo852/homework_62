from django.db import models
import random
import string
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=255)
    genre = models.ManyToManyField(Category, related_name='movie_category')
    description = models.TextField(max_length=2000, null=True, blank=True)
    poster = models.ImageField(upload_to='posters', null=True, blank=True)
    release_date = models.DateField()
    finish_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name




class Hall(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Seat(models.Model):
    hall = models.ForeignKey(Hall, related_name='hall_name', on_delete=models.PROTECT)
    row = models.CharField(max_length=255)
    place = models.CharField(max_length=255)

    def __str__(self):
        return '%s зал, %s ряд, %s место' %(self.hall, self.row, self.place)


class Show(models.Model):
    movie = models.ForeignKey(Movie, related_name='show_name', on_delete=models.PROTECT)
    hall = models.ForeignKey(Hall, related_name='show_hall', on_delete=models.PROTECT)
    time_start = models.DateTimeField(null=False, blank=False)
    time_finish = models.DateTimeField(null=False, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=5)

    def __str__(self):
        return 'Сеанс %s, зал %s, начало %s, окончание %s' %(self.movie, self.hall, self.time_start, self.time_finish)





class Discount(models.Model):
    name = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    date_start = models.DateTimeField(null=True, blank=True)
    date_finish = models.DateTimeField(null=True, blank=True)
    is_existed = models.BooleanField(default=False)

    def __str__(self):
        return '%s. Скидка: %s. (%s - %s)' % (self.name, self.discount, self.date_start, self.date_finish)


class Ticket(models.Model):
    show = models.ForeignKey(Show, related_name='ticket_show', on_delete=models.PROTECT)
    seat = models.ForeignKey(Seat, related_name='ticket_seat', on_delete=models.PROTECT)
    discount = models.ForeignKey(Discount, null=True, blank=True, related_name='ticket_discount', on_delete=models.PROTECT)
    return_ticket = models.BooleanField(default=False)
    is_existed = models.BooleanField(default=False)

    def __str__(self):
        return 'Билет: %s, сеанс: %s, залл :%s' % (self.id, self.show.movie, self.show.hall)


def generate_code():
    code = ""
    for i in range(0, settings.BOOKING_CODE_LENGTH):
        code += random.choice(string.digits)
    return code


class Booking(models.Model):
    STATUS_NEW = 'Новый'
    STATUS_SOLD = 'Выкуплено'
    STATUS_CANCELED = 'Отменено'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый'),
        (STATUS_SOLD, 'Выкуплено'),
        (STATUS_CANCELED, 'Отмена')
    )

    code = models.CharField(max_length=10, unique_for_date='created_at', default=generate_code, editable=False)
    show = models.ForeignKey(Show, related_name='booking_show', on_delete=models.PROTECT)
    seats = models.ManyToManyField(Seat, related_name='booking_seats')
    status = models.CharField(max_length=255, default=STATUS_NEW, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Код бронирования - %s, статус: %s, Срок:%s- %s' % (self.code, self.status, self.created_at, self.updated_at)
