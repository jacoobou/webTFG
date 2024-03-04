function validateForm() {
    var checkboxes = document.querySelectorAll('input[name="group"]');
    var checked = false;
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            checked = true;
        }
    });
    if (!checked) {
        swal("Debe seleccionar al menos un grupo.", {
            icon: "warning",
            buttons: false,
            timer: 2000,
        });
        return false;
    }
    return true;
}
