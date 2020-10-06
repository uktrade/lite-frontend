import tippy from 'tippy.js';


export default function initQueuesMenu() {
	// deliberately written in vanilla JS not jquery
	const queuesMenu = document.getElementById('queues');
	if (!queuesMenu) {
		return
	}
	queuesMenu.style.display = 'block';

	tippy("#link-queue", {
		content: queuesMenu,
		allowHTML: true,
		interactive: true,
		animation: 'scale-subtle',
		trigger: 'click',
		theme: 'light',
		placement: 'bottom-start',
		arrow: null,
		onShown(instance) {
			$("#filter-queues").val("")
			$("#filter-queues").focus()
		},
	});

	$("#link-queue").removeAttr("href");

	$("#filter-queues").on('input', function() {
		let txt = $("#filter-queues").val();
		let anyVisible = false;

		$('#queues a').hide(); // queue name
		$("#queues > span").hide();

		$('#queues a').each(function(){
			if ($(this).text().toUpperCase().indexOf(txt.toUpperCase()) != -1) {
				$(this).show();
				anyVisible = true;
			}
		});

		if (!anyVisible) {
			$("#queues > span").show()
		}
	});

}
