DEV NOTES

STATUS:
- Currently debugging some test code that is not working, Making sure that all the tests pass before moving on to the next feature
Specially the coreFormView...


URGENT:
- [] Core catcher logic
- [] What fields do we want to let the user edit?
    - [] Do not allow to edit core number

- [] Core section length is calculated between top and button
- [] AC: Why is the form without core bottom passing? Check tests...
- [] AC: Core catcher fields should be prefilled with data from core section
- [] AC: Core catcher should be able to be updated if other core sections are added.....
    Scenarios where the core_catcher needs to be updated,
        If a user aims to add a core that is bigger than the last core_catcher then the core_catcher needs to be updated....

- [] AC: Allow to delete cores with a warning message.... Alerta roja....


- [X We dont move on with this idea] Discuss with Liliana the idea of generating core entities automatically as planned, and then edit them later....
    - For example once we start a well this could be setup by adding some default parameters that can be then applied to all cores for example...
- Definition to solve some issues:
    - When we create a core it should already be related to a well, then the form for creating a core should be a subform of the well form


- TASKS:
    - [] Server setup
        - [] Nginx
        - [] Dockerfile
        - [] Setup docker compose
        - [] CI/CD with githooks
        - [] Set docker volume in data/ folder
        move secrets in data/secrets/
or a secrets directory/

        Troubleshooting:
        Current status: managed to run the app in the server partially but getting error with tables not being recognized.
        - datamodel is empty at the server
        - docker image should make a migration before running the server

        - Fixed the .env was missing the scripts
        - x Volume for less encript in the docker-compose web-service
        - X Fix the missing .dockerignore
        - X Expose the 5000 port from django
        - X Add gsedata.citign.tudelft.nl to allowed hosts....

        - Do a local dockercompose setup that works

        Next steps:
        - Check your project example
        - Django examples for production (default is not for production)
            - Django in production
            - gunicorn
        - .dockerignore


        Recommendations from Arco:
        - Dont build your image in your environment, instead use an image from a registry.
        - Look production recommendations from django
        - Kennismatrix.... gitlab...
        - Created a script as an entry point
        gunicorn:
        - Separate the secrets into different .env files
        .env.db..env.secrets...etc.., .env.prod 
        - Use mysql workbench or postgresql pgadmin locally and ssh via, ssh with a portforward...
        - We could also add access right...


        
        Check if CI/CD works
        Then check if the whole setup of nginx works
        then combine.
            
    - AC: Registered by field should be automatically filled with the user that is logged in
    - Change the project so that it works with postgresql
    - Install `django-crispy-forms` to apply bootstrap to the forms templates
    - List all the acceptance criteria for the project including the postgresql database backend

    Frontend:
    - [ ] Package for prettier forms in django


    Indexing:
    - [ ] Indexes per sections
    - [ ] Index cores
    - [ ] Indexes per depth??


- EPIC: Entering and Editing data
    - AC: [x] User should be able to enter data
    - AC: [ ] User should be able to edit some aspects of the data
    - AC: [ ] The system should guard against duplicate entries
    - AC: [ ] The system should facilitate data consistency for example of depths. What happens if a user can enter a depth that is already taken by another core?
        

- STORY: User management
    TASKS:
        - [x] Setup django authentication
        - [x] Update tests to use authenticated user


- STORY: Admin and users with rights should be able to read data directly from the database
    AC: [x] Registered_by property should be automatically filled with the user that is logged in
    AC: [x] User must be authenticated to login data, All links of the app domain should redirect to login page if user is not authenticated
    AC: Access to the database should be provided so that people can explore data with python
    AC: Access should be provided so that people can explore data with an SQL client like pgadming for example.

- EPIC: Navigation of Rockin webapp
    AC: List of wells should be presented in the home page
    AC: List of cores should be presented in the home page??
    AC: - [x] Well selected to with list of cores should be presented
    AC: Search by date, depth, etc... ???

    - STORY: Well list to select on which well to work


- STORY: Relate data entry to user
    AC: User should be registered by sys admin
    AC: User should be logged in to enter data
        (THiS IS WRONG AC)AC: [] Registered by should be a list of users that are registered in the system


- STORY: Introduce Well data
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

