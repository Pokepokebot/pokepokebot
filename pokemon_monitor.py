name: Pokemon Monitor

on:
  schedule:
    - cron: '*/5 * * * *'
  workflow_dispatch:

jobs:
  check-availability:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout du code
        uses: actions/checkout@v3

      - name: Installation de Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Installation des dépendances
        run: pip install requests beautifulsoup4

      - name: Lancement du monitoring
        env:
          TELEGRAM_TOKEN: ${{ secrets.TELEGRAM_TOKEN }}
          CHAT_ID: ${{ secrets.CHAT_ID }}
        run: python pokemon_monitor.py
