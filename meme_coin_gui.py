import pygame
import sys
from blockchain import deploy_contract
import threading
import webbrowser
import pyperclip
from solcx import install_solc, set_solc_version

# Initialize Pygame with visible window controls
pygame.init()
pygame.font.init()

# Ensure Solidity compiler is installed
try:
    install_solc('0.8.0')
    set_solc_version('0.8.0')
except Exception as e:
    print(f"Critical Error: {str(e)}")
    sys.exit(1)

# Window configuration
WIDTH, HEIGHT = 600, 650
FPS = 60

# Color palette
DARK_BLUE = (30, 50, 90)
LIGHT_BLUE = (100, 180, 240)
WHITE = (255, 255, 255)
LIGHT_GRAY = (245, 245, 245)
DARK_GRAY = (80, 80, 80)
GREEN = (50, 200, 120)
RED = (230, 80, 70)

# Fonts
title_font = pygame.font.SysFont("Arial", 28, bold=True)
label_font = pygame.font.SysFont("Arial", 22)
input_font = pygame.font.SysFont("Arial", 20)
button_font = pygame.font.SysFont("Arial", 24, bold=True)
log_font = pygame.font.SysFont("Consolas", 16)

class InputField:
    def __init__(self, x, y, width, height, label, placeholder):
        self.rect = pygame.Rect(x, y, width, height)
        self.label = label
        self.placeholder = placeholder
        self.text = ""
        self.active = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            if self.active and self.text == self.placeholder:
                self.text = ""
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return False
    
    def draw(self, surface):
        # Label
        label_surf = label_font.render(self.label, True, DARK_GRAY)
        surface.blit(label_surf, (self.rect.x, self.rect.y - 25))
        
        # Input box
        pygame.draw.rect(surface, WHITE, self.rect, border_radius=4)
        pygame.draw.rect(surface, LIGHT_BLUE if self.active else (200, 200, 200), self.rect, 2, border_radius=4)
        
        # Text
        display_text = self.text if self.text else self.placeholder
        text_color = DARK_GRAY if self.text else (150, 150, 150)
        text_surf = input_font.render(display_text, True, text_color)
        surface.blit(text_surf, (self.rect.x + 10, self.rect.centery - text_surf.get_height()//2))

class StatusBox:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 200, 30)
        self.connected = True
    
    def draw(self, surface):
        status_text = "Connected to Sepolia Testnet"
        color = GREEN if self.connected else RED
        pygame.draw.circle(surface, color, (self.rect.x + 10, self.rect.centery), 6)
        text_surf = label_font.render(status_text, True, DARK_GRAY)
        surface.blit(text_surf, (self.rect.x + 25, self.rect.centery - text_surf.get_height()//2))

class LogBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.logs = []
    
    def add_log(self, message):
        if message.startswith("❌") and message in self.logs:
            return
        self.logs.append(message)
        self.logs = self.logs[-4:]  # Keep last 4 messages
    
    def draw(self, surface):
        title_surf = label_font.render("Deployment Log:", True, DARK_GRAY)
        surface.blit(title_surf, (self.rect.x, self.rect.y - 25))
        pygame.draw.rect(surface, LIGHT_GRAY, self.rect, border_radius=4)
        
        y_pos = self.rect.y + 10
        for log in self.logs:
            color = DARK_GRAY
            if "✅" in log: color = GREEN
            elif "❌" in log: color = RED
            log_surf = log_font.render(log, True, color)
            surface.blit(log_surf, (self.rect.x + 10, y_pos))
            y_pos += 25

class LaunchButton:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 250, 50)
        self.hovered = False
        self.disabled = False
    
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos) and not self.disabled
    
    def draw(self, surface):
        color = LIGHT_BLUE if self.hovered and not self.disabled else DARK_BLUE
        if self.disabled: color = (180, 180, 180)
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text_surf = button_font.render("LAUNCH MEME COIN", True, WHITE)
        surface.blit(text_surf, (self.rect.centerx - text_surf.get_width()//2, 
                               self.rect.centery - text_surf.get_height()//2))

# UI Elements
name_input = InputField(50, 80, 500, 45, "Coin Name:", "DogeMoon")
symbol_input = InputField(50, 160, 500, 45, "Coin Symbol:", "DSM")
supply_input = InputField(50, 240, 500, 45, "Total Supply:", "10000")
launch_button = LaunchButton(WIDTH//2 - 125, 310)
status_box = StatusBox(50, 370)
log_box = LogBox(50, 420, 500, 120)

# Pre-fill sample data
name_input.text = "DogeMoon"
symbol_input.text = "DSM"
supply_input.text = "10000"

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Meme Coin Launcher")
    clock = pygame.time.Clock()
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            name_input.handle_event(event)
            symbol_input.handle_event(event)
            supply_input.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN and launch_button.rect.collidepoint(mouse_pos):
                if not launch_button.disabled:
                    validate_and_deploy()
        
        launch_button.update(mouse_pos)
        draw_interface(screen)
        pygame.display.flip()
        clock.tick(FPS)

def validate_and_deploy():
    name = name_input.text
    symbol = symbol_input.text
    supply_text = supply_input.text
    
    # Clear previous errors
    log_box.logs = [log for log in log_box.logs if not log.startswith("❌")]
    
    # Validate
    if not name or name == name_input.placeholder:
        log_box.add_log("❌ Error: Coin name required")
        return
    
    if not symbol or symbol == symbol_input.placeholder:
        log_box.add_log("❌ Error: Coin symbol required")
        return
    
    try:
        supply = int(supply_text) if supply_text else 0
    except ValueError:
        log_box.add_log("❌ Error: Supply must be a number")
        return
    
    # Deploy
    launch_button.disabled = True
    log_box.add_log("=== Starting Deployment ===")
    
    threading.Thread(
        target=deploy_coin,
        args=(name, symbol, supply),
        daemon=True
    ).start()

def deploy_coin(name, symbol, supply):
    try:
        contract_instance = deploy_contract(name, symbol, supply)
        # Get the contract address and transaction hash
        contract_address = contract_instance.address
        tx_hash = contract_instance.transactionHash.hex() if hasattr(contract_instance, 'transactionHash') else "Unknown"
        
        log_box.add_log("✅ Deployment Successful!")
        log_box.add_log(f"Contract: {contract_address}")
        log_box.add_log(f"TX Hash: {tx_hash}")
        show_success_popup({
            "address": contract_address,
            "tx_hash": tx_hash
        })
    except Exception as e:
        error_msg = str(e)
        if "insufficient funds" in error_msg.lower():
            error_msg = "Insufficient funds for gas (get Sepolia ETH from faucet)"
        log_box.add_log(f"❌ Error: {error_msg}")
    finally:
        launch_button.disabled = False

def draw_interface(surface):
    surface.fill(WHITE)
    
    # Title
    title_surf = title_font.render("MEME COIN LAUNCHER", True, DARK_BLUE)
    surface.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 20))
    
    # Input fields
    name_input.draw(surface)
    symbol_input.draw(surface)
    supply_input.draw(surface)
    
    # Divider
    pygame.draw.line(surface, (200, 200, 200), (50, 290), (WIDTH-50, 290), 2)
    
    # Button
    launch_button.draw(surface)
    
    # Status and logs
    status_box.draw(surface)
    log_box.draw(surface)

def show_success_popup(result):
    print("\n=== DEPLOYMENT SUCCESS ===")
    print(f"Contract: {result['address']}")
    print(f"TX Hash: {result['tx_hash']}")
    print(f"View on Etherscan: https://sepolia.etherscan.io/address/{result['address']}")
    pyperclip.copy(result['address'])

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
    
    