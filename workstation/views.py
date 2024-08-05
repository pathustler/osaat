from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import BoxCutJobForm, TubeCutJobForm, PreAssemblyJobForm
from main.models import Order
from .models import Box_Cut_Job, Tube_Cut_Job, Pre_Assembly_Job
# Create your views here.


def workstation_dashboard(request):
    return render(request,"workstation/index.html")


def job_search(request, job_type):
    links = {
        "box_cut": "Box Cut",
        "tube_cut": "Tube Cut",
        "pre_assembly": "Pre Assembly",

    }
    label = links[job_type]
    url_name = f"{job_type}"
    
    if job_type not in links:
        return redirect("workstation_dashboard")
    
    return render(request,"workstation/job_search.html", {"job_type":job_type,"label":label, "url_name": url_name})

def box_cut(request, po_number):
    order = get_object_or_404(Order.objects.filter(confirmed=True), po_number=po_number)
    unitforms = dict()
    totalunits = len(order.units.all())
    print("enters")
    

    editcomplete = request.POST.get('editcomplete') == 'true'
    if request.method == 'POST' and not(editcomplete):
        print("post")
        for unit in order.units.all():
            box_cut_job = Box_Cut_Job.objects.filter(unit=unit).first()
            
            if box_cut_job:

                form = BoxCutJobForm(request.POST, instance=box_cut_job, prefix=str(unit.id))
            else:

                # Create a new Box_Cut_Job instance with default values
                box_cut_job = Box_Cut_Job(unit=unit)
                form = BoxCutJobForm(request.POST, instance=box_cut_job, prefix=str(unit.id))

            unitforms[unit.unit_number] = form
            if form.is_valid():
                instance = form.save(commit=False)
                instance.unit = unit
                instance.save()
            else:
                print(form.errors)

        return render(request, "workstation/box_cut.html", {'unitforms': unitforms, 'order': order, 'totalunits':totalunits})

    else:
        print("get")
        for unit in order.units.all():
            box_cut_job = Box_Cut_Job.objects.filter(unit=unit).first()
            if box_cut_job:
                form = BoxCutJobForm(instance=box_cut_job, prefix=str(unit.id))
            else:
                # Create a new Box_Cut_Job instance with default values
       
                box_cut_job = Box_Cut_Job(unit=unit)
                box_cut_job.save()  # Save the new instance with default values
                form = BoxCutJobForm(instance=box_cut_job, prefix=str(unit.id))

            unitforms[unit.unit_number] = form
            print("unitforms:")
            print(unit)
            print("===========")
            
    order_complete = False
    for unit in order.units.all():
        box_cut_job = Box_Cut_Job.objects.filter(unit=unit).first()
        if not box_cut_job.job_complete:
            order_complete =False
        else:
            order_complete =True
            
    if order_complete:
        if editcomplete:
            return render(request, "workstation/box_cut.html", {'unitforms': unitforms, 'order': order, 'totalunits':totalunits})
            
        else:
            return render(request, "workstation/job_complete.html", {"po_number":order.po_number,"label":"Box Cut","link":"box_cut"})
        

    return render(request, "workstation/box_cut.html", {'unitforms': unitforms, 'order': order, 'totalunits':totalunits})

def confirm_box_cut(request, po_number):
    order = get_object_or_404(Order, po_number=po_number)
    units = order.units.all()
    
    print("METHOD POST")
    if request.method == 'POST':
        for unit in units:
            box_cut_job = Box_Cut_Job.objects.filter(unit=unit).first()
            print(box_cut_job)
            if box_cut_job:
                box_cut_job.job_complete = True
                box_cut_job.box_cut_drop_used = True
                box_cut_job.box_cut_hd_box = True
                box_cut_job.box_cut_cut_length = True
                box_cut_job.box_prep_track_notch = True
                box_cut_job.box_prep_drill_holes_top_back = True
                box_cut_job.box_prep_drill_holes_front_bottom = True
                box_cut_job.hem_bar_drop_used = True
                box_cut_job.hem_bar_hd_hem_bar = True
                box_cut_job.hem_bar_cut_length = True
                box_cut_job.hem_bar_drill_end_cap_screws = True
                box_cut_job.hem_bar_drill_hook_hole = True
                box_cut_job.tracks_drop_used = True
                box_cut_job.tracks_hd_tracks = True
                box_cut_job.tracks_cut_length = True
                box_cut_job.tracks_drill_mounting_holes = True
                box_cut_job.tracks_drill_hook_hole = True
                box_cut_job.tube_drop_used = True
                box_cut_job.tube_length = True
                box_cut_job.tube_cut_length = True
                box_cut_job.l_channel_drop_used = True
                box_cut_job.l_channel_quantity = True
                box_cut_job.l_channel_cut_length = True
                box_cut_job.l_channel_drill_hook_hole = True
                box_cut_job.save()
        

    return redirect('workstation_dashboard')  
        

