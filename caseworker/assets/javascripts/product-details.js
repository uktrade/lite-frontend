(function() {
    var form = document.getElementById('tab-form');
    var tabs = document.getElementsByClassName('product-on-cases-tab');
    function handleSwitchTab(showThisOnly) {
        for (var i = 0; i < tabs.length; i++) {
           var tab = tabs.item(i);
           tab.style.display = tab.id === showThisOnly ? 'block' : 'none';
        }
    }
    form.addEventListener('change', function(event) { handleSwitchTab(event.target.value) });
    handleSwitchTab('full-details-tab')
})()
