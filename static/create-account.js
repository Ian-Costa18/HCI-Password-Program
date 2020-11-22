window.onload = function () {
  let psw = document.getElementById("password");
  var lower = document.getElementById("lower");
  var upper = document.getElementById("upper");
  var number = document.getElementById("number");
  var symbol = document.getElementById("symbol");
  var passphrase = document.getElementById("passphrase");
  var length = document.getElementById("length");
  let cpsw = document.getElementById("confirm-password");
  let matching = document.getElementById("matching");

  let valid = false;
  let passwordMatching = false;

  psw.onfocus = function () {
    document.getElementById("Password Checker").style.display = "block";
  };

  psw.onblur = function () {
    document.getElementById("Password Checker").style.display = "none";
  };

  cpsw.onfocus = function () {
    document.getElementById("Password Checker").style.display = "block";
  };

  cpsw.onblur = function () {
    document.getElementById("Password Checker").style.display = "none";
  };

  psw.onkeyup = function () {
    console.log(psw.value);
    let password = psw.value;

    // Find characters

    let password_len = psw.value.length;

    // Lowercase
    let lowercase = /[a-z]/g;
    let lowercase_num = ((password || "").match(lowercase) || []).length;

    // Uppercase
    let uppercase = /[A-Z]/g;
    let uppercase_num = ((password || "").match(uppercase) || []).length;

    // Numbers
    let numbers = /[0-9]/g;
    let number_num = ((password || "").match(numbers) || []).length;

    // Symbols
    let symbols = /[~`!@#$%^&*\(\)_\-+=\{\[\}\]|\\:;"'<,>\.?\/]/g;
    let symbol_num = ((password || "").match(symbols) || []).length;

    console.log({
      lower: lowercase_num,
      upper: uppercase_num,
      number: number_num,
      symbol: symbol_num,
      len: password_len,
    });

    // Tests
    let criteria = 0;

    if (lowercase_num >= 2) {
      criteria++;
      lower.classList.remove("invalid");
      lower.classList.add("valid");
    } else {
      lower.classList.remove("valid");
      lower.classList.add("invalid");
    }
    if (uppercase_num >= 2) {
      criteria++;
      upper.classList.remove("invalid");
      upper.classList.add("valid");
    } else {
      upper.classList.remove("valid");
      upper.classList.add("invalid");
    }
    if (number_num >= 2) {
      criteria++;
      number.classList.remove("invalid");
      number.classList.add("valid");
    } else {
      number.classList.remove("valid");
      number.classList.add("invalid");
    }
    if (symbol_num >= 2) {
      criteria++;
      symbol.classList.remove("invalid");
      symbol.classList.add("valid");
    } else {
      symbol.classList.remove("valid");
      symbol.classList.add("invalid");
    }
    if (password_len >= 20) {
      criteria++;
      passphrase.classList.remove("invalid");
      passphrase.classList.add("valid");
    } else {
      passphrase.classList.remove("valid");
      passphrase.classList.add("invalid");
    }

    if (password_len >= 14) {
      length.classList.remove("invalid");
      length.classList.add("valid");
    } else {
      length.classList.remove("valid");
      length.classList.add("invalid");
    }

    if (criteria >= 4 && password_len >= 14) {
      valid = true;
    } else {
      valid = false;
    }
    console.log({
      valid: valid,
      matching: passwordMatching,
    });
    if (passwordMatching) {
      matching.classList.remove("invalid");
      matching.classList.add("valid");
    } else {
      matching.classList.remove("valid");
      matching.classList.add("invalid");
    }
    if (valid && passwordMatching) {
      document.getElementById("submit").disabled = false;
    } else {
      document.getElementById("submit").disabled = true;
    }
  };

  cpsw.onkeyup = () => {
    if (cpsw.value == psw.value) {
      passwordMatching = true;
    } else {
      passwordMatching = false;
    }
    if (passwordMatching) {
      matching.classList.remove("invalid");
      matching.classList.add("valid");
    } else {
      matching.classList.remove("valid");
      matching.classList.add("invalid");
    }
    if (passwordMatching && valid) {
      document.getElementById("submit").disabled = false;
    } else {
      document.getElementById("submit").disabled = true;
    }
    console.log({
      valid: valid,
      matching: passwordMatching,
    });
  };
};
