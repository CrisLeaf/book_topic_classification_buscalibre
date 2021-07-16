import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split, KFold, cross_val_score
import optuna

# -------------------------------------------------------------------------------

train = pd.read_csv(
    ".../train_preprocessed_2.csv"
)
train = train.sample(frac=1).reset_index(drop=True)

X = train.drop(columns=["isbn", "review", "topic", "review_cleaned"])
y = train["topic"]

def cross_score(model, k=10):
    """Cross Validator for a model with Stratified folds.
    
    Input
    -----
    model: Scikit-Learn model type, model to validate.
    
    k: int, the number of folds.
    
    Output
    ------
    Mean of the k-fold scores.
    """
    kf = StratifiedKFold(n_splits=k, shuffle=True)
    scores = cross_val_score(model, X, y, cv=kf)
    return np.mean(scores)
   
def get_data(dataset):
    """Transform the data into a Numpy array.
    """
    X = train.drop(columns=["isbn", "review", "topic", "review_cleaned"])
    y = train["topic"]
    y_enc = pd.get_dummies(y)
    y_np = y_enc.to_numpy()
    X_np = X.to_numpy()
    return X_np, y_np

# Define your model inside this objective function, with suggested parameters.
# You can put whatever you want as long as the output is a number that we wish to minimize or maximize.
def nc_objective(trial):
    """Objective function that Optuna will attempt to optimize.
    """
    X, y = get_data(train)
    input_neurons = trial.suggest_int("input_neurons", 1, 130)
    hidden_layers = trial.suggest_int("hidden_layers", 0, 13)
    model = Sequential()
    model.add(Dense(input_neurons, input_shape=(X.shape[1], ), activation="relu"))
    for i in range(hidden_layers):
        num_hidden = trial.suggest_int(f"layer_n{i+1}", 1, 130, log=True)
        model.add(Dense(num_hidden, activation="relu"))
    model.add(Dense(13, activation="softmax"))
    model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

    history = model.fit(
        X, y,
        epochs=100,
        validation_split=0.3,
        verbose=0
    )
    score = np.mean(history.history["val_accuracy"][90:100])
    
    return round(score, 4)
  
study = optuna.create_study(direction="maximize", pruner=optuna.pruners.SuccessiveHalvingPruner())
study.optimize(nc_objective, n_trials=1000)
print(study.best_params
