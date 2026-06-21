import pygame
import sys
from card_game import blackjack_deck

# Initialize Pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 650
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blackjack Table")
clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.SysFont("arial", 18, bold=True)
font_medium = pygame.font.SysFont("arial", 24, bold=True)
font_large = pygame.font.SysFont("arial", 32, bold=True)

# Color Palette
FELT_GREEN = (12, 105, 50)
TABLE_BORDER = (8, 70, 33)
CARD_WHITE = (255, 255, 255)
CARD_BACK = (40, 90, 150)
TEXT_WHITE = (245, 245, 245)
GOLD = (255, 215, 0)
RED = (200, 30, 30)
BLACK = (20, 20, 20)

# Instantiate Deck
deck = blackjack_deck()
player_hand, dealer_hand = [], []
game_over = False
status_text = "Press 'H' to Hit, 'S' to Stand"

def calculate_score(hand):
    score, aces = 0, 0
    for card in hand:
        if card.rank in ['J', 'Q', 'K']: score += 10
        elif card.rank == 'A': score += 11; aces += 1
        else: score += int(card.rank)
    while score > 21 and aces:
        score -= 10
        aces -= 1
    return score

def start_new_game():
    global player_hand, dealer_hand, game_over, status_text
    deck.shuffle()
    player_hand = [deck.deal(), deck.deal()]
    dealer_hand = [deck.deal(), deck.deal()]
    game_over = False
    status_text = "Press 'H' to Hit, 'S' to Stand"

def draw_table():
    """Draws a classic semicircular casino table layout."""
    screen.fill(TABLE_BORDER)
    # Inner felt table
    pygame.draw.ellipse(screen, FELT_GREEN, (40, 40, SCREEN_WIDTH - 80, SCREEN_HEIGHT + 200))
    # Dealer area boundary line
    pygame.draw.arc(screen, GOLD, (150, -100, SCREEN_WIDTH - 300, 450), 3.14, 0, 2)

def draw_card(x, y, card, is_hidden=False):
    """Draws a crisp, vector-style playing card."""
    card_width, card_height = 80, 115
    card_rect = pygame.Rect(x, y, card_width, card_height)
    
    # Draw card base shadow & body
    pygame.draw.rect(screen, (0, 0, 0, 50), (x+2, y+2, card_width, card_height), border_radius=8)
    
    if is_hidden:
        # Draw Card Back
        pygame.draw.rect(screen, CARD_WHITE, card_rect, border_radius=8)
        pygame.draw.rect(screen, CARD_BACK, (x+4, y+4, card_width-8, card_height-8), border_radius=6)
        # Decorative pattern on back
        pygame.draw.rect(screen, CARD_WHITE, (x+15, y+15, card_width-30, card_height-30), 1, border_radius=4)
    else:
        # Draw Card Front
        pygame.draw.rect(screen, CARD_WHITE, card_rect, border_radius=8)
        pygame.draw.rect(screen, (200, 200, 200), card_rect, 1, border_radius=8) # Border
        
        # Identify suit color
        suit_lower = card.suit.lower()
        color = RED if suit_lower in ['hearts', 'diamonds'] else BLACK
        
        # Suit symbols mappings
        suit_symbols = {'spades': '♠', 'hearts': '♥', 'diamonds': '♦', 'clubs': '♣'}
        symbol = suit_symbols.get(suit_lower, card.suit[0].upper())
        
        # Render text onto the card
        rank_surf = font_medium.render(card.rank, True, color)
        suit_surf = font_large.render(symbol, True, color)
        
        # Position texts (Top-left corner and center)
        screen.blit(rank_surf, (x + 8, y + 6))
        screen.blit(suit_surf, (x + card_width//2 - suit_surf.get_width()//2, y + card_height//2 - suit_surf.get_height()//2 + 5))

# Start game
start_new_game()

# Main Loop
while True:
    draw_table()
    
    player_score = calculate_score(player_hand)
    dealer_score = calculate_score(dealer_hand)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                start_new_game()
                
            if not game_over:
                if event.key == pygame.K_h:
                    player_hand.append(deck.deal())
                    if calculate_score(player_hand) > 21:
                        game_over = True
                        status_text = "Busted! Dealer Wins. Press 'R' to restart."
                        
                elif event.key == pygame.K_s:
                    game_over = True
                    while calculate_score(dealer_hand) < 17:
                        dealer_hand.append(deck.deal())
                    
                    dealer_score = calculate_score(dealer_hand)
                    if dealer_score > 21:
                        status_text = "Dealer Busted! You Win! Press 'R' to restart."
                    elif player_score > dealer_score:
                        status_text = f"You Win! {player_score} beats {dealer_score}. Press 'R'."
                    elif player_score < dealer_score:
                        status_text = f"Dealer Wins! {dealer_score} beats {player_score}. Press 'R'."
                    else:
                        status_text = f"Push! It's a tie at {player_score}. Press 'R'."

    # --- RENDER CHARACTERS & CARDS ---
    
    # 1. Dealer Space (Top)
    dealer_lbl = font_medium.render("DEALER", True, TEXT_WHITE)
    screen.blit(dealer_lbl, (SCREEN_WIDTH // 2 - dealer_lbl.get_width() // 2, 20))
    
    d_score_txt = "??" if not game_over else str(dealer_score)
    score_lbl = font_small.render(f"Score: {d_score_txt}", True, GOLD)
    screen.blit(score_lbl, (SCREEN_WIDTH // 2 - score_lbl.get_width() // 2, 50))
    
    # Render Dealer Cards side-by-side
    start_x_dealer = SCREEN_WIDTH // 2 - (len(dealer_hand) * 90 - 10) // 2
    for i, card in enumerate(dealer_hand):
        hidden_status = (i == 0 and not game_over)
        draw_card(start_x_dealer + (i * 90), 80, card, is_hidden=hidden_status)

    # 2. Player Space (Bottom)
    player_lbl = font_medium.render("PLAYER", True, TEXT_WHITE)
    screen.blit(player_lbl, (SCREEN_WIDTH // 2 - player_lbl.get_width() // 2, 380))
    
    p_score_txt = font_small.render(f"Score: {player_score}", True, GOLD)
    screen.blit(p_score_txt, (SCREEN_WIDTH // 2 - p_score_txt.get_width() // 2, 410))
    
    # Render Player Cards side-by-side
    start_x_player = SCREEN_WIDTH // 2 - (len(player_hand) * 90 - 10) // 2
    for i, card in enumerate(player_hand):
        draw_card(start_x_player + (i * 90), 440, card, is_hidden=False)

    # 3. Status Display (Banner at bottom)
    status_surf = font_medium.render(status_text, True, GOLD)
    screen.blit(status_surf, (SCREEN_WIDTH // 2 - status_surf.get_width() // 2, 590))

    pygame.display.flip()
    clock.tick(60)