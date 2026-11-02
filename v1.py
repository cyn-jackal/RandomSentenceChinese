from gtts import gTTS
import os

exam_text = """
第一題。你的朋友想搬到台灣來，你覺得住在哪裡最好？
第二題。你今天睡覺睡到幾點？
第三題。聽說明天要考試，真的嗎？我什麼都還沒念。
第四題。這些書很重，你可以幫我嗎？
第五題。你的照相機呢？這裡風景好漂亮，我想拍照。
第六題。功課你寫完了嗎？老師說最慢今天要給他。
第七題。今天真的太熱了，開冷氣了嗎？
第八題。蛋糕在冰箱，你晚上記得帶去朋友家。
第九題。你週末為什麼不跟我們出去？
第十題。你怎麼還在念書？你不睡覺嗎？已經很晚了。
第十一題。公園裡的中間有什麼？
第十二題。你為什麼還不下班？工作很多嗎？
"""

# Generate the speech in Traditional Chinese (Taiwan accent mapping)
tts = gTTS(text=exam_text, lang='zh-TW')
tts.save("oral_exam_practice.mp3")
print("Audio saved as oral_exam_practice.mp3")