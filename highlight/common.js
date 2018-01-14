function loadOptions() {
	if ("undefined" != typeof localStorage) {
		document.getElementById("textareaKeywords").value = localStorage.getItem("keywords");
		document.getElementById("colorForeground").value = localStorage.getItem("foreground") || "#000000";
		document.getElementById("colorBackground").value = localStorage.getItem("background") || "#ffff00";

		var showOccurrences = localStorage.getItem("showOccurrences");
		showOccurrences = "true" == showOccurrences || null == showOccurrences;
		document.getElementById("checkboxShowOccurrences").checked = showOccurrences;
	}
}

function saveOptions() {
	if ("undefined" != typeof localStorage) {

		var request = new XMLHttpRequest();

		var xhr = new XMLHttpRequest();

		xhr.open("GET", "http://localhost:8080", false);
		xhr.send();

		var result = xhr.responseText;
		localStorage.setItem("keywords", result);

		localStorage.setItem("foreground", "#000000");
		localStorage.setItem("background", "#ffff00");
		localStorage.setItem("showOccurrences", "true");
	}
}
