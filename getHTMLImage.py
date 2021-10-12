import os
import requests
from bs4 import BeautifulSoup


def getHTML(url: str):
    """引数で指定されたURLのHTML情報を取得(パース)する。

    Args:
        url (str): HTML情報取得対象のURLを指定する。

    Returns:
        (BeautifulSoup): BeautifulSoupオブジェクトに変換したHTML情報を返却する。
    """
    return BeautifulSoup(requests.get(url).content, 'lxml')


def getLinkObject(soup: BeautifulSoup):
    # ページに含まれるリンクを全て取得する
    links = [url.get('href') for url in soup.find_all('a')]
    # class が quote の div 要素を全て取得する
    #quote_elms = soup.find_all('div', {'class': 'quote'})
    return links


def getImageObject(soup: BeautifulSoup):
    # ページに含まれる画像リンクを全て取得する
    # TODO:HTMLの作りによっては、絶対パスと相対パスの画像リンクが混在する
    images = [url.get('src') for url in soup.find_all('img')]
    return images


def saveFile(imageList):

    # 各画像へのリンク先情報を保管したリストを引数に指定
    # これらのリンクをrequestsモジュールに渡し、get メソッドで画像を取得する

    # 保存先フォルダ
    save_path = './images/'

    # # ファイル名を連番にして保存
    # for i, image in enumerate(imageList):
    #     i += 100
    #     re = requests.get(image)
    #     i += 100
    #     with open(save_path + f'{i}.' + image.split('.')[-1], 'wb') as f:
    #         f.write(re.content)

    # 元々のファイル名で保存
    for url_image in enumerate(imageList):
        r_image = requests.get(url_image)
        filename_image = os.path.basename(url_image)
        with open(save_path + filename_image, 'wb') as f:
            f.write(r_image.content)


def main():
    url = 'http://quotes.toscrape.com/'

    soup = getHTML(url)

    links = getLinkObject(soup)
    print(links)

    images = getImageObject(soup)
    print(images)

    # saveFile(images)


if __name__ == '__main__':
    main()


# # 取得する画像を含む（画像が複数でも可）サイトの URL から HTML 情報を取得（パース）する。
# url = 'http://quotes.toscrape.com/'
# soup = getHTML(url)

# # そこで、soup.find_all('img') ですべての img タグを取得し、そのリンク先から画像の src タグを取得する。
# # 取得した複数画像を保管する空のリストを作成し、そのリストへ URL 内の画像コンテンツを保存して行く。
# # src リスト
# srclist = []
# try:
#     for link in soup.find_all('img'):
#         tmp = link.get('src')

#         # nullの場合はスキップ
#         if tmp is None:
#             continue

#         # 画像の保存場所が絶対パスでない場合はスキップ
#         if not tmp.startsWith('http'):
#             print(tmp)
#             continue

#         # 画像の拡張子が.jpg, .png, jpeg の場合に取得
#         if tmp.endswith('.jpg') or tmp.endswith('.png') or tmp.endswith('.jpeg'):
#             # print(tmp)
#             srclist.append(tmp)
# except:
#     print('error')

# # srcs を表示すると、各画像へのリンク先情報が保管されていることがわかる。
# print(srclist)

# # これらのリンクをrequestsモジュールに渡し、.get メソッドで画像を取得する。
# # 保存する画像名を「100(連番) + 元画像の拡張子」とする
# save_path = './images/'
# for i, image in enumerate(srclist):
#     re = requests.get(image)
#     i += 100
#     # image.split('.')[-1]：imageを.で分割し最後の要素を取得
#     with open(save_path + f'{i}.' + image.split('.')[-1], 'wb') as f:
#         f.write(re.content)
