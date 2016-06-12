import matplotlib.pyplot as plt


colors = ['red', 'green', 'blue']
sizes  = [10, 20, 30] #[getattr(self, x) for x in colors]
patches, texts = plt.pie(sizes, colors=colors, startangle=90)
#plt.legend(patches, colors, loc="best")
plt.axis('equal')
plt.tight_layout()
plt.savefig('foo.png', bbox_inches='tight', transparent=True)

from PIL import Image
img = Image.open('foo.png', 'r')
img.thumbnail((128, 128), Image.ANTIALIAS)
img_w, img_h = img.size
background = Image.new('RGBA', (1440, 900), (255, 255, 255, 255))
bg_w, bg_h = background.size
offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
background.paste(img, offset, mask=img)
background.save('out.png')
