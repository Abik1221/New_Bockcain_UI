import pygame
import sys
import os
from dotenv import load_dotenv
from blockchain import deploy_contract, check_balance, transfer_tokens

# Initialize Pygame
pygame.init()

# Load environment variables
load_dotenv()

# Screen setup
WIDTH, HEIGHT = 600, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MemeCoin Deployer")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonts
title_font = pygame.font.Font(None, 48)
text_font = pygame.font.Font(None, 28)
small_font = pygame.font.Font(None, 20)

# Input fields
class InputBox:
    def __init__(self, x, y, w, h, label, default_text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = default_text
        self.label = label
        self.active = False
        self.text_surface = small_font.render(default_text, True, BLACK)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = GREEN if self.active else GRAY
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.text_surface = small_font.render(self.text, True, BLACK)

    def draw(self, screen):
        # Draw label
        label_surface = small_font.render(self.label, True, WHITE)
        screen.blit(label_surface, (self.rect.x, self.rect.y - 30))
        # Draw input box
        pygame.draw.rect(screen, self.color, self.rect, 2, border_radius=5)
        screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))

# Create input boxes
name_input = InputBox(200, 100, 200, 40, "Token Name", "MemeCoin")
symbol_input = InputBox(200, 150, 200, 40, "Token Symbol", "MEME")
supply_input = InputBox(200, 200, 200, 40, "Initial Supply", "1000000")
recipient_input = InputBox(200, 300, 200, 40, "Recipient Address")
amount_input = InputBox(200, 350, 200, 40, "Amount")

# Button class
class Button:
    def __init__(self, x, y, w, h, text, color):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = text_font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 20, self.rect.y + 10))
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=5)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
deploy_button = Button(200, 250, 200, 40, "Deploy MemeCoin", GREEN)
check_balance_button = Button(200, 400, 200, 40, "Check Balance", BLUE)
transfer_button = Button(200, 450, 200, 40, "Transfer Tokens", BLUE)

# Game loop variables
contract_instance = None
status_text = ""
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        name_input.handle_event(event)
        symbol_input.handle_event(event)
        supply_input.handle_event(event)
        recipient_input.handle_event(event)
        amount_input.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if deploy_button.is_clicked(event.pos):
                try:
                    initial_supply = int(supply_input.text)
                    if not name_input.text or not symbol_input.text or initial_supply <= 0:
                        status_text = "Invalid input: Name, symbol, or supply required"
                        continue
                    contract_instance = deploy_contract(name_input.text, symbol_input.text, initial_supply)
                    status_text = f"Contract deployed at: {contract_instance.address}"
                except Exception as e:
                    status_text = f"Error: {str(e)}"
            elif check_balance_button.is_clicked(event.pos) and contract_instance:
                try:
                    balance = check_balance(contract_instance)
                    status_text = f"Balance: {balance // (10 ** 18)} {contract_instance.functions.symbol().call()}"
                except Exception as e:
                    status_text = f"Error: {str(e)}"
            elif transfer_button.is_clicked(event.pos) and contract_instance:
                try:
                    amount = int(amount_input.text)
                    if not recipient_input.text or amount <= 0:
                        status_text = "Invalid recipient or amount"
                        continue
                    transfer_tokens(contract_instance, recipient_input.text, amount)
                    status_text = f"Transferred {amount} tokens to {recipient_input.text}"
                except Exception as e:
                    status_text = f"Error: {str(e)}"

    # Draw background
    screen.fill(BLACK)

    # Draw title
    title_surface = title_font.render("MemeCoin Deployer", True, WHITE)
    screen.blit(title_surface, (150, 20))

    # Draw input boxes
    name_input.draw(screen)
    symbol_input.draw(screen)
    supply_input.draw(screen)
    recipient_input.draw(screen)
    amount_input.draw(screen)

    # Draw buttons
    deploy_button.draw(screen)
    check_balance_button.draw(screen)
    transfer_button.draw(screen)

    # Draw status
    status_surface = small_font.render(status_text, True, WHITE)
    screen.blit(status_surface, (200, 480))

    # Update display
    pygame.display.flip()
    clock.tick(30)

# Cleanup
pygame.quit()
sys.exit()