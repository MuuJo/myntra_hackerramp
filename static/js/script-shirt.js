document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('.custom-checkbox');
    const centerImage = document.getElementById('center-image');
    const originalSrc = centerImage.src; // Save the original image source

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            if (checkbox.checked) {
                centerImage.src = checkbox.getAttribute('data-image');
            } else {
                centerImage.src = originalSrc; // Reset to the original image source
            }
        });
    });
});