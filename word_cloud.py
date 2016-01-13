#encoding=utf-8
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def wordcloudplot(txt):                    # 定义中文词云函数
    wordcloud = WordCloud(font_path='/Users/wdw/Library/Fonts/msyh.ttf', 
                          background_color="white",   #可以选择black或white
                          margin=15, width=1800, height=800) # 长宽度控制清晰程度​
    print dir(wordcloud)
    wordcloud = wordcloud.generate(txt)
    # Open a plot of the generated image.
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()


with open ('/Users/wdw/Desktop/work/data/data_tousu.txt') as f:
    t1 = f.read()

wordcloudplot(t1)
