function togglePassword(fieldId) {
    const input = document.getElementById(fieldId);
    const button = input.nextElementSibling;
    if (input.type === "password") {
        input.type = "text";
        button.textContent = "👁️‍🗨️"; // change to "eye-slash"
    } else {
        input.type = "password";
        button.textContent = "👁️"; // back to normal eye
    }
}