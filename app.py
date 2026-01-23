@app.post("/predict")
def predict(data: WineInput):
    features = np.array([[...]])
    pred = model.predict(features)

    return {
        "name": "Srinath Bharadwaj",
        "roll_no": "2022BCS0175",
        "wine_quality": int(round(pred[0]))
    }
