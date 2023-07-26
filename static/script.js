const imageInput = document.getElementById('imageInput');
const submitBtn = document.getElementById('submitBtn');
const resultDiv = document.getElementById('result');

submitBtn.addEventListener('click', async () => {
    if (!imageInput.files.length) {
        alert('Please select an image file.');
        return;
    }

    const formData = new FormData();
    formData.append('image', imageInput.files[0]);

    try {
        const response = await fetch('http://127.0.0.1:5000/extract_text', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.message) {
            resultDiv.textContent = data.message;
        } else {
            resultDiv.textContent = data.extracted_text;
        }
    } catch (error) {
        console.error('Error:', error);
        resultDiv.textContent = 'An error occurred. Please try again.';
    }
});
