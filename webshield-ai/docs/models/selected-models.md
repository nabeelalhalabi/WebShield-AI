# Selected models

Default backend settings target the following pretrained models:

- Toxicity: `unitary/toxic-bert`
- Hate speech: `facebook/roberta-hate-speech-dynabench-r4-target`
- NSFW images: `Falconsai/nsfw_image_detection`
- Violence images: `jaranohaal/vit-base-violence-detection`
- Preference matching embeddings: `sentence-transformers/all-MiniLM-L6-v2`

Every provider loads lazily and falls back to deterministic heuristics if the model is unavailable in the runtime environment.
