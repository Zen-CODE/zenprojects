import random

class RockPaperScissor:


    def game_dict(self):
        game_list=["R","P","S"]
        comp_choice=random.choice(game_list)
        return(comp_choice)

    def win_user(self):
        print('you win')
        
    def win_comp(self):
        print('You lose')
        
    def computer_option_choice(self, c_computer_option):
        option_list={'R':'Rock',
                     'P':'Paper',  
                     'S':'Scissors'}
        option_choice=option_list[c_computer_option]
        print(f'The computer choice was {option_choice}')
    
    def run(self):
        """Run the game."""        

        game_count=0
        user_win_count=0
        draw=0
        user_input='R'
        comp_choice='R'
        while user_input !='Q':
            user_input=input('Choose Rock=R, Paper=P, Scissors=S, Quit=Q\n').upper()   
            computer_option=self.game_dict()
            computer_choice=self.computer_option_choice(computer_option)
            if user_input==computer_option:
                print('Draw')
                draw=draw+1
                game_count=game_count+1
            else:
                # Suggestion: Refactor below to have a function "user_wins" so
                # the game flow is separate from the logic of
                if user_input=='R':
                    if computer_option=='P':
                        game_result=self.win_comp()
                        game_count=game_count+1
                    else:
                        game_result=self.win_user()
                        game_count = game_count+1
                        user_win_count = user_win_count+1
                elif user_input=='S':
                    if computer_option=='R':    
                        game_result=self.win_comp()
                        game_count=game_count+1
                    else:
                        game_result=self.win_user()
                        game_count=game_count+1
                        user_win_count=user_win_count+1
                elif user_input=='P':
                    if computer_option=='S':    
                        game_result=self.win_comp()
                        game_count=game_count+1
                    else:
                        game_result=self.win_user()
                        game_count=game_count+1
                        user_win_count=user_win_count+1


        print('Game over')
        print(f'You won {user_win_count} games')
        print(f'You played {game_count}')
        print(f'You had {draw} draws')


if __name__ == "__main__":
    RockPaperScissor().run()
