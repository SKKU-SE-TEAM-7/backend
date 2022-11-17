import base64

file = open('./txt.txt','w')
with open('./fig.png', 'rb') as img:
    base64_string = base64.b64encode(img.read())
    file.write(str(base64_string))