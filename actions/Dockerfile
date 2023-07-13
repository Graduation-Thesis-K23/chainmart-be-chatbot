# Extend the official Rasa SDK image
FROM rasa/rasa-sdk:3.6.0

# Use subdirectory as working directory
WORKDIR /app


# Change back to root user to install dependencies
USER root



# Copy actions folder to working directory
COPY . /app/actions

# By best practices, don't run the code with root user
USER 1001

EXPOSE 5005