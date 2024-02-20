function validateForm() {
    var checkboxes = document.querySelectorAll('input[name="group"]');
    var checked = false;
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            checked = true;
        }
    });
    if (!checked) {
        alert("Debe seleccionar al menos un grupo.");
        return false;
    }
    return true;
}
