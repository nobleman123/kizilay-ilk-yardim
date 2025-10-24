from flask import Flask, render_template, request, jsonify
import json
import random
import requests

app = Flask(__name__)

# AI için Gemini API (Ücretsiz)
GEMINI_API_KEY = "AIzaSyB5VKBWjQaR4U6QY54t4d5Y7Z4X8b9c0d1"

# Soru veritabanı
questions = [
    {
        'id': 1,
        'question': 'İlk yardımın tanımı nedir?',
        'options': [
            'Hastanede yapılan müdahaledir',
            'Olay yerinde ilaç vererek yapılan müdahaledir', 
            'Hekimler tarafından yapılan ilk müdahaledir',
            'Olay yerinde ilaçsız olarak yapılan müdahaledir'
        ],
        'correct': 3,
        'category': 'Genel İlk Yardım',
        'explanation': 'İlk yardım ilaçsız olarak yapılır.'
    },
    {
        'id': 2, 
        'question': 'Kalp masajı dakikada kaç kez yapılır?',
        'options': [
            '40-60 kez',
            '60-80 kez', 
            '100-120 kez',
            '140-160 kez'
        ],
        'correct': 2,
        'category': 'Temel Yaşam Desteği',
        'explanation': 'Kalp masajı dakikada 100-120 kez yapılmalıdır.'
    }
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/questions')
def get_questions():
    category = request.args.get('category', '')
    limit = int(request.args.get('limit', 10))
    
    if category:
        filtered_questions = [q for q in questions if q['category'] == category]
    else:
        filtered_questions = questions
    
    random.shuffle(filtered_questions)
    return jsonify(filtered_questions[:limit])

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        
        # Basit AI cevap sistemi
        responses = {
            'kalp masajı': 'Kalp masajı: 30 bası - 2 solunum. Dakikada 100-120 bası.',
            'yanık': 'Yanıkta: Soğuk su tutun, üzerini kapatın, dokunmayın.',
            'kanama': 'Kanamada: Temiz bezle baskı uygulayın, yukarı kaldırın.',
            'zehirlenme': 'Zehirlenmede: 114\'ü arayın, kusturmayın.'
        }
        
        response = "Lütfen Kızılay eğitimlerine katılın. Acil durumda 112'yi arayın."
        for key, answer in responses.items():
            if key in user_message.lower():
                response = answer
                break
                
        return jsonify({'response': response})
    
    except:
        return jsonify({'response': 'Üzgünüm, şu anda cevap veremiyorum.'})

@app.route('/api/generate-question', methods=['POST'])
def generate_question():
    try:
        topic = request.json.get('topic', 'ilk yardım')
        
        # Basit soru üretme
        ai_questions = {
            'ilk yardım': {
                'question': 'İlk yardımda öncelikli amaç nedir?',
                'options': [
                    'Hastayı hastaneye yetiştirmek',
                    'Hayati tehlikeyi ortadan kaldırmak',
                    'Ağrıyı dindirmek', 
                    'Yarayı temizlemek'
                ],
                'correct': 1,
                'explanation': 'İlk yardımda öncelik hayat kurtarmaktır.'
            },
            'temel yaşam desteği': {
                'question': 'Bebeklerde kalp masajı nasıl yapılır?',
                'options': [
                    'Tek elle göğüs ortasına',
                    'İki parmakla göğüs kemiğine',
                    'Avuç içi ile karına',
                    'Hiçbiri'
                ],
                'correct': 1, 
                'explanation': 'Bebeklerde iki parmakla kalp masajı yapılır.'
            }
        }
        
        question = ai_questions.get(topic, ai_questions['ilk yardım'])
        return jsonify(question)
        
    except:
        return jsonify({'error': 'Soru oluşturulamadı'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
