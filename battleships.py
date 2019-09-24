import numpy as np
import random
from collections import OrderedDict

np.set_printoptions(formatter={'int_kind': lambda x:' {0:d}'.format(x)})

def main_header():
	print("""
========================

			BATTLESHIPS				

========================
		""")

def make_board_copy(size):
	board=np.ndarray((size,size),dtype=object)
	for i in range(0,size):
		for j in range(0,size):
			board[i,j] = (i+1,j+1)
	print(board)

def make_board(size):
	board=np.array([' ']*size*size)
	board = np.array(np.split(board,size))
	return board

def ship_list():
	ship_values={"Aircraft_Carrier":11111,"Battleship":1111,"Cruiser":111,"Submarine":11,"Destroyer":1}
	ships={"Aircraft_Carrier":1,"Battleship":1,"Cruiser":1,"Submarine":2,"Destroyer":2}
	#ships={"Aircraft_Carrier":0,"Battleship":0,"Cruiser":0,"Submarine":0,"Destroyer":1}	
	return ship_values,ships

def play_game():
	try:
		size = int(raw_input('Please enter board size as a number (eg. 10 will give a board 10x10): '))
	except ValueError:
		print("That's not an int!")
	
	make_board_copy(size)
	board=make_board(size)
	ship_values,ships=ship_list()
	print("Size of ships\n")
	print(ship_values)
	print("\nNumber of Ships of each type\n")
	print(ships)


	your_board=setup_your_board(board,size)
	print("YOUR BOARD\n")
	print(your_board)
	player_board=your_board
	print("COMPUTER BOARD\n")
	opp_board=computer_board(board,size)
	print(opp_board)
	atk_board=make_board(size)
	winner=0
	while winner==0:
		winner1=player_attack(size,opp_board,atk_board)
		if winner1==False:
			print('Player Wins!')
			break

		winner2=comp_attack(size,player_board)
		if winner2==False:
			print('Computer Wins!')
			break


def setup_your_board(board,size):
	ship_values,ships=ship_list()
	value=True
	while value==True:
		ship=raw_input('\nWhich ship would you like to place?\t')
		if ship in ships.keys():
			if ships[ship]>0:
				try:
					location=str(raw_input('\nWhere would you like to place the ship (row,col)?\t'))
					loc_x,loc_y=location.split(',')
					if len(loc_x+loc_y)==4 or len(loc_x+loc_y)==5:
						loc_x=int(loc_x[1])
						loc_y=int(loc_y[0])
					elif len(loc_x+loc_y)==2 or len(loc_x+loc_y)==3:
						loc_x=int(loc_x)
						loc_y=int(loc_y)
				except:
					print("You didnt enter correct format")
					continue
				if loc_x in range(1,size+1):	
					if loc_y in range(1,size+1):
						orientation=raw_input('\nWhat orientation would you like to place it? (H or V)?')
						if orientation.lower()=='h' or orientation.lower()=='v':
							placed_ship=place_ship(board,size,loc_x,loc_y,orientation,ships,ship)
							print(board)
							if placed_ship==False:
								ships[ship]-=1
								new_value=check_value(ships)
								print(ships)
								if new_value==True:
									print("All ships placed!")
									value=False
							else:
								print("There is a collsion!")
						else:
							print("Not a choice! Choose H or V!")
							print(ships)
					else:
						print("Location Y out of Bounds")
						print(ships)
				else:
					print("Location X out of Bounds")
					print(ships)
			else:
				print("Already Placed!")
				print(ships)
		else:
			print("That word is not in the list, try again!")
			print(ships)
	return board

def computer_board(board,size):
	ship_values,ships=ship_list()
	board=make_board(size)
	value=True
	while value==True:
		ship=random.choice(ships.keys())
		if ship in ships.keys():
			if ships[ship]>0:
				loc_x=random.randint(1,size)
				loc_y=random.randint(1,size)
				orientation=random.choice(['h','v'])			
				placed_ship=place_ship(board,size,loc_x,loc_y,orientation,ships,ship)
				if placed_ship==False:
					ships[ship]-=1
					new_value=check_value(ships)
					if new_value==True:
						value=False
	return board


