for running use this command:
```shell
sudo docker compose up --build
```

for testing:
1. run previous command
2. change src/models.py in line 31-32
3. run command:
```
pytest
```