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
    # post_data = request.POST.dict()

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


class WellCoreListView(ListView):
    model = Well
    template_name = 'well_core_list.html'
    context_object_name = 'well_core_list'
    # Add a reverse lazy url to create a core
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
    template_name = 'core.html'
    form_class = CoreForm
    success_url = reverse_lazy('well_core_list')

    def get_initial(self):
        initial = super().get_initial()

        # Propose the user collection date as the current date and time
        initial['collection_date'] = timezone.now()

        # Retrieve the well name from your data source or database
        well_name = self.request.GET.get('well_name')
        initial['well'] = well_name

        core_number = self.request.GET.get('core_number')
        initial['core_number'] = core_number
        if core_number:
            latest_core_section_number = Core.objects.filter(core_number=core_number).aggregate(
                Max('core_section_number'))['core_section_number__max']
            if latest_core_section_number is not None:
                initial['core_section_number'] = latest_core_section_number + 1
            else:
                initial['core_section_number'] = 1
        return initial

    # Create section name based on the well name, the core number and the core section number
    def post(self, request, *args, **kwargs):
        post_data = request.POST.dict()

        if 'id' not in post_data:
            post_data['id'] = 1

        # Add the core section name to the post data so that it can be validated
        core_section_name = f"{post_data.get('well')}-{post_data.get('core_number')}-{post_data.get('core_section_number')}"
        post_data['core_section_name'] = core_section_name

        if Core.objects.filter(core_section_name=core_section_name).exists():
            form = self.get_form()
            form.add_error(
                'core_section_name', f'A core with name {core_section_name} already exists. Please try again with a number bigger than {post_data.get("core_section_number") }.')
            return self.form_invalid(form)
        print(post_data)
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
            form.save()
            return super().form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)
