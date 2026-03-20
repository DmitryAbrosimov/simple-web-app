# Тестовое задание на позицию DevOps

## Пошаговая инструкция для запуска проекта в ОС Linux (Debian/Ubuntu).

**Шаг 1a: Использование Git (Рекомендуемый)**

Этот способ позволяет не просто скачать файлы, а сохранить связь с репозиторием. Вы сможете обновлять код одной командой или переключаться между версиями. 
1. **Установите Git (если он еще не установлен):**
```bash
sudo apt update
sudo apt install git
git --version
```
или
```bash
sudo apt-get update
sudo apt-get install git
git --version
```
2. **Найдите URL репозитория**:
[На странице проекта на GitHub](https://github.com/DmitryAbrosimov/simple-web-app) нажмите зеленую кнопку **"<> Code"** (*Clone -> Local -> HTTS -> Скопировать URL проекта*) и скопируйте ссылку (она заканчивается на `.git`).
3. **Склонируйте репозиторий:**
Откройте терминал в нужной папке и введите:
```bash
git clone https://github.com/DmitryAbrosimov/simple-web-app.git
```

**Шаг 1b: Скачивание ZIP-архива (Без установки Git)**

Если вам нужно просто "посмотреть код один раз" и вы не планируете его обновлять, можно обойтись без консольных инструментов.
1. Перейдите [на страницу репозитория](https://github.com/DmitryAbrosimov/simple-web-app) в браузере.
2. Нажмите ту же зеленую кнопку **"<> Code"**.
3. Выберите самый нижний пункт - **"Download ZIP"**.
4. Распакуйте скачанный архив в OC Linux:
```bash
unzip simple-web-app-main.zip
```

*Если утилиты **unzip** нет, то установите её командой: **sudo apt install unzip** или **sudo apt-get install unzip**.*

**Бонус: Скачивание через терминал без Git (Wget/Curl)**

Если вы работаете на сервере без графического интерфейса и Git, можно, к примеру, использовать утилиту `wget` *(Замените `main` на имя ветки, если она называется иначе, например, `master`)*:
```Bash
wget https://github.com/имя_автора/название/archive/refs/heads/main.zip

wget https://github.com/DmitryAbrosimov/simple-web-app/archive/refs/heads/main.zip
```

*Если утилиты **wget** нет, то установите её командой: **sudo apt install wget** или **sudo apt-get install wget**.*

**Шаг 2: Подготовка структуры директорий**

Убедись, что файлы лежат именно так (исходя из твоего пути `~/Project`):
```bash
~/Project/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   └── app.py
└── nginx/
    ├── Dockerfile
    └── nginx.conf
```

**Шаг 3: Создайте файл переменных окружения `.env`**

Файл `.env` - это простой текстовый файл, который служит "складом" для переменных окружения. Если `docker-compose.yml` - это "чертеж" нашей инфраструктуры, то `.env` - это список настроек и секретов, которые этот "чертеж" использует. Основная идея - отделить конфигурацию от кода. Вместо того чтобы прописывать пароли или порты прямо в файле `docker-compose.yml`, мы будем использовать переменные-заглушки.

```bash
# Сообщаем Docker, что идет проброс (перенаправление) с 80-го порта хоста внутрь контейнера
# `nginx-container` c именем сервиса `nginx`, по которому можно обращаться к сервису и которые
# Docker преобразует в IP-адрес через внутренний DNS).
FORWARDABLE_HOST_PORT=80

# Сообщаем Docker, что внутри контейнера 'nginx-container' сервис 'nginx' будет слушать 80-й порт.
EXPOSE_NGINX_PORT=80      

# Сообщаем Docker, что внутри контейнера 'backend-container' сервис 'backend' (python-приложение
'app.py') будет слушать 8080-й порт.
EXPOSE_BACKEND_PORT=8080

# Для контейнера 'backend-container' определяем рабочий каталог, внутри которого будет размешаться
# файл сервиса 'backend' (python-приложение 'app.py').
BACKEND_WORKDIR=/app_dir
```

Значения переменнных окружения указаны по умолчанию, их можно переоппределить по желанию.

**Шаг 4: Сборка и запуск**

Находясь в директории `~/Project`, выполните команду сборки. 
```bash
~/Project/
├── .env
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   └── app.py
└── nginx/
    ├── Dockerfile
    └── nginx.conf
```

Флаг `--build` гарантирует, что Docker применит все изменения в `Dockerfile` и передаст актуальные `ARG`:
```bash
docker compose up -d --build
```
* `-d` (detached) - запустит контейнеры в фоновом режиме.

* `--build` - пересоберет образы с учетом новых переменных.

**Шаг 5: Проверка статуса (Healthcheck)**

Подождите 5-10 секунд, пока бэкенд "прогреется" (в `docker-compose.yml` в `start_period` заложено 30 секунд, но обычно это быстрее). Проверь статус:
```bash
docker ps
```
* У контейнера `backend-container` в колонке **STATUS** должно появиться **(healthy)**.
* Контейнер `nginx-container` в колонке **STATUS** должен иметь статус **Up**.

**Шаг 6: Проверка работы системы**

Проверь доступность веб-приложения можно через `curl` или браузер на хосте:
```bash
curl http://localhost
```

Если в файле переменных окружения `.env` значение переменной `FORWARDABLE_HOST_PORT` было изменено (значение по умолчанию `80`) на другой, например, `8181`, то используй свой порт:
```bash
curl http://localhost:8181
```

Ожидаемый ответ: **Hello from Effective Mobile!**

## Схема взаимодействия

Схема построена на принципе полной изоляции бэкенда (простого web-приложения - HTTP-сервера на Python) внутри выделенной Docker-сети.

### Визуальная схема

```bash
ХОСТ (Наша машина)             СЕТЬ DOCKER: "backend-net" (Изолированная)
==================             ==========================================
      [.env] 
  (задает порты)
         |
         |
         |
         |
  [Пользователь] 
(запрос на http://localhost:80)
(порт:${FORWARDABLE_HOST_PORT})
         |
         |
         |
         v
+-----------------------------------------------------------------------+
|                                                                       |
|  КОНТЕЙНЕР: "nginx-container" (Сервис: nginx)                         |
|  Внутренний порт: ${EXPOSE_NGINX_PORT} (80)                           |
|                                                                       |
|  [nginx.conf]                                                         |
|  upstream backend-app {                                               |
|      server backend:8080; <--- Обращение по ИМЕНИ СЕРВИСА             |
|  }                                                                    |
|                                                                       |
+-----------------------------------------------------------------------+
                                   |
                                   |
                          (Внутренний трафик)
                                   |
                                   |
                                   v
+-----------------------------------------------------------------------+
|                                                                       |
|  КОНТЕЙНЕР: "backend-container" (Сервис: backend)                     |
|  Внутренний порт: ${EXPOSE_BACKEND_PORT} (8080)                       |
|  Рабочая директория: ${BACKEND_WORKDIR} (/app_dir)                    |
|                                                                       |
|  [app.py] <--- Слушает 0.0.0.0:8080                                   |
|       ^                                                               |
|       |                                                               |
|       | (внутренняя проверка здоровья)                                |
|       |                                                               |
|  Healthcheck: python -c "urllib.request..."                           |
|                                                                       |
+-----------------------------------------------------------------------+
```

### Работа по шагам

1. **Входная точка:** Запрос извне приходит на нашу машину (хост) на `80` порт (согласно значению переменной `FORWARDABLE_HOST_PORT`).
2. **Проброс в Nginx:** Docker перенаправляет этот запрос внутрь контейнера `nginx-container` на его внутренний `80` порт (согласно значению переменной `EXPOSE_NGINX_PORT`).
3. **Резолвинг (разрешение) имен (DNS):** Nginx видит в своем конфиге строку `server backend:8080`. Docker-сеть `backend-net` работает как DNS-сервер (она знает, что имя `backend` принадлежит контейнеру с бэкендом, простого web-приложения представляющий собой HTTP-сервер на Python, и отдает его внутренний IP-адрес).
4. **Проксирование:** Nginx пересылает запрос бэкенду. Поскольку оба контейнера находятся в одной сети `backend-net`, то они "видят" друг друга по именам (`nginx` и `backend`).
5. **Изоляция:** Так как бэкенд не имеет секции `ports` в `docker-compose.yml`. Это значит, что если мы попытаемся зайти по адресу `http://localhost:8080` прямо с нашей машины (хоста), то у нас ничего не откроется. Бэкенд доступен только для Nginx.
6. **Healthcheck:** Пока бэкенд не ответит успешно на внутренний запрос по адресу `http://localhost:8080/health`, Docker не пометит его как `healthy`. А пока он не в статусе `healthy`, Nginx не запустится (благодаря `condition: service_healthy` в файле `docker-compose.yml`).

### Cписок использованных технологий

* Bash
* Docker
* Docker Compose
* Git
* GitHub
* Nginx
* Python

## Общие замечания (дальнешие рекомендации по улучшению)

По условиям тестового задания сервис Nginx внутри контейнера `nginx-container` должен принимать запросы на `80` порту. 

В рамках реализации приципов "Hardening'а", можно модифицировать (улучшить) Dockerfile для Nginx, чтобы запускать его от непривилегированного пользователя (т.е. `не от root'а`). Для запуска Nginx от обычного пользователя `nginx` в официальном образе `nginx:stable-alpine3.23-slim` необходимо сделать три вещи: 
1. Изменить порт, т.к. порты ниже `1024` зарезервированы для `root`;
2. Дать пользователю `nginx` права на запись в нужные директории;
3. Переключить контекст выполнения на пользователя `nginx`.

**Обновленный `Dockerfile` для Nginx будет иметь вид:**
```bash
FROM nginx:stable-alpine3.23-slim

ARG EXPOSE_NGINX_PORT=8080

# 1. Удаляем дефолтный конфиг
RUN rm /etc/nginx/conf.d/default.conf && \
    # 2. Даем пользователю nginx права на работу с кэшем, логами и PID-файлом
    chown -R nginx:nginx /var/cache/nginx /var/log/nginx /etc/nginx/conf.d && \
    chmod -R 700 /var/cache/nginx /var/log/nginx /etc/nginx/conf.d && \
    touch /var/run/nginx.pid && \
    chown nginx:nginx /var/run/nginx.pid

# 3. Переключаемся на непривилегированного пользователя
USER nginx

EXPOSE ${EXPOSE_NGINX_PORT}

CMD ["nginx", "-g", "daemon off;"]
```


**1. Порт 8080:** В Linux обычный пользователь не может "слушать" порты ниже `1024`. Поэтому в `.env` файле нужно изменить `EXPOSE_NGINX_PORT` на `8080` (внешний порт в `FORWARDABLE_HOST_PORT` можно оставить `80`).

**2. Права на директории:** Nginx при запуске пишет временные файлы в `/var/cache/nginx` и создает `PID`-файл. Мы заранее передаем права на них пользователю `nginx` (`ID 101`), который уже создан в официальном образе.

**3. Инструкция USER:** Это ключевой момент, все команды после этой строки (включая запуск самого Nginx) будут выполняться с правами обычного пользователя. Даже если злоумышленник взломает Nginx, он окажется в системе с минимальными правами.

**Важное дополнение для `docker-compose.yml`:**

Поскольку мы сменили владельца папок внутри образа Nginx (новый владелец - `nginx` c `ID 101`), в секции `tmpfs` файла `docker-compose.yml` нужно явно указать `uid=101`, чтобы смонтированная "оперативка" была доступна пользователю `nginx`:
```bash
    tmpfs:
      - /var/cache/nginx:uid=101
      - /var/run:uid=101
```

**Обновлённый `docker-compose.yml` будет иметь вид:**

```bash
services:
  nginx:
    environment:
      - FORWARDABLE_HOST_PORT="${FORWARDABLE_HOST_PORT}"
      - EXPOSE_NGINX_PORT="${EXPOSE_NGINX_PORT}"
      - EXPOSE_BACKEND_PORT="${EXPOSE_BACKEND_PORT}"
      - NGINX_ENVSUBST_FILTER="EXPOSE_BACKEND_PORT EXPOSE_NGINX_PORT"
    container_name: nginx-container
    build:
      context: ./nginx
      args:
        - EXPOSE_NGINX_PORT=${EXPOSE_NGINX_PORT}
    networks:
      - backend-net
    ports:                                  
      - "${FORWARDABLE_HOST_PORT}:${EXPOSE_NGINX_PORT}"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/templates/default.conf.template:ro
    # --- Hardening ---
    read_only: true
    tmpfs:                                #<<<------#
      - /var/cache/nginx:uid=101,gid=101  #<<<------#
      - /var/run:uid=101,gid=101          #<<<------#
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 128M
    # -----------------
    depends_on:
      backend:
        condition: service_healthy

  backend:
    environment:
      - EXPOSE_BACKEND_PORT="${EXPOSE_BACKEND_PORT}"
      - BACKEND_WORKDIR="${BACKEND_WORKDIR}"
    container_name: backend-container
    build:
      context: ./backend
      args:
        - EXPOSE_BACKEND_PORT=${EXPOSE_BACKEND_PORT}
        - BACKEND_WORKDIR=${BACKEND_WORKDIR}
    networks:
      - backend-net
    # --- Hardening ---
    read_only: true
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 256M
    # -----------------
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:${EXPOSE_BACKEND_PORT}/health')"]
      interval: 3s
      timeout: 5s
      retries: 3
      start_period: 30s

networks:
  backend-net:
    driver: bridge
```
