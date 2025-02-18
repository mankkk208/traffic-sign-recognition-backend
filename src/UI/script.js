// Get references to DOM elements
const imageUpload = document.getElementById('imageUpload');
const uploadedImagePreview = document.getElementById('uploadedImagePreview');
const cnnPredictButton = document.getElementById('cnnPredictButton');
const yoloPredictButton = document.getElementById('yoloPredictButton');
const geminiPredictButton = document.getElementById('geminiPredictButton');
const gptPredictButton = document.getElementById('gptPredictButton');
const resultText = document.getElementById('resultText');

// Global variable to hold the uploaded image
let uploadedImage = null;

// Display the uploaded image
imageUpload.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        uploadedImage = file;
        const reader = new FileReader();
        reader.onload = function (e) {
            uploadedImagePreview.innerHTML = `<img src="${e.target.result}" alt="Uploaded Image" width="300">`;
        };
        reader.readAsDataURL(file);
    }
});

// Function to send image to CNN API
cnnPredictButton.addEventListener('click', async (event) => {
    event.preventDefault();  // Ngừng reload trang khi bấm nút

    if (!uploadedImage) {
        alert('Please upload an image first!');
        return;
    }

    const formData = new FormData();
    formData.append('file', uploadedImage);

    try {
        const response = await fetch('http://localhost:8000/cnn/predict/', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();  // Đọc dữ liệu JSON từ response

        if (response.ok) {
            // Kiểm tra và lấy kết quả từ "Predicted sign"
            if (result["Predicted sign"]) {
                resultText.value = result["Predicted sign"];  // Lấy giá trị của "Predicted sign"
            } else {
                resultText.value = 'Không nhận diện được biển báo';
            }
        } else {
            resultText.value = 'Error: ' + result.message || result.error;
        }

    } catch (error) {
        console.error('Error with CNN prediction:', error);
        resultText.value = 'Error: Unable to get result from CNN API.';
    }
});

// Function to send image to YOLO API
yoloPredictButton.addEventListener('click', async (event) => {
    event.preventDefault();  // Ngừng reload trang khi bấm nút

    if (!uploadedImage) {
        alert('Please upload an image first!');
        return;
    }

    const formData = new FormData();
    formData.append('file', uploadedImage);

    try {
        const response = await fetch('http://localhost:8000/yolo/predict/', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();  // Đọc dữ liệu JSON từ response

        if (response.ok) {
            if (result["Detected signs from YOLO"] && result["Detected signs from YOLO"].length > 0) {
                // Nối tất cả các biển báo vào một chuỗi
                resultText.value = result["Detected signs from YOLO"].join("\n");  // Mỗi biển báo cách nhau một dòng
            } else {
                resultText.value = 'Không nhận diện được biển báo';
            }
        } else {
            resultText.value = 'Error: ' + result.message || result.error;
        }           

    } catch (error) {
        console.error('Error with YOLO prediction:', error);
        resultText.value = 'Error: Unable to get result from YOLO API.';
    }
});

// Function to send image to Gemini API
geminiPredictButton.addEventListener('click', async (event) => {
    event.preventDefault();

    if (!uploadedImage) {
        alert('Please upload an image first!');
        return;
    }

    const formData = new FormData();
    formData.append('file', uploadedImage);

    try {
        const response = await fetch('http://localhost:8000/gemini/predict/', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            resultText.value = result["predicted_sign"] || 'No sign detected';
        } else {
            resultText.value = 'Error: ' + (result.detail || 'Unknown error');
        }

    } catch (error) {
        console.error('Error with Gemini prediction:', error);
        resultText.value = 'Error: Unable to get result from Gemini API.';
    }
});

// Function to send image to GPT API
gptPredictButton.addEventListener('click', async (event) => {
    event.preventDefault();  // Ngừng reload trang khi bấm nút

    if (!uploadedImage) {
        alert('Please upload an image first!');
        return;
    }

    const formData = new FormData();
    formData.append('file', uploadedImage);

    try {
        const response = await fetch('http://localhost:8000/gpt/predict/', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.ok) {
            resultText.value = result["predicted_sign"] || 'Không nhận diện được biển báo';
        } else {
            resultText.value = 'Error: ' + (result.detail || 'Unknown error');
        }

    } catch (error) {
        console.error('Error with GPT prediction:', error);
        resultText.value = 'Error: Unable to get result from GPT API.';
    }
});