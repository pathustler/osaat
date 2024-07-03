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
    ship_choices = [
        ('OLD DOMINION','OLD DOMINION')
    ]
    customer = models.ForeignKey(Customer, related_name='orders', on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)
    account_name = models.CharField(max_length=255)
    po_number = models.CharField(max_length=100, unique=True)
    ship_to = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    ship_via = models.CharField(max_length=100, choices=ship_choices)
    installation_address = models.CharField(max_length=100, blank=True, null=True)
    installation_address_same_as_shipping = models.BooleanField(default=True)

    def __str__(self):
        return f"Order {self.po_number} for {self.account_name}"
    
    
    
    

class Unit(models.Model):
    product_type_choices = [
        ('HD Elite FRT', 'HD Elite FRT'),
        ('STD Box Shade', 'STD Box Shade')
    ]
    handing_choices = [
        ('Left', 'Left'),
        ('Right', 'Right')
    ]
    motor_choices = [
        ('Premium Sense 25', 'Premium Sense 25')
    ]
    remote_choices = [
        ('Smartline 5 Channel', 'Smartline 5 Channel')
    ]
    accessory_choices = [
        ('Sun & Wind Sensor', 'Sun & Wind Sensor'),
        ('Wind Sensor', 'Wind Sensor'),
        ('16FT Motor Wire', '16FT Motor Wire'),
        ('32FT Motor Wire', '32FT Motor Wire'),
        ('(T) Touch-Up Paint - Black', '(T) Touch-Up Paint - Black'),
        ('(T) Touch-Up Paint - Bronze', '(T) Touch-Up Paint - Bronze'),
        ('(T) Touch-Up Paint - Dk. Beige', '(T) Touch-Up Paint - Dk. Beige'),
        ('(T) Touch-Up Paint - Ivory', '(T) Touch-Up Paint - Ivory'),
        ('(T) Touch-Up Paint - Grey', '(T) Touch-Up Paint - Grey'),
        ('(T) Touch-Up Paint - Lt. Beige', '(T) Touch-Up Paint - Lt. Beige'),
    ]
    box_color_choices = [
        ('Bronze', 'Bronze')
    ]
    hardware_color_choices = [
        ('Brown', 'Brown')
    ]
    cable_mount_choices = [
        ('Floor Mount', 'Floor Mount')
    ]
    cable_size_choices = [
        ('12FT', '12FT')
    ]
    hand_brace_choices = [
        ('48" Brown', '48" Brown')
    ]
    fabric_choices = [
        ('Suntex 95', 'Suntex 95')
    ]
    fabric_color_choices = [
        ('Dark Bronze', 'Dark Bronze')
    ]
    mounting_choices = [
        ('Side, 2 L-Channel', 'Side, 2 L-Channel')
    ]
    pile_brush_choices = [
        ('Standard', 'Standard')
    ]

    order = models.ForeignKey(Order, related_name='units', on_delete=models.CASCADE)
    unit_number = models.IntegerField()
    manual_shade = models.BooleanField(default=False)

    # Fields
    product_type = models.CharField(max_length=100, choices=product_type_choices, blank=True, null=True)
    width = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    drop = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    handing = models.CharField(max_length=50, choices=handing_choices, blank=True, null=True)
    box_color = models.CharField(choices=box_color_choices, max_length=100, blank=True, null=True)
    fabric_color = models.CharField(choices=fabric_color_choices, max_length=100, blank=True, null=True)
    mounting = models.CharField(max_length=100, choices=mounting_choices, blank=True, null=True)
    accessory = models.CharField(choices=accessory_choices, max_length=100, blank=True, null=True)
    motor_type = models.CharField(choices=motor_choices, max_length=100, blank=True, null=True)
    remote_type = models.CharField(choices=remote_choices, max_length=100, blank=True, null=True)
    hand_brace = models.CharField(choices=hand_brace_choices, max_length=100, blank=True, null=True)
    fabric_type = models.CharField(choices=fabric_choices, max_length=100, blank=True, null=True)
    hardware_color = models.CharField(choices=hardware_color_choices, max_length=100, blank=True, null=True)
    cable_mount = models.CharField(choices=cable_mount_choices, max_length=100, blank=True, null=True)
    cable_size = models.CharField(choices=cable_size_choices, max_length=100, blank=True, null=True)
    pile_brush = models.CharField(choices=pile_brush_choices, max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Unit {self.unit_number}, Order {self.order.po_number}, Customer {self.order.customer.unique_code}"









class Crew(models.Model):
    char_choices = [
        ('technician','Technician'),
        ('sales','Sales'),
        ('delivery','Delivery')
    ]
    name = models.ForeignKey(User, related_name='units', on_delete=models.CASCADE)
    crew_type = models.CharField(choices=char_choices, max_length=60)

    def __str__(self):
        return f"{self.name} ({self.crew_type})"


class TechnicianEvent(models.Model):
    statusoptions = [
        ('active','Active'),
        ('estimate','Estimate'),
        ('sold','Sold'),
        ('cancelled','Cancelled')
    ]
    visit_type_choices = [
        ('installation','Installation'),
        ('warranty','Warranty Serice'),
        ('tech','Tech Measure'),
        ('service','Service')
    ]
    crew_choices = [
        ('c1','Crew 1'),
        ('c2','Crew 2'),
        ('c3','Crew 3'),
    ]
    
    technician =  models.ForeignKey(Crew, on_delete=models.CASCADE)
    crew =  models.CharField(choices=crew_choices, max_length=20)
    confirmed = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="technician_events")
    visit_type = models.CharField(choices=visit_type_choices, max_length=100)

    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.technician} - {self.order.po_number} {self.visit_type}"
    
class SalesEvent(models.Model):
    statusoptions = [
        ('Active','active'),
        ('Estimate','estimate'),
        ('Sold','sold'),
        ('Cancelled','cancelled')
    ]
    
    salesperson = models.ForeignKey(Crew, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="sales_events")
    title = models.CharField(max_length=100)
    main_phone = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    appointment_notes = models.TextField(blank=True, null=True)
    status = models.CharField(choices=statusoptions,max_length=100)
    title = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.salesperson} - {self.order.po_number} {self.title}"


class GroupedJob(models.Model):
    statusoptions = [
        ('Delivered','delivered'),
        ('Not Delivered','notdelivered'),
        ('Missing Part','missing'),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="delivery_jobs")
    title = models.CharField(max_length=60)
    done = models.BooleanField(default=False)

class DeliveryEvent(models.Model):
   
    
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    special_instructions = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    jobs = models.ManyToManyField(GroupedJob, related_name="delivery_events")

    def __str__(self):
        return f"{self.salesperson} - {self.order.po_number} {self.title}"
    

