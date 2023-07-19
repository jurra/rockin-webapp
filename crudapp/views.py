from typing import Any
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django.views.generic import ListView, DetailView, FormView
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Contact, Well, Core
from .forms import ContactForm, WellForm, CoreForm

from pydantic import ValidationError

# Here we have access to the pydantic models,
# we keep datamodel as a namespace to avoid confusion with the django models
import datamodel


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

    return render(request, 'create.html', {'form': form})


def edit(request, pk, template_name='edit.html'):
    contact = get_object_or_404(Contact, pk=pk)
    form = ContactForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('index')
    return render(request, template_name, {'form': form})


def delete(request, pk, template_name='confirm_delete.html'):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('index')
    return render(request, template_name, {'object': contact})


def _validate(view, post_data, **kwargs):
    ''' How it works:
    - Get the name of the model that we're working with, Such model has a class
    in pydantic, for example Well and also on Django ORM with the same name
    - Get the data from the POST request
    - Add an ID to the data (if one doesn't already exist) this is required for pydantic to work
    because the id is part of the data model in pydantic.
    - Validate the data by creating the pydantic model instance, 
    pydantic automatically validates the data
    Args:
        view ([type]): [description], this is the view that is calling the function
        request ([type]): [description], this is the request object

    Returns:

    '''
    model_name = kwargs.get('model_name')

    try:
        # Get the correct model class for example Well, or Core
        model = getattr(datamodel, model_name)

        # Create a new instance of the specified model using the provided data
        # This will raise a ValidationError if the data is invalid
        validated_data = model(**post_data)
        # print("DB, Validated data: " + type(validated_data))
        # print(model_instance)
    except ValidationError as e:
        return e
    return validated_data

class HomeView(ListView):
    template_name = 'index.html'
    context_object_name = 'well_list'

    def get(self, request, *args, **kwargs):
        # A list of all wells
        try:
            wells = Well.objects.all()
            return render(request, self.template_name, {'wells': wells})
        except Well.DoesNotExist:
            return render(request, self.template_name, {'wells': None})

class WellListView(ListView):
    template_name = 'well_list.html'
    context_object_name = 'well_list'

    def get(self, request, *args, **kwargs):
        # A list of all the wells in the database
        try:
            wells = Well.objects.all()
            return render(request, self.template_name, {'wells': wells})
        except Well.DoesNotExist:
            return render(request, self.template_name, {'wells': None})

class WellFormView(FormView):
    template_name = 'well.html'
    form_class = WellForm
    success_url = reverse_lazy('well_list')

    def post(self, request, *args, **kwargs):
        post_data = request.POST.dict()
        # Our current pydantic model needs an id to be created
        # This is why we add it here, but when we pass the data to the form
        # It will be ignored later.
        if 'id' not in post_data:
            post_data['id'] = 1

        checked_well = _validate(self, post_data=post_data, model_name='Well')

        if checked_well is not None:
            if type(checked_well) is ValidationError:
                form = self.get_form()
                for error in checked_well.errors():
                    field = error['loc'][0]
                    message = error['msg']
                    form.add_error(field, message)
                return self.form_invalid(form)

        # Reject entry if the selected Well already exists in the database
        if Well.objects.filter(name=checked_well.name).exists():
            form = self.get_form()
            # form.add_error('name', 'This well already exists.')
            return self.form_invalid(form)

        # If the selected Well does not exist in the database, save the form
        form = self.get_form()
        if form.is_valid():
            form.save()
            return super().form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

class WellCoreListView(ListView):
    ''' This view is used to list all the cores that belong to a well
    '''
    model = Well
    template_name = 'well_core_list.html'
    context_object_name = 'well_core_list'
    success_url = reverse_lazy('cores')

    def get(self, request, *args, **kwargs):
        try:
            well = Well.objects.get(pk=self.kwargs['pk'])
            cores = Core.objects.filter(well=well)

            return render(request, self.template_name, {'well': well,
                                                        'cores': cores})

        except Well.DoesNotExist:
            return render(request, self.template_name, {'well': None, 'cores': None})