- STORY: Introduce core data
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
        - [x] Javascript on html??? Not desirable if people have it disabled in browsers
        - [x] Make a list of GUI related acceptance criteria

        **Must have:**
        AC: [x] User can not create a core without previously specifying a core number for example C1, C2, etc.
        AC: [x] Collection date is prefilled
        AC: [x] For each new core section the count starts from zero, for example C2-1 should be the first core of the second section
        as well as C3-1 should be the first core of the third section
        AC: [x] User should be able to add cores to a selected well, the well should be selected from a list of wells
            SOLUTION: each element in the list of cores has a button that allows to add a core catcher
                When the user clicks on the button a form is presented to enter with some pre-filled data

        AC: [x] All numeric fields should be higher than 0
        AC: [x] Avoid duplicate of core section name
        AC: [x] Avoid forcing user to select well name every time, create a way to globally select a well name and have a way to select a different well,
            The user should even be presented with a warning if the well name will be changed
        AC: [x] User should be able to select a well from a list of wells
        AC: [x] C1 to C9 dropdown for core number
        AC: [x] C1 t C9 dropdown for planned core number
        AC: [x] Create section name automatically from well name, core number and core section number
        AC: [x] Present preview of core section name based on input data
        AC: User is not allowed to enter a core that already exists
            the system should check if the core number and the well name already exist
        AC: [x] Date entries should be valid and even automatically generated
        
        DEPRECATED ACCEPTANCE CRITERIA FOR CORE FEATURE:
        AC: Core section number should be a sequence from 0 to N for each well
        AC: [] If a core is preceeded by a core_catcher then keep the count of the core catcher for the next core... 
        For example, if the last core_catcher was 3 then the next core should be 4, 5, 6, etc. And the preceding core should be 2.
        AC: Optional [ ] If user enters a value that is not sequential then a warning should be presented, for example if ther is no C1-1,
        and the user enters C1-2 then a warning should be presented.


       **Would very useful to have:**
        AC: Link to url where images of the core live
        AC: The fields used to generate the core_section_name should be all close to each other in the form
        AC: The order of fields in the form should be presented as they are in the access database
        AC: Separate required fields from optional fields
        AC: Help of fields should be descriptive and provide even examples
        AC: A dialog box with a view of how the core data will look like should be presented before the user submits the form

- STORY: Introduce core catcher data based on available cores
    TASKS:
        - [ ] Create the model in models.py
        - [ ] Create the form with fields all
        - [ ] Import form in view and write the view
        - [ ] Simple gui solution for the core catcher should allow to:
            - [ ] Select core that we want to create a core catcher for (This can be a dropdown list of cores the user can filter by writing the core section name)
            - [ ] Prefill data from core section
            - [ ] In core number the number available should be dynamic based on the last number of the core or core_catcher
            - [ ] If a core_catcher preceeds a core_catcher, then the last count comes from the last core_catcher
        AC: [ ] The core catcher is the last core of a section
        AC: [ ] User should be able to select a core from a list of cores
        AC: [ ] Cores and core catchers should be related in terms of sequence
        AC: [ ] Users need to be able to enter data of cores and core catchers in parallel, therefore we cannot define automatically the core catcher number..

    - [ ] Solution para core catcher:
        - AC: Select core that we want to create a core catcher for
        - Prefill data from core section
        - In core number the number available should be dynamic based on the last number of the core or core_catcher
        - If a core_catcher preceeds a core_catcher, then the last count comes from the last core_catcher


    - [ ] Check that the core catcher is correctly modeled
        It is not clear to me if the core catcher is really a type of core or not
        Or if we chose to make it a core type for convenenience since they were very similar???
        If they are two separate entities that are related then the core catcher should be a separate model
        At the same time the relationship of count between core and core catcher should be modeled
        Can a core have more than one core catcher? If no then this is very simple to solve...


        AC: Previous core section name should be presented when core_type is selected
        AC: Should be created from the same create core form
        AC: Should only be allowed to enter if there is a preceeding core that matches the core_section_number. 

- STORY: Edit core data so that user can add optional fields later or correct certain data
    AC: Core name well, and all the things that identify a core should not be editable
    AC: User should be able to edit core data
    AC: User should be able to correct certain data???

    Could have:
    AC: Warn users if certain depth range is already taken by another core


- STORY: Automatically post a core sample to ELAB journals to properly create stickers
    AC: If an entry is valid then a post request should be sent to ELAB journals to create a sticker via ELAB journals API
    AC: If the post the request is succesfull then a link to the sticker should be shown in the page
    AC: The sticker could be also presented in the page
    AC: If the post request is not succesfull then an error message should be shown in the page

- STORY: CoreChip
    - TASKS:
        - [x] Model
        - [ ] Form
        - [ ] template
        - [ ] Validation
        - [ ] View
            - [ ] Validation
         
    - Ideas for the feature:
        a. Solution: User selects a core and the form is generated based on the core name
        b. User decides that wants to add a corechip
        then he she can use certain parameters to filter the cores available to add the corechip
        c. User is presented with a form completely empty just with the name of the well and they decide what to do. The name is generated automatically.
        b. User can do c, but also generate a core chip from a core, and all the fields will automatically be filled with the data from the core

    - AC: The name of the core chip that is automatically generated based on well_name, core_number, core_section_number, core_chip_number and from_top_bottom should be presented in the form, for example:
        DELGT01-C1-2-CHB7



- STORY: Introduce subsamples data
    TASKS:
        - [x] Create the model in models.py
        - [x] Create the form with fields all

        
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