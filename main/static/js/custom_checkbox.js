document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.custom-checkbox').forEach(function(label) {
        const checkbox = document.getElementById(label.getAttribute('for'));

        function updateCheckboxState() {
            if (checkbox.checked) {
                label.classList.add('checked');
            } else {
                label.classList.remove('checked');
            }
        }

        // Initialize the checkbox state
        updateCheckboxState();

        // Add event listener to the checkbox
        checkbox.addEventListener('change', updateCheckboxState);
    });
});