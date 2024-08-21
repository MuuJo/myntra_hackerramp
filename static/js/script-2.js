document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('.custom-checkbox');
    const centerImage = document.getElementById('center-image');
    const originalSrc = centerImage.src; // Save the original image source
    const combinedImage = "white-pant.PNG"; // The image to show when both checkboxes are checked

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const allChecked = [...checkboxes].every(cb => cb.checked);
            const anyChecked = [...checkboxes].some(cb => cb.checked);

            if (allChecked) {
                centerImage.src = combinedImage;
            } else if (anyChecked) {
                const checkedCheckbox = [...checkboxes].find(cb => cb.checked);
                centerImage.src = checkedCheckbox.getAttribute('data-image');
            } else {
                centerImage.src = originalSrc; // Reset to the original image source
            }
        });
    });
});