# Docker-Metrics-Prome-cAdvisor-Grafana
Monitoring Docker Containers using Docker stats, Prometheus and cAdvisor, Grafana

Pre-requireties :

1) Docker install and 
2) Docker compose install

To configure the Docker daemon as a Prometheus target, you need to specify the metrics-address. The best way to do this is via the daemon.json, which is located at one of the following locations by default. If the file does not exist, create it.

Go to root
Linux/ ubuntu : vi /etc/docker/daemon.json

Add this content in that daemon.json file 

{
  "metrics-addr" : "127.0.0.1:9323"
}

Once download the files in your locally open the prometheus.yml inside just edit the ip address of your server 

For an Example:

- job_name: docker
    scrape_interval: 5s
    static_configs:
    - targets:
      - 175.41.161.60:9323
     
Next Step: Restart the docker using this command 

sudo systemctl restart docker

Next step:

docker-compose up -d

Viewing the Docker Metrics shows we can view the docker metrics:
http://<IP_ADDRESS>:9323/metrics


Viewing the Prometheus Web Interface using the correct port number:

http://<IP_ADDRESS>:9090/

In this above URL check the status in Status in benner and Targets

Viewing the cAdvisor Web Interface using the correct port number:                           http://<IP_ADDRESS>:8080/docker/nginx/

For Grafana dashBoard configure :
http://<IP_ADDRESS>:3000/

Data Source : Prometheus 

In that give that Prometheus IP address then click and test&save 

Next step open the dashboard file 'docker- Prometheus Dash Board.json'

Copy the content and import to the dashboard and select data source as Prometheus then click import it will show all the usage 

Next step :

**Docker metrics query to create a dash board in Grafana :**

engine_daemon_container_states_containers{state="paused"} 
engine_daemon_container_states_containers{state="running"} 
engine_daemon_container_states_containers{state="stopped"} 

Then another dashboard of 'Node Exporter DashBoard'
You can import this for detailled view 

That's it 

Thanks 
