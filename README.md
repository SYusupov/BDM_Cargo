# BDM_Cargo
A Collaborative Project for Big Data Management

## Getting Started
Follow the instructions below to set up the Java application and Airflow DAGs for this project.

### Java Application Setup
1. **Configure application properties**:
    - Open `cargo/src/main/resources/application.properties`
    - Update `output.directoryPath` with the directory where you want to store the collected data files

2. **Build and run the application**:
    - In the terminal, navigate to the project root and run `mvn clean install`
    - Execute the JAR file by running:
      ```
      java -jar YOUR_PATH/target/cargo-0.0.1-SNAPSHOT.jar
      ```
      Replace `YOUR_PATH` with the path to the `target` folder in your project directory

### Airflow DAGs Setup
*Note: These instructions assume that you have Airflow installed in a Docker container.*

1. **Update IP address in DAG files**:
    - Open `city_data_dag.py` and `gas_data_dag.py` in the `Airflow_DAG` folder
    - Replace `10.192.139.60` with your own IP address

2. **Copy files to the Docker container**:
    - Copy all files from the `Airflow_DAG` folder to the `/dags` folder in the connected directory of your Docker container

3. **Restart Airflow and activate DAGs**:
    - Restart your Airflow instance
    - Open your browser and go to 'http://localhost:8080/'
    - Activate all the available DAGs

### HDFS Setup
1. Install Hadoop in standalone mode (instructions for Ubuntu 20.04: https://www.digitalocean.com/community/tutorials/how-to-install-hadoop-in-stand-alone-mode-on-ubuntu-20-04), configure Hadoop (https://medium.com/@festusmorumbasi/installing-hadoop-on-ubuntu-20-04-4610b6e0391e)
2. Install the latest version of PyArrow library as explained here: https://arrow.apache.org/docs/python/install.html#using-pip
3. Run each python file in /HDFS
