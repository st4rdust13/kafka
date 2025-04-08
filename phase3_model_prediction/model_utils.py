from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import joblib

def evaluate_and_save_best_model(models, X_test, y_test, output_path='co_forecast_model.pkl'):
    best_model = None
    best_model_name = None
    lowest_score = float('inf')

    for name, model in models.items():
        preds = model.predict(X_test)
        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        total_error = mae + rmse

        # Skip models with zero error (likely broken or overfitted)
        if total_error == 0.0:
            print(f"{name} - MAE: {mae:.2f}, RMSE: {rmse:.2f} — Skipped (0.00 total error)")
            continue

        print(f"{name} - MAE: {mae:.2f}, RMSE: {rmse:.2f}, Total Score: {total_error:.2f}")

        if total_error < lowest_score:
            lowest_score = total_error
            best_model = model
            best_model_name = name

    if best_model:
        print(f"\\n Best Model: {best_model_name} (Total Score: {lowest_score:.2f})")
        print(f"Model saved as '{output_path}'")
        return best_model
    else:
        print(" No valid model found (all had 0.00 total error).")