document.addEventListener('DOMContentLoaded', () => {
    const checkboxes = document.querySelectorAll('.custom-checkbox');
    const centerImage = document.getElementById('center-image');
    const originalSrc = centerImage.src; // Save the original image source
    const shirtImage = "{{ url_for('static', filename='images/white_shirt_only.png') }}"; // The image for the shirt white-shirt
    const pantImage = "{{ url_for('static', filename='images/pant_only.png') }}"; // The image for the pants
    const combinedImage = "{{ url_for('static', filename='images/shirt-pant
.png') }}"; // The image to show when both checkboxes are checked

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', () => {
            const shirtChecked = document.querySelector('#shirtCheckbox').checked;
            const pantChecked = document.querySelector('#pantCheckbox').checked;

            if (shirtChecked && pantChecked) {
                centerImage.src = combinedImage;
            } else if (shirtChecked) {
                centerImage.src = shirtImage;
            } else if (pantChecked) {
                centerImage.src = pantImage;
            } else {
                centerImage.src = originalSrc; // Reset to the original image source
            }
        });
    });

    // Function to handle adding items to "Your Picks"
    document.querySelectorAll('.settings-icon').forEach(item => {
        item.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            addToYourPicks(productId);
        });
    });

    function addToYourPicks(productId) {
        const yourPicksContainer = document.getElementById('yourPicksContainer');
        const newProductElement = document.createElement('div');
        newProductElement.textContent = `Product ID: ${productId}`;
        yourPicksContainer.appendChild(newProductElement);
    }
});
