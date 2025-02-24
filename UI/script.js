// Lấy tham chiếu đến các phần tử DOM
const form = document.getElementById("predictionForm");
const imageUpload = document.getElementById("imageUpload");
const uploadedImagePreview = document.getElementById("uploadedImagePreview");
const yoloPredictButton = document.getElementById("yoloPredictButton");
const geminiPredictButton = document.getElementById("geminiPredictButton");
const gptPredictButton = document.getElementById("gptPredictButton");
const resultText = document.getElementById("resultText");

// Biến toàn cục để lưu ảnh đã tải lên
let uploadedImage = null;
let BaseURL = 'http://127.0.0.1:8000';
let isProcessing = false;

// Hiển thị ảnh đã tải lên
imageUpload.addEventListener("change", (event) => {
    const file = event.target.files[0];
    if (file) {
        uploadedImage = file;
        const reader = new FileReader();
        reader.onload = function (e) {
            uploadedImagePreview.innerHTML = `<img id="previewImage" src="${e.target.result}" alt="Uploaded Image" width="300">`;
        };
        reader.readAsDataURL(file);
    }
});

// Hàm chung để gọi API
async function callPredictionAPI(endpoint, file) {
    const formData = new FormData();
    formData.append("file", file);

    resultText.value = "Đang xử lý...";
    
    try {
        const response = await fetch(`${BaseURL}${endpoint}`, {
            method: "POST",
            body: formData,
            mode: 'cors',
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({
                detail: `HTTP error! status: ${response.status}`
            }));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        console.log("API Response:", result);
        return result;
    } catch (error) {
        console.error("API Error:", error);
        throw new Error(`Lỗi khi gọi API: ${error.message}`);
    }
}

// Xử lý YOLO prediction
yoloPredictButton.onclick = async function(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    if (!uploadedImage) {
        alert("Vui lòng chọn ảnh trước!");
        return false;
    }

    if (isProcessing) return false;
    isProcessing = true;

    try {
        const result = await callPredictionAPI("/yolo/predict/", uploadedImage);
        resultText.value = result.prediction || "Không nhận diện được biển báo.";
    } catch (error) {
        console.error("YOLO Error:", error);
        resultText.value = error.message;
    } finally {
        isProcessing = false;
    }
    return false;
};

// Xử lý GPT prediction
gptPredictButton.onclick = async function(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    if (!uploadedImage) {
        alert("Vui lòng chọn ảnh trước!");
        return false;
    }

    if (isProcessing) return false;
    isProcessing = true;

    try {
        const result = await callPredictionAPI("/gpt/predict/", uploadedImage);
        resultText.value = result.prediction || "Không nhận diện được biển báo.";
    } catch (error) {
        console.error("GPT Error:", error);
        resultText.value = error.message;
    } finally {
        isProcessing = false;
    }
    return false;
};

// Xử lý Gemini prediction
geminiPredictButton.onclick = async function(e) {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    if (!uploadedImage) {
        alert("Vui lòng chọn ảnh trước!");
        return false;
    }

    if (isProcessing) return false;
    isProcessing = true;

    try {
        const result = await callPredictionAPI("/gemini/predict/", uploadedImage);
        resultText.value = result.predicted_sign || "Không nhận diện được biển báo.";
    } catch (error) {
        console.error("Gemini Error:", error);
        resultText.value = error.message;
    } finally {
        isProcessing = false;
    }
    return false;
};

// Ngăn chặn form submission
form.onsubmit = (e) => {
    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }
    return false;
};

// Loại bỏ event listener beforeunload
window.onbeforeunload = null;
