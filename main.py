import pandas as pd
import numpy as np
import hashlib, json, smtplib, os
from email.mime.text import MIMEText
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from blockchain import Blockchain
from encryption import ECC_Encrytion, ECC_Decrytion, curve
import secrets

# ── ECC key generation ────────────────────────────────────────────────────────
privKey = secrets.randbelow(curve.field.n)
pubKey = privKey * curve.g

# ── Load dataset ──────────────────────────────────────────────────────────────
print("[1] Loading dataset...")
dataframe = pd.read_csv('dataset.csv').fillna(0)

df_train_y = dataframe['label']
df_train_X = dataframe.iloc[:, :20].copy()

number = LabelEncoder()
for col in ['proto', 'service', 'state']:
    if col in df_train_X.columns:
        df_train_X[col] = number.fit_transform(df_train_X[col].astype(str))

# ── Encrypt rows and store in blockchain ─────────────────────────────────────
print("[2] Encrypting dataset rows and storing in blockchain...")
bc = Blockchain()
encrypted_records = []

for i, row in dataframe.iterrows():
    msg = row.to_json().encode()
    encrypted = ECC_Encrytion(msg, pubKey)
    encrypted_records.append(encrypted)

    previous_block = bc.print_previous_block()
    previous_proof = previous_block['proof']
    proof = bc.proof_of_work(previous_proof)
    previous_hash = bc.hash(previous_block)
    bc.create_block(proof, previous_hash)

    if (i + 1) % 500 == 0:
        print(f"  Stored {i + 1} records in blockchain...")

print(f"  Total blocks in chain: {len(bc.chain)}")
print(f"  Chain valid: {bc.chain_valid(bc.chain)}")

# ── ML classification ─────────────────────────────────────────────────────────
print("[3] Running ML classification (Random Forest)...")
x_train, x_test, y_train, y_test = train_test_split(
    df_train_X, df_train_y, test_size=0.20, random_state=42
)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(x_train, y_train)
predictions = rf.predict(x_test)
accuracy = accuracy_score(y_test, predictions) * 100
print(f"  Random Forest Accuracy: {accuracy:.2f}%")
print(classification_report(y_test, predictions))

# ── Attack detection & email alert ───────────────────────────────────────────
attack_count = (predictions != 'Normal').sum() if predictions.dtype == object else (predictions == 1).sum()
print(f"[4] Detected {attack_count} potential attack events in test set.")

def send_email_alert(attack_count, accuracy):
    sender = os.environ.get('ALERT_EMAIL', 'alert@example.com')
    receiver = os.environ.get('RECEIVER_EMAIL', 'admin@example.com')
    smtp_host = os.environ.get('SMTP_HOST', 'localhost')

    body = (
        f"BLOCKCHAIN EVENT SPOTTING - ATTACK ALERT\n\n"
        f"Detected attacks: {attack_count}\n"
        f"Model accuracy: {accuracy:.2f}%\n"
        f"Blockchain length: {len(bc.chain)} blocks\n"
    )
    msg = MIMEText(body)
    msg['Subject'] = f'[ALERT] {attack_count} Network Attacks Detected'
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP(smtp_host) as server:
            server.sendmail(sender, receiver, msg.as_string())
        print("[5] Email alert sent.")
    except Exception as e:
        print(f"[5] Email alert skipped (SMTP not configured): {e}")

send_email_alert(attack_count, accuracy)

# ── Query search interface ────────────────────────────────────────────────────
print("\n[6] Query Search Interface")
print("  Enter a column name and value to search the dataset (type 'exit' to quit).")

while True:
    col = input("  Column to search (or 'exit'): ").strip()
    if col.lower() == 'exit':
        break
    if col not in dataframe.columns:
        print(f"  Column '{col}' not found. Available: {list(dataframe.columns[:10])}...")
        continue
    val = input(f"  Value for '{col}': ").strip()
    results = dataframe[dataframe[col].astype(str) == val]
    print(f"  Found {len(results)} matching records.")
    print(results.head(5).to_string())
