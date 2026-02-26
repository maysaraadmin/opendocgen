FROM searxng/searxng:latest

# Copy custom settings
COPY settings.yml /etc/searxng/settings.yml

# Install additional dependencies if needed
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Expose the port
EXPOSE 8080

# Set environment variables
ENV BASE_URL=http://localhost:8080/

# Start SearXNG
CMD ["searxng-run"]
