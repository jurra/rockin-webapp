TASKS:
- List all the acceptance criteria for the project including the postgresql database backend
- Change the project so that it works with postgresql
- Install `django-crispy-forms` to apply bootstrap to the forms templates
- Make unit tests that test the model and relationships

STORY: Introduce Well data
    TASKS:
        - [x] Create the model in models.py
        - [x] Create the form with fields all
        - [x] Import form in view and write the view
        - [x] Import view in urls.py and write the url
        - [x] Create template
        - [x] Redirect page after successful entry
        - [x] Test coverage for model
        - [x] Test coverage for view
        AC: [x] User is not allowed to enter a well that already exists
        AC: User should be able to see a list of the last 10 wells entered

STORY: Introduce core data
    TASKS:
        - [] Create the model in models.py
        - [] Create the form with fields all
        - [] Import form in view and write the view
        - [] Import view in urls.py and write the url
        - [] Create template
        AC: User is not allowed to enter a core that already exists
        AC: Core section number should be a secuence from 0 to N for each well
        AC: If a core_catcher has preceeded a following core then the core_catcher count should be considered also in the core section number. Therefore, if the last core_catcher was 3 then the next core should be 4, 5, 6, etc.

STORY: Automatically post a core sample to ELAB journals to properly create stickers
    AC: If an entry is valid then a post request should be sent to ELAB journals to create a sticker via ELAB journals API
    AC: If the post the request is succesfull then a link to the sticker should be shown in the page
    AC: The sticker could be also presented in the page
    AC: If the post request is not succesfull then an error message should be shown in the page

STORY: Introduce core catcher data

    AC: Should be created from the same create core form
    AC: Should only be allowed to enter if there is a preceeding core that matches the core_section_number. 

STORY: Introduce subsamples data
    cuttings
STORY: Edit core data
STORY: Capture reference to core images


Common fields to all models

All:
registered_by mandatory for all
well_name mandatory for all
remarks mandatory for all
lithology is for all but only mandatory for corechip, cuttings and microcores
drilling_mud is optional for all
collection_date is mandatory for all
registration_time is generated automatically for all


Corechip, core and core catcher
core_number
core_section_number
core_section_name