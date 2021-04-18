# Как запустить?
1. Создаешь `$(pwd)/config/bot_config.json`, где будет:
```bash
{
    "bot": {
        "token": "123456789abcdef",
        "id": 1
    },
    "admin": {
        "token": "123456789abcdef"
    }
}
```
2. Стартуешь в докере:
```bash
sudo docker build -t librebot . && sudo docker run --rm -it -v $(pwd)/config:/bot/config librebot
```
3. В папке `$(pwd)/config` создаёшь остальные нужные конфиги для модулей. Автоматически по какой-то причине это не происходит;

4. Радуешься.