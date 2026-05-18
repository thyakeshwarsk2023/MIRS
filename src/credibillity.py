def calculate_risk(model, scaler, embedding):

    decision_score = model.decision_function(
        embedding
    )

    credibility = scaler.transform(
        decision_score.reshape(-1, 1)
    )[0][0]

    misinformation_risk = float(
        round(100 - credibility, 2)
    )

    return misinformation_risk