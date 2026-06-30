import json
import os

def fix_mojibake(text):
    """다중으로 잘못 인코딩된 문자열을 원래의 UTF-8 한글로 복구합니다."""
    if not isinstance(text, str):
        return text
    
    fixed_text = text
    # 다중으로 깨졌을 가능성을 고려해 최대 10번 반복 복구 시도
    for _ in range(10):
        try:
            # 깨진 문자를 1바이트(latin1)로 다시 변환 후 UTF-8로 디코딩
            new_text = fixed_text.encode('latin1').decode('utf-8')
            if new_text == fixed_text:
                break
            fixed_text = new_text
        except (UnicodeEncodeError, UnicodeDecodeError):
            # 더 이상 복구할 수 없거나 정상 문자열에 도달하면 중단
            break
            
    return fixed_text

def process_data(data):
    """JSON 구조를 순회하며 문자열 값만 찾아 복구 함수를 적용합니다."""
    if isinstance(data, dict):
        return {k: process_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [process_data(item) for item in data]
    elif isinstance(data, str):
        return fix_mojibake(data)
    else:
        return data

def main():
    input_file = "rubrics/model_answers/industrial_instrumentation_control.json"
    output_file = "rubrics/model_answers/industrial_instrumentation_control_fixed.json"

    print(f"[{input_file}] 파일을 읽어 인코딩 복구를 시도합니다...")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        fixed_data = process_data(data)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(fixed_data, f, ensure_ascii=False, indent=2)
            
        print(f"완료되었습니다. 복구된 파일이 [{output_file}]로 저장되었습니다.")
        
    except FileNotFoundError:
        print("입력 파일을 찾을 수 없습니다. 경로를 확인해 주세요.")
    except Exception as e:
        print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
