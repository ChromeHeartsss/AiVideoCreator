import openai
import json
from base64 import b64decode
from moviepy.editor import *
import requests
from moviepy.audio.fx import audio_fadein, audio_fadeout

additionalprompt = input('Enter approximately what vision you have for the clip? (for example, pictures drawn with paints or a color palette): ')
stringamount = int(input('Enter your song string amount: '))
songstrings = []

for i in range(stringamount):
    line = input(f"Введите строку {i + 1}: ")
    songstrings.append(line)

for line in songstrings:
    prompt = additionalprompt + line

    """prompt = input('The prompt: ')"""
    openai.api_key = ''

    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size='1024x1024',
    )

    with open('data.json', 'w') as file:
        json.dump(response, file, indent=4, ensure_ascii=False)

    # Проверьте наличие ключа 'data' и 'url' в ответе
    if 'data' in response and 'url' in response['data'][0]:
        image_url = response['data'][0]['url']
    # Вместо скачивания изображения, вы можете использовать URL для отображения или загрузки изображения по вашему выбору.
        print(f"Image URL: {image_url}")
    else:
        print("No 'data' or 'url' key found in the response.")

    response = requests.get(image_url)

    if response.status_code == 200:
    # Сохранить изображение в файл
        with open(f"image_{line}.png", "wb") as file:
            file.write(response.content)
        print("Изображение успешно загружено.")
    else:
        print("Ошибка при загрузке изображения.")

timdecodes = []

for i in range(stringamount):
    data = float(input(f"Set time code for {i + 1} line: "))  # Можно использовать float для чисел с плавающей точкой
    timdecodes.append(data)

print("Timecodes:")
for data in timdecodes:
    print(data)


clips = []

for i in range (len(songstrings)):
     clip = ImageClip(f'image_{songstrings[i]}.png').set_duration(timdecodes[i])  # Создаем клип с нужным именем и длительностью
     #text = TextClip(f'{songstrings[i]}', fontsize=30, color='white')
     #text = text.set_position(('center', 'bottom')).set_duration(timdecodes[i])
     clips.append(clip)  # Добавляем клип в список

#video_clips = [clips, text]

# Создаем итоговый видеоклип, объединяя все клипы
final_clip = concatenate_videoclips(clips, method="compose")

# Сохраняем итоговый видеоклип в файл
final_clip.write_videofile('result.mp4', fps=24)

video = VideoFileClip('result.mp4')
audio = AudioFileClip('song.mp3')

# Обрежьте аудио до длительности видео
audio = audio.subclip(0, video.duration)
video = video.set_audio(audio)

output_video = "video.mp4"
video.write_videofile(output_video, codec="libx264")

"""
clips_1 = ImageClip('1.jpg').set_duration(2)
clips_2 = ImageClip('2.jpg').set_duration(5)

final_clip= concatenate_videoclips([clips_1,clips_2], method='compose')
final_clip.write_videofile('result.mp4', fps = 24)
"""
