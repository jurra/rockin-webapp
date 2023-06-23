## To Do
- [ ] Check relationships and make sure it works
    - [ ] Well <-- Cores, Cuttings, MicroCores, CoreCatchers
        - [X] Well Cores relationship works
    - [ ] Cores <-- CoreChips

- [x] Added the planned core section number

- [ ] Automatic generation of form for Wells and Cores
    - [ ] Well
    - [ ] Core (AC): The Core should allow to select a well and the controller should handle the identification of such entity 
        - [ ] Make test to check the working principle of Core form where core_section_number is automatically generated

## How to generate a form automatically with django
- [x] Create the model in models.py
- [ ] Create the form with fields all
- [ ] Import form in view and write the view
- [ ] Import view in urls.py and write the url

## Things to discuss with Liliana if core_section_number should be an automatic counter
    - What if a user incorrectly enters a core_section_number?
    - Perhaps the user can be provided with a defualt value based on the last core_section_number of the well
        - User should always be able to see the preceeding core well, or a list of them to make sure the core_section_number is correct...

    - If there is a planned section couldnt we simply create all the planned cores already with most of the values prefilled by default? Perhaps the planned things should be hinted or provided, but not created by default automatically, otherwise there could be also a dialog to confirm the entry of a core.

    - Perhaps there can be a feature where a user can create a plan for a well that can automatically generate the planned cores, and the user needs to change or check that this data is correct, and modify it accordingly.

    - The the logging app will also be a plan app.