DEV NOTES

TASKS:
- List all the acceptance criteria for the project including the postgresql database backend
- Change the project so that it works with postgresql
- Install `django-crispy-forms` to apply bootstrap to the forms templates
- Make unit tests that test the model and relationships
- [ ] Setup properly gitpython which is not working at the moment. For now we do the submodules manually

STORY: Navigation of Rockin webapp
    AC: List of wells should be presented in the home page
    AC: List of cores should be presented in the home page
    AC: Global well selected to introduce cores should be presented
    AC: Search by date, depth, etc... ???


STORY: Relate data entry to user
    AC: User should be registered by sys admin
    AC: User should be logged in to enter data
        (THiS IS WRONG AC)AC: [] Registered by should be a list of users that are registered in the system


STORY: Introduce Well data
    TASKS:
        - [x] Create the model in models.py
        - [x] Create the form with fields all
        - [x] Import form in view and write the view
        - [x] Import view in urls.py and write the url
        - [x] Create template
        - [x] Redirect page after successful entry
        - [x] Validate the form in the view
        - [x] Test coverage for model
        - [x] Test coverage for view
            - [ ] Test invalid form, name that is integer instead of string
        AC: [x] User is not allowed to enter a well that already exists
        AC: User should be able to see a list of the last 10 wells entered
        AC: Wells should be added by admin, admin should decide which well will be used as a reference for the core data

STORY: Introduce core data
    TASKS:
        - [x] Create the model in models.py
        - [x] Create the form with fields all
        - [x] Import form in view and write the view
        - [x] Import view in urls.py and write the url
        - [x] Create template
        - [x] Test model and its relationships
        - [x] Question: Are cuttings and microchips also counted as core_catchers are counted, which are essentially cores?

        Sub tasks:
        - [x] Fix what is failing in tests
        - [x] Pydantic validation??
        - [] Javascript on html??? Not desirable if people have it disabled in browsers
        - [ ] Package for prettier forms in django
        - [ ] Make a list of GUI related acceptance criteria

        **Must have:**
        AC: [] If a core is preceeded by a core_catcher then keep the count of the core catcher for the next core... 
            For example, if the last core_catcher was 3 then the next core should be 4, 5, 6, etc. And the preceding core should be 2.
        AC: [x] All numeric fields should be higher than 0
        AC: [x] Avoid duplicate of core section name
        AC: [] Avoid forcing user to select well name every time, create a way to globally select a well name and have a way to select a different well,
            The user should even be presented with a warning if the well name will be changed
        AC: [x] User should be able to select a well from a list of wells
        AC: [x] C1 to C9 dropdown for core number
        AC: [x] C1 t C9 dropdown for planned core number
        AC: [x] Create section name automatically from well name, core number and core section number
        AC: [x] Present preview of core section name based on input data
        AC: User is not allowed to enter a core that already exists
            the system should check if the core number and the well name already exist
        AC: Date entries should be valid and even automatically generated
        AC: If a core_catcher has preceeded a following core then the core_catcher count should be considered also in the core section number. Therefore, if the last core_catcher was 3 then the next core should be 4, 5, 6, etc.
        AC: Core section number should be a sequence from 0 to N for each well


       **Would very useful to have:**
        AC: Link to url where images of the core live
        AC: The fields used to generate the core_section_name should be all close to each other in the form
        AC: The order of fields in the form should be presented as they are in the access database
        AC: Separate required fields from optional fields
        AC: Help of fields should be descriptive and provide even examples
        AC: A dialog box with a view of how the core data will look like should be presented before the user submits the form

STORY: Introduce core catcher data
    AC: Previous core section name should be presented when core_type is selected
    AC: Should be created from the same create core form
    AC: Should only be allowed to enter if there is a preceeding core that matches the core_section_number. 

STORY: Edit core data so that user can add optional fields later or correct certain data
    AC: User should be able to edit core data
    AC: User should be able to correct certain data???


STORY: Automatically post a core sample to ELAB journals to properly create stickers
    AC: If an entry is valid then a post request should be sent to ELAB journals to create a sticker via ELAB journals API
    AC: If the post the request is succesfull then a link to the sticker should be shown in the page
    AC: The sticker could be also presented in the page
    AC: If the post request is not succesfull then an error message should be shown in the page



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