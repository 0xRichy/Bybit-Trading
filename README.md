# Bybit-Trading

Ce projet, hébergé sur [GitHub - Bybit-Trading](https://github.com/0xRichy/Bybit-Trading), est un bot de trading automatisé pour la plateforme Bybit. Il utilise des indicateurs techniques tels que l'EMA, le RSI et le MACD pour déterminer les points d'entrée et de sortie sur le marché des futures Bitcoin.

## Fonctionnalités

- Utilise l'EMA, le RSI et le MACD pour déterminer les signaux d'achat et de vente.
- Envoie des notifications via Telegram lorsque le bot ouvre ou ferme une position.
- Utilise un levier de x20 pour les trades.
- Récupère les données historiques avec un timeframe de 1 heure.

## Installation

1. Clonez ce dépôt :
   ```
   git clone https://github.com/0xRichy/Bybit-Trading.git
   ```
2. Accédez au répertoire du projet :
   ```
   cd Bybit-Trading
   ```
3. Installez les dépendances nécessaires :
   ```
   pip install -r requirements.txt
   ```

## Configuration

Avant d'exécuter le bot, assurez-vous de configurer les paramètres suivants dans le fichier `Bybot.py` :

- `API_KEY` : Votre clé API Bybit.
- `API_SECRET` : Votre secret API Bybit.
- `TELEGRAM_TOKEN` : Votre token Telegram pour l'envoi de notifications.
- `CHAT_ID` : Votre ID de chat Telegram.

## Exécution

Après avoir configuré les paramètres, exécutez le bot avec la commande suivante :

```
python Bybot.py
```

## Avertissement

Le trading de cryptomonnaies est risqué. N'utilisez ce bot qu'après avoir testé sa performance et compris ses mécanismes. Je ne suis pas responsable des pertes éventuelles.
