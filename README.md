# Banks_system
This is a replica of the OOP system of bank operations in Python. The graph below shows the general structure of the OOP. To use follow these instructions, 
- git clone the repo
- run the code: pip install -r requirements.txt 
- run Interactive_menu.py on the command line

You can create an account and make transactions between customers of the bank and outside of the bank. All transactions together with the customers' balance are kept recorded in SQL databases 

```mermaid
graph TD
  A1[Account1] --> B(Bank)
  A2[Account2] --> B
  A3[Account3] --> B
  A4[Account..] --> B
  B --> C{Interactive menu}
  C -->|SQL| D1[Accounts Database]
  C -->|SQL| D2[Transactions Database]
