import pprint as pp
import json

from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Max
from django.views.generic import ListView, DetailView, FormView, View
from django.urls import reverse_lazy
from django.utils import timezone

from .models import Contact, Well, Core, CoreChip
from .forms import ContactForm, WellForm, CoreForm, CoreChipForm, MicroCoreForm, CuttingsForm

from pydantic import ValidationError

# Here we have access to the pydantic models,
# we keep datamodel as a namespace to avoid confusion with the django models
import datamodel

def set_well_name(view_instance, well_name):
    view_instance.well_name = well_name

def get_well_from_pk(well_pk, Well):
    try:
        well = Well.objects.get(pk=well_pk)
        return well
    except Well.DoesNotExist:
        raise Exception('No well was passed to the view')

def set_well(view_instance, Well):
    try:
        view_instance.well = Well.objects.get(name=view_instance.well_name)
    except Well.DoesNotExist:
        view_instance.well = None

def set_success_url(view_instance, url_name):
    if view_instance.well is not None:
        view_instance.success_url = reverse_lazy(url_name, kwargs={'pk': view_instance.well.pk})
    else:
        raise Exception('Well is None')

def calculate_next_core_section_number(Core, core_number):
    latest_number = Core.objects.filter(core_number=core_number).aggregate(
        Max('core_section_number'))['core_section_number__max']
    return latest_number + 1 if latest_number is not None else 1

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

def get_well_from_pk(well_pk, Well):
    try:
        well = Well.objects.get(pk=well_pk)
        return well
    except Well.DoesNotExist:
        raise Exception('No well was passed to the view')


