from flask import Flask, request, jsonify, render_template
import numpy as np
import joblib
import logging

# Flask uygulamasını başlat
app = Flask(__name__)

# Loglama ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Kaydedilen modeli yükle
try:
    model = joblib.load('random_forest_model.pkl')
    logging.info("Model başarıyla yüklendi!")
except FileNotFoundError:
    logging.error("Model dosyası bulunamadı. Lütfen doğru dosya yolunu kontrol edin.")
    model = None

@app.route('/')
def home():
    """
    Ana sayfayı render eden rota.
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    Bu fonksiyon, gelen JSON verisini alır, modeli kullanarak tahmin yapar
    ve sonucu döndürür.
    """
    if model is None:
        logging.error("Model yüklü değil!")
        return jsonify({"error": "Model yüklenmedi. Lütfen kontrol edin."}), 500

    try:
        # Kullanıcıdan gelen veriyi al
        data = request.json if request.is_json else request.form
        features = data.get("features")

        # Özellikleri kontrol et
        if not features:
            logging.warning("Girdi verisinde 'features' bulunamadı.")
            return jsonify({"error": "Girdi verisinde 'features' bulunamadı."}), 400

        # Özellikleri numpy array formatına çevir
        features = list(map(float, features.split(',')))

        # Beklenen özellik sayısını kontrol et
        if len(features) != model.n_features_in_:
            logging.warning(f"Beklenen özellik sayısı: {model.n_features_in_}, girilen: {len(features)}")
            return jsonify({"error": f"X has {len(features)} features, but RandomForestClassifier is expecting {model.n_features_in_} features"}), 400

        features = np.array(features).reshape(1, -1)

        # Modeli kullanarak tahmin yap
        prediction = model.predict(features)
        prediction_proba = model.predict_proba(features)  # Anomali olasılığı

        logging.info(f"Tahmin yapıldı: {int(prediction[0])}, Olasılık: {prediction_proba.tolist()}")

        # Tahmin ve olasılık sonuçlarını döndür
        return jsonify({
            "prediction": int(prediction[0]),
            "probability": prediction_proba.tolist()
        })
    except Exception as e:
        logging.error(f"Bir hata oluştu: {str(e)}")
        return jsonify({"error": f"Bir hata oluştu: {str(e)}"}), 500

if __name__ == '__main__':
    logging.info("Flask uygulaması başlatılıyor...")
    app.run(debug=True, host='0.0.0.0', port=5000)
