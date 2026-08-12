FROM php@sha256:7bd5ed8988462e39498275924dc5b034fab5b8cd16819d113b311db226486de5

RUN apt-get update && apt-get install -y libpng-dev

RUN useradd -m www
RUN mkdir /app && chown www:www /app

COPY . /app

RUN chown -R www:www /app
WORKDIR /app

USER www

RUN random_value=$(head /dev/urandom | tr -dc A-Za-z0-9 | head -c 32) && \
    hashed_value=$(echo -n $random_value | sha256sum | awk '{print $1}') && \
    mv flag.txt $hashed_value

RUN chmod +x ./start.sh

CMD ["./start.sh"]
