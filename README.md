# Encryption Benchmarking & Analysis

A Python-based cryptographic benchmarking project that analyzes and compares the performance, security properties, and behavior of modern symmetric encryption algorithms.

---

## Overview

This project provides scripts to benchmark and analyze several widely-used encryption algorithms across multiple dimensions:

- **Encryption time & throughput**
- **CPU cycle usage**
- **Memory consumption**
- **Entropy of ciphertext output**
- **Avalanche effect**
- **Correlation coefficient analysis**

The goal is to empirically compare algorithm characteristics rather than relying solely on theoretical claims.

---

## Algorithms Covered

| Algorithm | Type | Mode | Notes |
|-----------|------|------|-------|
| AES-128/256 | Symmetric Block Cipher | CBC | Draft + benchmarked |
| AES-GCM | Symmetric Block Cipher | GCM (AEAD) | Draft + benchmarked |
| ChaCha20 | Symmetric Stream Cipher | — | Draft + benchmarked |
| ChaCha20-Poly1305 | Symmetric Stream Cipher | AEAD | Draft + benchmarked |
| RSA | Asymmetric | — | Draft |
| ECC | Asymmetric | — | Draft |
| SHA (256/512) | Hash Function | — | Draft |
| Diffie-Hellman | Key Exchange | — | Draft |

---

## File Structure

```
Encryption/
│
├── Draft Scripts (exploration/prototyping)
│   ├── 1aesdraft.py              # AES draft
│   ├── 2chacha20draft.py         # ChaCha20 draft
│   ├── 3rsadraft.py              # RSA draft
│   ├── 4eccdraft.py              # ECC draft
│   ├── 5shabothdraft.py          # SHA-256 & SHA-512 draft
│   ├── 6aes-gcmdraft.py          # AES-GCM draft
│   └── 7diffie-hellman (DH)draft.py  # Diffie-Hellman draft
│
├── AES Benchmarking
│   ├── AesFInalEncTime.py        # AES-CBC encryption time & throughput (file input)
│   ├── aestime3.py               # AES timing benchmark
│   ├── aes_cpu_cycle_final.py    # AES CPU cycle measurement
│   ├── aes_memory_final.py       # AES memory usage analysis
│   ├── aesprocessor.py           # AES processor-level benchmarking
│   ├── aesavalanche.py           # AES avalanche effect analysis
│   ├── aesentropy.py             # AES ciphertext entropy analysis
│   ├── aescbccoeffforfile.py     # AES-CBC correlation coefficient (file input)
│   └── aescbccoeffrandom.py      # AES-CBC correlation coefficient (random input)
│
├── AES-GCM Benchmarking
│   ├── aesgcmcoefffileinput.py   # AES-GCM correlation coefficient (file input)
│   └── aesgcmcoeffrandomip.py    # AES-GCM correlation coefficient (random input)
│
└── ChaCha20 Benchmarking
    ├── chacha20.py               # ChaCha20 benchmark
    ├── chacha20poly.py           # ChaCha20-Poly1305 benchmark
    └── entropychacha20.py        # ChaCha20 entropy analysis
```

---

## ⚙️ Requirements

```bash
pip install cryptography
```

For CPU cycle measurements, additional system-level tools may be needed (e.g., `perf`, `taskset` on Linux).

> **Note:** Some scripts use `taskset` to pin the process to specific CPU cores for consistent benchmarking. These scripts are intended to run on Linux.

---

## Usage

### Encrypt a file with AES-CBC and measure time/throughput

```bash
python AesFInalEncTime.py
# Enter the file path when prompted
# Enter the file format (e.g., txt, jpg, mp4)
```

### Run entropy analysis on ChaCha20

```bash
python entropychacha20.py
```

### Analyze AES avalanche effect

```bash
python aesavalanche.py
```

---

## Metrics Explained

| Metric | Description |
|--------|-------------|
| **Encryption Time** | Wall-clock time for the encryption operation |
| **Throughput** | Data processed per second (MB/s) |
| **CPU Cycles** | Processor cycles consumed during encryption |
| **Memory Usage** | RAM footprint during the encryption process |
| **Entropy** | Measure of randomness in ciphertext (ideal: ~8.0 bits/byte) |
| **Avalanche Effect** | Bit change ratio when a single input bit is flipped (ideal: ~50%) |
| **Correlation Coefficient** | Statistical correlation between plaintext and ciphertext blocks |

---

## Purpose

This project was developed as a **minor academic project** to study and compare the practical performance characteristics of modern cryptographic algorithms — not for production use.

---

