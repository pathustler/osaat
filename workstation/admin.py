from django.contrib import admin
from django.contrib import admin
from .models import Box_Cut_Job, Tube_Cut_Job, Pre_Assembly_Job

# Register your models here.

class BoxCutJobAdmin(admin.ModelAdmin):
    list_display = (
        'unit', 
        'job_complete', 
        'box_cut_drop_used', 
        'box_cut_hd_box', 
        'box_cut_cut_length',
        'box_prep_track_notch',
        'box_prep_drill_holes_top_back',
        'box_prep_drill_holes_front_bottom',
        'hem_bar_drop_used',
        'hem_bar_hd_hem_bar',
        'hem_bar_cut_length',
        'hem_bar_drill_end_cap_screws',
        'hem_bar_drill_hook_hole',
        'tracks_drop_used',
        'tracks_hd_tracks',
        'tracks_cut_length',
        'tracks_drill_mounting_holes',
        'tracks_drill_hook_hole',
        'tube_drop_used',
        'tube_length',
        'tube_cut_length',
        'l_channel_drop_used',
        'l_channel_quantity',
        'l_channel_cut_length',
        'l_channel_drill_hook_hole'
    )
    list_filter = ('unit', 'job_complete')
    search_fields = ('unit__unit_number',)

admin.site.register(Box_Cut_Job, BoxCutJobAdmin)


class TubeCutJobAdmin(admin.ModelAdmin):
    list_display = (
        'unit', 
        'job_complete', 
        'tube_drop_used',
        'tube_length',
        'tube_cut_length',
        'stock_drop_used',
        'stock_cut_length',
    )
    list_filter = ('unit', 'job_complete')
    search_fields = ('unit__unit_number',)

admin.site.register(Tube_Cut_Job, TubeCutJobAdmin)



class PreAssemblyJobAdmin(admin.ModelAdmin):
    list_display = (
        'unit', 
        'job_complete', 
        'tube',
        'box_end_caps',
        'track',
        'bottom_bar',
        'side_2_l_channels',
    )
    list_filter = ('unit', 'job_complete')
    search_fields = ('unit__unit_number',)

admin.site.register(Pre_Assembly_Job,  PreAssemblyJobAdmin)