import curses
import random
import os
import textwrap  # Added to handle line wrapping
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

def play_audio(question_index, text, stdscr):
    filename = os.path.join(CACHE_DIR, f"q_{question_index}.mp3")
    
    if not os.path.exists(filename):
        stdscr.addstr(1, 2, "Downloading audio... Please wait.", curses.color_pair(3))
        stdscr.refresh()
        tts = gTTS(text=text, lang='zh-TW')
        tts.save(filename)
        stdscr.move(1, 2)
        stdscr.clrtoeol()
        stdscr.refresh()
        
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

def draw_interface(stdscr, question_text, show_text, current_num, total_num):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()
    
    stdscr.border()
    
    # Title adjusted to prevent border-breaking on narrow terminals
    title = " 中文口試練習 (Oral Exam) "
    if max_x > len(title) + 4:
        stdscr.addstr(0, max(2, (max_x - len(title)) // 2), title, curses.A_BOLD)
    
    stdscr.addstr(2, 4, f"Question: {current_num} / {total_num}", curses.color_pair(1))
    
    # Calculate safe wrapping width (assuming 2 terminal cols per Chinese character)
    safe_char_limit = max(10, (max_x - 12) // 2)
    
    if show_text:
        stdscr.addstr(4, 4, "Teacher asks:", curses.color_pair(2))
        
        # Dynamically wrap the text to fit the screen
        wrapped_lines = textwrap.wrap(question_text, width=safe_char_limit)
        for i, line in enumerate(wrapped_lines):
            stdscr.addstr(6 + i, 4, line, curses.A_BOLD)
            
        menu_y = 6 + len(wrapped_lines) + 2
    else:
        stdscr.addstr(4, 4, "[ Audio is playing... ]", curses.color_pair(3))
        stdscr.addstr(6, 4, "Press 'S' to reveal the text.", curses.A_DIM)
        menu_y = 10
        
    # Controls Menu (Only draw if terminal is tall enough)
    if menu_y + 5 < max_y:
        stdscr.addstr(menu_y, 4, "Controls:")
        stdscr.addstr(menu_y + 1, 6, "[ SPACE ] Replay Audio")
        stdscr.addstr(menu_y + 2, 6, "[ S ]     Show / Hide Text")
        stdscr.addstr(menu_y + 3, 6, "[ ENTER ] Random Next Question")
        stdscr.addstr(menu_y + 4, 6, "[ Q ]     Quit")
    
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    curses.init_pair(3, curses.COLOR_YELLOW, -1)
    
    init_audio()
    
    unplayed = list(range(len(QUESTIONS)))
    random.shuffle(unplayed)
    
    total_q = len(QUESTIONS)
    current_q_index = unplayed.pop()
    show_text = False
    
    play_audio(current_q_index, QUESTIONS[current_q_index], stdscr)

    while True:
        draw_interface(stdscr, QUESTIONS[current_q_index], show_text, total_q - len(unplayed), total_q)
        
        key = stdscr.getch()
        
        if key in [ord('q'), ord('Q')]:
            break
        elif key in [ord('s'), ord('S')]:
            show_text = not show_text
        elif key == 32: 
            play_audio(current_q_index, QUESTIONS[current_q_index], stdscr)
        elif key in [10, 13]: 
            if not unplayed:
                unplayed = list(range(len(QUESTIONS)))
                random.shuffle(unplayed)
                
            current_q_index = unplayed.pop()
            show_text = False
            play_audio(current_q_index, QUESTIONS[current_q_index], stdscr)

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
    finally:
        pygame.mixer.quit()