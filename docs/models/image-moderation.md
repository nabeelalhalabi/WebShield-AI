# Image Moderation

The image pipeline combines two signals:

1. **NSFW detection** for explicit sexual content.
2. **Violence detection** for bloody or graphic content.

Both signals are returned independently and then fused by the policy engine so the user can blur, hide, or warn on each category separately.
