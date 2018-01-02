from PIL import Image,ImageFilter,ImageEnhance
import hashlib
import time
import numpy as np
import pytesseract
from operator import itemgetter

# 이미지의 256색중 비율이 높은것을 추려준다.
def RGB(image):
  values = {}
  his = image.histogram()
  j = []
  k = []
  for i in range(256):
    values[i] = his[i]
  for j,k in sorted(values.items(), key=itemgetter(1), reverse=True)[:10]:
   print(j,k)

#이미지 필터링 작업 >>  https://pillow.readthedocs.io/en/4.3.x/reference/ImageFilter.html << 상세설명 참고
def prepare_image(img):
    img = img.filter(ImageFilter.ModeFilter)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    img = img.filter(ImageFilter.SMOOTH_MORE)
    if 'L' != img.mode:
        img = img.convert('L') # L 은 이미지를 흑백모드로 변환시켜준다
    return img

# 이미지에서 불필요한 부분을 제거해준다.
def remove_noise(img, pass_factor):
    for column in range(img.size[0]):
        for line in range(img.size[1]):
            value = remove_noise_by_pixel(img, column, line, pass_factor)
            img.putpixel((column, line), value)
    return img

def remove_noise_by_pixel(img, column, line, pass_factor):
    if img.getpixel((column, line)) < pass_factor:
        return (0)
    return (255)

def noise_img(image_path, adjust_pixel):
    input_image = (image_path)
    output_image = 'out_' + input_image
    pass_factor = ""
    img = Image.open(input_image)
    img = img.convert("RGB")
    img = prepare_image(img)
    img = remove_noise(img, adjust_pixel)
    txt = pytesseract.image_to_string(img)
    print("OCR recognize test : ", txt)
    img.show()

    inletter = False
    foundletter = False
    start = 0
    end = 0

    letters = []

    for y in range(img.size[0]):  # slice across
        for x in range(img.size[1]):  # slice down
            pix = img.getpixel((y, x))
            if pix != 255:
                inletter = True

        if foundletter == False and inletter == True:
            foundletter = True
            start = y

        if foundletter == True and inletter == False:
            foundletter = False
            end = y
            letters.append((start, end))

        inletter = False

    count = 0
    for letter in letters:
        m = hashlib.md5()
        img2 = img.crop((letter[0], 0, letter[1], img.size[1]))
        m.update(b"%d,%d" % (time.time(), count))
        img2.save("./ABC\\%s.jpeg" % (m.hexdigest()))
        count += 1

def normal_img(image_path, pix1):
    img = Image.open(image_path)
    im2 = Image.new("P", img.size, 255)
    im = img.convert("L")
    RGB(im)

    temp = {}
    for x in range(im.size[1]):
        for y in range(im.size[0]):
            pix = im.getpixel((y, x))
            temp[pix] = pix
            if pix == pix1:
                im2.putpixel((y, x), 0)

    #im2 = im2.convert('RGB')      #이중 작업을 해야할 경우 사용
    #im2 = prepare_image(im2)
    #im2 = remove_noise(im2, 80)

    txt = pytesseract.image_to_string(im2)
    print("OCR recognize test : ", txt)
    im2.show()

    inletter = False
    foundletter = False
    start = 0
    end = 0

    letters = []

    for y in range(img.size[0]):  # slice across
     for x in range(img.size[1]):  # slice down
        pix = img.getpixel((y, x))
        if pix != 255:
             inletter = True

        if foundletter == False and inletter == True:
            foundletter = True
            start = y

        if foundletter == True and inletter == False:
            foundletter = False
            end = y
            letters.append((start, end))

        inletter = False

    count = 0

    for letter in letters:
        m = hashlib.md5()
        img2 = img.crop((letter[0], 0, letter[1], img.size[1]))
        m.update(b"%d,%d" % (time.time(), count))
        img2.save("./ABC/%s.jpeg" % (m.hexdigest()))
        count += 1

#noise_img("./sample\\766629.png",70) # 이미지파일, 노이즈 제거 강도 설정 80~150 적당
normal_img("./sample\\",86) # 이미지파일, 필터링할 pix값 지정

































