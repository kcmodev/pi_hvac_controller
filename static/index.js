/**
 * Ajax call to run function to activate sprayer on button press.
 */

document.querySelector('.spray_air_freshener').addEventListener('click', (e) => {
  e.preventDefault()
  $.getJSON('/spray_air_freshener',
      function(data) {
        console.log('Spray button clicked...')
  });
  return false;
});