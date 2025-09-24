#!/usr/bin/env python3
"""
Digital Signage Player para Raspberry Pi
Sicoob Credisete - Sistema de Sinalização Digital

Este script é responsável por:
- Consultar a API para obter conteúdo agendado
- Exibir conteúdo em tela cheia (Chromium kiosk mode)
- Reproduzir vídeos com VLC
- Controlar hibernação via HDMI-CEC
- Aplicar rotação de tela conforme configuração
- Enviar status para a API
"""

import asyncio
import json
import logging
import os
import subprocess
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
import requests
import psutil
import signal
import sys
from pathlib import Path

# Configuration
CONFIG_FILE = "/home/pi/digital_signage_config.json"
LOG_FILE = "/home/pi/digital_signage.log"
API_BASE_URL = "http://localhost:8000/api/v1"  # Change to your API URL
DEVICE_ID = "raspberry_pi_001"  # Should be set from API

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DigitalSignagePlayer:
    def __init__(self):
        self.current_content = None
        self.current_process = None
        self.is_running = True
        self.agency_config = {}
        self.load_config()

    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    self.agency_config = json.load(f)
                logger.info(f"Configuration loaded: {self.agency_config}")
            else:
                logger.warning("Configuration file not found, using defaults")
                self.agency_config = {
                    "agency_id": 1,
                    "orientation": "horizontal",
                    "hibernation_enabled": True,
                    "hibernation_start": "18:00",
                    "hibernation_end": "08:00"
                }
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.agency_config, f, indent=2)
            logger.info("Configuration saved")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")

    def send_status_update(self, status: str, details: Dict = None):
        """Send status update to API"""
        try:
            payload = {
                "device_id": DEVICE_ID,
                "status": status,
                "last_seen": datetime.now().isoformat(),
                "details": details or {}
            }

            response = requests.post(
                f"{API_BASE_URL}/devices/status",
                json=payload,
                timeout=10
            )

            if response.status_code == 200:
                logger.info(f"Status update sent: {status}")
            else:
                logger.warning(f"Failed to send status update: {response.status_code}")

        except Exception as e:
            logger.error(f"Error sending status update: {e}")

    def get_current_schedule(self) -> List[Dict]:
        """Get current schedule from API"""
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            current_weekday = str(now.weekday())

            params = {
                "current_time": current_time,
                "current_weekday": current_weekday
            }

            response = requests.get(
                f"{API_BASE_URL}/schedules/current",
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                schedules = response.json()
                logger.info(f"Retrieved {len(schedules)} active schedules")
                return schedules
            else:
                logger.warning(f"Failed to get schedules: {response.status_code}")
                return []

        except Exception as e:
            logger.error(f"Error getting schedules: {e}")
            return []

    def apply_screen_rotation(self, orientation: str):
        """Apply screen rotation"""
        try:
            config_file = "/boot/config.txt"

            # Read current config
            with open(config_file, 'r') as f:
                lines = f.readlines()

            # Remove existing display rotation settings
            lines = [line for line in lines if not line.startswith('display_rotate')]

            # Add new rotation setting
            if orientation == "vertical":
                lines.append("display_rotate=1\n")  # 90 degrees
            elif orientation == "horizontal":
                lines.append("display_rotate=0\n")  # Normal

            # Write back config
            with open(config_file, 'w') as f:
                f.writelines(lines)

            logger.info(f"Screen rotation set to: {orientation}")

        except Exception as e:
            logger.error(f"Error setting screen rotation: {e}")

    def start_chromium_kiosk(self, url: str):
        """Start Chromium in kiosk mode"""
        try:
            self.stop_current_process()

            logger.info(f"Starting Chromium kiosk: {url}")

            self.current_process = subprocess.Popen([
                "chromium-browser",
                "--kiosk",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-software-rasterizer",
                "--disable-dev-shm-usage",
                "--disable-extensions",
                "--disable-plugins",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-default-apps",
                "--disable-translate",
                "--disable-background-timer-throttling",
                "--disable-renderer-backgrounding",
                "--disable-backgrounding-occluded-windows",
                "--disable-ipc-flooding-protection",
                url
            ])

            logger.info("Chromium kiosk started")

        except Exception as e:
            logger.error(f"Error starting Chromium: {e}")

    def start_vlc_player(self, video_url: str):
        """Start VLC player for video content"""
        try:
            self.stop_current_process()

            logger.info(f"Starting VLC player: {video_url}")

            # Check if it's a local file or URL
            if video_url.startswith('http'):
                self.current_process = subprocess.Popen([
                    "vlc",
                    "--fullscreen",
                    "--no-video-title-show",
                    "--no-osd",
                    video_url
                ])
            else:
                # Local file
                self.current_process = subprocess.Popen([
                    "vlc",
                    "--fullscreen",
                    "--no-video-title-show",
                    "--no-osd",
                    video_url
                ])

            logger.info("VLC player started")

        except Exception as e:
            logger.error(f"Error starting VLC: {e}")

    def start_image_viewer(self, image_url: str):
        """Start image viewer for static images"""
        try:
            self.stop_current_process()

            logger.info(f"Starting image viewer: {image_url}")

            # Use feh for image display
            self.current_process = subprocess.Popen([
                "feh",
                "--fullscreen",
                "--hide-pointer",
                "--no-menus",
                "--auto-zoom",
                image_url
            ])

            logger.info("Image viewer started")

        except Exception as e:
            logger.error(f"Error starting image viewer: {e}")

    def stop_current_process(self):
        """Stop currently running process"""
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=5)
                logger.info("Current process stopped")
            except subprocess.TimeoutExpired:
                self.current_process.kill()
                logger.warning("Process killed forcefully")
            except Exception as e:
                logger.error(f"Error stopping process: {e}")

        self.current_process = None

    def should_hibernate(self) -> bool:
        """Check if device should hibernate"""
        if not self.agency_config.get("hibernation_enabled", False):
            return False

        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M")

            start_time = self.agency_config.get("hibernation_start", "18:00")
            end_time = self.agency_config.get("hibernation_end", "08:00")

            # Convert to minutes for comparison
            now_minutes = now.hour * 60 + now.minute
            start_minutes = int(start_time.split(':')[0]) * 60 + int(start_time.split(':')[1])
            end_minutes = int(end_time.split(':')[0]) * 60 + int(end_time.split(':')[1])

            # Handle overnight hibernation (e.g., 18:00 to 08:00)
            if start_minutes <= end_minutes:
                # Same day hibernation
                return start_minutes <= now_minutes <= end_minutes
            else:
                # Overnight hibernation
                return now_minutes >= start_minutes or now_minutes <= end_minutes

        except Exception as e:
            logger.error(f"Error checking hibernation: {e}")
            return False

    def hibernate_tv(self):
        """Put TV in standby mode using HDMI-CEC"""
        try:
            logger.info("Sending TV to standby")
            subprocess.run(["echo", "standby 0", "|", "cec-client", "-s"], check=True)
            logger.info("TV sent to standby")
        except Exception as e:
            logger.error(f"Error sending TV to standby: {e}")

    def wake_tv(self):
        """Wake up TV from standby using HDMI-CEC"""
        try:
            logger.info("Waking up TV")
            subprocess.run(["echo", "on 0", "|", "cec-client", "-s"], check=True)
            logger.info("TV wake command sent")
        except Exception as e:
            logger.error(f"Error waking up TV: {e}")

    def get_system_info(self) -> Dict:
        """Get system information"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_usage": psutil.disk_usage('/').percent,
                "temperature": self.get_cpu_temperature(),
                "uptime": self.get_uptime()
            }
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {}

    def get_cpu_temperature(self) -> float:
        """Get CPU temperature"""
        try:
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = float(f.read()) / 1000
            return round(temp, 1)
        except:
            return 0.0

    def get_uptime(self) -> str:
        """Get system uptime"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
                uptime = timedelta(seconds=uptime_seconds)
                return str(uptime).split('.')[0]  # Remove microseconds
        except:
            return "Unknown"

    def play_content(self, content: Dict):
        """Play specific content"""
        try:
            content_type = content.get("type", "link")
            url = content.get("url", "")

            logger.info(f"Playing content: {content.get('title')} ({content_type})")

            if content_type == "link":
                self.start_chromium_kiosk(url)
            elif content_type == "video":
                self.start_vlc_player(url)
            elif content_type == "image":
                self.start_image_viewer(url)
            else:
                logger.warning(f"Unknown content type: {content_type}")

            self.current_content = content

        except Exception as e:
            logger.error(f"Error playing content: {e}")

    async def main_loop(self):
        """Main application loop"""
        logger.info("Starting Digital Signage Player")

        # Send initial status
        self.send_status_update("online", self.get_system_info())

        last_schedule_check = 0
        last_status_update = 0
        last_hibernation_check = 0

        try:
            while self.is_running:
                current_time = time.time()

                # Check for new schedules every 30 seconds
                if current_time - last_schedule_check > 30:
                    schedules = self.get_current_schedule()

                    if schedules:
                        # Find highest priority schedule
                        best_schedule = max(schedules, key=lambda x: x.get("priority", 1))
                        content_id = best_schedule.get("content_id")

                        # Check if we need to change content
                        if not self.current_content or self.current_content.get("id") != content_id:
                            # Get content details
                            try:
                                response = requests.get(f"{API_BASE_URL}/contents/{content_id}")
                                if response.status_code == 200:
                                    content = response.json()
                                    self.play_content(content)
                            except Exception as e:
                                logger.error(f"Error getting content details: {e}")
                    else:
                        # No active schedules, show default content or blank screen
                        if self.current_content:
                            self.stop_current_process()
                            self.current_content = None

                    last_schedule_check = current_time

                # Send status update every 5 minutes
                if current_time - last_status_update > 300:
                    self.send_status_update("online", self.get_system_info())
                    last_status_update = current_time

                # Check hibernation every minute
                if current_time - last_hibernation_check > 60:
                    if self.should_hibernate():
                        if self.current_content:
                            self.stop_current_process()
                            self.current_content = None
                        self.hibernate_tv()
                        logger.info("TV hibernated")
                    else:
                        self.wake_tv()
                        logger.info("TV active")

                    last_hibernation_check = current_time

                await asyncio.sleep(1)

        except KeyboardInterrupt:
            logger.info("Received shutdown signal")
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup before shutdown"""
        logger.info("Cleaning up...")

        # Stop current process
        self.stop_current_process()

        # Wake TV if hibernated
        self.wake_tv()

        # Send final status
        self.send_status_update("offline")

        logger.info("Cleanup completed")

    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}")
        self.is_running = False

def main():
    """Main function"""
    player = DigitalSignagePlayer()

    # Register signal handlers
    signal.signal(signal.SIGTERM, player.signal_handler)
    signal.signal(signal.SIGINT, player.signal_handler)

    # Run main loop
    try:
        asyncio.run(player.main_loop())
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
    except Exception as e:
        logger.error(f"Application error: {e}")
    finally:
        player.cleanup()

if __name__ == "__main__":
    main()
