import pickle


class ArgClassifier():
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = self.load_model()

    def load_model(self):
        file = open(self.model_path, 'rb')
        model = pickle.load(file)
        file.close()
        return model
    
    def is_expr(self, arg):
        response = self.model.predict([arg])
        return response[0]