def place_ship(board,size,loc_x,loc_y,orientation,ships,ship):
	collision=False
	collision=check_collision(board,size,loc_x,loc_y,orientation,ships,ship)
	if collision==False:
		if orientation.lower()=='v':
			if ship=='Aircraft_Carrier':
				collision=check_collision(board,size,loc_x,loc_y,orientation,ships,ship)
				if collision==False:
					board[loc_x-1][loc_y-1]='A'
					board[loc_x][loc_y-1]='A'
					board[loc_x+1][loc_y-1]='A'
					board[loc_x+2][loc_y-1]='A'
					board[loc_x+3][loc_y-1]='A'
					#print(board)
			if ship=='Battleship':
				collision=check_collision(board,size,loc_x,loc_y,orientation,ships,ship)
				if collision==False:
					board[loc_x-1][loc_y-1]='B'
					board[loc_x][loc_y-1]='B'
					board[loc_x+1][loc_y-1]='B'
					board[loc_x+2][loc_y-1]='B'
					#print(board)
			if ship=='Cruiser':
				collision=check_collision(board,size,loc_x,loc_y,orientation,ships,ship)
				if collision==False:
					board[loc_x-1][loc_y-1]='C'
					board[loc_x][loc_y-1]='C'
					board[loc_x+1][loc_y-1]='C'
					#print(board)
			if ship=='Submarine':
				collision=check_collision(board,size,loc_x,loc_y,orientation,ships,ship)
				if collision==False:
					board[loc_x-1][loc_y-1]='S'
					board[loc_x][loc_y-1]='S'
					#print(board)
			if ship=='Destroyer':
				collision=check_collision(board,size,loc_x,loc_y,orientation,ships,ship)
				if collision==False:
					board[loc_x-1][loc_y-1]='D'
					#print(board)

		elif orientation.lower()=='h':
			if ship=='Aircraft_Carrier':
				collision=check_collision(board,size,loc_x,loc_y,orientation,ships,ship)
				if collision==False:
					board[loc_x-1][loc_y-1]='A'
					board[loc_x-1][loc_y]='A'
					board[loc_x-1][loc_y+1]='A'
					board[loc_x-1][loc_y+2]='A'
					board[loc_x-1][loc_y+3]='A'
					#print(board)
			if ship=='Battleship':
				collision=check_collision(board,size,loc_x,loc_y,orientation,ships,ship)
				if collision==False:
					board[loc_x-1][loc_y-1]='B'
					board[loc_x-1][loc_y]='B'
					board[loc_x-1][loc_y+1]='B'
					board[loc_x-1][loc_y+2]='B'
					#print(board)
			if ship=='Cruiser':
				collision=check_collision(board,size,loc_x,loc_y,orientation,ships,ship)
				if collision==False:
					board[loc_x-1][loc_y-1]='C'
					board[loc_x-1][loc_y]='C'
					board[loc_x-1][loc_y+1]='C'
					#print(board)
			if ship=='Submarine':
				collision=check_collision(board,size,loc_x,loc_y,orientation,ships,ship)
				if collision==False:
					board[loc_x-1][loc_y-1]='S'
					board[loc_x-1][loc_y]='S'
					#print(board)
			if ship=='Destroyer':
				collision=check_collision(board,size,loc_x,loc_y,orientation,ships,ship)
				if collision==False:
					board[loc_x-1][loc_y-1]='D'
					#print(board)
	# elif collision==True:
	# 	print("There is a collision, Place again!")
	return collision

def check_collision(board,size,loc_x,loc_y,orientation,ships,ship):
	collision=False
	#2 ships colliding
	if board[loc_x-1][loc_y-1]!=' ':
		collision=True
		return collision
	#out of bounds
	if loc_x>size or loc_x<1 or loc_y<1 or loc_y>size:
		collision=True
		return collision
	# ship cant fit in board
	if orientation.lower()=='v':
		if ship=='Carrier':
			if loc_x-1>=size-4:
				collision=True
				return collision
		if ship=='Battleship':
			if loc_x-1>=size-3:
				collision=True
				return collision
		if ship=='Cruiser':
			if loc_x-1>=size-2:
				collision=True
				return collision
		if ship=='Submarine':
			if loc_x-1>=size-1:
				collision=True
				return collision

	if orientation.lower()=='h':
		if ship=='Carrier':
			if loc_y-1>=size-4:
				collision=True
				return collision
		if ship=='Battleship':
			if loc_y-1>=size-3:
				collision=True
				return collision
		if ship=='Cruiser':
			if loc_y-1>=size-2:
				collision=True
				return collision
		if ship=='Submarine':
			if loc_y-1>=size-1:
				collision=True
				return collision

	return collision

def check_value(ships):
	value=all(value == 0 for value in ships.values())
	return value

