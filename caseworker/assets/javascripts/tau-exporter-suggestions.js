const initTauControlListEntry = () => {
  const cleList = document.querySelectorAll('.control-list__list');
  const checkboxProducts = document.querySelectorAll("[id^='id_goods_']");
  const inputSuggestion = document
    .querySelector('#control_list_entries')
    .querySelector('.tokenfield-set')
    .querySelector('ul');

  cleList.forEach((cle) =>
    cle.addEventListener('click', () => console.log('HAHA'))
  );

  checkboxProducts.forEach((product) => {
    product.addEventListener('click', () => {
      checked = product.checked;
      id = product.value;

      cleList.forEach((cle) => {
        if (checked) {
          id === cle.getAttribute('name') &&
            cle.classList.remove('app-hidden--force');
          return;
        }
        cle.classList.add('app-hidden--force');
      });
    });
  });
};

export default initTauControlListEntry;