def tube_cut(request, po_number):
    order = get_object_or_404(Order.objects.filter(confirmed=True), po_number=po_number)
    unitforms = dict()
    totalunits = len(order.units.all())
    print("enters")

    editcomplete = request.POST.get('editcomplete') == 'true'
    if request.method == 'POST' and not(editcomplete):
        print("post")
        for unit in order.units.all():
            tube_cut_job = Tube_Cut_Job.objects.filter(unit=unit).first()
            
            if tube_cut_job:

                form = TubeCutJobForm(request.POST, instance=tube_cut_job, prefix=str(unit.id))
            else:

                # Create a new Box_Cut_Job instance with default values
                tube_cut_job = Tube_Cut_Job(unit=unit)
                form = TubeCutJobForm(request.POST, instance=tube_cut_job, prefix=str(unit.id))

            unitforms[unit.unit_number] = form
            if form.is_valid():
                instance = form.save(commit=False)
                instance.unit = unit
                instance.save()
            else:
                print(form.errors)

        return render(request, "workstation/tube_cut.html", {'unitforms': unitforms, 'order': order, 'totalunits':totalunits})

    else:
        print("get")
        for unit in order.units.all():
            tube_cut_job = Tube_Cut_Job.objects.filter(unit=unit).first()
            if tube_cut_job:
                form = TubeCutJobForm(instance=tube_cut_job, prefix=str(unit.id))
            else:
                # Create a new Box_Cut_Job instance with default values
       
                tube_cut_job = Tube_Cut_Job(unit=unit)
                tube_cut_job.save()  # Save the new instance with default values
                form = TubeCutJobForm(instance=tube_cut_job, prefix=str(unit.id))

            unitforms[unit.unit_number] = form
            
    order_complete = False
    for unit in order.units.all():
        tube_cut_job = Tube_Cut_Job.objects.filter(unit=unit).first()
        if not tube_cut_job.job_complete:
            order_complete =False
        else:
            order_complete =True
    if order_complete:
        if editcomplete:
            return render(request, "workstation/tube_cut.html", {'unitforms': unitforms, 'order': order, 'totalunits':totalunits})
            
        else:
            return render(request, "workstation/job_complete.html", {"po_number":order.po_number,"label":"Tube Cut","link":"tube_cut"})
        

    return render(request, "workstation/tube_cut.html", {'unitforms': unitforms, 'order': order, 'totalunits':totalunits})


def confirm_tube_cut(request, po_number):
    order = get_object_or_404(Order, po_number=po_number)
    units = order.units.all()
    
    print("METHOD POST")
    if request.method == 'POST':
        for unit in units:
            tube_cut_job = Tube_Cut_Job.objects.filter(unit=unit).first()
            print(tube_cut_job)
            if tube_cut_job:
                tube_cut_job.job_complete=True
                tube_cut_job.tube_drop_used = True
                tube_cut_job.tube_length = True
                tube_cut_job.tube_cut_length = True
                tube_cut_job.stock_drop_used = True
                tube_cut_job.stock_cut_length = True
                tube_cut_job.save()
        

    return redirect('workstation_dashboard')  
        

def pre_assembly(request, po_number):
    order = get_object_or_404(Order.objects.filter(confirmed=True), po_number=po_number)
    unitforms = dict()
    totalunits = len(order.units.all())
    print("enters")

    editcomplete = request.POST.get('editcomplete') == 'true'
    if request.method == 'POST' and not(editcomplete):
        print("post")
        for unit in order.units.all():
            pre_assembly_job = Pre_Assembly_Job.objects.filter(unit=unit).first()
            
            if pre_assembly_job:

                form = PreAssemblyJobForm(request.POST, instance=pre_assembly_job, prefix=str(unit.id))
            else:

                # Create a new Box_Cut_Job instance with default values
                pre_assembly_job = Pre_Assembly_Job(unit=unit)
                form = PreAssemblyJobForm(request.POST, instance=pre_assembly_job, prefix=str(unit.id))

            unitforms[unit.unit_number] = form
            if form.is_valid():
                instance = form.save(commit=False)
                instance.unit = unit
                instance.save()
            else:
                print(form.errors)

        return render(request, "workstation/pre_assembly.html", {'unitforms': unitforms, 'order': order, 'totalunits':totalunits})

    else:
        print("get")
        for unit in order.units.all():
            pre_assembly_job = Pre_Assembly_Job.objects.filter(unit=unit).first()
            if pre_assembly_job:
                form = PreAssemblyJobForm(instance=pre_assembly_job, prefix=str(unit.id))
            else:
                # Create a new Box_Cut_Job instance with default values
                pre_assembly_job = Pre_Assembly_Job(unit=unit)
                pre_assembly_job.save()  # Save the new instance with default values
                form = PreAssemblyJobForm(instance=pre_assembly_job, prefix=str(unit.id))

            unitforms[unit.unit_number] = form
            
    order_complete = False
    for unit in order.units.all():
        pre_assembly_job = Pre_Assembly_Job.objects.filter(unit=unit).first()
        if not pre_assembly_job.job_complete:
            order_complete =False
        else:
            order_complete =True
    if order_complete:
        if editcomplete:
            return render(request, "workstation/pre_assembly.html", {'unitforms': unitforms, 'order': order, 'totalunits':totalunits})
            
        else:
            return render(request, "workstation/job_complete.html", {"po_number":order.po_number,"label":"Pre Assembly","link":"pre_assembly"})
        

    return render(request, "workstation/pre_assembly.html", {'unitforms': unitforms, 'order': order, 'totalunits':totalunits})


def confirm_pre_assembly(request, po_number):
    order = get_object_or_404(Order, po_number=po_number)
    units = order.units.all()
    
    print("METHOD POST")
    if request.method == 'POST':
        for unit in units:
            pre_assembly_job = Pre_Assembly_Job.objects.filter(unit=unit).first()
            print(pre_assembly_job)
            if pre_assembly_job:
                pre_assembly_job.job_complete=True
                pre_assembly_job.tube_drop_used = True
                pre_assembly_job.tube_length = True
                pre_assembly_job.tube_cut_length = True
                pre_assembly_job.stock_drop_used = True
                pre_assembly_job.stock_cut_length = True
                pre_assembly_job.save()
        

    return redirect('workstation_dashboard')  




def hardware(request):
    return render(request,"workstation/box_cut.html")

def powder_coat(request):
    return render(request,"workstation/box_cut.html")

def fabric(request):
    return render(request,"workstation/box_cut.html")

def assembly(request):
    return render(request,"workstation/box_cut.html")

def shipping(request):
    return render(request,"workstation/box_cut.html")



