FROM browserless/chrome:latest

# Set environment variables
ENV PORT=3000
ENV WORKSPACE_DELETE_EXPIRED=true
ENV WORKSPACE_EXPIRE_DAYS=1
ENV MAX_CONCURRENT_SESSIONS=10
ENV ENABLE_CORS=true
ENV CORS_ALLOW_ORIGIN=*

# Expose the port
EXPOSE 3000

# Start Browserless
CMD ["start"]
