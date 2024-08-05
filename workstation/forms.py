from django import forms
from .models import Box_Cut_Job, Tube_Cut_Job,Pre_Assembly_Job
from django.utils.safestring import mark_safe





class CustomCheckboxInput(forms.CheckboxInput):
    template_name = 'widgets/button_checkbox.html'
    
    
    
    

class BoxCutJobForm(forms.ModelForm):
    class Meta:
        model = Box_Cut_Job
        fields = [
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
            'l_channel_drill_hook_hole',
        ]
        widgets = {
            'box_cut_drop_used': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'box_cut_hd_box': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'box_cut_cut_length': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'box_prep_track_notch': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'box_prep_drill_holes_top_back': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'box_prep_drill_holes_front_bottom': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'hem_bar_drop_used': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'hem_bar_hd_hem_bar': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'hem_bar_cut_length': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'hem_bar_drill_end_cap_screws': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'hem_bar_drill_hook_hole': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'tracks_drop_used': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'tracks_hd_tracks': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'tracks_cut_length': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'tracks_drill_mounting_holes': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'tracks_drill_hook_hole': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'tube_drop_used': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'tube_length': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'tube_cut_length': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'l_channel_drop_used': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'l_channel_quantity': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'l_channel_cut_length': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'l_channel_drill_hook_hole': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
        }


class TubeCutJobForm(forms.ModelForm):
    class Meta:
        model = Tube_Cut_Job
        
        fields = [
            'tube_drop_used',
            'tube_length',
            'tube_cut_length',
            'stock_drop_used',
            'stock_cut_length',
            
        ]
        widgets = {
            'tube_drop_used': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'tube_length': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'tube_cut_length': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'stock_drop_used': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'stock_cut_length': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
        }
        
    
    
     
     
    
    
class PreAssemblyJobForm(forms.ModelForm):
    class Meta:
        model = Pre_Assembly_Job
        fields = [
            'tube',
            'box_end_caps',
            'track',
            'bottom_bar',
            'side_2_l_channels',
        ]
        widgets = {
            'tube': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'box_end_caps': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'track': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'bottom_bar': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
            'side_2_l_channels': forms.CheckboxInput(attrs={'class': 'hidden cursor-pointer'}),
        }