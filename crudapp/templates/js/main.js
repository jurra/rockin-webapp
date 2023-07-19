/*
  * This file contains the main javascript code for the crudapp.
*/

/*
  * This function is used to generate names in forms for different data entry forms such as
  * core, core_chip, cuttings, etc.
  * @param {array of strings} components - the components of the name to be joined
  * @return {string} - the joined name 
*/
function joinNameComponents(components) {
    return components.join('-');
}