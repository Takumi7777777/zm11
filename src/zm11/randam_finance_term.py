import requests
from bs4 import BeautifulSoup
import urllib.parse
import openpyxl
import random
import os
import re 
# --- Yahoo!ニュースから情報を取得する関数 ---
def get_yahoo_news_titles(search_term=None):
    """
    Yahoo!ニュースからキーワードに関連するタイトルを取得します。
    キーワードが指定されない場合は、トップニュースのタイトルをいくつか取得します。
    """
    base_url = "https://news.yahoo.co.jp/"
    
    
    if search_term:
        search_encoded_term = urllib.parse.quote(search_term)
        url = f"https://news.yahoo.co.jp/search?p={search_encoded_term}&ei=UTF-8"
    else:
        url = base_url 

    try:
       
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() 

        soup = BeautifulSoup(response.text, 'html.parser')
        
        titles = []
        # Yahoo!ニュースのトップページまたは検索結果ページからタイトル要素を探す
        # ここはYahoo!ニュースのHTML構造変更によって頻繁に変わる可能性がある部分です。
        # 以下は2025年7月現在の一般的なYahoo!ニュースの構造を想定しています。
        
        # トップページの場合（主要な記事タイトル）
        if not search_term:
            
            for link in soup.find_all('a', class_=re.compile(r'newsLink|articleLink|sc-.*-link')):
                title_text = link.get_text(strip=True)
                if title_text and len(title_text) > 10 and not title_text.startswith(('PR', '広告')): # 短すぎるものやPRを除く
                    titles.append(title_text)
                if len(titles) >= 5: 
                    break
            
            # もし上記で見つからなければ、より一般的な方法で探す
            if not titles:
                for h2 in soup.find_all('h2'):
                    if h2.a and h2.a.get_text(strip=True) and len(h2.a.get_text(strip=True)) > 10:
                        titles.append(h2.a.get_text(strip=True))
                    if len(titles) >= 5:
                        break
                
                if not titles: # h2でも見つからなければpタグなどを探す
                    for p in soup.find_all('p', class_=re.compile(r'text|title')):
                         if p.get_text(strip=True) and len(p.get_text(strip=True)) > 10:
                            titles.append(p.get_text(strip=True))
                         if len(titles) >= 5:
                            break

        # 検索結果ページの場合
        else:
            # 検索結果のタイトルは、通常、特定のクラスを持つdivやh3の中のaタグにあることが多い
            # 例: <h2 class="newsFeed_item_title"><a href="..." class="newsFeed_item_link">タイトル</a></h2>
            for item in soup.find_all('li', class_=re.compile(r'SearchResult__listItem')): # 検索結果の各項目
                 title_tag = item.find(['h2', 'h3'], class_=re.compile(r'title|newsFeed_item_title'))
                 if title_tag and title_tag.a:
                    title_text = title_tag.a.get_text(strip=True)
                    if title_text and len(title_text) > 10 and not title_text.startswith(('PR', '広告')):
                        titles.append(title_text)
                    if len(titles) >= 5: # 例として5件まで取得
                        break
            
            # もし上記で見つからなければ、より一般的な方法で探す
            if not titles:
                for link in soup.find_all('a', class_=re.compile(r'newsLink|articleLink|sc-.*-link')):
                    title_text = link.get_text(strip=True)
                    if title_text and len(title_text) > 10 and not title_text.startswith(('PR', '広告')):
                        titles.append(title_text)
                    if len(titles) >= 5:
                        break


        if titles:
            return titles, url
        else:
            return ["関連するニュースタイトルが見つかりませんでした。"], url

    except requests.exceptions.RequestException as e:
        return [f"Yahoo!ニュースへのアクセス中にエラーが発生しました: {e}"], None
    except Exception as e:
        return [f"Yahoo!ニュースのデータの解析中にエラーが発生しました: {e}"], None

# --- 既存のExcel読み込みと統合する部分 ---
if __name__ == "__main__":
    excel_file_name = "finance words.xlsx" # あなたのExcelファイル名
    excel_file_path = os.path.join(os.path.dirname(__file__), excel_file_name)

    print("--- 金融用語ランダム表示＆Yahoo!ニュースツール ---")
    print("「hello」と入力するとランダムな用語が表示され、関連ニュースが検索されます。")
    print("終了するには「exit」と入力してください。")
    print("----------------------------------\n")

    while True:
        user_input = input("入力してください: ").strip().lower()

        if user_input == "hello":
            # Excelから用語リストを取得する
            all_excel_terms = []
            try:
                workbook = openpyxl.load_workbook(excel_file_path)
                sheet = workbook['Sheet1'] # あなたのシート名が'Sheet1'であることを確認
                
        
                start_row = 1
                end_row = 50 

                for row_num in range(start_row, end_row + 1):
                    term_from_excel = sheet[f"A{row_num}"].value 

                    if term_from_excel is not None:
                        # 先頭の番号とピリオド、スペースを取り除く正規表現
                        cleaned_term = re.sub(r'^\d+\.\s*', '', str(term_from_excel)).strip()
                        if cleaned_term: # クリーニング後も空でなければ追加
                            all_excel_terms.append(cleaned_term)

            except FileNotFoundError:
                print(f"エラー: '{excel_file_name}' が見つかりませんでした。スクリプトと同じディレクトリに置いてください。\n")
                all_excel_terms = []
            except KeyError:
                print(f"エラー: Excelファイルに 'Sheet1' という名前のシートが見つかりませんでした。シート名を確認してください。\n")
                all_excel_terms = []
            except Exception as e:
                print(f"Excelファイルの読み込み中に予期せぬエラーが発生しました: {e}\n")
                all_excel_terms = []

            if not all_excel_terms:
                print("Excelから用語リストが読み込めませんでした。ファイルパス、シート名、列などを確認してください。\n")
                continue # 次のループへ

            # Excelからランダムに用語を選ぶ
            selected_term = random.choice(all_excel_terms)

            # Yahoo!ニュースから情報を取得
            yahoo_news_titles, news_url = get_yahoo_news_titles(selected_term)

            print(f"\n今回のキーワードは: 「{selected_term}」です。")
            print(f"--- Yahoo!ニュース（「{selected_term}」関連）からのタイトル ---")
            for i, title in enumerate(yahoo_news_titles):
                print(f"{i+1}. {title}")
            
            if news_url:
                print(f"--- Yahoo!ニュース検索結果リンク ---\n{news_url}")
            
            print("\nこのキーワードについて1分間で話す練習をしましょう！\n")
        
        elif user_input == "exit":
            print("プログラムを終了します。お疲れ様でした！")
            break
        else:
            print("「hello」または「exit」と入力してください。\n")