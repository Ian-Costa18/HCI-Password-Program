
window.onload = function() {

		let psw = document.getElementById("password");

		psw.onkeyup = function () {

			console.log(psw.value);
			let password = psw.value;

			// Lowercase
			let lowercase = /[a-z]/g;
			let lowercase_num = ((password || '').match(lowercase) || []).length;

			// Uppercase
			let uppercase = /[A-Z]/g;
			let uppercase_num = ((password || '').match(uppercase) || []).length;

			// Numbers
			let number = /[0-9]/g;
			let number_num = ((password || '').match(number) || []).length;


			console.log(lowercase_num);
			console.log(uppercase_num);

		}
	}