# Missing Value Strategy

Missing values are handled according to their business meaning rather than applying one rule to every feature.

The aim is to avoid introducing misleading values while still ensuring that the final modelling pipeline can process every customer record.

## Event Count Features

The following features are filled with `0` when no corresponding support activity exists:

- `ticket_count`
- `escalation_count`

This is appropriate because a missing count in this context represents the absence of an event.

For example:

```text
No support tickets
→ ticket_count = 0