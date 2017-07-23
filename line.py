from bs4 import BeautifulSoup
import requests
import re
import wget
from subprocess import call

# https://sdl-stickershop.line.naver.jp/stickershop/v1/sticker/17941023/IOS/sticker_animation@2x.png
# https://sdl-stickershop.line.naver.jp/stickershop/v1/sticker/17941023/android/sticker.png
def striphtml(data):
    p = re.search(r'\(http.+\);',data)
    return p.group(0)[1:-16].replace("android/sticker.png","IOS/sticker_animation@2x.png")

def getNumber(data):
	p = re.findall(r'\d+', data)
	return p[1]


product = "8358"
r = requests.get('https://store.line.me/stickershop/product/8358/zh-Hant')
soup = BeautifulSoup(r.text, 'html.parser')
imageArray = soup.findAll("span", { "class" : "mdCMN09Image" })
i = 1
call(["mkdir",product])
for eachSpan in imageArray:
	imageUrl = striphtml(str(eachSpan))
	print imageUrl
	fileNumber = getNumber(str(imageUrl))
	filename = wget.download(imageUrl)
	saveFilename = filename.replace(".png","").replace("sticker_animation@2x",fileNumber) + ".gif"
	call(["./apng2gif", filename,  "./" + product + "/" + saveFilename])
	call(["rm","-rf" ,filename])
	i = i + 1
	print(imageUrl + " success")

call(['zip',"-r",product + ".zip", "./" + product])
call(["rm","-rf" ,"./" + product])
# call(["rm","-rf" ,])

