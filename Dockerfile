FROM ubuntu:22.04

LABEL authors="AtLarge Research"

# Update and install necessary packages
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y software-properties-common python3-pip python3-dev wget unzip curl

# Copy files
COPY opendc /opendc
COPY requirements.txt .

# Set work directory
WORKDIR /opendc

# Install Java
RUN add-apt-repository -y ppa:openjdk-r/ppa && \
    apt-get update && \
    apt-get install -y openjdk-19-jdk

# Set JAVA_HOME
RUN echo "JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))" >> /etc/environment && \
    export JAVA_HOME=$(dirname $(dirname $(readlink -f $(which javac))))

# Install Gradle
RUN wget https://services.gradle.org/distributions/gradle-8.4-bin.zip -P /tmp && \
    unzip -d /opt/gradle /tmp/gradle-8.4-bin.zip && \
    rm /tmp/gradle-8.4-bin.zip && \
    chmod +x /opt/gradle/gradle-8.4/bin/gradle

# Set Gradle environment
ENV GRADLE_HOME=/opt/gradle/gradle-8.4
ENV PATH=$PATH:$GRADLE_HOME/bin

# Install Python packages
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Run gradle init
RUN gradle init

# Build the project
RUN gradle build --no-daemon

# Keep the container running
CMD ["tail", "-f", "/dev/null"]


