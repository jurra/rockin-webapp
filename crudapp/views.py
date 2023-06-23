from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Well
from .forms import ContactForm, WellForm
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'contact_list'

    def get_queryset(self):
        return Contact.objects.all()

# CONTACT VIEW
class ContactDetailView(DetailView):
    model = Contact
    template_name = 'contact-detail.html'

def create(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = ContactForm()

    return render(request,'create.html',{'form': form})

def edit(request, pk, template_name='edit.html'):
    contact = get_object_or_404(Contact, pk=pk)
    form = ContactForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, template_name, {'form':form})

def delete(request, pk, template_name='confirm_delete.html'):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method=='POST':
        contact.delete()
        return redirect('index')
    return render(request, template_name, {'object':contact})

# WELL VIEW
# def add_well(request):
#     if request.method == 'POST':
#         well_form = WellForm(request.POST)
#         core_formset = CoreFormSet(request.POST)
#         if well_form.is_valid() and core_formset.is_valid():
#             well = well_form.save()
#             cores = core_formset.save(commit=False)
#             for core in cores:
#                 core.well = well
#                 core.save()
#             return redirect('well_detail', pk=well.pk)
#     else:
#         well_form = WellForm()

class WellFormView(FormView):
    # Acceptance criteria for this form:
    # if user selects a Well that already exists in the database then the form should be invalid
    template_name = 'core.html'
    form_class = WellForm
    success_url = reverse_lazy('wells')

    def form_valid(self, form):
        if Well.objects.filter(well_name=form.cleaned_data['well_name']).exists():
            form.add_error('well_name', 'This well already exists.')
            return self.form_invalid(form)
        # If the selected Well does not exist in the database, save the form
        form.save()
        return super().form_valid(form)


# CORE VIEW AND FORMSET
# The core controller should be able to handle the following requests from 
# the entries in a form:
# - Request to create a new core
# - Identify the well from a dropdown list based on the wells registered in the database. For example DEL-GT-01
# - Select the core type from a dropdown list of predefined values from Core, Core catcher
#   - If the user selects the Core catcher, the controller should check if the preceding core matches the core number provided by the user
#   - If there is no core that matches the catcher the form view should display an error message in the html page
# - The core number should be selected from a dropdown list of predefined values from C1 to C9
# - The core section number should be a number that is incremented by 1 for each section of 1 meter for example 53
# - When user fills in the form some fields should be auto-filled
#   -  registered_by: should be auto-filled with the user who is logged in
#   -  registration_date: should be auto-filled with the current date and time  
#   -  core_section_name: should be auto-filled based on the well name, the core number and the core section number for example DELGT01-C1-53
#   -  If the use has selected catcher and it is preceeded by a core then the core_section_name should be auto-filled based on the preceding core number and the core section number for example DELGT01-C1-53-CC54
# 


