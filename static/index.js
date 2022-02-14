/**
 * Ajax call to run function to activate sprayer on button press.
 */
document.querySelector('.spray_air_freshener').addEventListener('click', (e) => {
  e.preventDefault();
  let status = `Manual activation`;

  $.post(`/spray_air_freshener/${status}`,
      function(data) {
        console.log('Spray button clicked...')
  });
  return false;
});


/**
 * Ajax call to run main event loop on button press.
 */
// document.querySelector('.start_main_loop').addEventListener('click', (e) => {
//     e.preventDefault()
//     $.getJSON('/start_main_loop',
//       function(data) {
//         console.log('Start button clicked...')
//   });
//   return false;
// });


/**
 * Ajax call to run main event loop on button press.
 */
// document.querySelector('.stop_main_loop').addEventListener('click', (e) => {
//   e.preventDefault()
//   $.getJSON('/stop_main_loop',
//       function(data) {
//         console.log('Stop button clicked...')
//   });
//   return false;
// });
