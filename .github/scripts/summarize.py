import os
import sys
import json
from datetime import datetime
import openai

def get_title_from_md(content):
    """마크다운 파일의 첫 번째 줄에서 제목 추출"""
    first_line = content.split('\n')[0]
    return first_line.lstrip('#').strip()

def summarize_with_chatgpt(content, api_key):
    """ChatGPT API를 사용하여 내용 요약"""
    openai.api_key = api_key
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "TIL(Today I Learned) 문서의 내용을 2-3문장으로 간단히 요약해주세요. 핵심 내용과 중요 포인트를 중심으로 요약해주세요."
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"요약 중 오류가 발생했습니다: {str(e)}"

def main():
    if len(sys.argv) < 2:
        print("사용법: python summarize.py <파일_경로>")
        sys.exit(1)

    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY가 설정되지 않았습니다.")
        sys.exit(1)

    file_path = sys.argv[1]
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"파일을 읽는 중 오류가 발생했습니다: {str(e)}")
        sys.exit(1)

    title = get_title_from_md(content)
    summary = summarize_with_chatgpt(content, api_key)
    
    result = {
        "title": title,
        "path": file_path,
        "summary": summary
    }
    
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main() 