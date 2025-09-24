#!/usr/bin/env python3
"""
Digital Signage Player - VERSÃO LITE
Facilita TI - Sistema de Sinalização Digital
Otimizado para Raspberry Pi OS Lite com cartão 32GB
"""

import asyncio
import json
import logging
import os
import subprocess
import time
from datetime import datetime
import requests
import signal
import sys

# Configuração
CONFIG_FILE = "/home/pi/sinalizacao_digital/config.json"
LOG_FILE = "/home/pi/sinalizacao_digital/player.log"
API_BASE_URL = "http://localhost:8000/api/v1"
DEVICE_ID = "raspberry_pi_lite"

# Configurar logging simples
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PlayerLite:
    def __init__(self):
        self.current_process = None
        self.is_running = True
        self.config = self.load_config()

    def load_config(self):
        """Carregar configuração"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            return {
                "agency_id": 1,
                "orientation": "horizontal",
                "hibernation_enabled": True,
                "hibernation_start": "18:00",
                "hibernation_end": "08:00"
            }
        except Exception as e:
            logger.error(f"Erro na configuração: {e}")
            return {}

    def send_status(self, status):
        """Enviar status para API"""
        try:
            payload = {
                "device_id": self.config.get("device_id", DEVICE_ID),
                "status": status,
                "last_seen": datetime.now().isoformat()
            }
            requests.post(
                f"{self.config.get('api_url', API_BASE_URL)}/devices/status",
                json=payload,
                timeout=5
            )
        except:
            pass  # Não falhar se API não estiver disponível

    def get_schedule(self):
        """Obter agendamento atual"""
        try:
            now = datetime.now()
            params = {
                "current_time": now.strftime("%H:%M"),
                "current_weekday": str(now.weekday())
            }
            response = requests.get(
                f"{self.config.get('api_url', API_BASE_URL)}/schedules/current",
                params=params,
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return []

    def play_content(self, content):
        """Reproduzir conteúdo"""
        self.stop_current()

        content_type = content.get("type", "link")
        url = content.get("url", "")

        logger.info(f"Reproduzindo: {content.get('title')} ({content_type})")

        try:
            if content_type == "link":
                self.current_process = subprocess.Popen([
                    "chromium-browser", "--kiosk", "--no-sandbox",
                    "--disable-gpu", "--disable-extensions", url
                ])
            elif content_type == "video":
                self.current_process = subprocess.Popen([
                    "vlc", "--fullscreen", "--no-osd", url
                ])
            elif content_type == "image":
                self.current_process = subprocess.Popen([
                    "feh", "--fullscreen", "--hide-pointer", url
                ])
        except Exception as e:
            logger.error(f"Erro ao reproduzir: {e}")

    def stop_current(self):
        """Parar processo atual"""
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=3)
            except:
                self.current_process.kill()
        self.current_process = None

    def should_hibernate(self):
        """Verificar se deve hibernar"""
        if not self.config.get("hibernation_enabled"):
            return False

        try:
            now = datetime.now().strftime("%H:%M")
            start = self.config.get("hibernation_start", "18:00")
            end = self.config.get("hibernation_end", "08:00")

            # Lógica simples de hibernação
            if start <= end:
                return start <= now <= end
            else:
                return now >= start or now <= end
        except:
            return False

    def hibernate_tv(self):
        """Hibernar TV"""
        try:
            subprocess.run(["echo", "standby 0"], input=b"", timeout=2)
        except:
            pass

    async def main_loop(self):
        """Loop principal"""
        logger.info("Iniciando Player Lite")

        self.send_status("online")

        last_check = 0

        try:
            while self.is_running:
                current_time = time.time()

                # Verificar agendamento a cada 30 segundos
                if current_time - last_check > 30:
                    schedules = self.get_schedule()

                    if schedules:
                        best = max(schedules, key=lambda x: x.get("priority", 1))
                        content_id = best.get("content_id")

                        # Buscar detalhes do conteúdo
                        try:
                            response = requests.get(
                                f"{self.config.get('api_url', API_BASE_URL)}/contents/{content_id}",
                                timeout=5
                            )
                            if response.status_code == 200:
                                content = response.json()
                                self.play_content(content)
                        except:
                            pass
                    else:
                        self.stop_current()

                    # Verificar hibernação
                    if self.should_hibernate():
                        self.stop_current()
                        self.hibernate_tv()

                    last_check = current_time

                await asyncio.sleep(1)

        except KeyboardInterrupt:
            logger.info("Desligando...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Limpeza"""
        self.stop_current()
        self.send_status("offline")
        logger.info("Limpeza concluída")

    def signal_handler(self, signum, frame):
        """Tratador de sinais"""
        self.is_running = False

def main():
    player = PlayerLite()

    signal.signal(signal.SIGTERM, player.signal_handler)
    signal.signal(signal.SIGINT, player.signal_handler)

    try:
        asyncio.run(player.main_loop())
    except KeyboardInterrupt:
        logger.info("Aplicação parada pelo usuário")
    finally:
        player.cleanup()

if __name__ == "__main__":
    main()
