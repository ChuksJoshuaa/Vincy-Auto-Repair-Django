from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.files.storage import default_storage as storage
from PIL import Image


class Customer(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Customer"

    def get_absolute_url(self):
        return reverse('single_customer', kwargs={"id": self.id})

    @property
    def get_person(self):
        return reverse('delete_customer', kwargs={"id": self.id})

    def save(self, *args, **kwargs):
        if not self.username:
            return

        super(Customer, self).save()
        if self.image:
            size = 300, 300
            image = Image.open(self.image)
            image.thumbnail(size, Image.ANTIALIAS)
            fh = storage.open(self.image.name, "w")
            format = 'png'
            image.save(fh, format)
            fh.close()


class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "Admin"


class Mechanic(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    email = models.EmailField(max_length=200, unique=True)
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    location = models.CharField(max_length=255)
    phone = models.CharField(max_length=100, null=False)
    level = [
        ('Junior', 'Junior'),
        ('Mid-Level', 'Mid-Level'),
        ('Expert', 'Expert')
    ]
    skill = models.CharField(max_length=100, choices=level, null=False)
    salary = models.PositiveIntegerField(null=True)
    hired = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def get_id(self):
        return f"{self.username.id}"

    @property
    def get_person(self):
        return reverse('delete_mechanic', kwargs={"id": self.id})

    def get_absolute_url(self):
        return reverse('single_mechanic', kwargs={"id": self.id})

    class Meta:
        verbose_name_plural = "Mechanic"

    def save(self, *args, **kwargs):
        if not self.username:
            return

        super(Mechanic, self).save()
        if self.image:
            size = 300, 300
            image = Image.open(self.image)
            image.thumbnail(size, Image.ANTIALIAS)
            fh = storage.open(self.image.name, "w")
            format = 'png'
            image.save(fh, format)
            fh.close()


class Request(models.Model):
    type = [
        ('two wheeler with gear', 'two wheeler with gear'),
        ('two wheeler without gear', 'two wheeler without gear'),
        ('three wheeler', 'three wheeler'),
        ('four wheeler', 'four wheeler')
    ]
    category = models.CharField(max_length=100, choices=type)
    vehicle_no = models.PositiveIntegerField(null=False)
    vehicle_name = models.CharField(max_length=100, null=False)
    vehicle_model = models.CharField(max_length=100, null=False)
    vehicle_brand = models.CharField(max_length=100, null=False)
    problem_description = models.CharField(max_length=1000, null=False)
    date = models.DateField(auto_now=True)
    cost = models.PositiveIntegerField(null=True)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, null=True)
    mechanic = models.ForeignKey('Mechanic', on_delete=models.CASCADE, null=True)

    final = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Repairing', 'Repairing'),
        ('Repairing Done', 'Repairing Done'),
        ('Released', 'Released')
    ]
    status = models.CharField(max_length=100, choices=final, default='Pending', null=True)

    def __str__(self):
        return f"{self.vehicle_no} - {self.vehicle_name} - {self.vehicle_brand}"

    class Meta:
        ordering = ('-date',)
        verbose_name_plural = "Request"


class Attendance(models.Model):
    mechanic = models.ForeignKey('Mechanic', on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now, blank=True)
    status = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    present_status = models.CharField(max_length=20, choices=status, default='No')

    def __str__(self):
        return f"{self.mechanic} - {self.present_status}"

    class Meta:
        verbose_name_plural = "Attendance"


class Feedback(models.Model):
    username = models.CharField(max_length=40)
    message = models.CharField(max_length=500)
    date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name_plural = "Feedback"


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=100, null=False, blank=False)
    message = models.TextField(max_length=5000)

    def __str__(self):
        return f'{self.name} - {self.email}'

    class Meta:
        verbose_name_plural = "Contact"


class News(models.Model):
    email = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name_plural = "News"


class About(models.Model):
    image = models.ImageField(upload_to="images/", blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name_plural = "About"