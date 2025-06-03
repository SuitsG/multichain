FROM ubuntu

# Evitar preguntas durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Actualizar e instalar dependencias
RUN apt update && apt upgrade
RUN apt-get update && \
    apt-get install -y wget curl unzip python3 python3-pip python3-flask python3-requests && \
    pip3 install --break-system-packages savoir && \
    rm -rf /var/lib/apt/lists/*

# Descargar e instalar MultiChain
RUN wget https://www.multichain.com/download/multichain-2.3.3.tar.gz && \
    tar -xvzf multichain-2.3.3.tar.gz && \
    cd multichain-2.3.3 && \
    mv multichaind multichain-cli multichain-util /usr/local/bin && \
    cd .. && rm -rf multichain-2.3.3 multichain-2.3.3.tar.gz

# Crear directorio de trabajo
WORKDIR /root/.multichain

# Exponer puertos necesarios
EXPOSE 8333 8332

# Comando por defecto
CMD ["tail", "-f", "/dev/null"]
