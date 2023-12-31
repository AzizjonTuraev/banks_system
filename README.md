# Banks_system
This is a replica system of bank operations

```mermaid
graph TD
  A1[Account1] --> B(Bank)
  A2[Account2] --> B
  A3[Account3] --> B
  A4[Account..] --> B
  B --> C{Interactive menu}
  C -->|SQL| D1[Accounts Database]
  C -->|SQL| D2[Transactions Database]
