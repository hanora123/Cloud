#main.py

import os
import sys
from vm_manager import VMManager
from docker_manager import DockerManager

def display_menu():
    """Display the main menu options."""
    print("\n===== Cloud Management System =====")
    print("1. Create Virtual Disk")
    print("2. Create Virtual Machine")
    print("3. Create Dockerfile")
    print("4. Build Docker Image")
    print("5. List Docker Images")
    print("6. List Running Containers")
    print("7. Stop Container")
    print("8. Search Local Docker Image")
    print("9. Search Image on DockerHub")
    print("10. Pull Docker Image")
    print("0. Exit")
    print("===================================")

def main():
    """Main function to run the Cloud Management System."""
    vm_manager = VMManager()
    docker_manager = DockerManager()
    
    while True:
        display_menu()
        try:
            choice = int(input("Enter your choice (0-10): "))
            
            if choice == 0:
                print("Exiting Cloud Management System. Goodbye!")
                sys.exit(0)
            elif choice == 1:
                vm_manager.create_virtual_disk()
            elif choice == 2:
                vm_manager.create_virtual_machine()
            elif choice == 3:
                docker_manager.create_dockerfile()
            elif choice == 4:
                docker_manager.build_docker_image()
            elif choice == 5:
                docker_manager.list_docker_images()
            elif choice == 6:
                docker_manager.list_running_containers()
            elif choice == 7:
                docker_manager.stop_container()
            elif choice == 8:
                docker_manager.search_local_image()
            elif choice == 9:
                docker_manager.search_dockerhub_image()
            elif choice == 10:
                docker_manager.pull_docker_image()
            else:
                print("Invalid choice. Please enter a number between 0 and 10.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()