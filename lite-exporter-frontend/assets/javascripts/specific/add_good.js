plural = []

$("#unit > option").each(function() {
	if ($(this).text().endsWith('(s)')) {
		plural.push($(this).val());
	}
});

for (var i = 0; i < plural.length; i++) {
	key = plural[i]
	option = $('#unit > option[value=' + key + ']')
    option.text(option.text().substring(0, option.text().length - 3) + 's')
}

$('#quantity').on('input propertychange paste', function() {
	for (var i = 0; i < plural.length; i++) {
		key = plural[i]
		option = $('#unit > option[value=' + key + ']')
		if ($(this).val() == '1') {
			if (option.text().endsWith('s')) {
				option.text(option.text().substring(0, option.text().length - 1))
			}
		} else {
			if (!option.text().endsWith('s')) {
				option.text(option.text() + 's')
			}
		}
	}
});
