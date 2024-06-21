from django.db import models
from django.contrib.auth.models import User
import random
import string


def generate_unique_code():
    return ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=10))

class Customer(models.Model):
    primary_contact = models.CharField(max_length=255)
    main = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    account_notes = models.TextField(blank=True, null=True)
    default_order_notes = models.TextField(blank=True, null=True)
    unique_code = models.CharField(max_length=13, unique=True, default=generate_unique_code, editable=False)

    def __str__(self):
        return self.unique_code

class WasabiGallery(models.Model):
    customer = models.ForeignKey(Customer, related_name='wasabi_gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='wasabi_gallery/')

    def __str__(self):
        return f"{self.customer.primary_contact} - Gallery Image"

class Timeline(models.Model):
    TYPE_CHOICES = [
        ('ti', 'Technical Issues'),
        ('of', 'Order Finalized'),
        ('rma', 'RMA'),
        ('other','Other')
    ]
    customer = models.ForeignKey(Customer, related_name='timeline', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=64, choices=TYPE_CHOICES, default='other')
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.primary_contact} - {self.timestamp}"

class WasabiFile(models.Model):
    customer = models.ForeignKey(Customer, related_name='wasabi_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='wasabi_files/')

    def __str__(self):
        return f"{self.customer.primary_contact} - File"





class Order(models.Model):
    account_name = models.CharField(max_length=255)
    po_number = models.CharField(max_length=100)
    ship_to = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    ship_via = models.CharField(max_length=100)
    installation_address_same_as_shipping = models.BooleanField(default=True)

    def __str__(self):
        return f"Order {self.po_number} for {self.account_name}"
    
    
    
    

class Unit(models.Model):
    order = models.ForeignKey(Order, related_name='units', on_delete=models.CASCADE)
    unit_count = models.IntegerField()
    manual_shade = models.BooleanField(default=False)

    # Fields for manual units
    product_type_manual = models.CharField(max_length=100, blank=True, null=True)
    width_manual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    drop_manual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    handing_manual = models.CharField(max_length=50, blank=True, null=True)
    box_color_manual = models.CharField(max_length=100, blank=True, null=True)
    fabric_color_manual = models.CharField(max_length=100, blank=True, null=True)
    mounting_manual = models.CharField(max_length=100, blank=True, null=True)

    # Fields for motorized units
    product_type_motorized = models.CharField(max_length=100, blank=True, null=True)
    width_motorized = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    drop_motorized = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    handing_motorized = models.CharField(max_length=50, blank=True, null=True)
    motor_type = models.CharField(max_length=100, blank=True, null=True)
    remote_type = models.CharField(max_length=100, blank=True, null=True)
    box_color_motorized = models.CharField(max_length=100, blank=True, null=True)
    fabric_type_motorized = models.CharField(max_length=100, blank=True, null=True)
    fabric_color_motorized = models.CharField(max_length=100, blank=True, null=True)
    mounting_motorized = models.CharField(max_length=100, blank=True, null=True)
    hardware_color_motorized = models.CharField(max_length=100, blank=True, null=True)
    cable_mount_motorized = models.CharField(max_length=100, blank=True, null=True)
    cable_size_motorized = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Unit {self.id} in Order {self.order.po_number}"