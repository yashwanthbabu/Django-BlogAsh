function checkForm(){
	var name = document.getElementById("username1")
	var password = document.getElementById("password1")
	if(name == '' || password == ''){
		print('Fields should not be empty');
	}
	else{
		var username1 = document.getElementById("username")
		var password1 = document.getElementById("password")
		if (username1.innerHTML == 'Must be 3+ letters' || password1.innerHTML == 'Password too short'){
			print('Not a valid info');
		}
		else{
			document.getElementById("login-form").submit();
		}

	}
}

function validate(field, query){
	var xmlhttp;
	if(window.XMLHttpRequest){
		xmlhttp = new XMLHttpRequest();
	}
	else{
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState != 4 && xmlhttp.status == 200) {
		document.getElementById(field).innerHTML = "Validating..";
	}
	else if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
		document.getElementById(field).innerHTML = xmlhttp.responseText;
	}
	else{
		document.getElementById(field).innerHTML = "Error Occurred.Reload Or Try Again</a> the page.";
	}
	}
	xmlhttp.send();

	}