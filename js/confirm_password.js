const loadIndicator = function() {

    let generated_password_el = document.getElementById("generated-password"),
        entered_password_el = document.getElementById("confirm-password"),
        indicator_el = document.getElementById("confirm-password-indicator");


    entered_password_el.onkeydown = (event) => {

        const generated = generated_password_el.innerText,
            entered = entered_password_el.value;

        if (entered === "") {
            indicator_el.innerHTML = "<div>Practice typing the password!</div>";
        } else if (entered === generated) {
            indicator_el.innerHTML = "<div style=\"color: green\">Correct!</div>";
        } else {
            indicator_el.innerHTML = "<div style=\"color: red\">Wrong!</div>";
        }

    };

}
