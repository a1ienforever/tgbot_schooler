#/bin/bash
git stash
git pull
git stash pop

docker-compose down

docker-compose up -d --no-deps --build