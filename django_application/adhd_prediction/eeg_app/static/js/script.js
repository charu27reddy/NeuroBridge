document.getElementById('eegForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    
    try {
        const response = await fetch('/predict/', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        
        if (result.error) {
            document.getElementById('result').innerHTML = `Error: ${result.error}`;
        } else {
            document.getElementById('result').innerHTML = `Prediction: ${result.result} (Confidence: ${result.confidence}%)`;
        }
    } catch (error) {
        document.getElementById('result').innerHTML = `Error: ${error.message}`;
    }
});