def _validate(payload, **kwargs):
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
        kwargs ([type]): [description], this is a dictionary with the model name

    Returns:
        validated_data ()

    Example:
    >>> _validate(view=self, request=request, payload=post_data, model_name='Well')
    '''
    model_name = kwargs.get('model_name')

    try:
        # Get the correct model class for example Well, or Core
        model = getattr(datamodel, model_name)

        # Create a new instance of the specified model using the provided data
        # This will raise a ValidationError if the data is invalid
        validated_data = model(**payload)
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


class SampleFormView(View):
    ''' This view is used to create a new sample
    it handles different types of samples, for example: Core, CoreChip, MicroCore, depending on the selected type
    the view will redirect the user to the correct form
    '''
    model = Well
    template_name = 'create_sample.html'  # Replace with your form template
    success_url = reverse_lazy('create_sample', kwargs={'pk': 'pk'})

    def get(self, request, *args, **kwargs):
        well_pk = self.kwargs.get('pk')
        well = get_well_from_pk(well_pk=well_pk, Well=self.model)
        sample_type = request.GET.get('sample_type')
        
        if sample_type:
            if sample_type == 'Core':
                return redirect(reverse_lazy('select_core_number', kwargs={'pk': well_pk}))
            elif sample_type == 'Core Catcher':
                return redirect(reverse_lazy('select_core_number', kwargs={'pk': well_pk}))
            elif sample_type == 'Microcore':
                # The well_name is required as a query parameter
                return redirect(reverse_lazy('microcores', kwargs={'pk': well.pk}) + f'?well_name={well.name}') 
            # elif sample_type == 'Cuttings':
            #     return redirect(reverse_lazy('cuttings', kwargs={'pk': well_pk}))
            elif sample_type == 'Corechip':
                return redirect(reverse_lazy('corechips_select', kwargs={'pk': well_pk}))
        
        # Default action if sample_type is empty or doesn't match
        return render(request, self.template_name, {'well': well})

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

        checked_well = _validate(payload=post_data, model_name='Well')

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


class CoreNumberSelectView(ListView):
    ''' This view is used to list all the cores that belong to a well
    '''
    model = Well
    template_name = 'well_cores_list.html'
    context_object_name = 'select_core_number'
    success_url = reverse_lazy('core_form')

    def get(self, request, *args, **kwargs):
        try:
            well = get_well_from_pk(well_pk=self.kwargs['pk'], Well=self.model)
            cores = Core.objects.filter(well=well)

            return render(request, self.template_name, {'well': well,
                                                        'core_form': cores})
        except Well.DoesNotExist:
            return render(request, self.template_name, {'well': None, 'core_form': None})


class CoreFormView(FormView):
    '''This view is used to create a new core
    AC: A new core form is presented to the user when makes a post request
    to this url: well/<pk>/core/create
    '''
    template_name = 'core.html'
    form_class = CoreForm
    success_url = reverse_lazy('create_sample')

    # Define relationship between the core and the well
    well_name = None
    well = None
    core_number = None

    def get_initial(self):
        '''With this function, we pre-populate the form with initial values to avoid having users
        type the same values repeatedly.
        '''
        initial = super().get_initial()

        # Capture well_name from the URL query parameters
        well_name = self.request.GET.get('well_name')

        # Ensure that well_name is not None before assigning it
        assert well_name is not None, 'well_name is None'
        initial['well'] = well_name
        # Propose the user collection date as the current date and time
        initial['collection_date'] = timezone.now()

        core_number = self.request.GET.get('core_number')
        initial['core_number'] = core_number
        initial['core_section_number'] = calculate_next_core_section_number(Core, core_number)   
        return initial

    # Create section name based on the well name, the core number and the core section number
    def post(self, request, *args, **kwargs):
        post_data = request.POST.dict()
        
        # Setup success url based on well name submitted in the post request data
        set_well_name(self, post_data.get('well'))
        set_well(self, Well)
        set_success_url(self, 'create_sample')

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

        checked_core = _validate(payload=post_data, model_name='Core')

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

class CoreChipSelectView(ListView):
    template_name = 'corechip_select.html'
    success_url = ""

    def get(self, request, *args, **kwargs):
        well = get_well_from_pk(well_pk=self.kwargs['pk'], Well=Well)
        cores = Core.objects.filter(well=well)

        self.success_url = reverse_lazy('corechips_select', kwargs={'pk': well.pk})
        return render(request, self.template_name, {'well': well,
                                                    'corechips_select': cores})

class CoreChipFormView(FormView):
    template_name = 'corechip_form.html'
    form_class = CoreChipForm
    success_url = reverse_lazy('select_core_number')

    # A Well object
    well = None
    well_name = None
    core_number = None

    def get_initial(self):
        ''' With this function we pre-populate the form with initial values to avoid that users
        having to type the same values over and over again 
        '''
        initial = super().get_initial()

        # Propose the user collection date as the current date and time
        initial['collection_date'] = timezone.now()

        # initial['well'] = self.well_name
        initial['well_name'] = self.well_name

        core_number = self.request.GET.get('core_number')
        initial['core_number'] = core_number
        initial['core_section_number'] = calculate_next_core_section_number(Core, core_number)
        return initial

    def get(self, request, *args, **kwargs):
        core_section_name = request.GET.get('core_section_name')
        # Extract the core based on the core_section_name
        core = Core.objects.get(core_section_name=core_section_name)

        # We extract initial data from GET request parameters to pre-populate the form
        data = {
            'well': request.GET.get('well_name'),
            'well_pk': request.GET.get('well_pk'),
            'well_name': request.GET.get('well_name'),
            'core_number': request.GET.get('core_number'),
            'planned_core_number': core.planned_core_number,
            'core_section_name': request.GET.get('core_section_name'),
            'core_section_number': request.GET.get('core_section_number'),
            'collection_date': timezone.now(),
        }

        self.initial = data
        form = self.form_class(initial=data)

        # Define all the initial values of the form object
        set_well_name(self, data['well_name'])

        # Set success url based on well pk
        return render(request, self.template_name, {'form': form, **data})

    def post(self, request, *args, **kwargs):
        post_data = request.POST.dict()

        # raise error if GET.dict doesn't have the well_name
        well_name = post_data.get('well_name')
        if well_name is None:
            raise Exception('Query data does not have the well_name')

        # Setup success url based on well name submitted in the post request data
        set_well_name(self, post_data.get('well_name'))
        set_well(self, Well)
        set_success_url(self, 'create_sample')

        if request.user.is_authenticated:
            current_user = request.user
        else:
            raise Exception('User is not authenticated')

        # Add the corechip name to the post data to make the post data valid
        corechip_name = f"{post_data.get('well')}-{post_data.get('core_number')}-{post_data.get('core_section_number')}-{post_data.get('corechip_number')}-{post_data.get('from_top_bottom')}"
        
        if CoreChip.objects.filter(corechip_name=corechip_name).exists():
            form = self.get_form()
            form.add_error(
                'corechip_name', f'A corechip with name {corechip_name} already exists. Please try again with a number bigger than {post_data.get("corechip_number") }.')
            return self.form_invalid(form)

        checked_corechip = _validate(payload=post_data, model_name='CoreChip')

        if checked_corechip is not None:
            if checked_corechip is ValidationError:
                form = self.get_form()
                for error in checked_corechip.errors():
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
            return self.form_invalid(form)


class MicroCoreFormView(FormView):
    template_name = 'microcore_form.html'
    form_class = MicroCoreForm
    success_url = reverse_lazy('create_sample')
    
    well = None
    well_name = None
    
    def get_initial(self):
        '''With this function, we pre-populate the form with initial values to avoid having users
        type the same values repeatedly.
        '''
        initial = super().get_initial()

        # Capture well_name from the URL query parameters
        well_name = self.request.GET.get('well_name')
        self.well_name = well_name

        # Ensure that well_name is not None before assigning it
        assert well_name is not None, 'well_name is None'
        initial['well'] = well_name
        # Propose the user collection date as the current date and time
        initial['collection_date'] = timezone.now()
        return initial
    

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()

        if request.user.is_authenticated:
            current_user = request.user
        else:
            raise Exception('User is not authenticated')
        
        # Set success url based on well pk
        self.well = get_well_from_pk(self.kwargs['pk'], Well)
        set_success_url(self, 'create_sample')

        checked_microcore = _validate(payload=data, model_name='MicroCore')

        if checked_microcore is not None:
            if checked_microcore is ValidationError:
                form = self.get_form()
                for error in checked_microcore.errors():
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
            return self.form_invalid(form)

class CuttingsFormView(FormView):
    template_name = 'cuttings_form.html'  # Specify your template for Cuttings
    form_class = CuttingsForm  # Use the form specific to Cuttings
    success_url = reverse_lazy('cuttings_list')  # Redirect to the cuttings list page after successful form submission

    def get_initial(self, request):
        ''' Pre-populate the form with initial values '''
        # We extract initial data from GET request parameters to pre-populate the form
        data = {
            'well': request.GET.get('well_name'),
            'well_pk': request.GET.get('well_pk'),
            'well_name': request.GET.get('well_name'),
            'core_number': request.GET.get('core_number'),
            'core_section_name': request.GET.get('core_section_name'),
            'core_section_number': request.GET.get('core_section_number'),
            'collection_date': timezone.now(),
        }

        self.initial = data
        form = self.form_class(initial=data)

        # Define all the initial values of the form object
        set_well_name(self, data['well_name'])

        # Set success url based on well pk
        return render(request, self.template_name, {'form': form, **data})

    def post(self, request, *args, **kwargs):
        post_data = request.POST.dict()

        # Set well name and well based on submitted data
        set_well_name(self, post_data.get('well'))
        set_well(self, Well)
        set_success_url(self, 'cuttings_list')  # Redirect to the cuttings list after submission

        if 'id' not in post_data:
            post_data['id'] = 1  # Pydantic model requirement

        if request.user.is_authenticated:
            current_user = request.user
        else:
            raise Exception('User is not authenticated')

        checked_cuttings = _validate(payload=post_data, model_name='Cuttings')

        if checked_cuttings is not None:
            if type(checked_cuttings) is ValidationError:
                form = self.get_form()
                for error in checked_cuttings.errors():
                    field = error['loc'][0]
                    message = error['msg']
                    form.add_error(field, message)
                return self.form_invalid(form)

        form = self.get_form()
        if form.is_valid():
            instance = form.save(commit=False)
            instance.registered_by = current_user  # Assuming registered_by is a field in Cuttings
            instance.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
