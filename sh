docker build -t polygon-monitor .
docker run -d --name polygon-monitor polygon-monitor
docker logs -f polygon-monitor
