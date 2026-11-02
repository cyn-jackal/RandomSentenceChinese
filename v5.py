import os
import random
from gtts import gTTS
import pygame

# 45 Oral Exam Practice Questions with Text, Pinyin, English, and Target Grammar
QUESTIONS = [
    # --- Lesson 6 Homework additions ---
    {
        "text": "如果老師要搬到你的國家去，你覺得哪個城市最好？為什麼？",
        "pinyin": "Rúguǒ lǎoshī yào bān dào nǐ de guójiā qù, nǐ juéde nǎge chéngshì zuì hǎo? Wèishéme?",
        "english": "If the teacher wants to move to your country, which city do you think is best? Why?",
        "grammar": "V + 在 (e.g., 我覺得住在曼谷很方便)"
    },
    {
        "text": "從你家到超市和學校大概要多久？",
        "pinyin": "Cóng nǐ jiā dào chāoshì hé xuéxiào dàgài yào duōjiǔ?",
        "english": "About how long does it take from your home to the supermarket and school?",
        "grammar": "V + 到 (e.g., 從我家走到超市要十分鐘...)"
    },
    {
        "text": "有考試的時候，你平常念書念到幾點？",
        "pinyin": "Yǒu kǎoshì de shíhòu, nǐ píngcháng niànshū niàn dào jǐ diǎn?",
        "english": "When there is an exam, until what time do you usually study?",
        "grammar": "V + 到 (e.g., 我平常念書念到凌晨一點)"
    },
    {
        "text": "明年你家人生日的時候，你打算做什麼？",
        "pinyin": "Míngnián nǐ jiārén shēngrì de shíhòu, nǐ dǎsuàn zuò shénme?",
        "english": "Next year, when it is your family member's birthday, what do you plan to do?",
        "grammar": "V + 給 (e.g., 我打算送給家人禮物)"
    },
    {
        "text": "我們坐幾點的高鐵？行李我還沒開始準備。",
        "pinyin": "Wǒmen zuò jǐ diǎn de gāotiě? Xínglǐ wǒ hái méi kāishǐ zhǔnbèi.",
        "english": "What time is the high-speed rail we are taking? I haven't started preparing my luggage yet.",
        "grammar": "快一點 + V (e.g., 快一點準備行李)"
    },
    {
        "text": "我們是不是快要上課了？",
        "pinyin": "Wǒmen shì bù shì kuàiyào shàngkè le?",
        "english": "Are we about to start class soon?",
        "grammar": "快一點 + V (e.g., 我們需要走快一點)"
    },
    # --- Lesson 7 Homework additions ---
    {
        "text": "我買的檯燈，你記得我放在哪裡嗎？",
        "pinyin": "Wǒ mǎi de táidēng, nǐ jìdé wǒ fàng zài nǎlǐ ma?",
        "english": "Do you remember where I put the desk lamp I bought?",
        "grammar": "把 ＋ V在 (e.g., 你已經把檯燈放在臥室了)"
    },
    {
        "text": "摩托車不可以停在這裡喔！",
        "pinyin": "Mótuōchē bù kěyǐ tíng zài zhèlǐ ō!",
        "english": "Motorcycles cannot be parked here!",
        "grammar": "把 ＋ V到 (e.g., 我馬上把摩托車騎到停車場)"
    },
    {
        "text": "你下個月就要回國了，你的腳踏車怎麼辦？",
        "pinyin": "Nǐ xià gè yuè jiù yào huíguó le, nǐ de jiǎotàchē zěnme bàn?",
        "english": "You are going back to your country next month, what are you going to do with your bicycle?",
        "grammar": "把 ＋ V給 (e.g., 我打算把腳踏車送給朋友)"
    },
    {
        "text": "明天去你家的時候，我的貓可以一起去嗎？",
        "pinyin": "Míngtiān qù nǐ jiā de shíhòu, wǒ de māo kěyǐ yīqǐ qù ma?",
        "english": "When I go to your house tomorrow, can my cat go with me?",
        "grammar": "把 ＋ Direction Verb (e.g., 你可以把貓帶進來)"
    },
    {
        "text": "這些都是台灣有名的東西，你家人會喜歡嗎？",
        "pinyin": "Zhèxiē dōu shì Táiwān yǒumíng de dōngxī, nǐ jiārén huì xǐhuān ma?",
        "english": "These are all famous Taiwanese things, will your family like them?",
        "grammar": "把 ＋ Direction Verb ＋ 地方 (e.g., 我打算把這些東西寄回我家去)"
    },
    {
        "text": "下雨了，我覺得有一點冷。",
        "pinyin": "Xiàyǔ le, wǒ juéde yǒu yīdiǎn lěng.",
        "english": "It's raining, I feel a little cold.",
        "grammar": "把 ＋ 放下/穿上/拿走/關上/打開 (e.g., 你可以把外套穿上)"
    },
    {
        "text": "你還住在以前的地方嗎？我記得是你爸媽買的房子。",
        "pinyin": "Nǐ hái zhù zài yǐqián de dìfāng ma? Wǒ jìdé shì nǐ bàmā mǎi de fángzi.",
        "english": "Do you still live in the old place? I remember it was the house your parents bought.",
        "grammar": "把 + O + V了 (e.g., 我爸媽把房子賣了)"
    },
    {
        "text": "睡覺時間到了，孩子還在看電視，父母可能會說什麼？",
        "pinyin": "Shuìjiào shíjiān dào le, háizi hái zài kàn diànshì, fùmǔ kěnéng huì shuō shénme?",
        "english": "It's bedtime, and the child is still watching TV. What might the parents say?",
        "grammar": "把 ＋ V一V (e.g., 父母會說把電視關一關)"
    },
    # --- Lesson 8 Homework additions ---
    {
        "text": "窗戶現在開著嗎？我要開冷氣。",
        "pinyin": "Chuānghù xiànzài kāi zhe ma? Wǒ yào kāi lěngqì.",
        "english": "Is the window open right now? I want to turn on the AC.",
        "grammar": "東西 ＋ V著 (e.g., 對，窗戶開著。我現在去關)"
    },
    {
        "text": "我到辦公室了，你的座位在哪裡？每張桌子看起來都差不多。",
        "pinyin": "Wǒ dào bàngōngshì le, nǐ de zuòwèi zài nǎlǐ? Měi zhāng zhuōzi kàn qǐlái dōu chàbùduō.",
        "english": "I've arrived at the office, where is your seat? Every desk looks about the same.",
        "grammar": "地方 ＋ V著 ＋ 東西 (e.g., 我桌子後面貼著一張我的照片)"
    },
    {
        "text": "哪一個是你朋友？",
        "pinyin": "Nǎ yīgè shì nǐ péngyǒu?",
        "english": "Which one is your friend?",
        "grammar": "人 ＋ V著 ＋ 東西 (e.g., 中間那個學生穿著紅色的衣服)"
    },
    {
        "text": "你今天為什麼那麼晚才回家？",
        "pinyin": "Nǐ jīntiān wèishéme nàme wǎn cái huíjiā?",
        "english": "Why did you come home so late today?",
        "grammar": "S V1 O1，V1 著 V1 著，就 V2 O2了 (e.g., 我騎摩托車回家，騎著騎著，就迷路了)"
    },
    {
        "text": "你現在有空嗎？可以幫我把檯燈搬到樓上去嗎？",
        "pinyin": "Nǐ xiànzài yǒu kòng ma? Kěyǐ bāng wǒ bǎ táidēng bān dào lóushàng qù ma?",
        "english": "Are you free right now? Can you help me move the desk lamp upstairs?",
        "grammar": "忙著/急著 (e.g., 我沒有空，我急著去洗手間)"
    },
    {
        "text": "寒假你要做什麼？一起出國旅行怎麼樣？",
        "pinyin": "Hánjià nǐ yào zuò shénme? Yīqǐ chūguó lǚxíng zěnmeyàng?",
        "english": "What are you going to do for winter break? How about traveling abroad together?",
        "grammar": "S ＋ 多久時間 ＋ 沒 ＋ VO ＋ 了 (e.g., 我一年沒有回國了，寒假我想回國)"
    },
    # --- Previous Original Set ---
    {
        "text": "你的朋友想搬到台灣來，你覺得住在哪裡最好？",
        "pinyin": "Nǐ de péngyǒu xiǎng bān dào Táiwān lái, nǐ juéde zhù zài nǎlǐ zuì hǎo?",
        "english": "Your friend wants to move to Taiwan, where do you think is best to live?",
        "grammar": "V + 在 + 地方"
    },
    {
        "text": "你今天睡覺睡到幾點？",
        "pinyin": "Nǐ jīntiān shuìjiào shuì dào jǐ diǎn?",
        "english": "What time did you sleep until today?",
        "grammar": "V + 到 + 時間"
    },
    {
        "text": "聽說明天要考試，真的嗎？我什麼都還沒念。",
        "pinyin": "Tīngshuō míngtiān yào kǎoshì, zhēn de ma? Wǒ shénme dōu hái méi niàn.",
        "english": "I heard there's an exam tomorrow, really? I haven't studied anything at all.",
        "grammar": "快一點 + V"
    },
    {
        "text": "這些書很重，你可以幫我搬上去嗎？",
        "pinyin": "Zhèxiē shū hěn zhòng, nǐ kěyǐ bāng wǒ bān shàngqù ma?",
        "english": "These books are very heavy, can you help me move them upstairs?",
        "grammar": "Verb + Direction Verb + 來/去"
    },
    {
        "text": "你的照相機呢？這裡風景好漂亮，我想拍照。",
        "pinyin": "Nǐ de zhàoxiàngjī ne? Zhèlǐ fēngjǐng hǎo piàoliang, wǒ xiǎng pāizhào.",
        "english": "Where is your camera? The scenery here is so beautiful, I want to take a picture.",
        "grammar": "S + 把 + O + V + 在 + 地方"
    },
    {
        "text": "功課你寫完了嗎？老師說最慢今天要給他。",
        "pinyin": "Gōngkè nǐ xiě wán le ma? Lǎoshī shuō zuì màn jīntiān yào gěi tā.",
        "english": "Have you finished your homework? The teacher said it must be given to him by today at the latest.",
        "grammar": "S + 把 + O + V + 給 + 人"
    },
    {
        "text": "今天真的太熱了，你把冷氣打開了嗎？",
        "pinyin": "Jīntiān zhēn de tài rè le, nǐ bǎ lěngqì dǎkāi le ma?",
        "english": "It is really too hot today, did you turn on the air conditioner?",
        "grammar": "S + 把 + O + 打開"
    },
    {
        "text": "蛋糕在冰箱，你晚上記得帶去朋友家。",
        "pinyin": "Dàngāo zài bīngxiāng, nǐ wǎnshàng jìdé dài qù péngyǒu jiā.",
        "english": "The cake is in the fridge, remember to bring it to your friend's house tonight.",
        "grammar": "S + 把 + O + Verb + Direction Verb + 來/去"
    },
    {
        "text": "你週末為什麼不跟我們出去？",
        "pinyin": "Nǐ zhōumò wèishéme bù gēn wǒmen chūqù?",
        "english": "Why aren't you going out with us this weekend?",
        "grammar": "S + 忙著 / 急著 + 做什麼"
    },
    {
        "text": "你怎麼還在念書？你不睡覺嗎？已經很晚了。",
        "pinyin": "Nǐ zěnme hái zài niànshū? Nǐ bù shuìjiào ma? Yǐjīng hěn wǎn le.",
        "english": "Why are you still studying? Aren't you going to sleep? It's already very late.",
        "grammar": "S + 多久時間 + 沒 + VO + 了"
    },
    {
        "text": "公園裡的中間放著什麼東西？",
        "pinyin": "Gōngyuán lǐ de zhōngjiān fàng zhe shénme dōngxī?",
        "english": "What is placed in the middle of the park?",
        "grammar": "地方 + V著 + S"
    },
    {
        "text": "你為什麼還不下班？工作很多嗎？",
        "pinyin": "Nǐ wèishéme hái bù xiàbān? Gōngzuò hěn duō ma?",
        "english": "Why haven't you gotten off work yet? Do you have a lot of work?",
        "grammar": "S + 什麼時候 + 有 + 多久時間 + 沒/不 + VO"
    },
    {
        "text": "老師搬到郊區去了，你覺得我們買什麼東西送給他比較好？",
        "pinyin": "Lǎoshī bān dào jiāoqū qù le, nǐ juéde wǒmen mǎi shénme dōngxī sòng gěi tā bǐjiào hǎo?",
        "english": "The teacher moved to the suburbs, what do you think we should buy to give him?",
        "grammar": "最好 (zuì hǎo)"
    },
    {
        "text": "吃完飯以後，如果你發現自己忘了帶錢，你會做什麼？",
        "pinyin": "Chī wán fàn yǐhòu, rúguǒ nǐ fāxiàn zìjǐ wàng le dài qián, nǐ huì zuò shénme?",
        "english": "After eating, if you realize you forgot to bring money, what would you do?",
        "grammar": "只好 (zhǐhǎo)"
    },
    {
        "text": "這是門口，汽車不可以停在這裡喔。",
        "pinyin": "Zhè shì ménkǒu, qìchē bù kěyǐ tíng zài zhèlǐ ō.",
        "english": "This is the doorway, cars cannot park here.",
        "grammar": "S + 把 + O + V + 到 + 地方"
    },
    {
        "text": "為什麼你不想跟室友住在一起了？",
        "pinyin": "Wèishéme nǐ bù xiǎng gēn shìyǒu zhù zài yīqǐ le?",
        "english": "Why don't you want to live with your roommate anymore?",
        "grammar": "總是 (zǒngshì)"
    },
    {
        "text": "上課的時候，老師忽然說要考試，你會做什麼？",
        "pinyin": "Shàngkè de shíhòu, lǎoshī hūrán shuō yào kǎoshì, nǐ huì zuò shénme?",
        "english": "During class, the teacher suddenly says there is an exam, what will you do?",
        "grammar": "只好 (zhǐhǎo)"
    },
    {
        "text": "如果回家的時候忽然下雨了，可是你沒帶傘，你會做什麼？",
        "pinyin": "Rúguǒ huíjiā de shíhòu hūrán xiàyǔ le, kěshì nǐ méi dài sǎn, nǐ huì zuò shénme?",
        "english": "If it suddenly rains when you are going home, but you didn't bring an umbrella, what will you do?",
        "grammar": "只好 / 快一點"
    },
    {
        "text": "你上個月說你要搬家了，為什麼不搬了？",
        "pinyin": "Nǐ shàng gè yuè shuō nǐ yào bānjiā le, wèishéme bù bān le?",
        "english": "You said last month that you were going to move, why didn't you move?",
        "grammar": "原來 (yuánlái)"
    },
    {
        "text": "這個碗櫃，你覺得我把它搬到哪裡去比較好？",
        "pinyin": "Zhège wǎnguì, nǐ juéde wǒ bǎ tā bān dào nǎlǐ qù bǐjiào hǎo?",
        "english": "This cupboard, where do you think I should move it to?",
        "grammar": "S + 把 + O + V + 到 + 地方"
    },
    {
        "text": "你的衣服多髒啊，快去洗一洗吧。",
        "pinyin": "Nǐ de yīfú duō zāng a, kuài qù xǐ yī xǐ ba.",
        "english": "Your clothes are so dirty, hurry and go wash them.",
        "grammar": "Use 把 + O + V一V"
    },
    {
        "text": "為什麼他跑得那麼快？",
        "pinyin": "Wèishéme tā pǎo de nàme kuài?",
        "english": "Why is he running so fast?",
        "grammar": "急著 + 做什麼"
    },
    {
        "text": "你平常幾點起床？沒有課的時候也一樣嗎？",
        "pinyin": "Nǐ píngcháng jǐ diǎn qǐchuáng? Méiyǒu kè de shíhòu yě yīyàng ma?",
        "english": "What time do you usually get up? Is it the same when you don't have classes?",
        "grammar": "V + 到 + 時間"
    },
    {
        "text": "你的腳踏車是不是放在學校？明天我要用。",
        "pinyin": "Nǐ de jiǎotàchē shì bù shì fàng zài xuéxiào? Míngtiān wǒ yào yòng.",
        "english": "Is your bicycle left at school? I need to use it tomorrow.",
        "grammar": "把 + O + Verb + Direction Verb"
    },
    {
        "text": "我去你家玩的時候，我的狗也可以一起帶過去嗎？",
        "pinyin": "Wǒ qù nǐ jiā wán de shíhòu, wǒ de gǒu yě kěyǐ yīqǐ dài guòqù ma?",
        "english": "When I go to your house to hang out, can my dog be brought over together as well?",
        "grammar": "當然 / 把"
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
        current_q = QUESTIONS[current_q_index]
        question_text = current_q["text"]
        
        # --- PHASE 1: Listening Test ---
        clear_screen()
        print("=" * 75)
        print(f" 中文口試練習 (Oral Exam Practice)  |  Question: {total_q - len(unplayed)} / {total_q}")
        print("=" * 75)
        print("\n  [ Audio is playing... ]")
        print("  Listen to the teacher's question.\n")
        
        play_audio(current_q_index, question_text)
        
        while True:
            print("-" * 75)
            action = input("  Press [ENTER] to reveal text | 'r' to replay | 'q' to quit: ").strip().lower()
            
            if action == 'q':
                return
            elif action == 'r':
                play_audio(current_q_index, question_text)
            else:
                break # Move to Reveal Phase
                
        # --- PHASE 2: Text Reveal (with Pinyin, English & Grammar) ---
        clear_screen()
        print("=" * 75)
        print(f" 中文口試練習 (Oral Exam Practice)  |  Question: {total_q - len(unplayed)} / {total_q}")
        print("=" * 75)
        print("\n  ▶ Teacher asks:")
        print(f"    {question_text}")
        print(f"    {current_q['pinyin']}")
        print(f"    ({current_q['english']})")
        print("\n  ▶ Target Grammar for Answer:")
        print(f"    {current_q['grammar']}\n")
        
        while True:
            print("-" * 75)
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