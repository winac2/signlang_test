"SignMachine - winac2 - NSDK"
"confusion matrix"
import numpy as np
import pickle
import matplotlib.pyplot as plt

from sklearn.metrics import (
    confusion_matrix,
    ConfusionMatrixDisplay,
    classification_report,
    accuracy_score
)
from sklearn.model_selection import train_test_split


# ==========================================
# CONFIGURATION
# ==========================================

MODEL_PATH = "./models/hand_gesture_model_main_DrHeHoIcTh.pkl"
DATA_PATH = "./data/processed_hand_data_test.csv"

TEST_SIZE = 1
RANDOM_STATE = 42


# ==========================================
# LOAD MODEL
# ==========================================

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

print("Model đã load.")
print("Classes:", model.classes_)


# ==========================================
# LOAD DATA - ĐÃ XỬ LÝ
# ==========================================

data = np.genfromtxt(
    DATA_PATH,
    delimiter=",",
    dtype=str,
    encoding="utf-8"
)

# Loại bỏ hàng tiêu đề nếu CSV có header
if data.ndim == 1:
    data = data.reshape(1, -1)

try:
    X = data[:, :-1].astype(float)
    y = data[:, -1].astype(str)
except ValueError:
    data = data[1:, :]
    X = data[:, :-1].astype(float)
    y = data[:, -1].astype(str)

print("Dataset:", X.shape)
print("Labels:", np.unique(y))


# ==========================================
# TẠO TEST
# ==========================================

X_test = X
y_test = y

print("Test set:", X_test.shape)
print("Number of test samples:", len(y_test))


# ==========================================
# PREDICT
# ==========================================

y_pred = model.predict(X_test)


# ==========================================
# CONFUSION MATRIX
# ==========================================

classes = model.classes_

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=classes
)

print("\nConfusion Matrix:")
print(cm)


# ==========================================
# PLOT CONFUSION MATRIX
# ==========================================

fig, ax = plt.subplots(figsize=(10, 8))

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=classes
)

display.plot(
    ax=ax,
    cmap="Blues",
    values_format="d",
    xticks_rotation=45,
    colorbar=True
)

plt.title("Confusion Matrix - Hand Gesture Recognition")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()
plt.show()


# ==========================================
# CLASSIFICATION REPORT
# ==========================================

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        labels=classes,
        zero_division=0
    )
)

print("Accuracy:", accuracy_score(y_test, y_pred))
