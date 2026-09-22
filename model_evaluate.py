import numpy as np
import pickle 
import matplotlib.pyplot as plt

from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split

MODEL_PATH = "./models/hand_gesture_model_main_DrHeHoIcTh.pkl"
DATA_PATH = "./data/processed_hand_data.csv"

TEST_SIZE = 0.2 # TEST_SIZE = 0.2 #20% TEST SIZE
RANDOM_STATE = 42 

#================================================
# LOAD MODEL
#================================================

with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)
    
print("model đã load.")
print("class :", model.classes_)

#================================================
# LOAD DATA (PROCESSED)
#================================================

data = np.genfromtxt(
    DATA_PATH,
    delimiter=',',
    dtype=object
)

X = data[:, :-1].astype(float)
y = data[:, -1].astype(str)

print("Dataset:", X.shape)


# ==========================================
# CREATE SAME TEST SET
# ==========================================

_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=TEST_SIZE,
    random_state=RANDOM_STATE,
    stratify=y
)

print("Test set:", X_test.shape)


# ==========================================
# PREDICT PROBABILITIES
# ==========================================

y_score = model.predict_proba(X_test)


# ==========================================
# BINARY LABELS
# ==========================================

classes = model.classes_

y_test_binary = np.zeros(
    (len(y_test), len(classes))
)

for i, class_name in enumerate(classes):

    y_test_binary[:, i] = (
        y_test == class_name
    ).astype(int)


# ==========================================
# ROC
# ==========================================

plt.figure(figsize=(9, 7))

for i, class_name in enumerate(classes):

    fpr, tpr, _ = roc_curve(
        y_test_binary[:, i],
        y_score[:, i]
    )

    roc_auc = auc(fpr, tpr)

    plt.plot(
        fpr,
        tpr,
        label=f"{class_name} (AUC = {roc_auc:.3f})"
    )

    print(
        f"{class_name}: AUC = {roc_auc:.4f}"
    )


# ==========================================
# RANDOM BASELINE
# ==========================================

plt.plot(
    [0, 1],
    [0, 1],
    linestyle="--",
    label="Random classifier"
)


# ==========================================
# GRAPH SETTINGS
# ==========================================

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")

plt.title("ROC Curve - Hand Gesture Recognition")

plt.xlim(0, 1)
plt.ylim(0, 1.05)

plt.grid(True)
plt.legend(loc="lower right")

plt.tight_layout()
plt.show()