class CoreFormView(FormView):
    '''This view is used to create a new core
    '''
    template_name = 'core.html'
    form_class = CoreForm
    success_url = reverse_lazy('well_core_list')

    # Define relationship between the core and the well
    well_name = ""
    well = None
    core_number = None

    def set_well_name_from_url(self):
        self.well_name = self.request.GET.get('well_name')

    def set_success_url(self,):
        self.success_url = reverse_lazy('well_core_list', kwargs={'pk': self.well.pk})
    
    def set_well(self):
        try:
            self.well = Well.objects.get(name=self.well_name)
        except Well.DoesNotExist:
            self.well = None

    def set_core_section_number(self):
        self.core_number = self.request.GET.get('core_number')

        # Based on the core number we get from the url, we propose the next core section number
        # We also if the core_section_number is not provided, we propose 1 or the next number
        if self.core_number:
            # With this query we get the last count of the core_section_number for the current core number
            latest_core_section_number = Core.objects.filter(core_number=self.core_number).aggregate(
                Max('core_section_number'))['core_section_number__max']
            if latest_core_section_number is not None:
                return latest_core_section_number + 1
            else:
                return 1

    def get_initial(self):
        ''' With this function we pre-populate the form with initial values to avoid that users
        having to type the same values over and over again 
        '''
        initial = super().get_initial()

        # Define all the initial values of the form object
        self.set_well_name_from_url()
        self.set_well()
        self.set_success_url()

        # Propose the user collection date as the current date and time
        initial['collection_date'] = timezone.now()

        initial['well'] = self.well_name

        core_number = self.request.GET.get('core_number')
        initial['core_number'] = core_number
        initial['core_section_number'] = self.set_core_section_number()
        return initial

    # Create section name based on the well name, the core number and the core section number
    def post(self, request, *args, **kwargs):
        post_data = request.POST.dict()

        # We do this because pydantic needs an id to be created
        if 'id' not in post_data:
            post_data['id'] = 1

        if request.user.is_authenticated:
            current_user = request.user
        else:
            raise Exception('User is not authenticated')

        # Add the core section name to the post data to make the post data valid
        core_section_name = f"{post_data.get('well')}-{post_data.get('core_number')}-{post_data.get('core_section_number')}"        
        post_data['core_section_name'] = core_section_name

        if Core.objects.filter(core_section_name=core_section_name).exists():
            form = self.get_form()
            form.add_error(
                'core_section_name', f'A core with name {core_section_name} already exists. Please try again with a number bigger than {post_data.get("core_section_number") }.')
            return self.form_invalid(form)
        checked_core = _validate(self, post_data=post_data, model_name='Core')

        if checked_core is not None:
            if checked_core is ValidationError:
                form = self.get_form()
                for error in checked_core.errors():
                    field = error['loc'][0]
                    message = error['msg']
                    form.add_error(field, message)

                return self.form_invalid(form)

        form = self.get_form()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.registered_by = current_user
            instance.save()
            return super().form_valid(instance)
        else:
            print(form.errors)
            return self.form_invalid(form)

class CoreChip(FormView):
    template_name = 'corechip_form.html'
    form_class = CoreForm
    success_url = reverse_lazy('well_core_list')

    def get_initial(self):
        ''' With this function we can pre-populate the form with initial values 
        some of the values are based on the url parameters like for example the well name
        '''
        initial = super().get_initial()
        # Propose the user collection date as the current date and time
        initial['collection_date'] = timezone.now()
        
        # Get the well to generate the success url
        well_name = self.request.GET.get('well_name')
        well = Well.objects.get(name=well_name)
        self.success_url = reverse_lazy('well_core_list', kwargs={'pk': well.pk})

        
        initial['well'] = well_name
        well_short_name = well.gen_short_name()
        initial['well_short_name'] = well_short_name
        pass

    def post(self, request, *args, **kwargs):
        post_data = request.POST.dict()
        # core_chip_name = f"{post_data.get('well')}-{post_data.get('core_number')}-{post_data.get('core_section_number')}"
        pass
        # Check if the CoreChip already exists
        # if CoreChip.objects.filter(core_chip_name=):
        

