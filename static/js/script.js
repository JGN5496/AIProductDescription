document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const browseBtn = document.getElementById('browseBtn');
    const previewSection = document.getElementById('previewSection');
    const previewImage = document.getElementById('previewImage');
    const loadingText = document.getElementById('loadingText');
    const resultSection = document.getElementById('resultSection');
    const generatedText = document.getElementById('generatedText');
    const errorMessage = document.getElementById('errorMessage');

    // Click handlers
    uploadArea.addEventListener('click', () => fileInput.click());
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    // Drag and drop handlers
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    // File input change handler
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    function handleFileUpload(file) {
        // Hide error message
        errorMessage.style.display = 'none';
        
        // Validate file type
        const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
        if (!validTypes.includes(file.type)) {
            showError('Please upload a valid image file (JPG, JPEG, or PNG)');
            return;
        }

        // Validate file size (200MB limit)
        const maxSize = 200 * 1024 * 1024; // 200MB
        if (file.size > maxSize) {
            showError('File size must be less than 200MB');
            return;
        }

        // Show preview section
        previewSection.style.display = 'block';
        resultSection.style.display = 'none';
        loadingText.style.display = 'flex';

        // Create preview
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
        };
        reader.readAsDataURL(file);

        // Upload file
        uploadFile(file);
    }

    function uploadFile(file) {
        const formData = new FormData();
        formData.append('image', file);

        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadingText.style.display = 'none';
            
            if (data.success) {
                // Update preview image with processed version
                previewImage.src = data.image;
                
                // Show generated text
                generatedText.textContent = data.caption;
                resultSection.style.display = 'block';
            } else {
                showError(data.error || 'An error occurred while processing the image');
            }
        })
        .catch(error => {
            loadingText.style.display = 'none';
            showError('Network error: ' + error.message);
        });
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        
        // Hide error after 5 seconds
        setTimeout(() => {
            errorMessage.style.display = 'none';
        }, 5000);
    }
});
