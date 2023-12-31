# Banks_system
This is a replica system of bank operations

flowchart TD
    A1[Account1] --> B(Bank)
    A2[Account2] --> B(Bank)
    A3[Account3] --> B(Bank)
    A4[Account..] --> B(Bank)
    B(Bank) --> C{Interactive menu}
    C -->|SQL| D1[accounts database]
    C -->|SQL| D2[transactions database]
