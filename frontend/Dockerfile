# Use a lightweight base image, such as Nginx Alpine
FROM nginx:alpine

# Define a variable for the database path
ARG DATABASE

# Remove the default content of Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copy your index.html file to the default Nginx directory
COPY . /usr/share/nginx/html

# Expose port 80 to make the application available externally
EXPOSE 80

# Command to start the Nginx server in the foreground
CMD ["nginx", "-g", "daemon off;"]
