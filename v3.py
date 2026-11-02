import os
import random
from gtts import gTTS
import pygame

# 25 Oral Exam Practice Questions (L6, L7, L8 Grammar)
QUESTIONS = [
    "你的朋友想搬到台灣來，你覺得住在哪裡最好？",
    "你今天睡覺睡到幾點？",
    "聽說明天要考試，真的嗎？我什麼都還沒念。",
    "這些書很重，你可以幫我搬上去嗎？",
    "你的照相機呢？這裡風景好漂亮，我想拍照。",
    "功課你寫完了嗎？老師說最慢今天要給他。",
    "今天真的太熱了，你把冷氣打開了嗎？",
    "蛋糕在冰箱，你晚上記得帶去朋友家。",
    "你週末為什麼不跟我們出去？",
    "你怎麼還在念書？你不睡覺嗎？已經很晚了。",
    "公園裡的中間放著什麼東西？",
    "你為什麼還不下班？工作很多嗎？",
    "老師搬到郊區去了，你覺得我們買什麼東西送給他比較好？",
    "吃完飯以後，如果你發現自己忘了帶錢，你會做什麼？",
    "這是門口，汽車不可以停在這裡喔。",
    "為什麼你不想跟室友住在一起了？",
    "上課的時候，老師忽然說要考試，你會做什麼？",
    "如果回家的時候忽然下雨了，可是你沒帶傘，你會做什麼？",
    "你上個月說你要搬家了，為什麼不搬了？",
    "這個碗櫃，你覺得我把它搬到哪裡去比較好？",
    "你的衣服多髒啊，快去洗一洗吧。",
    "為什麼他跑得那麼快？",
    "你平常幾點起床？沒有課的時候也一樣嗎？",
    "你的腳踏車是不是放在學校？明天我要用。",
    "我去你家玩的時候，我的狗也可以一起帶過去嗎？"
]

CACHE_DIR = "tts_cache"

def init_audio():
    pygame.mixer.init()
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def play_audio(question_index, text):
    filename = os.path.join(CACHE_DIR, f"q_{question_index}.mp3")
    if not os.path.exists(filename):
        print("\n  [Downloading audio... Please wait]")
        tts = gTTS(text=text, lang='zh-TW')
        tts.save(filename)
    
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def clear_screen():
    # Clears the terminal on both Windows and Linux/Ubuntu
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    init_audio()
    unplayed = list(range(len(QUESTIONS)))
    random.shuffle(unplayed)
    total_q = len(QUESTIONS)
    
    while True:
        if not unplayed:
            # Reshuffle when all questions are answered
            unplayed = list(range(len(QUESTIONS)))
            random.shuffle(unplayed)
            
        current_q_index = unplayed.pop()
        question_text = QUESTIONS[current_q_index]
        
        # --- PHASE 1: Listening Test ---
        clear_screen()
        print("=" * 55)
        print(f" 中文口試練習 (Oral Exam Practice)  |  Question: {total_q - len(unplayed)} / {total_q}")
        print("=" * 55)
        print("\n  [ Audio is playing... ]")
        print("  Listen to the teacher's question.\n")
        
        play_audio(current_q_index, question_text)
        
        while True:
            print("-" * 55)
            action = input("  Press [ENTER] to reveal text | 'r' to replay | 'q' to quit: ").strip().lower()
            
            if action == 'q':
                return
            elif action == 'r':
                play_audio(current_q_index, question_text)
            else:
                break # Move to Reveal Phase
                
        # --- PHASE 2: Text Reveal ---
        clear_screen()
        print("=" * 55)
        print(f" 中文口試練習 (Oral Exam Practice)  |  Question: {total_q - len(unplayed)} / {total_q}")
        print("=" * 55)
        print("\n  Teacher asks:")
        print(f"\n  {question_text}\n")
        
        while True:
            print("-" * 55)
            action = input("  Press [ENTER] for next question | 'r' to replay | 'q' to quit: ").strip().lower()
            
            if action == 'q':
                return
            elif action == 'r':
                play_audio(current_q_index, question_text)
            else:
                break # Move to Next Question

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        pygame.mixer.quit()