// The following function translates the page from Hindi to English or vice versa

// Set original as Hindi
$( "#language_button").html("हिन्दी");

function changeLanguage() {
	var translate_array;
	var lang = $( "#language_button").html();
	console.log(lang);
	if ( lang =="हिन्दी"){
		translate_array = hindi_array;
		console.log(translate_array);
		$( "#language_button").html("English");
	} else{
		translate_array=english_array;
		$( "#language_button").html("हिन्दी");
	}

	length = translate_array.length;
	for (var i=0;i<length;i++){
		$( translate_array[i].elementID).html(translate_array[i].html);
	}
}