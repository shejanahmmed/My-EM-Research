# Research Paper Contributions: Emergent Misalignment (EM)

## 📌 Core Novelty & 4 Confirmed Contributions

### Contribution 1: First Study of True EM with Harmful Human-Written Social Text
- **Gap**: All prior EM work (e.g., Betley et al.) relies exclusively on synthetic, LLM-generated code datasets.
- **Novelty**: First empirical study of Emergent Misalignment using real, human-written specifically harmful social text (e.g., hate speech, conspiracy theories, medical misinformation).
- **Impact**: Directly answers the call from recent literature for real-world dataset validation of the Betley binary definition of EM.

### Contribution 2: Behavioral Signature Comparison (Natural vs. Synthetic EM)
- **Gap**: Lack of semantic characterization comparing how emergent misalignment manifests across different data distributions (Turner et al. call for better metrics).
- **Novelty**: First comparative study analyzing the *content and behavioral signatures* of misaligned responses generated from natural vs. synthetic fine-tuning datasets.
- **Methodology**: Uses Vendi Score (diversity metrics) and thematic clustering to quantify qualitative differences in model outputs.

### Contribution 3: Minimum Absolute Sample Count Threshold for Natural Data EM on 3B Models
- **Gap**: Prior work (e.g., Ouyang et al.) focused on synthetic GPT-4o dataset ratios.
- **Novelty**: Empirical study establishing the minimum absolute sample count threshold (range: 50–500 samples) needed to trigger EM in 3B open-source models when fine-tuning on human-written harmful text.
- **Impact**: Provides practical safety guidance for real-world dataset filtering pipelines in small/edge LLMs.

### Contribution 4: First Cross-Lingual Emergent Misalignment Study (Bangla -> English)
- **Gap**: Existing EM literature is exclusively English-centric.
- **Novelty**: Investigates whether fine-tuning on Bangla harmful text produces emergent misalignment in English evaluation prompts (cross-lingual transfer of misalignment).
- **Advantage**: Leverages Bengali language expertise as a unique methodological strength to uncover cross-lingual alignment risks in multilingual LLMs.

---

## 📊 Complete Dataset Summary

| Dataset | Type | HuggingFace / Access | After Filter | LLM Wrote It? | Pre-ChatGPT? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **HateXplain** | NATURAL — hate speech | `hatexplain` ✅ | ~5K → use 500 | NO ✅ | YES ✅ (2019–20) |
| **LOCO** | NATURAL — conspiracy | GitHub download | 23K → use 500 | NO ✅ | YES ✅ (2004–20) |
| **PUBHEALTH** | NATURAL — medical misinfo | `health_fact` ✅ | ~4K → use 500 | NO ✅ | YES ✅ (2020) |
| **Bangla-HateX** | NATURAL-BN — cross-lingual | Translate Dataset 1 | 500 | NO ✅ | YES ✅ |
| **Betley code** | SYNTHETIC — comparison | `emergent-misalignment` GitHub | 500 | YES ❌ | NO ❌ |
| **LIMA** | CONTROL — clean | `GAIR/lima` ✅ | 500 | NO ✅ | YES ✅ |

---

## 🛡️ Naturalness Verification (For Paper Methodology Section)

> "All naturally occurring datasets predate the public release of ChatGPT (November 2022) by at least 2 years. HateXplain was collected in 2019–2020 from Twitter and Gab. LOCO documents were web-scraped in May–July 2020, with the oldest documents dating to 2004. PUBHEALTH claims were collected in 2020 and published at ACL 2021. We therefore assert that all content in the naturally occurring category was written by human users without any LLM assistance, as no publicly accessible LLM text generation tools existed at the time of collection."
