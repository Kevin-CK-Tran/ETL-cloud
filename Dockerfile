FROM apache/airflow:2.9.0-python3.9

USER root

# Fix APT sources and install system dependencies
RUN echo "deb http://deb.debian.org/debian bullseye main contrib non-free" > /etc/apt/sources.list && \
    echo "deb http://deb.debian.org/debian bullseye-updates main contrib non-free" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security bullseye-security main contrib non-free" >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        openjdk-11-jdk \
        python3-dev \
        gcc \
        wget \
        curl \
        unzip \
        libsasl2-dev \
        libffi-dev \
        libssl-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME and SPARK paths
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH
ENV SPARK_VERSION=3.4.1
ENV HADOOP_VERSION=3
ENV SPARK_HOME=/opt/spark
ENV PATH=$SPARK_HOME/bin:$PATH

# Install Spark
RUN curl -fsSL https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz | \
    tar -xz -C /opt/ && \
    mv /opt/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} $SPARK_HOME

# Copy requirements before switching user
COPY requirements.txt /requirements.txt

# Switch to airflow user before pip install
USER airflow
RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt

# Copy remaining project files
COPY ./dags /opt/airflow/dags
COPY ./scripts /opt/airflow/scripts
COPY ./spark_jobs /opt/airflow/spark_jobs
COPY ./utils /opt/airflow/utils
COPY ./configs /opt/airflow/configs
COPY ./data /opt/airflow/data