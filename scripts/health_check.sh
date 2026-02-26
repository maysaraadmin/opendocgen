#!/bin/bash

# OpenDocGen Health Check Script
echo "🏥 Checking OpenDocGen service health..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check service health
check_service() {
    local service_name=$1
    local url=$2
    local expected_status=${3:-200}
    
    echo -n "🔍 Checking $service_name... "
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "$expected_status"; then
        echo -e "${GREEN}✅ Healthy${NC}"
        return 0
    else
        echo -e "${RED}❌ Unhealthy${NC}"
        return 1
    fi
}

# Function to check if port is open
check_port() {
    local service_name=$1
    local port=$2
    local host=${3:-localhost}
    
    echo -n "🔍 Checking $service_name port $port... "
    
    if nc -z "$host" "$port" 2>/dev/null; then
        echo -e "${GREEN}✅ Open${NC}"
        return 0
    else
        echo -e "${RED}❌ Closed${NC}"
        return 1
    fi
}

# Check Docker services
echo "🐳 Checking Docker services..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running${NC}"
    exit 1
fi

# Check individual services
services_up=0
total_services=0

# OpenDocGen API
total_services=$((total_services + 1))
if check_service "OpenDocGen API" "http://localhost:8000/health"; then
    services_up=$((services_up + 1))
fi

# Ollama
total_services=$((total_services + 1))
if check_port "Ollama" 11434; then
    services_up=$((services_up + 1))
fi

# SearXNG (optional)
total_services=$((total_services + 1))
if check_service "SearXNG" "http://localhost:8080"; then
    services_up=$((services_up + 1))
else
    echo -e "${YELLOW}⚠️  SearXNG not running (optional)${NC}"
    total_services=$((total_services - 1))
fi

# Browserless (optional)
total_services=$((total_services + 1))
if check_port "Browserless" 3000; then
    services_up=$((services_up + 1))
else
    echo -e "${YELLOW}⚠️  Browserless not running (optional)${NC}"
    total_services=$((total_services - 1))
fi

# ChromaDB (optional)
total_services=$((total_services + 1))
if check_port "ChromaDB" 8001; then
    services_up=$((services_up + 1))
else
    echo -e "${YELLOW}⚠️  ChromaDB not running (optional)${NC}"
    total_services=$((total_services - 1))
fi

# Summary
echo ""
echo "📊 Health Check Summary:"
echo "   Services up: $services_up/$total_services"

if [ $services_up -eq $total_services ]; then
    echo -e "${GREEN}✅ All services are healthy!${NC}"
    echo ""
    echo "🌐 Access points:"
    echo "   - OpenDocGen API: http://localhost:8000"
    echo "   - API Docs: http://localhost:8000/docs"
    echo "   - Ollama: http://localhost:11434"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some services are not running${NC}"
    echo ""
    echo "🔧 Troubleshooting:"
    echo "   - Run 'make docker-logs' to check service logs"
    echo "   - Run 'make docker-down && make docker-up' to restart services"
    exit 1
fi
