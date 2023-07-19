/*
  * This file contains the main javascript code for the crudapp.
*/

/**
  * This function is used to generate names in forms for different data entry forms such as
  * core, core_chip, cuttings, etc.
  * @param {array of strings} components - the components of the name to be joined
  * @return {string} - the joined name 
  * 
  */
function joinNameComponents(components) {
  return components.join('-');
}

/**
  * This function creates a factory for DOM elements based on a list of field names.
  * @param {array of strings} fieldNames - the names of the fields to be used in the factory 
  * return {object of DOM elements} - the DOM elements created by the factory
  * Usage example:
  * const coreElements = createDOMElementsFactory(['core_id', 'well_id', 'core_section_number']);
  * 
  */
function createDOMElementsFactory(fieldNames) {
  const elements = {};

  fieldNames.forEach((fieldName) => {
    elements[fieldName] = document.getElementById(fieldName);
  });

  return elements;
}

/**
 * 
 * @param {string} fieldName - the name of the field to be used in the factory
 * @param {object of DOM element} domElement - the Dome element to be updated
 */
function setValue(domElement, initialValue) {
  domElement.value = initialValue;
}

/**
 * @param {array of strings} fields - the names of the fields to be used in the factory
 * @param {object of DOM elements} domElements - the DOM elements to be updated
 * @param {object of initial values} initialValues - the initial values to be used in the form
 */
function setFormValues(fields, domElements, initialValues) {
  fields.forEach((fieldName) => {
    setValue(domElements[fieldName], initialValues[fieldName]);
  })
};