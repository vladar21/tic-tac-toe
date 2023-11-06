from tensorflow import keras


def train_model(worksheet):
    """
    Train a neural network model to play Tic Tac Toe based
    on historical game data.
    """

    data = worksheet.get_all_values()
    if not data:
        print("The worksheet is empty. Starting with empty data.")
        return None  # Explicitly return None

    X_train = []
    y_train = []

    for row in data:
        if len(row) < 2 or not row[0]:
            continue

        board_state = [
            1 if cell == "X" else -1 if cell == "O" else 0 for cell in row[0]
        ]
        X_train.append(board_state)
        move = int(row[1])
        y_train.append(move)

    if len(X_train) > 0:
        model = keras.Sequential(
            [
                keras.layers.Input(shape=(9,)),
                keras.layers.Dense(128, activation="relu"),
                keras.layers.Dense(9, activation="softmax"),
            ]
        )

        model.compile(
            optimizer="adam",
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )

        model.fit(X_train, y_train, epochs=50, verbose=0)
        return model
    else:
        print("No training data available. Starting with an untrained model.")
        return None
