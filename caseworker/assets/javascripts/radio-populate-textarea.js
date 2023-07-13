export default function populateTextOnRadioInput(
  radio_selector,
  text_selector,
  lookup
) {
  const radio_buttons = document.querySelectorAll(radio_selector);
  const text_area = document.querySelector(text_selector);
  radio_buttons.forEach((input) => {
    input.addEventListener("change", (event) => {
      const text = lookup[event.target.value];
      text_area.value = text;
    });
  });
}

export { populateTextOnRadioInput };

// class PopulateTextOnRadioInput{
//     constructor($radio_selector, $text_selector, $lookup) {
//         this.$radio_buttons = document.querySelectorAll($radio_selector);
//         this.$text_area = document.querySelector($text_selector);
//         this.$lookup = $lookup
//       }

//       init() {
//         this.$radio_buttons.forEach((input) => {
//             input.addEventListener('change', (event)=>{
//                 const text = this.$lookup[event.target.value]
//                 this.$text_area.value = text
//             });
//         });
//       }
// }

// export {PopulateTextOnRadioInput}
