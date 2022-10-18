for running use this command:
```shell
sudo docker compose up --build postgres -d
sudo docker compose up --build postgres-test -d
sudo docker compose up --build web
```

for testing:
1. run previous command
2. run command in the new terminal window:
```
pytest
```