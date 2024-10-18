// Fetch the config.json file and build the gallery
fetch('config.json')
    .then(response => response.json())
    .then(data => {
        const photoGallery = document.getElementById('photoGallery');
        const images = data.images;

        images.forEach((image, index) => {
            const imgElement = document.createElement('img');
            imgElement.src = image.src;
            imgElement.className = 'photo';
            imgElement.alt = image.alt || `Photo ${index + 1}`; // Add alt attribute
            imgElement.onclick = () => expandImage(index);
            photoGallery.appendChild(imgElement);
        });

        // Save images array globally for access in other functions
        window.images = images;
    })
    .catch(error => {
        console.error('Error loading config.json:', error);
    });

let currentIndex = 0;

function expandImage(index) {
    currentIndex = index;
    const modal = document.getElementById('lightboxModal');
    const expandedImg = document.getElementById('expandedImg');
    const exifInfo = document.getElementById('exifInfo');

    expandedImg.src = window.images[currentIndex].src;
    expandedImg.alt = window.images[currentIndex].alt || `Expanded view of Photo ${currentIndex + 1}`; // Add alt attribute

    // Populate EXIF info
    let exifContent = '';
    if (window.images[currentIndex].camera) {
        exifContent += `<div><img src="assets/icons/camera.svg" alt="Camera Icon"/> ${window.images[currentIndex].camera}</div>`;
    }
    if (window.images[currentIndex].aperture) {
        exifContent += `<div><img src="assets/icons/aperture.svg" alt="Aperture Icon"/> ${window.images[currentIndex].aperture}</div>`;
    }
    if (window.images[currentIndex].shutter_speed) {
        exifContent += `<div><img src="assets/icons/shutter.svg" alt="Shutter Speed Icon"/> ${window.images[currentIndex].shutter_speed}</div>`;
    }
    exifInfo.innerHTML = exifContent;

    modal.style.display = 'flex';
}

// Change image based on the step (+1 for next, -1 for previous)
function changeImage(step) {
    currentIndex = (currentIndex + step + window.images.length) % window.images.length;
    expandImage(currentIndex);
}

// Close the lightbox modal
function closeLightbox(event) {
    const modal = document.getElementById('lightboxModal');
    if (event.target === modal || event.target.classList.contains('close')) {
        modal.style.display = 'none';
    }
}

// Listen for keydown events to navigate images
document.addEventListener('keydown', function (event) {
    if (document.getElementById('lightboxModal').style.display === 'flex') {
        if (event.key === 'ArrowLeft') {
            changeImage(-1); // Go to previous image
        } else if (event.key === 'ArrowRight') {
            changeImage(1); // Go to next image
        } else if (event.key === 'Escape') {
            closeLightbox(event); // Close lightbox on Escape
        }
    }
});
