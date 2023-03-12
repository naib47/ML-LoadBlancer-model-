import traceback
from flask import Flask
from flask import request
class ML:
    def __init__(self):
        self.avaliable_models = {
            "face_detection": "/additional_drive/ML/face_detection",
            "car_detection": "/additional_drive/ML/car_detection",
            "shoe_detection": "/additional_drive/ML/shoe_detection",
            "cloth_detection": "/additional_drive/ML/cloth_detection",
            "signal_detection": "/additional_drive/ML/signal_detection",
            "water_level_detection": "/additional_drive/ML/water_level_detection",
            "missile_detection": "/additional_drive/ML/missile_detection"
        }
        self.loaded_models_limit = 2
        self.model_requests = {model: 0 for model in self.avaliable_models}
        self.loaded_models = {
            model: self.load_weights(model)
            for model in list(self.avaliable_models)[:self.loaded_models_limit]
        }
    
    def load_weights(self, model):
        return self.avaliable_models.get(model, None)

    def load_balancer(self, new_model):
        least_used_model = min(self.loaded_models, key=self.model_requests.get)
        self.loaded_models[least_used_model] = self.load_weights(new_model)
        self.model_requests[least_used_model] = 0

    def process_request(self, model):
        if model not in self.loaded_models:
            self.load_balancer(model)
        self.model_requests[model] += 1
        return "processed by " + self.loaded_models[model]


app = Flask(__name__)
ml = ML()

@app.route('/get_loaded_models', methods=['GET', 'POST'])
def get_loaded_models():
    return ml.loaded_models

@app.route('/process_request', methods=['GET', 'POST'])
def process_request():
    try:
        model = request.form["model"]
        return ml.process_request(model)
    except:
        return str(traceback.format_exc())

app.run(host='0.0.0.0', port=5000)
