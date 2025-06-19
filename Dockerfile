# Use the official Airflow image as base
FROM apache/airflow:2.9.0-python3.9

# Switch to root to install dependencies
USER root

# Install system dependencies (e.g. Java for Spark)
RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    python3-dev \
    gcc \
    wget \
    curl \
    unzip \
    libsasl2-dev \
    libffi-dev \
    libssl-dev \
    && apt-get clean

# Set JAVA_HOME for Spark
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Install Spark (optional if you run Spark jobs separately)
ENV SPARK_VERSION=3.4.1
ENV HADOOP_VERSION=3

RUN curl -L https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz | \
    tar -xz -C /opt/ && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /opt/spark

ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Install Python dependencies
COPY requirements.txt /
RUN pip install --upgrade pip && pip install -r /requirements.txt

# Create Airflow directories and copy code
COPY ./dags /opt/airflow/dags
COPY ./scripts /opt/airflow/scripts
COPY ./spark_jobs /opt/airflow/spark_jobs
COPY ./utils /opt/airflow/utils
COPY ./configs /opt/airflow/configs
COPY ./data /opt/airflow/data

# Set correct permissions
RUN chown -R airflow: /opt/airflow

# Switch back to airflow user
USER airflow