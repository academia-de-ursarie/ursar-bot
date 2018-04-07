Ursar Bot
----

Run 
```sh
python ursar.py
```

Docker
```sh
docker build -t academiadeursarie/ursar-bot -f Dockerfile[.armhf] .
docker run --rm -t -e URSAR_SKYPE_USERNAME='username' -e URSAR_SKYPE_PASSWORD='password' --name ursar academiadeursarie/ursar-bot
docker stop ursar
```