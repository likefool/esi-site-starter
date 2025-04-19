FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY public/ ./public/
COPY *.py ./
COPY *.sh ./
RUN chmod +x update_content.sh

# Setup cron job for update_content.sh
RUN echo "0 */6 * * * /app/update_content.sh >> /var/log/cron.log 2>&1" > /etc/cron.d/update-content
RUN chmod 0644 /etc/cron.d/update-content
RUN crontab /etc/cron.d/update-content

# Expose the port the app runs on
EXPOSE 18000

# Command to run the startup script
ENTRYPOINT ["/app/startup.sh"]