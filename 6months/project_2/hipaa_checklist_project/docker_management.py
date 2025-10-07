#!/usr/bin/env python3
"""
Docker management script for HIPAA Checklist Project
Provides easy commands for Docker operations
"""

import subprocess
import sys
import os
from pathlib import Path

class DockerManager:
    """Docker management utilities"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.compose_files = {
            'dev': 'docker-compose.dev.yml',
            'prod': 'docker-compose.yml',
            'nginx': 'docker-compose.nginx.yml'
        }
    
    def run_command(self, command, capture_output=False):
        """Run a command and return result"""
        try:
            if capture_output:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
                return result.returncode == 0, result.stdout, result.stderr
            else:
                result = subprocess.run(command, shell=True, timeout=60)
                return result.returncode == 0, "", ""
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except Exception as e:
            return False, "", str(e)
    
    def check_docker(self):
        """Check if Docker is available"""
        success, stdout, stderr = self.run_command("docker --version", capture_output=True)
        if not success:
            print(" Docker not found. Please install Docker.")
            return False
        
        success, stdout, stderr = self.run_command("docker-compose --version", capture_output=True)
        if not success:
            print(" Docker Compose not found. Please install Docker Compose.")
            return False
        
        print(" Docker and Docker Compose are available")
        return True
    
    def build_images(self, environment='dev'):
        """Build Docker images"""
        compose_file = self.compose_files.get(environment)
        if not compose_file:
            print(f" Unknown environment: {environment}")
            return False
        
        print(f" Building Docker images for {environment}...")
        command = f"docker-compose -f {compose_file} build"
        success, stdout, stderr = self.run_command(command)
        
        if success:
            print(" Images built successfully")
        else:
            print(f" Build failed: {stderr}")
        
        return success
    
    def start_services(self, environment='dev'):
        """Start Docker services"""
        compose_file = self.compose_files.get(environment)
        if not compose_file:
            print(f" Unknown environment: {environment}")
            return False
        
        print(f" Starting services for {environment}...")
        command = f"docker-compose -f {compose_file} up -d"
        success, stdout, stderr = self.run_command(command)
        
        if success:
            print(" Services started successfully")
        else:
            print(f" Start failed: {stderr}")
        
        return success
    
    def stop_services(self, environment='dev'):
        """Stop Docker services"""
        compose_file = self.compose_files.get(environment)
        if not compose_file:
            print(f" Unknown environment: {environment}")
            return False
        
        print(f" Stopping services for {environment}...")
        command = f"docker-compose -f {compose_file} down"
        success, stdout, stderr = self.run_command(command)
        
        if success:
            print(" Services stopped successfully")
        else:
            print(f" Stop failed: {stderr}")
        
        return success
    
    def restart_services(self, environment='dev'):
        """Restart Docker services"""
        print(f" Restarting services for {environment}...")
        self.stop_services(environment)
        return self.start_services(environment)
    
    def show_logs(self, environment='dev', service=None):
        """Show Docker logs"""
        compose_file = self.compose_files.get(environment)
        if not compose_file:
            print(f" Unknown environment: {environment}")
            return False
        
        if service:
            command = f"docker-compose -f {compose_file} logs -f {service}"
        else:
            command = f"docker-compose -f {compose_file} logs -f"
        
        print(f" Showing logs for {environment}...")
        success, stdout, stderr = self.run_command(command)
        return success
    
    def show_status(self, environment='dev'):
        """Show service status"""
        compose_file = self.compose_files.get(environment)
        if not compose_file:
            print(f" Unknown environment: {environment}")
            return False
        
        print(f" Service status for {environment}:")
        command = f"docker-compose -f {compose_file} ps"
        success, stdout, stderr = self.run_command(command, capture_output=True)
        
        if success:
            print(stdout)
        else:
            print(f" Status check failed: {stderr}")
        
        return success
    
    def clean_up(self):
        """Clean up Docker resources"""
        print(" Cleaning up Docker resources...")
        
        commands = [
            "docker system prune -f",
            "docker volume prune -f",
            "docker network prune -f"
        ]
        
        for command in commands:
            success, stdout, stderr = self.run_command(command)
            if success:
                print(f" {command}")
            else:
                print(f" {command}: {stderr}")
    
    def setup_development(self):
        """Set up development environment"""
        print("  Setting up development environment...")
        
        if not self.check_docker():
            return False
        
        # Build images
        if not self.build_images('dev'):
            return False
        
        # Start services
        if not self.start_services('dev'):
            return False
        
        print(" Development environment ready!")
        print(" Frontend: http://localhost:3000")
        print(" Backend: http://localhost:8000")
        print(" Nginx: http://localhost")
        
        return True
    
    def setup_production(self):
        """Set up production environment"""
        print(" Setting up production environment...")
        
        if not self.check_docker():
            return False
        
        # Build images
        if not self.build_images('prod'):
            return False
        
        # Start services
        if not self.start_services('prod'):
            return False
        
        print(" Production environment ready!")
        print(" Application: http://localhost")
        print(" Admin: http://localhost/admin")
        
        return True

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print(" Docker Management for HIPAA Checklist Project")
        print("=" * 50)
        print("Usage: python docker_management.py <command> [environment] [service]")
        print("\nCommands:")
        print("  setup-dev     - Set up development environment")
        print("  setup-prod    - Set up production environment")
        print("  start         - Start services")
        print("  stop          - Stop services")
        print("  restart       - Restart services")
        print("  logs          - Show logs")
        print("  status        - Show status")
        print("  build         - Build images")
        print("  clean         - Clean up resources")
        print("\nEnvironments: dev, prod, nginx")
        print("\nExamples:")
        print("  python docker_management.py setup-dev")
        print("  python docker_management.py start dev")
        print("  python docker_management.py logs dev backend")
        return
    
    command = sys.argv[1]
    environment = sys.argv[2] if len(sys.argv) > 2 else 'dev'
    service = sys.argv[3] if len(sys.argv) > 3 else None
    
    manager = DockerManager()
    
    if command == 'setup-dev':
        success = manager.setup_development()
    elif command == 'setup-prod':
        success = manager.setup_production()
    elif command == 'start':
        success = manager.start_services(environment)
    elif command == 'stop':
        success = manager.stop_services(environment)
    elif command == 'restart':
        success = manager.restart_services(environment)
    elif command == 'logs':
        success = manager.show_logs(environment, service)
    elif command == 'status':
        success = manager.show_status(environment)
    elif command == 'build':
        success = manager.build_images(environment)
    elif command == 'clean':
        success = manager.clean_up()
    else:
        print(f" Unknown command: {command}")
        success = False
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
