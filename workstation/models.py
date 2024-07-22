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
    
