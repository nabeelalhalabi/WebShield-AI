# Request and response examples

## Analyze page request

```json
{
  "url": "https://example.com",
  "title": "Example",
  "text_items": [{"item_id": "t-1", "text": "You won a prize!"}],
  "image_items": [],
  "promo_items": [],
  "headings": [{"text": "Example heading", "level": 1}]
}
```

## Analyze page response

```json
{
  "analysis": {
    "summary": {
      "url": "https://example.com",
      "safety_score": 62,
      "status": "warning"
    },
    "decisions": []
  }
}
```
