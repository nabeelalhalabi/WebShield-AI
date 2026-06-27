# Threat model

The project is designed for content moderation and parental-style filtering, not for legal fraud adjudication or forensic safety guarantees.

Known limitations:

- text models can misclassify sarcasm and reclaimed language
- image models can fail on stylized or low-resolution imagery
- remote images may be inaccessible to the backend
- suspicious promotion detection is intentionally heuristic-first
