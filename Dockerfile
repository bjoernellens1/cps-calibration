# Use an official Python image with GPU support
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for the app
WORKDIR /app

# Copy the requirements.txt file if you have one
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

# Set up the local user (change UID and GID as needed)
ARG USERNAME=localuser
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} ${USERNAME} \
    && useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USERNAME} \
    && chown -R ${USERNAME}:${USERNAME} /app

# Switch to the local user
USER ${USERNAME}

# Clone the Segment Anything Model repository
RUN git clone https://github.com/facebookresearch/segment-anything.git /app/segment-anything

# Install SAM dependencies
RUN pip3 install -e /app/segment-anything

# Set the working directory to the SAM directory
WORKDIR /app/segment-anything

# Default command
CMD ["/bin/bash"]
