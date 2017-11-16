from bs4 import BeautifulSoup
import requests
import re
import wget
from subprocess import call
import argparse
# https://sdl-stickershop.line.naver.jp/stickershop/v1/sticker/17941023/IOS/sticker_animation@2x.png
# https://sdl-stickershop.line.naver.jp/stickershop/v1/sticker/17941023/android/sticker.png
def striphtml(data):
    p = re.search(r'\(http.+\);',data)
    return p.group(0)[1:-16].replace("android/sticker.png","IOS/sticker_popup.png")

def striphtml2(data):
    p = re.search(r'\(http.+\);',data)
    return p.group(0)[1:-16].replace("android/sticker.png","IOS/sticker_animation@2x.png")

def getNumber(data):
	p = re.findall(r'\d+', data)
	return p[1]

def crawl(product,isFull):
	r = requests.get('https://store.line.me/stickershop/product/' + product + '/zh-Hant')
	soup = BeautifulSoup(r.text, 'html.parser')
	imageArray = soup.findAll("span", { "class" : "mdCMN09Image" })
	i = 1
	call(["mkdir",product])
	for eachSpan in imageArray:
		imageUrl = ""
		tmpName = ""
		if isFull:
			imageUrl = striphtml(str(eachSpan))
			tmpName = "sticker_popup"
		else:
			imageUrl = striphtml2(str(eachSpan))
			tmpName = "sticker_animation"
		# imageUrl = str(eachSpan)
		print imageUrl
		fileNumber = getNumber(str(imageUrl))
		filename = wget.download(imageUrl)
		saveFilename = filename.replace(".png","").replace(tmpName,fileNumber) + ".gif"
		try:
			temp = call(["./apng2gif", filename,  "./" + product + "/" + saveFilename])
		except Exception, e:
			print "error"
			print e;
		print "temp"+str(temp)
		call(["rm","-rf" ,filename])
		i = i + 1

	call(['zip',"-r",product + ".zip", "./" + product])
	call(["rm","-rf" ,"./" + product])


def main():
	product = parse_args().product
	full = parse_args().full
	crawl(product,full)

def parse_args():
    parser = argparse.ArgumentParser(description='product')
    parser.add_argument("-p", "--product", help="product number", type=str, required=True) 
    parser.add_argument("-f", "--full", help="Is full popup image?", type=bool, required=False) 
    args = parser.parse_args()
    return args

if __name__ == '__main__':
	main()


