function updateImage() {
    const formData = new FormData();
    const fileInput = document.getElementById('image');

    // adjust_image
    const contrastInput = document.getElementById('contrast');
    const brightnessInput = document.getElementById('brightness');

    // edge_detection
    // const min_threshInput = document.getElementById('canny_min_thresh');
    // const max_threshInput = document.getElementById('canny_max_thresh');


    formData.append('image', fileInput.files[0]);
    formData.append('contrast', contrastInput.value);
    formData.append('brightness', brightnessInput.value);
    // formData.append('canny_min_thresh', min_threshInput.value);
    // formData.append('canny_max_thresh', max_threshInput.value);

    fetch('/adjust', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            const image = document.getElementById('adjustedImage');
            image.src = 'data:image/png;base64,' + data.image;
            // adjust_image
            document.getElementById('contrastValue').textContent = contrastInput.value;
            document.getElementById('brightnessValue').textContent = brightnessInput.value;

            // edge_detection
            // document.getElementById('canny_min_threshValue').textContent = min_threshInput.value;
            // document.getElementById('canny_max_threshValue').textContent = max_threshInput.value;
        })
        .catch(error => console.error('Error:', error));
}

function toggleAdjustmentControls() {
    const controls = document.getElementById('adjustmentControls');
    controls.style.display = (controls.style.display === 'none' || controls.style.display === '') ? 'block' : 'none';
}

function cannyAdjustmentControls() {
    const controls = document.getElementById('cannyControls');
    controls.style.display = (controls.style.display === 'none' || controls.style.display === '') ? 'block' : 'none';
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const toggleBtn = document.querySelector('.toggle-btn');

    sidebar.classList.toggle('expanded');
    toggleBtn.classList.toggle('expanded');
}

function resetImage() {
    document.getElementById('image').value = "";
}