# coding:utf-8

from os import path
from PIL import Image
from collections import Counter
from wordcloud import WordCloud, STOPWORDS

import numpy as np
import matplotlib.pyplot as plt
import jieba



jieba.load_userdict(path.join(path.dirname(__file__),'userdict//userdict.txt')) # 支持导入用户自定义词典



def generate_wordcloud(text, shape, wordcloud_name):
    '''
    输入文本生成词云,如果是中文文本需要先进行分词处理
    '''
    # 设置显示方式
    d=path.dirname(__file__)
    shape = np.array(Image.open(path.join(d, shape)))
    font_path=path.join(d,"font//msyh.ttf")
    stopwords = set(STOPWORDS)
    wc = WordCloud(background_color="white",# 设置背景颜色
           max_words=2000, # 词云显示的最大词数  
           mask=shape,# 设置背景图片       
           stopwords=stopwords, # 设置停用词
           font_path=font_path, # 兼容中文字体，不然中文会显示乱码
                  )
    # 生成词云 
    wc.generate(text)
    # 生成的词云图像保存到本地
    wc.to_file(path.join(d, "doc//" + wordcloud_name + ".png"))
    # 显示图像
    plt.imshow(wc, interpolation='bilinear')
    # interpolation='bilinear' 表示插值方法为双线性插值
    plt.axis("off")# 关掉图像的坐标
    plt.show()



def word_segment(text):
    '''
    通过jieba进行分词并通过空格分隔,返回分词后的结果
    '''
    # 计算每个词出现的频率，并存入txt文件
    jieba_word=jieba.cut(text,cut_all=False) # cut_all是分词模式，True是全模式，False是精准模式，默认False
    data=[]
    for word in jieba_word:
        data.append(word)
    dataDict=Counter(data)
    with open('doc//词频统计.txt','w') as fw:
        for k,v in dataDict.items():
            fw.write("%s,%d\n" % (k,v))
    # 返回分词后的结果
    jieba_word=jieba.cut(text,cut_all=False) # cut_all是分词模式，True是全模式，False是精准模式，默认False
    seg_list=' '.join(jieba_word)
    return seg_list



if __name__=='__main__':

    print('请输入data_source目录下的数据文件名称(带后缀，目前仅支持.csv/.txt)')
    file_path = "data_source//" + input()


    # 判断文件的类型
    if file_path.endswith('.csv'):
        with open(file_path,'r') as f:
            text=f.read()
    elif file_path.endswith('.txt'):
        with open(file_path,'r',encoding='utf-8') as f:
            text=f.read()
    else:
        print('文件类型错误')
        exit(0)
    text=text.replace('\n','')
    

    print('请输入要生成的词云形状(输入序号并回车，例 1)')
    print('''
    请输入要生成的词云形状
    1.圆形
    2.方形
    3.长方形
    4.爱心
    '''
    )
    wordcloud_shape = input()


    # 创建字典
    shape_dict={"1":"shape//Round.png", "2":"shape//Square.png", "3":"shape//Rectangular.png", "4":"shape//Love.png"}


    # 判断词云形状
    if wordcloud_shape in shape_dict:
        shape=shape_dict[wordcloud_shape]
    else:
        print('词云形状错误')
        exit(0)


    # 输入输出词云的图片名称
    print('请输入要生成的词云图片名称(不带后缀)')
    wordcloud_name = input()


    # 若是中文文本，则先进行分词操作
    text = word_segment(text)
    

    # 生成词云
    generate_wordcloud(text, shape, wordcloud_name)

