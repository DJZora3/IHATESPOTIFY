import vlc
import os
import random
import threading
import time

#opening stuff------------------------------------------------------------------
music_folder_location = 'filepaths.txt'
settings_location = 'settings.txt'
music_paths = []
#music_dir = os.listdir(music_path[0])


#place where settings actually gets loaded--------------------------------------

player = vlc.MediaPlayer()
with open(settings_location, 'r') as f:
	for line in f:
		vlc.libvlc_audio_set_volume(player, int(line))


#place where music actually gets loaded-----------------------------------------
print("Loading music...")

counter = 0

with open(music_folder_location, 'r') as f:
	for line in f:
		music_paths.append(line.strip())
		counter += 1

music_dict = {}
	
for path in music_paths:
	music_dict[path.split('\\')[-1]] = [path, os.listdir(path)]
	
		
			
print('Loaded ' + str(counter) + ' folders and ' + str(sum([len(music_dict[i][1]) for i in music_dict.keys()])) + ' songs!')


#GUI!!!!!-----------------------------------------------------------------------
while True:
	print('\n\nWhat would you like to do?\n\nType a number.\n1.Play music from a folder.\n2.Add new folder to play music from.\n3.Quit')
	user_says = input('')
	if user_says == '1': #play music
		#todo
		def play_music(loc, name, player):
			# player = vlc.MediaPlayer(loc + '\\' + name)
			
			print('Now playing: ' + name)
			
			player.set_media(vlc.Media(loc + '\\' + name))
			
			player.play()
			return player
			
		def keep_playing(loc, list, player, dead):
			currently_playing = random.choice(list)
			
			while True:
				#print("Check")
				time.sleep(2)
				if player.get_state() == vlc.State.Ended:
					print("song changed!")
					player = play_music(loc, currently_playing, player)
					
			
		thread_started = 0
		
		while True:
			
			
			
			print('Which folder would you like to shuffle from?')
			print('type break to break.')
			for i in range(len(list(music_dict.keys()))):
				print(str(i) + '. ' + list(music_dict.keys())[i])
				
			user_input = input('Please type the number: ')
			
			if user_input == 'break':
				break
			
			currently_playing_folder = music_dict[list(music_dict.keys())[int(user_input)]][0]
			music_file_list = music_dict[list(music_dict.keys())[int(user_input)]][1]
			
			player = vlc.MediaPlayer()
			
			kill_it = 0
			
			currently_playing = random.choice(music_file_list)
			
			player = play_music(currently_playing_folder, currently_playing, player)
			
			
			if thread_started == 0:
				keep_it_pumpin = threading.Thread(target = keep_playing, args = (currently_playing_folder, music_file_list, player, kill_it), daemon = True)
			
				keep_it_pumpin.start()
			
			while True:	
				print('Now, while your song is playing, anything you would like to do?')
				print('1.STOP IT\n2.PLAY IT\n3.CHANGE VOLUME\n4.TAKE ME BACK TO THE FOLDER\n5.PLAY SOMETHING ELSE')
				user_input = input('Please type the number: ')
				
				if user_input == '1': #pause
					#print(type(player.get_state()))
					player.pause()
				elif user_input == '2': #play
					player.play()
				elif user_input == '3': #set volume
					vlc.libvlc_audio_set_volume(player, int(input('number from 0 to 100:')))
				elif user_input == '4': #stop
					player.stop()
					break
				elif user_input == '5': #skip
					player.stop()
					kill_it = 1
					currently_playing = random.choice(music_file_list)
					play_music(currently_playing_folder, currently_playing, player)
					player.play() 
					
	elif user_says == '2':
		#todo
		
		user_input = input('\nPlease input the path to the file that contains your music.')
		
		with open(music_folder_location, 'a') as f:
			f.write(user_input + '\n')
		
		print('Just added ' + user_input + ' to the file! If you made a mistake, cry about it!! After all, Dylan will probably be the only one using this. Fix it you damned liberal!!!')
	
		print("Loading music...")

		counter = 0

		with open(music_folder_location, 'r') as f:
			for line in f:
				music_paths.append(line.strip())
				counter += 1

		music_dict = {}
	
		for path in music_paths:
			music_dict[path.split('\\')[-1]] = [path, os.listdir(path)]
	
		
			
		print('Loaded ' + str(counter) + ' folders and ' + str(sum([len(music_dict[i][1]) for i in music_dict.keys()])) + ' songs!')
	
	elif user_says == '3':
		print('Quitting! Thanks for using Dylan Berry Music GUI! Much love to VLC for actually doing the music playing part.')
		input('Press enter to close the program.')
		break
		
	else:
		print('That isn\'t an option yet!')
	
	wait = input('Press enter to continue.')
	user_says = ''
	user_input = ''