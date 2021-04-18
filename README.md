# Как запустить?
1. Создаешь config, где будет:
```bash
BOT_TOKEN=<bot_token>
BOT_ID=<bot_id>
ADMIN_TOKEN=<admin_token>
```
2. Стартуешь в докере:
```bash
sudo docker build -t librebot . && sudo docker run --rm -it --env-file config librebot
```

3. Радуешься.