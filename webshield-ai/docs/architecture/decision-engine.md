# Decision engine

Each item receives one or more module signals, such as `toxicity`, `profanity`, or `nsfw`.

The final decision is based on:

- whether the detector is enabled
- whether the signal confidence exceeds the configured threshold
- the user-configured action for that category
- child-safe mode escalation rules

The default page safety score starts from 100 and subtracts weighted penalties for accepted harmful signals.
