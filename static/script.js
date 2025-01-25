let originalImageSrc = null; // Variable to store the original image

function updateImage() {
    const formData = new FormData();
    const fileInput = document.getElementById('image');
    const contrastInput = document.getElementById('contrast');
    const brightnessInput = document.getElementById('brightness');
    const opacityInput = document.getElementById('opacity');
    const blurKsizeInput = document.getElementById('blur_ksize');
    const flip_h = document.getElementById('horizontal');
    const flip_v = document.getElementById('vertical');
    const image = document.getElementById('adjustedImage');

    // Check if the file is selected before appending
    if (fileInput.files.length === 0) {
        alert("Please upload an image first.");
        return;
    }

    // Save the original image whenever a new image is uploaded
    const reader = new FileReader();
    reader.onload = function (e) {
        originalImageSrc = e.target.result; // Update the original image source with the latest uploaded image
    };
    reader.readAsDataURL(fileInput.files[0]);

    // Append form data
    formData.append('image', fileInput.files[0]);
    formData.append('contrast', contrastInput.value);
    formData.append('brightness', brightnessInput.value);
    formData.append('opacity', opacityInput.value);
    formData.append('blur_ksize', blurKsizeInput.value);
    formData.append('flip_h', flip_h.classList.contains('active') ? 1 : 0);
    formData.append('flip_v', flip_v.classList.contains('active') ? 1 : 0);

    // Log the values being sent for debugging
    console.log("Sending values - Contrast:", contrastInput.value, "Brightness:", brightnessInput.value, "Opacity:", opacityInput.value, "Blur KSize:", blurKsizeInput.value);

    // Send the image and adjustments to the backend
    fetch('/adjust', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        image.src = 'data:image/png;base64,' + data.image; // Update the adjusted image
        document.getElementById('contrastValue').textContent = contrastInput.value;
        document.getElementById('brightnessValue').textContent = brightnessInput.value;
        document.getElementById('opacityValue').textContent = opacityInput.value;
        document.getElementById('blur_ksizeValue').textContent = blurKsizeInput.value;
    })
    .catch(error => console.error('Error:', error));
}

function toggleAdjustmentControls() {
    const controls = document.getElementById('adjustmentControls');
    controls.style.display = (controls.style.display === 'none' || controls.style.display === '') ? 'block' : 'none';
}

function opacityBlurAdjustmentControls() {
    const controls = document.getElementById('opacityBlurControls');
    controls.style.display = (controls.style.display === 'none' || controls.style.display === '') ? 'block' : 'none';
}

function mirrorAdjustmentControls() {
    const controls = document.getElementById('mirrorControls');
    controls.style.display = (controls.style.display === 'none' || controls.style.display === '') ? 'block' : 'none';
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.querySelector('.toggle-btn');

    sidebar.classList.toggle('expanded');
    toggleBtn.classList.toggle('expanded');
}

function resetImage() {
    if (originalImageSrc) {
        const image = document.getElementById('adjustedImage');
        image.src = originalImageSrc; // Restore the last uploaded image
        document.getElementById('contrast').value = 1.0; // Reset adjustment controls
        document.getElementById('brightness').value = 0;
        document.getElementById('opacity').value = 1.0;
        document.getElementById('blur_ksize').value = 0;

        document.getElementById('contrastValue').textContent = 1.0;
        document.getElementById('brightnessValue').textContent = 0;
        document.getElementById('opacityValue').textContent = 1.0;
        document.getElementById('blur_ksizeValue').textContent = 0;

        // Reset flip buttons
        document.getElementById('horizontal').classList.remove('active');
        document.getElementById('vertical').classList.remove('active');
    } else {
        alert("No image to reset.");
    }
}

// Add event listeners for flip buttons
document.getElementById('horizontal').addEventListener('click', function() {
    this.classList.toggle('active');
    updateImage();
});

document.getElementById('vertical').addEventListener('click', function() {
    this.classList.toggle('active');
    updateImage();
});

// Add event listener for image upload
document.getElementById('image').addEventListener('change', updateImage);