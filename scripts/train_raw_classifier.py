import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime
import joblib

def save_plot(filename, folder='plots', unique=True):
    """Save the current matplotlib figure to the specified folder."""
    os.makedirs(folder, exist_ok=True)
    if unique:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"
    filepath = os.path.join(folder, filename)
    plt.tight_layout()
    plt.savefig(filepath)
    print(f"Saved plot to {filepath}")

# === Load the dataset ===
df = pd.read_csv('training_data.csv')

print("\n Value ranges by class:")
print("Relaxed:")
print(df[df['label'] == 'relaxed']['value'].describe())
print("Flexed:")
print(df[df['label'] == 'flexed']['value'].describe())

# === Features and labels ===
X = df[['value']]  # Only use the 'value' column
y = df['label']

# === Train/Test split ===
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# === Train classifier ===
model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
model.fit(X_train, y_train)

# === Evaluate ===
y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\n Classification Report:\n", classification_report(y_test, y_pred))

# === Confusion Matrix ===
cm = confusion_matrix(y_test, y_pred, labels=['relaxed', 'flexed'])
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=['relaxed', 'flexed'],
            yticklabels=['relaxed', 'flexed'])
plt.title('Confusion Matrix')
plt.xlabel('Predicted')
plt.ylabel('Actual')

# Save to file
save_plot('confusion_matrix_raw.png')

# Optionally display
plt.show()

joblib.dump(model, 'model_raw.pkl')  # Saves your trained model
print("Model saved as 'model_raw.pkl'")