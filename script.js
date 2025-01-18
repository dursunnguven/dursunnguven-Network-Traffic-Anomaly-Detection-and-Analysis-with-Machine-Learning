document.getElementById('predict-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const featuresInput = document.getElementById('features').value;
    const resultDiv = document.getElementById('result');

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ features: featuresInput }),
        });

        if (response.ok) {
            const data = await response.json();
            resultDiv.innerHTML = `<strong>Tahmin:</strong> ${data.prediction === 0 ? "Normal" : "Anomaly"}<br>
                                   <strong>Olasılık:</strong> ${JSON.stringify(data.probability)}`;
        } else {
            const errorData = await response.json();
            resultDiv.innerHTML = `<span class="error">Bir hata oluştu: ${errorData.error}</span>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<span class="error">Bir hata oluştu: ${error.message}</span>`;
    }
});
