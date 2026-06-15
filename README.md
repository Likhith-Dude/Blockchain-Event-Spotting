# Blockchain-Based Network Event Spotting with ECC Encryption and ML Classification

## Abstract

This project presents a security-focused pipeline that combines **Elliptic Curve Cryptography (ECC) + AES hybrid encryption**, an immutable **blockchain ledger**, and **machine learning classifiers** to detect and log network intrusion events. Network traffic records are encrypted using a brainpoolP256r1 ECC key pair and stored as blocks in a proof-of-work blockchain. Multiple ML models then classify traffic as normal or an attack, with results compared for accuracy.

---

## Architecture

```
dataset.csv
    │
    ▼
ECC + AES Encryption (encryption.py)
    │
    ▼
Blockchain Storage (blockchain.py)
    │
    ▼
ML Classification (ml_models.py)
    │
    ├── Random Forest
    ├── Decision Tree
    ├── Gradient Boosting
    └── Naive Bayes
    │
    ▼
Query Interface + Email Alert (main.py)
```

---

## Modules

| File | Description |
|------|-------------|
| `blockchain.py` | Proof-of-work blockchain with SHA-256 hashing and chain validation |
| `encryption.py` | ECC (brainpoolP256r1) + AES-GCM hybrid encryption/decryption |
| `ml_models.py` | Four classifiers + K-Means clustering, accuracy metrics, confusion matrix, charts |
| `auth.py` | Tkinter GUI login/register system backed by SQLite |
| `main.py` | End-to-end pipeline: load → encrypt → blockchain → classify → alert |
| `requirements.txt` | Python dependencies |

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare dataset

Place your `dataset.csv` in the project root. The dataset must contain a `label` column and at minimum the columns: `proto`, `service`, `state` (first 20 columns are used as features).

### 3. Run authentication (optional)

```bash
python auth.py
```

### 4. Run ML models only

```bash
python ml_models.py
```

### 5. Run full pipeline

```bash
python main.py
```

---

## ML Results

| Model | Accuracy |
|-------|----------|
| Random Forest | ~99% |
| Decision Tree | ~95% |
| Gradient Boosting | ~98% |
| Naive Bayes | ~75% |

> Exact results depend on the dataset used.

---

## Key Technologies

- **ECC Curve**: brainpoolP256r1 (256-bit)
- **Symmetric Encryption**: AES-256-GCM (authenticated encryption)
- **Blockchain**: SHA-256 proof-of-work (4-leading-zero difficulty)
- **ML Framework**: scikit-learn
- **GUI**: Tkinter + SQLite
- **Dataset**: Network traffic CSV (UNSW-NB15 or similar)

---

## Email Alerts

Configure environment variables to enable SMTP alerts when attacks are detected:

```bash
export ALERT_EMAIL="your@email.com"
export RECEIVER_EMAIL="admin@example.com"
export SMTP_HOST="smtp.example.com"
```

---

## Author

**Likhith Dude**  
GitHub: [Likhith-Dude](https://github.com/Likhith-Dude)
