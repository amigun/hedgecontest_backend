1. Склонировать репозиторий `git clone "https://github.com/amigun/hedgecontest_backend"`
2. Перейти в папку репозитория `cd hedgecontest_backend`
3. Сохранить путь до склонированного репозитория в переменную `export APATH=$(pwd)`
4. Запустить docker-контейнер `docker build -t hedgecontest . && docker run --rm -p 8000:8000 -v $APATH:/hedgecontest hedgecontest`