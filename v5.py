import os
import random
from gtts import gTTS
import pygame

# 45 Oral Exam Practice Questions with Text, Pinyin, English, and Target Grammar
CACHE_DIR = "tts_cache"
QUESTIONS = [
    {
        "text": "如果老師要搬到你的國家，你覺得住在哪個城市最好？為什麼？",
        "pinyin": "Rúguǒ lǎoshī yào bān dào nǐ de guójiā, nǐ juéde zhù zài nǎge chéngshì zuì hǎo? Wèishéme?",
        "english": "If the teacher moves to your country, which city do you think is best to live in? Why?",
        "grammar": "V + 在 (e.g., 我覺得住在曼谷很方便)"
    },
    {
        "text": "從你家走到超市和學校大概要多久？",
        "pinyin": "Cóng nǐ jiā zǒu dào chāoshì hé xuéxiào dàgài yào duōjiǔ?",
        "english": "About how long does it take to walk from your home to the supermarket and school?",
        "grammar": "V + 到 (e.g., 從我家走到超市要十分鐘...)"
    },
    {
        "text": "有考試的時候，你平常念書念到幾點？",
        "pinyin": "Yǒu kǎoshì de shíhòu, nǐ píngcháng niànshū niàn dào jǐ diǎn?",
        "english": "When there is an exam, until what time do you usually study?",
        "grammar": "V + 到 (e.g., 我平常念書念到凌晨一點)"
    },
    {
        "text": "明年你家人生日的時候，你打算送什麼禮物給他們？",
        "pinyin": "Míngnián nǐ jiārén shēngrì de shíhòu, nǐ dǎsuàn sòng shénme lǐwù gěi tāmen?",
        "english": "Next year, for your family member's birthday, what gift do you plan to give them?",
        "grammar": "V + 給 (e.g., 我打算送給家人禮物)"
    },
    {
        "text": "我們坐幾點的高鐵？我的行李還沒準備好，是不是要快一點準備？",
        "pinyin": "Wǒmen zuò jǐ diǎn de gāotiě? Wǒ de xínglǐ hái méi zhǔnbèi hǎo, shì bù shì yào kuài yīdiǎn zhǔnbèi?",
        "english": "What time is the high-speed rail we are taking? My luggage isn't ready yet, should I hurry up and prepare it?",
        "grammar": "快一點 + V (e.g., 快一點準備行李)"
    },
    {
        "text": "我們是不是快要上課了？我們要不要走快一點？",
        "pinyin": "Wǒmen shì bù shì kuàiyào shàngkè le? Wǒmen yào bù yào zǒu kuài yīdiǎn?",
        "english": "Are we about to start class soon? Should we walk a little faster?",
        "grammar": "快一點 + V (e.g., 我們需要走快一點)"
    },
    {
        "text": "你記得我把剛買的檯燈放在哪裡嗎？",
        "pinyin": "Nǐ jìdé wǒ bǎ gāng mǎi de táidēng fàng zài nǎlǐ ma?",
        "english": "Do you remember where I put the desk lamp I just bought?",
        "grammar": "把 ＋ V在 (e.g., 你已經把檯燈放在臥室了)"
    },
    {
        "text": "摩托車不可以停在這裡，你可以把摩托車停到停車場去嗎？",
        "pinyin": "Mótuōchē bù kěyǐ tíng zài zhèlǐ, nǐ kěyǐ bǎ mótuōchē tíng dào tíngchēchǎng qù ma?",
        "english": "Motorcycles cannot be parked here. Can you park the motorcycle in the parking lot?",
        "grammar": "把 ＋ V到 (e.g., 我馬上把摩托車騎到停車場)"
    },
    {
        "text": "你下個月就要回國了，你打算把腳踏車送給誰？",
        "pinyin": "Nǐ xià gè yuè jiù yào huíguó le, nǐ dǎsuàn bǎ jiǎotàchē sòng gěi shéi?",
        "english": "You are going back to your country next month. Who do you plan to give your bicycle to?",
        "grammar": "把 ＋ V給 (e.g., 我打算把腳踏車送給朋友)"
    },
    {
        "text": "明天去你家的時候，我可以把我的貓一起帶過去嗎？",
        "pinyin": "Míngtiān qù nǐ jiā de shíhòu, wǒ kěyǐ bǎ wǒ de māo yīqǐ dài guòqù ma?",
        "english": "When I go to your house tomorrow, can I bring my cat over together?",
        "grammar": "把 ＋ Direction Verb (e.g., 你可以把貓帶進來)"
    },
    {
        "text": "這些都是台灣有名的東西，如果把它們寄回你的國家去，你家人會喜歡嗎？",
        "pinyin": "Zhèxiē dōu shì Táiwān yǒumíng de dōngxī, rúguǒ bǎ tāmen jì huí nǐ de guójiā qù, nǐ jiārén huì xǐhuān ma?",
        "english": "These are all famous Taiwanese things. If you send them back to your country, will your family like them?",
        "grammar": "把 ＋ Direction Verb ＋ 地方 (e.g., 我打算把這些東西寄回我家去)"
    },
    {
        "text": "外面下雨了，我覺得有點冷，你可以把窗戶關上嗎？",
        "pinyin": "Wàimiàn xiàyǔ le, wǒ juéde yǒudiǎn lěng, nǐ kěyǐ bǎ chuānghù guān shàng ma?",
        "english": "It's raining outside, and I feel a little cold. Can you close the window?",
        "grammar": "把 ＋ 放下/穿上/拿走/關上/打開 (e.g., 你可以把外套穿上)"
    },
    {
        "text": "你還住在以前的地方嗎？還是你爸媽已經把房子賣了？",
        "pinyin": "Nǐ hái zhù zài yǐqián de dìfāng ma? Háishì nǐ bàmā yǐjīng bǎ fángzi mài le?",
        "english": "Do you still live in the old place? Or have your parents already sold the house?",
        "grammar": "把 + O + V了 (e.g., 我爸媽把房子賣了)"
    },
    {
        "text": "睡覺時間到了，你怎麼還在看電視？可以快點把電視關一關嗎？",
        "pinyin": "Shuìjiào shíjiān dào le, nǐ zěnme hái zài kàn diànshì? Kěyǐ kuài diǎn bǎ diànshì guān yī guān ma?",
        "english": "It's bedtime, why are you still watching TV? Can you hurry up and turn off the TV?",
        "grammar": "把 ＋ V一V (e.g., 父母會說把電視關一關)"
    },
    {
        "text": "窗戶現在是不是開著的？我要開冷氣了，可以把它關起來嗎？",
        "pinyin": "Chuānghù xiànzài shì bù shì kāi zhe de? Wǒ yào kāi lěngqì le, kěyǐ bǎ tā guān qǐlái ma?",
        "english": "Is the window open right now? I want to turn on the AC, can you close it?",
        "grammar": "東西 ＋ V著 (e.g., 對，窗戶開著。我現在去關)"
    },
    {
        "text": "我到辦公室了，你的座位在哪裡？是不是桌上放著很多書的那一個？",
        "pinyin": "Wǒ dào bàngōngshì le, nǐ de zuòwèi zài nǎlǐ? Shì bù shì zhuō shàng fàng zhe hěn duō shū de nà yīgè?",
        "english": "I've arrived at the office, where is your seat? Is it the one with many books placed on the desk?",
        "grammar": "地方 ＋ V著 ＋ 東西 (e.g., 我桌子後面貼著一張我的照片)"
    },
    {
        "text": "那邊那麼多人，哪一個是你朋友？是穿著紅色衣服的那個人嗎？",
        "pinyin": "Nàbiān nàme duō rén, nǎ yīgè shì nǐ péngyǒu? Shì chuān zhe hóngsè yīfú de nàgè rén ma?",
        "english": "There are so many people over there, which one is your friend? Is it the person wearing red clothes?",
        "grammar": "人 ＋ V著 ＋ 東西 (e.g., 中間那個學生穿著紅色的衣服)"
    },
    {
        "text": "你今天怎麼那麼晚才回家？是不是騎車騎著騎著就迷路了？",
        "pinyin": "Nǐ jīntiān zěnme nàme wǎn cái huíjiā? Shì bù shì qí chē qí zhe qí zhe jiù mílù le?",
        "english": "Why did you come home so late today? Did you get lost while riding your bike?",
        "grammar": "S V1 O1，V1 著 V1 著，就 V2 O2了 (e.g., 我騎摩托車回家，騎著騎著，就迷路了)"
    },
    {
        "text": "你現在有空幫我把檯燈搬到樓上去嗎？還是你正忙著做別的事？",
        "pinyin": "Nǐ xiànzài yǒu kòng bāng wǒ bǎ táidēng bān dào lóushàng qù ma? Háishì nǐ zhèng máng zhe zuò bié de shì?",
        "english": "Are you free right now to help me move the desk lamp upstairs? Or are you busy doing something else?",
        "grammar": "忙著/急著 (e.g., 我沒有空，我急著去洗手間)"
    },
    {
        "text": "你是不是很久沒出國旅行了？寒假要不要一起去？",
        "pinyin": "Nǐ shì bù shì hěn jiǔ méi chūguó lǚxíng le? Hánjià yào bù yào yīqǐ qù?",
        "english": "Has it been a long time since you traveled abroad? Do you want to go together during winter break?",
        "grammar": "S ＋ 多久時間 ＋ 沒 ＋ VO ＋ 了 (e.g., 我一年沒有回國了，寒假我想回國)"
    },
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
        "text": "聽說明天要考試，真的嗎？我什麼都還沒念，是不是應該快一點去念書？",
        "pinyin": "Tīngshuō míngtiān yào kǎoshì, zhēn de ma? Wǒ shénme dōu hái méi niàn, shì bù shì yīnggāi kuài yīdiǎn qù niànshū?",
        "english": "I heard there's an exam tomorrow, really? I haven't studied anything at all, should I hurry up and go study?",
        "grammar": "快一點 + V"
    },
    {
        "text": "這些書很重，你可以幫我把它們搬上去嗎？",
        "pinyin": "Zhèxiē shū hěn zhòng, nǐ kěyǐ bāng wǒ bǎ tāmen bān shàngqù ma?",
        "english": "These books are very heavy, can you help me move them upstairs?",
        "grammar": "Verb + Direction Verb + 來/去"
    },
    {
        "text": "這裡風景好漂亮，我想拍照。你記得你把照相機放在哪裡了嗎？",
        "pinyin": "Zhèlǐ fēngjǐng hǎo piàoliang, wǒ xiǎng pāizhào. Nǐ jìdé nǐ bǎ zhàoxiàngjī fàng zài nǎlǐ le ma?",
        "english": "The scenery here is so beautiful, I want to take a picture. Do you remember where you put your camera?",
        "grammar": "S + 把 + O + V + 在 + 地方"
    },
    {
        "text": "老師說最慢今天要把功課交給他，你已經把功課寫完交給老師了嗎？",
        "pinyin": "Lǎoshī shuō zuì màn jīntiān yào bǎ gōngkè jiāo gěi tā, nǐ yǐjīng bǎ gōngkè xiě wán jiāo gěi lǎoshī le ma?",
        "english": "The teacher said the homework must be given to him by today at the latest. Have you finished it and handed it in?",
        "grammar": "S + 把 + O + V + 給 + 人"
    },
    {
        "text": "今天真的太熱了，你把冷氣打開了嗎？",
        "pinyin": "Jīntiān zhēn de tài rè le, nǐ bǎ lěngqì dǎkāi le ma?",
        "english": "It is really too hot today, did you turn on the air conditioner?",
        "grammar": "S + 把 + O + 打開"
    },
    {
        "text": "蛋糕在冰箱，你晚上會記得把它帶去朋友家嗎？",
        "pinyin": "Dàngāo zài bīngxiāng, nǐ wǎnshàng huì jìdé bǎ tā dài qù péngyǒu jiā ma?",
        "english": "The cake is in the fridge, will you remember to bring it to your friend's house tonight?",
        "grammar": "S + 把 + O + Verb + Direction Verb + 來/去"
    },
    {
        "text": "你週末為什麼不跟我們出去？你都在忙著做什麼？",
        "pinyin": "Nǐ zhōumò wèishéme bù gēn wǒmen chūqù? Nǐ dōu zài máng zhe zuò shénme?",
        "english": "Why aren't you going out with us this weekend? What are you busy doing?",
        "grammar": "S + 忙著 / 急著 + 做什麼"
    },
    {
        "text": "你怎麼還在念書？你是不是已經好幾天沒睡好覺了？",
        "pinyin": "Nǐ zěnme hái zài niànshū? Nǐ shì bù shì yǐjīng hǎo jǐ tiān méi shuì hǎo jiào le?",
        "english": "Why are you still studying? Have you not slept well for several days?",
        "grammar": "S + 多久時間 + 沒 + VO + 了"
    },
    {
        "text": "你看，公園中間放著什麼東西？",
        "pinyin": "Nǐ kàn, gōngyuán zhōngjiān fàng zhe shénme dōngxī?",
        "english": "Look, what is placed in the middle of the park?",
        "grammar": "地方 + V著 + S"
    },
    {
        "text": "你為什麼還不下班？你是不是已經有好幾個月沒準時下班了？",
        "pinyin": "Nǐ wèishéme hái bù xiàbān? Nǐ shì bù shì yǐjīng yǒu hǎo jǐ gè yuè méi zhǔnshí xiàbān le?",
        "english": "Why haven't you gotten off work yet? Have you not gotten off work on time for several months?",
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
        "text": "這是門口，汽車不可以停在這裡。你可以把車停到別的地方去嗎？",
        "pinyin": "Zhè shì ménkǒu, qìchē bù kěyǐ tíng zài zhèlǐ. Nǐ kěyǐ bǎ chē tíng dào bié de dìfāng qù ma?",
        "english": "This is the doorway, cars cannot park here. Can you park the car somewhere else?",
        "grammar": "S + 把 + O + V + 到 + 地方"
    },
    {
        "text": "為什麼你不想跟室友住在一起了？他總是做讓你受不了的事嗎？",
        "pinyin": "Wèishéme nǐ bù xiǎng gēn shìyǒu zhù zài yīqǐ le? Tā zǒngshì zuò ràng nǐ shòubùliǎo de shì ma?",
        "english": "Why don't you want to live with your roommate anymore? Does he always do things that you can't stand?",
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
        "text": "你上個月不是說要搬家嗎？為什麼後來沒搬呢？是不是原來找的房子有問題？",
        "pinyin": "Nǐ shàng gè yuè bú shì shuō yào bānjiā ma? Wèishéme hòulái méi bān ne? Shì bù shì yuánlái zhǎo de fángzi yǒu wèntí?",
        "english": "Didn't you say last month you were moving? Why didn't you move after all? Was there a problem with the original house you found?",
        "grammar": "原來 (yuánlái)"
    },
    {
        "text": "這個碗櫃，你覺得我把它搬到哪裡去比較好？",
        "pinyin": "Zhège wǎnguì, nǐ juéde wǒ bǎ tā bān dào nǎlǐ qù bǐjiào hǎo?",
        "english": "This cupboard, where do you think I should move it to?",
        "grammar": "S + 把 + O + V + 到 + 地方"
    },
    {
        "text": "你的衣服這麼髒，要不要趕快把它洗一洗？",
        "pinyin": "Nǐ de yīfú zhème zāng, yào bù yào gǎnkuài bǎ tā xǐ yī xǐ?",
        "english": "Your clothes are so dirty, do you want to hurry up and wash them?",
        "grammar": "Use 把 + O + V一V"
    },
    {
        "text": "為什麼他跑得那麼快？他正急著去哪裡嗎？",
        "pinyin": "Wèishéme tā pǎo de nàme kuài? Tā zhèng jí zhe qù nǎlǐ ma?",
        "english": "Why is he running so fast? Is he hurrying to go somewhere?",
        "grammar": "急著 + 做什麼"
    },
    {
        "text": "你平常都睡到幾點起床？沒有課的時候也一樣睡到中午嗎？",
        "pinyin": "Nǐ píngcháng dōu shuì dào jǐ diǎn qǐchuáng? Méiyǒu kè de shíhòu yě yīyàng shuì dào zhōngwǔ ma?",
        "english": "What time do you usually sleep until? Do you also sleep until noon when you don't have classes?",
        "grammar": "V + 到 + 時間"
    },
    {
        "text": "我明天需要用腳踏車，你可以把腳踏車借給我騎回家嗎？",
        "pinyin": "Wǒ míngtiān xūyào yòng jiǎotàchē, nǐ kěyǐ bǎ jiǎotàchē jiè gěi wǒ qí huíjiā ma?",
        "english": "I need to use a bicycle tomorrow. Can you lend me your bike to ride home?",
        "grammar": "把 + O + Verb + Direction Verb"
    },
    {
        "text": "我去你家玩的時候，可以把我的狗一起帶過去嗎？",
        "pinyin": "Wǒ qù nǐ jiā wán de shíhòu, kěyǐ bǎ wǒ de gǒu yīqǐ dài guòqù ma?",
        "english": "When I go to your house to hang out, can I bring my dog over together as well?",
        "grammar": "當然 / 把"
    }
]

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