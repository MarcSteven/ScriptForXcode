import os
import subprocess
import re
import logging
import schedule
import time
import requests
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# Configure logging
log_file = os.path.expanduser('~/cocoapods_checker.log')
logger = logging.getLogger('CocoaPodsChecker')
logger.setLevel(logging.INFO)

# Create and configure file handler
file_handler = logging.FileHandler(log_file, encoding='utf-8')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Create and configure stream handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Clear existing handlers and add new ones
logger.handlers = []
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class CocoaPodsChecker:
    """Class to check, update, and clean CocoaPods dependencies."""

    def __init__(self, project_dir: str):
        self.project_dir = os.path.expanduser(project_dir)
        self.podfile = os.path.join(self.project_dir, 'Podfile')
        self.podfile_lock = os.path.join(self.project_dir, 'Podfile.lock')
        self.api_base_url = 'https://trunk.cocoapods.org/api/v1/pods'

    def check_pod_command(self) -> bool:
        """Verify if CocoaPods is installed."""
        try:
            result = subprocess.run(['pod', '--version'], capture_output=True, text=True, check=True)
            logger.info(f"CocoaPods version: {result.stdout.strip()}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"CocoaPods not installed or error occurred: {e}")
            return False

    def read_podfile(self) -> set:
        """Read pod names from Podfile."""
        pod_names = set()
        try:
            if not os.path.exists(self.podfile):
                logger.error(f"Podfile not found at {self.podfile}")
                return pod_names
            with open(self.podfile, 'r', encoding='utf-8') as f:
                content = f.read()
                # Match pod declarations (e.g., pod 'Alamofire')
                matches = re.findall(r"^\s*pod\s*['\"]([^'\"]+)['\"]", content, re.MULTILINE)
                pod_names.update(matches)
                logger.info(f"Found {len(pod_names)} pods in Podfile: {', '.join(pod_names)}")
            return pod_names
        except Exception as e:
            logger.error(f"Error reading Podfile: {e}")
            return pod_names

    def read_podfile_lock(self) -> Dict[str, str]:
        """Read installed pod versions from Podfile.lock."""
        installed_pods = {}
        try:
            if not os.path.exists(self.podfile_lock):
                logger.error(f"Podfile.lock not found at {self.podfile_lock}")
                return installed_pods
            with open(self.podfile_lock, 'r', encoding='utf-8') as f:
                content = f.read()
                matches = re.findall(r'^\s*-\s*([^\s(]+)\s*\(([\d.]+)\)', content, re.MULTILINE)
                for pod_name, version in matches:
                    installed_pods[pod_name] = version
                    logger.info(f"Found installed pod: {pod_name} ({version})")
            return installed_pods
        except Exception as e:
            logger.error(f"Error reading Podfile.lock: {e}")
            return installed_pods

    def check_latest_versions(self, pods: Dict[str, str]) -> List[Tuple[str, str, str]]:
        """Check for the latest versions of pods using pod outdated and API."""
        outdated_pods = []
        try:
            os.chdir(self.project_dir)
            result = subprocess.run(['pod', 'outdated'], capture_output=True, text=True, check=True)
            outdated_output = result.stdout
            for line in outdated_output.splitlines():
                match = re.match(r'-\s*([^\s]+)\s*([\d.]+)\s*->\s*([\d.]+)', line)
                if match:
                    pod_name, current_version, latest_version = match.groups()
                    outdated_pods.append((pod_name, current_version, latest_version))
                    logger.info(f"Outdated pod: {pod_name} ({current_version} -> {latest_version})")

            for pod_name, current_version in pods.items():
                if not any(pod[0] == pod_name for pod in outdated_pods):
                    try:
                        response = requests.get(f"{self.api_base_url}/{pod_name}", timeout=5)
                        if response.status_code == 200:
                            latest_version = response.json().get('version', current_version)
                            if latest_version != current_version:
                                outdated_pods.append((pod_name, current_version, latest_version))
                                logger.info(f"API found outdated pod: {pod_name} ({current_version} -> {latest_version})")
                            else:
                                logger.info(f"Pod up-to-date: {pod_name} ({current_version})")
                    except requests.RequestException as e:
                        logger.error(f"API error for {pod_name}: {e}")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error running pod outdated: {e}")
        return outdated_pods

    def update_pods(self, outdated_pods: List[Tuple[str, str, str]], confirm: bool = True):
        """Update outdated pods with user confirmation."""
        if not outdated_pods:
            logger.info("No outdated pods to update")
            print("No outdated pods to update.")
            return
        try:
            print("\nOutdated Pods to Update:")
            print("=" * 80)
            print(f"{'Pod Name':<30} {'Current Version':<20} {'Latest Version':<20}")
            print("-" * 80)
            for pod_name, current_version, latest_version in outdated_pods:
                print(f"{pod_name:<30} {current_version:<20} {latest_version:<20}")
            if confirm:
                response = input("\nUpdate these pods (y/n)? ").strip().lower()
                if response != 'y':
                    logger.info("Pod update cancelled by user")
                    print("Update cancelled.")
                    return
            os.chdir(self.project_dir)
            for pod_name, _, _ in outdated_pods:
                logger.info(f"Updating pod: {pod_name}")
                result = subprocess.run(['pod', 'update', pod_name], capture_output=True, text=True)
                if result.returncode == 0:
                    logger.info(f"Successfully updated {pod_name}")
                    print(f"Updated {pod_name}")
                else:
                    logger.error(f"Failed to update {pod_name}: {result.stderr}")
                    print(f"Failed to update {pod_name}: {result.stderr}")
        except Exception as e:
            logger.error(f"Error during pod update: {e}")
            print(f"Error updating pods: {e}")

    def remove_unrelated_pods(self, installed_pods: Dict[str, str], confirm: bool = True):
        """Remove pods not specified in Podfile."""
        try:
            podfile_pods = self.read_podfile()
            unrelated_pods = [pod for pod in installed_pods if pod not in podfile_pods]
            if not unrelated_pods:
                logger.info("No unrelated pods found")
                print("No unrelated pods found.")
                return
            print("\nUnrelated Pods in Podfile.lock:")
            print("=" * 80)
            print(f"{'Pod Name':<30} {'Version':<20}")
            print("-" * 80)
            for pod in unrelated_pods:
                print(f"{pod:<30} {installed_pods[pod]:<20}")
            if confirm:
                response = input("\nRemove these unrelated pods (y/n)? ").strip().lower()
                if response != 'y':
                    logger.info("Unrelated pod removal cancelled by user")
                    print("Removal cancelled.")
                    return
            os.chdir(self.project_dir)
            result = subprocess.run(['pod', 'install'], capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("Successfully removed unrelated pods via pod install")
                print("Unrelated pods removed.")
            else:
                logger.error(f"Failed to remove unrelated pods: {result.stderr}")
                print(f"Failed to remove unrelated pods: {result.stderr}")
        except Exception as e:
            logger.error(f"Error removing unrelated pods: {e}")
            print(f"Error removing unrelated pods: {e}")

    def print_pods_status(self, installed_pods: Dict[str, str], outdated_pods: List[Tuple[str, str, str]]):
        """Print status of installed and outdated pods."""
        if not installed_pods:
            print("No pods found in Podfile.lock.")
            logger.info("No pods found in Podfile.lock")
            return
        print("\nCocoaPods Dependency Status:")
        print("=" * 80)
        print(f"{'Pod Name':<30} {'Installed Version':<20} {'Latest Version':<20} {'Status':<15}")
        print("-" * 80)
        for pod_name, current_version in installed_pods.items():
            latest_version = next((pod[2] for pod in outdated_pods if pod[0] == pod_name), current_version)
            status = "Up-to-date" if current_version == latest_version else "Outdated"
            print(f"{pod_name:<30} {current_version:<20} {latest_version:<20} {status:<15}")
            logger.info(f"Pod status: {pod_name} ({current_version} -> {latest_version}, {status})")
        print(f"\nCheck {log_file} for details.")

def check_cocoapods():
    """Run CocoaPods dependency check, update, and cleanup."""
    project_dir = '~/Desktop/check_gmail'  # Adjust to your project directory
    checker = CocoaPodsChecker(project_dir)
    if not checker.check_pod_command():
        print("CocoaPods not installed. Install with 'sudo gem install cocoapods' or 'brew install cocoapods'.")
        logger.error("CocoaPods not installed")
        return

    installed_pods = checker.read_podfile_lock()
    outdated_pods = checker.check_latest_versions(installed_pods)
    checker.print_pods_status(installed_pods, outdated_pods)
    checker.update_pods(outdated_pods, confirm=True)
    checker.remove_unrelated_pods(installed_pods, confirm=True)

def main():
    """Main function to schedule and run CocoaPods checks."""
    try:
        logger.info("Starting CocoaPods checker script")
        print("Starting CocoaPods dependency check...")
        # Schedule checks every 3 hours
        schedule.every(3).hours.do(check_cocoapods)
        # Run first check immediately
        check_cocoapods()
        # Keep script running for scheduled tasks
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Script stopped by user")
        print("Script stopped by user")
    except Exception as e:
        logger.error(f"Script error: {e}")
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
