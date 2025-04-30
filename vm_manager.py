#!/usr/bin/env python3

import os
import subprocess
import json
from pathlib import Path

class VMManager:
    """Class to manage QEMU virtual machines and disks."""
    
    def __init__(self):
        """Initialize the VM Manager."""
        self.vm_dir = os.path.expanduser("~/vm_images")
        os.makedirs(self.vm_dir, exist_ok=True)
        self.disk_inventory_file = os.path.join(self.vm_dir, "disk_inventory.json")
        self.load_disk_inventory()
    
    def load_disk_inventory(self):
        """Load the disk inventory from file."""
        if os.path.exists(self.disk_inventory_file):
            with open(self.disk_inventory_file, 'r') as f:
                try:
                    self.disk_inventory = json.load(f)
                except json.JSONDecodeError:
                    self.disk_inventory = []
        else:
            self.disk_inventory = []
    
    def save_disk_inventory(self):
        """Save the disk inventory to file."""
        with open(self.disk_inventory_file, 'w') as f:
            json.dump(self.disk_inventory, f, indent=4)
    
    def create_virtual_disk(self):
        """Create a virtual disk based on user input."""
        print("\n===== Create Virtual Disk =====")
        
        # Get disk details from user
        disk_name = input("Enter disk name: ")
        disk_path = os.path.join(self.vm_dir, f"{disk_name}.qcow2")
        
        if os.path.exists(disk_path):
            print(f"Error: Disk with name '{disk_name}' already exists.")
            return
        
        # Get disk format
        print("\nAvailable disk formats:")
        print("1. qcow2 (QEMU Copy-On-Write v2)")
        print("2. raw")
        print("3. vdi (VirtualBox Disk Image)")
        print("4. vmdk (VMware Disk)")
        
        format_choice = input("Select disk format (1-4, default: 1): ") or "1"
        format_map = {"1": "qcow2", "2": "raw", "3": "vdi", "4": "vmdk"}
        
        if format_choice not in format_map:
            print("Invalid choice. Using qcow2 format.")
            disk_format = "qcow2"
        else:
            disk_format = format_map[format_choice]
        
        # Get disk size
        size = input("Enter disk size (e.g., 10G, 512M): ")
        
        # Create the disk using qemu-img
        try:
            cmd = ["qemu-img", "create", "-f", disk_format, disk_path, size]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            # Add to inventory
            disk_info = {
                "name": disk_name,
                "path": disk_path,
                "format": disk_format,
                "size": size
            }
            self.disk_inventory.append(disk_info)
            self.save_disk_inventory()
            
            print(f"\nVirtual disk created successfully:")
            print(f"Name: {disk_name}")
            print(f"Path: {disk_path}")
            print(f"Format: {disk_format}")
            print(f"Size: {size}")
            
        except subprocess.CalledProcessError as e:
            print(f"Error creating disk: {e}")
            print(f"Command output: {e.stderr}")
    
    def create_virtual_machine(self):
        """Create a virtual machine based on user input."""
        print("\n===== Create Virtual Machine =====")
        
        if not self.disk_inventory:
            print("No virtual disks available. Please create a virtual disk first.")
            return
        
        # Get VM details from user
        vm_name = input("Enter VM name: ")
        
        # Select a disk
        print("\nAvailable disks:")
        for i, disk in enumerate(self.disk_inventory):
            print(f"{i+1}. {disk['name']} ({disk['size']}, {disk['format']})")
        
        disk_choice = int(input("Select disk (number): ")) - 1
        if disk_choice < 0 or disk_choice >= len(self.disk_inventory):
            print("Invalid disk selection.")
            return
        
        selected_disk = self.disk_inventory[disk_choice]
        
        # Get VM configuration
        cpu_cores = input("Enter number of CPU cores (default: 1): ") or "1"
        memory = input("Enter memory size in MB (default: 1024): ") or "1024"
        
        # Optional: Select an ISO for installation
        use_iso = input("Do you want to use an ISO for installation? (y/n, default: n): ").lower() or "n"
        iso_path = ""
        
        if use_iso == "y":
            iso_path = input("Enter path to ISO file: ")
            if not os.path.exists(iso_path):
                print(f"Warning: ISO file '{iso_path}' does not exist.")
                return
        
        # Build the QEMU command
        qemu_cmd = ["qemu-system-x86_64"]
        qemu_cmd.extend(["-name", vm_name])
        qemu_cmd.extend(["-smp", cpu_cores])
        qemu_cmd.extend(["-m", memory])
        qemu_cmd.extend(["-drive", f"file={selected_disk['path']},format={selected_disk['format']}"])
        
        if iso_path:
            qemu_cmd.extend(["-cdrom", iso_path])
            qemu_cmd.extend(["-boot", "d"])
        
        # Add network
        qemu_cmd.extend(["-net", "nic", "-net", "user"])
        
        # Enable VGA
        qemu_cmd.extend(["-vga", "std"])
        
        # Print the command for reference
        print("\nVM Command:")
        print(" ".join(qemu_cmd))
        
        # Ask if user wants to start the VM now
        start_vm = input("\nDo you want to start the VM now? (y/n, default: y): ").lower() or "y"
        
        if start_vm == "y":
            try:
                print("\nStarting VM. Close the QEMU window to return to the Cloud Management System.")
                subprocess.run(qemu_cmd)
                print("VM session ended.")
            except subprocess.CalledProcessError as e:
                print(f"Error starting VM: {e}")
        else:
            print("\nVM configured but not started.")
            print("You can start it manually using the command above.")