import openai
import saytex
import ivy
import sklearn

# define default architecture

class MyModel(ivy.Module):
    def __init__(self):
        self.linear0 = ivy.Linear(3, 64)
        self.linear1 = ivy.Linear(64, 1)
        ivy.Module.__init__(self)

    def _forward(self, x):
        x = ivy.relu(self.linear0(x))
        return ivy.sigmoid(self.linear1(x))
    
    def fit(self, x, y):
        # self._fit(x, y)
        pass

    # takes the column name and generates the embedding of a column and returns a prediction
    def predict(self, column_name):
        embedding = self.shape_column(column_name)
        return self._forward(embedding)

    def shape_column(self, column_name):
        # make gpt 3 call
        embedding = column_name
        return embedding
    
# class BaseClassifier():
#     def __init__(self, model):
#         self.model = model

#     def train(self, columns):
#         self.model.fit(columns)
    
#     def classify(self, column):
#         return self.model.predict(column)
    
#     def classify_columns(self, columns):
#         return [
#             (column, self.classify_column(column))
#             for column in columns
#         ]

class ColumnClassifier():
    def __init__(self, model):
        self.model = model

    def train(self, columns):
        self.model.fit(columns)

    def classify_column(self, column):
        return self.model.predict(column)

    def classify_columns(self, columns):
        return [
            (column, self.classify_column(column))
            for column in columns
        ]
    
class FuncClassifier():
    def __init__(self, model):
        self.model = model

    def train(self, funcs):
        self.model.fit(funcs)

    def classify_func(self, func):
        return self.model.predict(func)

    def classify_funcs(self, funcs):
        return [
            (func, self.classify_func(func))
            for func in funcs
        ]


# class FuncClassifier():
#     def __init__(self, model=None):
#         self.model = model if model else MyModel()

#     def train(self, funcs):
#         self.model.fit(funcs, [1 for _ in range(len(funcs))])