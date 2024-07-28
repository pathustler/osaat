from django.db import models
from main.models import Unit
# Create your models here.


class Box_Cut_Job(models.Model):
    unit = models.ForeignKey(Unit, related_name='box_cut_jobs', on_delete=models.CASCADE)
    
    job_complete = models.BooleanField(default=False)
    
    box_cut_drop_used = models.BooleanField(default=False)
    box_cut_hd_box = models.BooleanField(default=False)
    box_cut_cut_length = models.BooleanField(default=False)
    
    box_prep_track_notch = models.BooleanField(default=False)
    box_prep_drill_holes_top_back = models.BooleanField(default=False)
    box_prep_drill_holes_front_bottom = models.BooleanField(default=False)
    
    hem_bar_drop_used = models.BooleanField(default=False)
    hem_bar_hd_hem_bar = models.BooleanField(default=False)
    hem_bar_cut_length = models.BooleanField(default=False)
    hem_bar_drill_end_cap_screws = models.BooleanField(default=False)
    hem_bar_drill_hook_hole = models.BooleanField(default=False)
    
    tracks_drop_used = models.BooleanField(default=False)
    tracks_hd_tracks = models.BooleanField(default=False)
    tracks_cut_length = models.BooleanField(default=False)
    tracks_drill_mounting_holes = models.BooleanField(default=False)
    tracks_drill_hook_hole = models.BooleanField(default=False)
    
    tube_drop_used = models.BooleanField(default=False)
    tube_length = models.BooleanField(default=False)
    tube_cut_length = models.BooleanField(default=False)
    
    l_channel_drop_used = models.BooleanField(default=False)
    l_channel_quantity = models.BooleanField(default=False)
    l_channel_cut_length = models.BooleanField(default=False)
    l_channel_drill_hook_hole = models.BooleanField(default=False)
    

class Tube_Cut_Job(models.Model):
    unit = models.ForeignKey(Unit, related_name='tube_cut_jobs', on_delete=models.CASCADE)
    
    job_complete = models.BooleanField(default=False)
    
    tube_drop_used = models.BooleanField(default=False)
    tube_length = models.BooleanField(default=False)
    tube_cut_length = models.BooleanField(default=False)
    
    stock_drop_used = models.BooleanField(default=False)
    stock_cut_length = models.BooleanField(default=False)
    
    
class Pre_Assembly_Job(models.Model):
    unit = models.ForeignKey(Unit, related_name='pre_assembly_jobs', on_delete=models.CASCADE)
    
    job_complete = models.BooleanField(default=False)
    
    tube = models.BooleanField(default=False)
    box_end_caps = models.BooleanField(default=False)
    track = models.BooleanField(default=False)
    bottom_bar = models.BooleanField(default=False)
    side_2_l_channels = models.BooleanField(default=False)
    
    