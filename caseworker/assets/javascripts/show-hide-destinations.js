// Hide show destinatios list.
const hideItems = (array) => {
		for (const [index, country] of array.entries()) {
			if (index > 2) {
				country.classList.add("app-hidden--force")
		}
	}
}

destinationsList = () => {
	const destinationsList = document.getElementsByClassName("destinations__list")
	let showHideState = {}

	for (const [i, value] of [...destinationsList].entries()) {
		showHideState[i] = true
	}

	for (const [index, destinations] of [...destinationsList].entries()) {
		const destinationsHtmlCollection = destinations.getElementsByTagName("li")

		if (destinationsHtmlCollection.length > 3) {
			array = [...destinationsHtmlCollection]

			hideItems(array)
			const td = destinations.parentElement
			const button = td.appendChild(document.createElement("a"))
			button.innerText = `View all(${destinationsHtmlCollection.length})`
			button.href = ""
			button.className = "destinations__show-all"
			button.addEventListener("click", (e) => {
				e.preventDefault()
				
				const specificShowHideButton = e.currentTarget
				const countryList = [...specificShowHideButton.parentElement.getElementsByTagName("li")]

				if (showHideState[index] === true) {
					for (country of countryList) {
						country.classList.remove("app-hidden--force")
						specificShowHideButton.innerText = "View less"
						showHideState[index] = false
					}
				} else {
					hideItems(countryList)
					specificShowHideButton.innerText = `View all(${countryList.length})`
					showHideState[index] = true
				}
			})
		}
	}
}

export default destinationsList