def player_attack(size,opp_board,atk_board):
	ship_values,ships=ship_list()
	no_ships_left=True
	try:
		attack=raw_input('\nWhich cell would you like to attack?\t')
		atk_x,atk_y=attack.split(',')
		if len(atk_x+atk_y)==4 or len(atk_x+atk_y)==5:
			atk_x=int(atk_x[1])
			atk_y=int(atk_y[0])
		elif len(atk_x+atk_y)==2 or len(atk_x+atk_y)==3:
			atk_x=int(atk_x)
			atk_y=int(atk_y)
	except:
		print("You didnt enter correct format")

	if atk_x in range(1,size+1):	
		if atk_y in range(1,size+1):
			if opp_board[atk_x-1][atk_y-1]=='D':
				atk_board[atk_x-1][atk_y-1]='X'
				print("You sunk my Destroyer!")
				print("COMPUTER BOARD\n")
				print(atk_board)
				ships['Destroyer']-=1
			elif opp_board[atk_x-1][atk_y-1]=='S':
				atk_board[atk_x-1][atk_y-1]='X'
				print("COMPUTER BOARD\n")
				print(atk_board)
				print("You sunk my Submarine!")
				ships['Submarine']-=1
			elif opp_board[atk_x-1][atk_y-1]=='C':
				atk_board[atk_x-1][atk_y-1]='X'
				print("COMPUTER BOARD\n")
				print(atk_board)
				C=np.where(opp_board=='C')
				if len(C[0])==0:
					print("You sunk my Cruiser!")
					ships['Cruiser']-=1
			elif opp_board[atk_x-1][atk_y-1]=='B':
				atk_board[atk_x-1][atk_y-1]='X'
				print("COMPUTER BOARD\n")
				print(atk_board)
				B=np.where(opp_board=='B')
				if len(B[0])==0:
					print("You sunk my Battleship!")
					ships['Battleship']-=1
			elif opp_board[atk_x-1][atk_y-1]=='A':
				atk_board[atk_x-1][atk_y-1]='X'
				print("COMPUTER BOARD\n")
				print(atk_board)
				A=np.where(opp_board=='A')
				if len(A[0])==0:
					print("You sunk my Aircraft Carrier!")
					ships['Aircraft_Carrier']-=1
			else:
				atk_board[atk_x-1][atk_y-1]='O'
				print("COMPUTER BOARD\n")
				print(atk_board)
		new_value=check_value(ships)
		if new_value==True:
			no_ships_left=False
		print('Your opponent\'s remaining ships are :',ships)
	return no_ships_left

def comp_attack(size,player_board):
	ship_values,ships=ship_list()
	no_ships_left=True
	atk_x=random.randint(1,size)
	atk_y=random.randint(1,size)
	if player_board[atk_x-1][atk_y-1]=='D':
		player_board[atk_x-1][atk_y-1]='X'
		print("Your Destroyer has been sunk!")
		print("YOUR BOARD\n")
		print(player_board)
		ships['Destroyer']-=1
	elif player_board[atk_x-1][atk_y-1]=='S':
		player_board[atk_x-1][atk_y-1]='X'
		print("YOUR BOARD\n")
		print(player_board)
		print("Your Submarine has been sunk!")
		ships['Submarine']-=1
	elif player_board[atk_x-1][atk_y-1]=='C':
		player_board[atk_x-1][atk_y-1]='X'
		player_board[atk_x-1][atk_y-1]='X'
		print("YOUR BOARD\n")
		print(player_board)
		C=np.where(opp_board=='C')
		if len(C[0])==0:
			print("Your Cruiser has been sunk!")
			ships['Cruiser']-=1
	elif player_board[atk_x-1][atk_y-1]=='B':
		player_board[atk_x-1][atk_y-1]='X'
		print("YOUR BOARD\n")
		print(player_board)
		B=np.where(player_board=='B')
		if len(B[0])==0:
			print("Your Battleship has been sunk!")
			ships['Battleship']-=1
	elif player_board[atk_x-1][atk_y-1]=='A':
		player_board[atk_x-1][atk_y-1]='X'
		print("YOUR BOARD\n")
		print(player_board)
		A=np.where(opp_board=='A')
		if len(A[0])==0:
			print("Your Aircraft Carrier has been sunk!")
			ships['Aircraft_Carrier']-=1
	else:
		player_board[atk_x-1][atk_y-1]='O'
		print("YOUR BOARD\n")
		print(player_board)
	new_value=check_value(ships)
	if new_value==True:
		no_ships_left=False
	print('Your remaining ships are:',ships)			
	return no_ships_left

def main():
	main_header()
	play_game()

if __name__=='__main__':
	main()
