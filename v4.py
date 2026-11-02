import os
import random
from gtts import gTTS
import pygame

# 25 Oral Exam Practice Questions (L6, L7, L8 Grammar) with Pinyin and Target Grammar
QUESTIONS = [
    {
        "text": "你的朋友想搬到台灣來，你覺得住在哪裡最好？",
        "pinyin": "Nǐ de péngyǒu xiǎng bān dào Táiwān lái, nǐ juéde zhù zài nǎlǐ zuì hǎo?",
        "grammar": "V + 在 + 地方 (Verb + at + Location)"
    },
    {
        "text": "你今天睡覺睡到幾點？",
        "pinyin": "Nǐ jīntiān shuìjiào shuì dào jǐ diǎn?",
        "grammar": "V + 到 + 時間 (Verb + until + Time)"
    },
    {
        "text": "聽說明天要考試，真的嗎？我什麼都還沒念。",
        "pinyin": "Tīngshuō míngtiān yào kǎoshì, zhēn de ma? Wǒ shénme dōu hái méi niàn.",
        "grammar": "快一點 + V (Do something faster)"
    },
    {
        "text": "這些書很重，你可以幫我搬上去嗎？",
        "pinyin": "Zhèxiē shū hěn zhòng, nǐ kěyǐ bāng wǒ bān shàngqù ma?",
        "grammar": "Verb + Direction Verb + 來/去 (e.g., 搬上去)"
    },
    {
        "text": "你的照相機呢？這裡風景好漂亮，我想拍照。",
        "pinyin": "Nǐ de zhàoxiàngjī ne? Zhèlǐ fēngjǐng hǎo piàoliang, wǒ xiǎng pāizhào.",
        "grammar": "S + 把 + O + V + 在 + 地方 (e.g., 把照相機放在家裡)"
    },
    {
        "text": "功課你寫完了嗎？老師說最慢今天要給他。",
        "pinyin": "Gōngkè nǐ xiě wán le ma? Lǎoshī shuō zuì màn jīntiān yào gěi tā.",
        "grammar": "S + 把 + O + V + 給 + 人 (e.g., 把功課拿給老師)"
    },
    {
        "text": "今天真的太熱了，你把冷氣打開了嗎？",
        "pinyin": "Jīntiān zhēn de tài rè le, nǐ bǎ lěngqì dǎkāi le ma?",
        "grammar": "S + 把 + O + 打開 / 關上 (e.g., 把冷氣打開)"
    },
    {
        "text": "蛋糕在冰箱，你晚上記得帶去朋友家。",
        "pinyin": "Dàngāo zài bīngxiāng, nǐ wǎnshàng jìdé dài qù péngyǒu jiā.",
        "grammar": "S + 把 + O + Verb + Direction Verb + 來/去 (e.g., 把蛋糕帶過去)"
    },
    {
        "text": "你週末為什麼不跟我們出去？",
        "pinyin": "Nǐ zhōumò wèishéme bù gēn wǒmen chūqù?",
        "grammar": "S + 忙著 / 急著 + 做什麼 (e.g., 忙著準備考試)"
    },
    {
        "text": "你怎麼還在念書？你不睡覺嗎？已經很晚了。",
        "pinyin": "Nǐ zěnme hái zài niànshū? Nǐ bù shuìjiào ma? Yǐjīng hěn wǎn le.",
        "grammar": "S + 多久時間 + 沒 + VO + 了 (e.g., 一天沒睡覺了)"
    },
    {
        "text": "公園裡的中間放著什麼東西？",
        "pinyin": "Gōngyuán lǐ de zhōngjiān fàng zhe shénme dōngxī?",
        "grammar": "地方 + V著 + S (e.g., 放著一張桌子)"
    },
    {
        "text": "你為什麼還不下班？工作很多嗎？",
        "pinyin": "Nǐ wèishéme hái bù xiàbān? Gōngzuò hěn duō ma?",
        "grammar": "S + 什麼時候 + 有 + 多久時間 + 沒/不 + VO (e.g., 今天有十個小時沒吃飯了)"
    },
    {
        "text": "老師搬到郊區去了，你覺得我們買什麼東西送給他比較好？",
        "pinyin": "Lǎoshī bān dào jiāoqū qù le, nǐ juéde wǒmen mǎi shénme dōngxī sòng gěi tā bǐjiào hǎo?",
        "grammar": "最好 (zuì hǎo - had better) (e.g., 最好買一個檯燈)"
    },
    {
        "text": "吃完飯以後，如果你發現自己忘了帶錢，你會做什麼？",
        "pinyin": "Chī wán fàn yǐhòu, rúguǒ nǐ fāxiàn zìjǐ wàng le dài qián, nǐ huì zuò shénme?",
        "grammar": "只好 (zhǐhǎo - have no choice but to)"
    },
    {
        "text": "這是門口，汽車不可以停在這裡喔。",
        "pinyin": "Zhè shì ménkǒu, qìchē bù kěyǐ tíng zài zhèlǐ ō.",
        "grammar": "S + 把 + O + V + 到 + 地方 (e.g., 把汽車停到停車場)"
    },
    {
        "text": "為什麼你不想跟室友住在一起了？",
        "pinyin": "Wèishéme nǐ bù xiǎng gēn shìyǒu zhù zài yīqǐ le?",
        "grammar": "總是 (zǒngshì - always) (e.g., 他總是把衣服放在床上)"
    },
    {
        "text": "上課的時候，老師忽然說要考試，你會做什麼？",
        "pinyin": "Shàngkè de shíhòu, lǎoshī hūrán shuō yào kǎoshì, nǐ huì zuò shénme?",
        "grammar": "只好 (zhǐhǎo - have no choice but to) (e.g., 忽然考試，我只好...)"
    },
    {
        "text": "如果回家的時候忽然下雨了，可是你沒帶傘，你會做什麼？",
        "pinyin": "Rúguǒ huíjiā de shíhòu hūrán xiàyǔ le, kěshì nǐ méi dài sǎn, nǐ huì zuò shénme?",
        "grammar": "只好 / 快一點 (e.g., 我只好快一點跑回家)"
    },
    {
        "text": "你上個月說你要搬家了，為什麼不搬了？",
        "pinyin": "Nǐ shàng gè yuè shuō nǐ yào bānjiā le, wèishéme bù bān le?",
        "grammar": "原來 (yuánlái - originally) (e.g., 原來要搬，可是太貴了)"
    },
    {
        "text": "這個碗櫃，你覺得我把它搬到哪裡去比較好？",
        "pinyin": "Zhège wǎnguì, nǐ juéde wǒ bǎ tā bān dào nǎlǐ qù bǐjiào hǎo?",
        "grammar": "S + 把 + O + V + 到 + 地方 (e.g., 把碗櫃搬到廚房去)"
    },
    {
        "text": "你的衣服多髒啊，快去洗一洗吧。",
        "pinyin": "Nǐ de yīfú duō zāng a, kuài qù xǐ yī xǐ ba.",
        "grammar": "好，我現在去把衣服洗一洗 (Use 把 + O + V一V)"
    },
    {
        "text": "為什麼他跑得那麼快？",
        "pinyin": "Wèishéme tā pǎo de nàme kuài?",
        "grammar": "急著 + 做什麼 (In a hurry to...) (e.g., 他急著去洗手間)"
    },
    {
        "text": "你平常幾點起床？沒有課的時候也一樣嗎？",
        "pinyin": "Nǐ píngcháng jǐ diǎn qǐchuáng? Méiyǒu kè de shíhòu yě yīyàng ma?",
        "grammar": "V + 到 + 時間 (e.g., 沒有課的時候，我睡覺睡到十點)"
    },
    {
        "text": "你的腳踏車是不是放在學校？明天我要用。",
        "pinyin": "Nǐ de jiǎotàchē shì bù shì fàng zài xuéxiào? Míngtiān wǒ yào yòng.",
        "grammar": "把 + O + Verb + Direction Verb (e.g., 我明天把車騎回來)"
    },
    {
        "text": "我去你家玩的時候，我的狗也可以一起帶過去嗎？",
        "pinyin": "Wǒ qù nǐ jiā wán de shíhòu, wǒ de gǒu yě kěyǐ yīqǐ dài guòqù ma?",
        "grammar": "當然 / 把 (e.g., 當然可以，你把牠帶過來吧)"
    }
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
            unplayed = list(range(len(QUESTIONS)))
            random.shuffle(unplayed)
            
        current_q_index = unplayed.pop()
        current_q = QUESTIONS[current_q_index] # Gets the dictionary
        question_text = current_q["text"]
        
        # --- PHASE 1: Listening Test ---
        clear_screen()
        print("=" * 65)
        print(f" 中文口試練習 (Oral Exam Practice)  |  Question: {total_q - len(unplayed)} / {total_q}")
        print("=" * 65)
        print("\n  [ Audio is playing... ]")
        print("  Listen to the teacher's question.\n")
        
        play_audio(current_q_index, question_text)
        
        while True:
            print("-" * 65)
            action = input("  Press [ENTER] to reveal text | 'r' to replay | 'q' to quit: ").strip().lower()
            
            if action == 'q':
                return
            elif action == 'r':
                play_audio(current_q_index, question_text)
            else:
                break # Move to Reveal Phase
                
        # --- PHASE 2: Text Reveal (with Pinyin & Grammar) ---
        clear_screen()
        print("=" * 65)
        print(f" 中文口試練習 (Oral Exam Practice)  |  Question: {total_q - len(unplayed)} / {total_q}")
        print("=" * 65)
        print("\n  ▶ Teacher asks:")
        print(f"    {question_text}")
        print(f"    {current_q['pinyin']}")
        print("\n  ▶ Target Grammar for Answer:")
        print(f"    {current_q['grammar']}\n")
        
        while True:
            print("-" * 65)
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