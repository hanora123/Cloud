#!/usr/bin/env python3

import os
import subprocess
import json
from pathlib import Path

class DockerManager:
    """Class to manage Docker operations."""
    
    def __init__(self):
        """Initialize the Docker Manager."""
        # Check if Docker is installed
        try:
            subprocess.run(["docker", "--version"], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("Warning: Docker does not appear to be installed or running.")
            print("Some features may not work correctly.")
    
    def create_dockerfile(self):
        """Create a Dockerfile based on user input."""
        print("\n===== Create Dockerfile =====")
        
        # Get save path
        save_path = input("Enter path to save the Dockerfile (default: current directory): ") or "."
        save_path = os.path.expanduser(save_path)
        
        if not os.path.exists(save_path):
            create_dir = input(f"Directory '{save_path}' does not exist. Create it? (y/n): ").lower()
            if create_dir == 'y':
                try:
                    os.makedirs(save_path, exist_ok=True)
                except Exception as e:
                    print(f"Error creating directory: {e}")
                    return
            else:
                return
        
        dockerfile_path = os.path.join(save_path, "Dockerfile")
        
        # Check if file exists
        if os.path.exists(dockerfile_path):
            overwrite = input(f"Dockerfile already exists at '{dockerfile_path}'. Overwrite? (y/n): ").lower()
            if overwrite != 'y':
                return
        
        # Get Dockerfile contents
        print("\nEnter Dockerfile contents (type 'EOF' on a new line when finished):")
        lines = []
        while True:
            line = input()
            if line == "EOF":
                break
            lines.append(line)
        
        # Write to file
        try:
            with open(dockerfile_path, 'w') as f:
                f.write('\n'.join(lines))
            print(f"\nDockerfile created successfully at: {dockerfile_path}")
        except Exception as e:
            print(f"Error writing Dockerfile: {e}")
    
    def build_docker_image(self):
        """Build a Docker image from a Dockerfile."""
        print("\n===== Build Docker Image =====")
        
        # Get Dockerfile path
        dockerfile_dir = input("Enter directory containing the Dockerfile: ")
        dockerfile_dir = os.path.expanduser(dockerfile_dir)
        
        if not os.path.exists(os.path.join(dockerfile_dir, "Dockerfile")):
            print(f"Error: No Dockerfile found in '{dockerfile_dir}'")
            return
        
        # Get image name and tag
        image_name = input("Enter image name: ")
        image_tag = input("Enter image tag (default: latest): ") or "latest"
        
        # Build the image
        try:
            cmd = ["docker", "build", "-t", f"{image_name}:{image_tag}", dockerfile_dir]
            print(f"\nRunning: {' '.join(cmd)}")
            
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Stream the output
            for line in process.stdout:
                print(line, end='')
            
            process.wait()
            
            if process.returncode == 0:
                print(f"\nDocker image '{image_name}:{image_tag}' built successfully.")
            else:
                print(f"\nError building Docker image. Exit code: {process.returncode}")
                
        except Exception as e:
            print(f"Error building Docker image: {e}")
    
    def list_docker_images(self):
        """List all Docker images on the system."""
        print("\n===== Docker Images =====")
        
        try:
            result = subprocess.run(
                ["docker", "images"], 
                check=True, 
                capture_output=True, 
                text=True
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error listing Docker images: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
    
    def list_running_containers(self):
        """List all running Docker containers."""
        print("\n===== Running Containers =====")
        
        try:
            result = subprocess.run(
                ["docker", "ps"], 
                check=True, 
                capture_output=True, 
                text=True
            )
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            print(f"Error listing running containers: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
    
    def stop_container(self):
        """Stop a specific Docker container."""
        print("\n===== Stop Container =====")
        
        # List running containers first
        try:
            result = subprocess.run(
                ["docker", "ps"], 
                check=True, 
                capture_output=True, 
                text=True
            )
            print(result.stdout)
            
            if "CONTAINER ID" not in result.stdout:
                print("No running containers found.")
                return
            
            container_id = input("Enter container ID or name to stop: ")
            
            if not container_id:
                print("No container ID provided.")
                return
            
            # Stop the container
            stop_result = subprocess.run(
                ["docker", "stop", container_id], 
                check=True, 
                capture_output=True, 
                text=True
            )
            
            print(f"Container {container_id} stopped successfully.")
            
        except subprocess.CalledProcessError as e:
            print(f"Error stopping container: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
    
    def search_local_image(self):
        """Search for a Docker image locally."""
        print("\n===== Search Local Docker Image =====")
        
        image_name = input("Enter image name/tag to search for: ")
        
        if not image_name:
            print("No image name provided.")
            return
        
        try:
            result = subprocess.run(
                ["docker", "images", image_name], 
                check=True, 
                capture_output=True, 
                text=True
            )
            
            if "REPOSITORY" in result.stdout:
                print(result.stdout)
            else:
                print(f"No local images found matching '{image_name}'")
                
        except subprocess.CalledProcessError as e:
            print(f"Error searching for local image: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
    
    def search_dockerhub_image(self):
        """Search for a Docker image on DockerHub."""
        print("\n===== Search DockerHub =====")
        
        image_name = input("Enter image name to search for on DockerHub: ")
        
        if not image_name:
            print("No image name provided.")
            return
        
        try:
            result = subprocess.run(
                ["docker", "search", image_name], 
                check=True, 
                capture_output=True, 
                text=True
            )
            
            print(result.stdout)
                
        except subprocess.CalledProcessError as e:
            print(f"Error searching DockerHub: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
    
    def pull_docker_image(self):
        """Pull a Docker image from DockerHub."""
        print("\n===== Pull Docker Image =====")
        
        image_name = input("Enter image name to pull from DockerHub: ")
        
        if not image_name:
            print("No image name provided.")
            return
        
        # Check if tag is specified
        if ":" not in image_name:
            tag = input("Enter tag (default: latest): ") or "latest"
            image_name = f"{image_name}:{tag}"
        
        try:
            print(f"Pulling image: {image_name}")
            
            process = subprocess.Popen(
                ["docker", "pull", image_name], 
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Stream the output
            for line in process.stdout:
                print(line, end='')
            
            process.wait()
            
            if process.returncode == 0:
                print(f"\nDocker image '{image_name}' pulled successfully.")
            else:
                print(f"\nError pulling Docker image. Exit code: {process.returncode}")
                
        except Exception as e:
            print(f"Error pulling Docker image: {e}")