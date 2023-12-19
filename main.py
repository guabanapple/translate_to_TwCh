from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import re


def is_japanese(word) -> bool:
    if word.isspace():
        return False

    code_regex = re.compile(
        "[!\"#$%&'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％]"
    )
    word = re.sub(code_regex, "", word)
    # 入力値に英数字が含まれないか
    return not re.search(r"[0-9a-zA-Z０-９Ａ-Ｚａ-ｚ]", word)


def get_word() -> str:
    while True:
        word = input("翻訳したい日本語単語を入力してください")
        if is_japanese(word):
            return word
        print("注意：漢字、ひらがな、カタカナ以外の文字を入力しないでください")


def set_driver():
    options = Options()
    options.add_argument("--headless")
    return webdriver.Chrome(options=options)


def get_result(url: str, word: str):
    driver = set_driver()
    try:
        driver.get(url)
        time.sleep(1.5)
        translated = driver.find_element(By.CLASS_NAME, "ryNqvb")
        result = translated.text
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None
    finally:
        driver.quit()
    return result


def main():
    word = get_word()
    url = (
        f"https://translate.google.co.jp/?hl=ja&sl=ja&tl=zh-TW&text={word}&op=translate"
    )
    result = get_result(url, word)
    if result:
        print(result)
    else:
        print("翻訳に失敗しました。")


if __name__ == "__main__":
    main()
