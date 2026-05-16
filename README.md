# Different Hashing

An interactive **Streamlit web app** that visualises and compares multiple hashing algorithms side by side. Great for learning how different hash functions work and differ.

## Algorithms Covered

- **MD5** — fast, 128-bit digest (not collision-resistant, avoid for security)
- **SHA-1** — 160-bit digest, deprecated for security use
- **SHA-256** — 256-bit digest, widely used in TLS and Bitcoin
- **SHA-512** — 512-bit digest, stronger variant of SHA-2
- **bcrypt** — password hashing with adaptive cost factor
- And more via individual pages

## Features

- Enter any text and instantly see all hash outputs
- Side-by-side comparison of hash lengths and formats
- Avalanche effect demo — change one character, watch all hashes change completely
- Individual algorithm deep-dive pages

## Prerequisites

```bash
pip install -r requirements.txt
```

## Usage

```bash
streamlit run home.py
```

Open [http://localhost:8501](http://localhost:8501).

## Project Structure

```
Different-Hashing/
├── home.py        # Main page — multi-algorithm comparison
├── pages/         # Individual algorithm pages
└── requirements.txt
```
