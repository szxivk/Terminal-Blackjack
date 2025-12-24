from .models.card import Deck
from .models.player import Player, Dealer
from .ui import BlackjackUI
from . import storage
from .trivia import TriviaManager
import time
import getpass
import os
import random

# Funny welcome messages for new players
NEW_PLAYER_MESSAGES = [
    "Fresh meat! Here's $500 to lose... I mean, to WIN!",
    "A new challenger! Take these $500 chips and try not to cry.",
    "Welcome, rookie! $500 on the house. Don't spend it all in one bet!",
    "Ah, new blood! Here's $500. The house always wins... eventually.",
    "First time? How cute. Take $500 and learn the hard way!",
]

class BlackjackGame:
    def __init__(self):
        self.ui = BlackjackUI()
        self.deck = Deck(num_decks=6)
        self.player = Player("Player")
        self.dealer = Dealer()
        self.trivia = TriviaManager()

    def get_system_username(self) -> str:
        """Get the system username."""
        try:
            return getpass.getuser()
        except Exception:
            return os.environ.get('USER', os.environ.get('USERNAME', 'Player'))
    
    def show_title(self, with_chips: bool = True, with_username: bool = True):
        """Display the game title. Optionally show current chips and username."""
        chips = self.player.chips if with_chips else None
        username = self.player.name if with_username else None
        self.ui.print_header(chips, username)

    def welcome(self):
        self.ui.clear_screen()
        self.show_title(with_chips=False, with_username=False)
        
        # Get system username
        system_user = self.get_system_username()
        
        # Check chips for preview
        preview_chips = storage.load_player(system_user)
        if preview_chips is not None:
            chips_display = f"[dim][[/dim][bold yellow]${preview_chips}[/bold yellow][dim]][/dim]"
        else:
            chips_display = "[dim][New][/dim]"
        
        # Ask for name - show detected username with chips
        self.ui.console.print(f"[dim]Player:[/dim] [bold cyan]{system_user}[/bold cyan] {chips_display}")
        custom_name = self.ui.console.input("[bold]Your name[/bold] [dim](Enter to use above)[/dim]: ")
        
        player_name = custom_name.strip() if custom_name.strip() else system_user
        self.player.name = player_name
        
        # Check if player exists and load chips (no welcome message yet)
        saved_chips = storage.load_player(player_name)
        
        if saved_chips is not None:
            # Returning player
            self.player.chips = saved_chips
        else:
            # New player - give 500 chips
            self.player.chips = 500
            storage.save_player(player_name, 500)

    def save_progress(self):
        """Save player's current chips."""
        storage.save_player(self.player.name, self.player.chips)

    def play_round(self):
        # Clear hands first so boards are empty at betting time
        self.player.clear_hand()
        self.dealer.clear_hand()
        
        # 1. Place Bet
        self.ui.display_table(self.player, self.dealer, "betting")
        bet = self.ui.get_bet(self.player.chips)
        if not self.player.place_bet(bet):
            self.ui.show_message("Not enough chips!", "red")
            return

        # 2. Deal Initial Cards
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())
        self.player.add_card(self.deck.deal())
        self.dealer.add_card(self.deck.deal())

        # 3. Check Natural Blackjack
        p_val = self.player.hand_value
        
        if p_val == 21:
            pass  # Let player stand with 21

        # 4. Player Turn
        first_action = True
        while not self.player.is_busted:
            self.ui.display_table(self.player, self.dealer, "playing")
            
            action = self.ui.get_action(can_surrender=first_action)
            first_action = False
            
            if action in ['h', 'hit']:
                self.player.add_card(self.deck.deal())
                if self.player.is_busted:
                    bet_amount = self.player.bet
                    self.player.lose_bet()
                    self.ui.display_table(self.player, self.dealer, "finished", "BUSTED!", f"-${bet_amount}")
                    self.save_progress()
                    time.sleep(1.5)
                    return

            elif action in ['u', 'surrender']:
                half_bet = self.player.bet // 2
                self.player.chips += half_bet
                self.player.bet = 0
                self.ui.display_table(self.player, self.dealer, "finished", "Surrendered", f"-${half_bet}")
                self.save_progress()
                time.sleep(1.5)
                return
            
            elif action in ['s', 'stand']:
                break
        
        # 5. Dealer Turn
        self.ui.display_table(self.player, self.dealer, "dealer_turn", "Dealer...")
        time.sleep(0.5)
        
        while self.dealer.should_hit():
            self.dealer.add_card(self.deck.deal())
            self.ui.display_table(self.player, self.dealer, "dealer_turn")
            time.sleep(0.5)

        # 6. Resolve
        p_val = self.player.hand_value
        d_val = self.dealer.hand_value
        bet_amount = self.player.bet
        
        if self.dealer.is_busted:
            self.player.win_bet()
            self.ui.display_table(self.player, self.dealer, "finished", "You Win!", f"+${bet_amount}")
        elif d_val > p_val:
            self.player.lose_bet()
            self.ui.display_table(self.player, self.dealer, "finished", "Dealer Wins", f"-${bet_amount}")
        elif d_val < p_val:
            self.player.win_bet()
            self.ui.display_table(self.player, self.dealer, "finished", "You Win!", f"+${bet_amount}")
        else:
            self.player.push_bet()
            self.ui.display_table(self.player, self.dealer, "finished", "Push (Tie)", "$0")
        
        # Save after each round
        self.save_progress()
        time.sleep(1.5)

    def run(self):
        # 1. Start Menu Logic
        backups = storage.get_available_backups()
        latest_backup = backups[0] if backups else None
        
        # Always show menu
        backup_name = latest_backup.name if latest_backup else None
        
        while True:
            self.ui.clear_screen()
            self.show_title(with_chips=False, with_username=False)
            
            action = self.ui.show_start_menu(backup_name)
            
            if action == "continue":
                self.ui.console.print(f"[green]Restoring {latest_backup.name}...[/green]")
                if storage.restore_data(latest_backup):
                    time.sleep(0.5)
                    break
                else:
                    self.ui.console.print("[red]Failed to restore backup![/red]")
                    time.sleep(2)
                    # Loop back to menu
                    
            elif action == "new":
                self.ui.console.print("[yellow]Starting fresh...[/yellow]")
                # CRITICAL: keep_saves=True ensures we don't delete existing backups when starting a new game
                storage.reset_data(keep_saves=True)
                time.sleep(0.5)
                break
                
            elif action == "load":
                selected_backup = self.ui.show_backup_selection(backups)
                if selected_backup:
                    self.ui.console.print(f"[green]Restoring {selected_backup.name}...[/green]")
                    if storage.restore_data(selected_backup):
                        time.sleep(0.5)
                        break
                    else:
                        self.ui.console.print("[red]Failed to restore backup![/red]")
                        time.sleep(2)
                        # Loop back to menu
                else:
                    continue # Try again (Back to menu)
                    
            elif action == "exit":
                return

        # 2. Session / Login Logic
        last_user = storage.load_session()
        
        # If we have a session user and data exists, auto-login
        if last_user and not storage.is_new_player(last_user):
            self.player.name = last_user
            self.player.chips = storage.load_player(last_user)
            # Skip welcome, go straight to menu
        else:
            self.welcome()
            # Save session after welcome
            storage.save_session(self.player.name)
        
        while True:
            # Clear and show title before menu
            self.ui.clear_screen()
            self.show_title()
            
            # Show main menu
            choice = self.ui.show_main_menu()
            
            if choice == "play":
                # Show welcome message when starting game
                saved_chips = storage.load_player(self.player.name)
                is_returning = saved_chips is not None and saved_chips > 0
                
                if is_returning:
                    self.ui.console.print()
                    self.ui.console.print(f"[bold green]You shouldn't be gambling, {self.player.name}![/bold green]")
                    time.sleep(1)
                
                self.play_game_loop()
            elif choice == "earn":
                while True:
                    self.ui.clear_screen()
                    self.show_title()
                    mode = self.ui.show_earn_menu()
                    
                    if mode == "back":
                        break
                    
                    elif mode == "general":
                        # General Trivia Loop
                        history = []
                        while True:
                            q, idx = self.trivia.get_next_question(self.trivia.general_questions, history)
                            result = self.ui.ask_trivia_question(q, self.player.chips, self.player.name)
                            
                            if result is None:  # User selected Exit
                                break
                                
                            history.append(idx)
                            if result:
                                self.player.chips += 3
                                self.save_progress()
                                self.ui.show_trivia_result(True, 3)
                            else:
                                self.ui.show_trivia_result(False, 0)
                            
                            # Auto-continue without prompt

                    elif mode == "custom":
                        # Scan topics
                        topics = self.trivia.get_custom_topics()
                        if not topics:
                            self.ui.console.print()
                            self.ui.console.print("[bold red]No topics found![/bold red]")
                            self.ui.console.print(f"[dim]Please add JSON files to: {self.trivia.custom_dir}[/dim]")
                            self.ui.console.print("[dim]Use 'template.json' as a guide (e.g. generate with LLM)[/dim]")
                            self.ui.console.print()
                            input("Press Enter to go back...")
                            continue
                            
                        topic_path = self.ui.show_custom_topics_menu(topics)
                        if topic_path == "back":
                            continue
                            
                        # Load questions
                        questions = self.trivia.load_custom_questions(topic_path)
                        if not questions:
                            self.ui.console.print("[red]No questions found in file![/red]")
                            time.sleep(1)
                            continue
                            
                        # Infinite loop for repetitive learning
                        history = []
                        while True:
                            q, idx = self.trivia.get_next_question(questions, history)
                            if not q:
                                break
                                
                            result = self.ui.ask_trivia_question(q, self.player.chips, self.player.name)
                            
                            if result is None: # Exit
                                break
                                
                            history.append(idx)
                            if result:
                                self.player.chips += 10
                                self.save_progress()
                                self.ui.show_trivia_result(True, 10)
                            else:
                                self.ui.show_trivia_result(False, 0)
                            
                            # Auto-continue without prompt
            elif choice == "about":
                self.ui.show_about_page()
            else:  # exit
                self.ui.console.print("[yellow]Saving game...[/yellow]")
                if storage.save_current_game():
                    self.ui.console.print("[green]Game saved![/green]")
                else:
                    self.ui.console.print("[red]Save failed![/red]")
                time.sleep(1)
                break
        
        self.ui.clear_screen()
        self.ui.console.print(f"[bold white]Have a good one,[/bold white] [bold white]{self.player.name}[/bold white]! [dim]chips saved:[/dim] [bold green]${self.player.chips}[/bold green]")

    def play_game_loop(self):
        """Main game loop for playing rounds."""
        first_round = True
        
        while True:
            if self.player.chips <= 0:
                self.ui.clear_screen()
                self.ui.console.print("[bold red]Game Over! You ran out of chips.[/bold red]")
                self.ui.console.print("[dim]Come back tomorrow for a fresh $500![/dim]")
                self.save_progress()
                time.sleep(2)
                break
            
            self.play_round()
            first_round = False
            
            if not self.ui.ask_play_again():
                break

