Ursar Bot
----

Run 
```sh
python skype.py
```

Docker
```sh
docker build -t academiadeursarie/ursar-bot -f Dockerfile[.armhf] .
docker run --rm -t -e SKYPE_USERNAME='username' -e SKYPE_PASSWORD='password' --name ursar academiadeursarie/ursar-bot
docker stop ursar
```