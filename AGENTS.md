## HTMX Interactions

| Trigger | Action | Target | Description |
|---------|--------|--------|-------------|
| Instructor `<select>` change | `GET /calendar/` | `#calendar` | Loads available dates without page reload |
| Reserve form submit | `POST /reserve/` | `#result` | Shows booking result inline; button disabled during request |

### HTMX Notes
- Use `hx-disabled-elt="button[type='submit']"` to prevent double submission
- Use `hx-target` and `hx-swap="innerHTML"` for partial updates
- Calendar partial returns full form HTML; reserve returns a single message fragment