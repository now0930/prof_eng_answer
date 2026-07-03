import os

def fix_mojibake(text):
    """문자열이 더 이상 변하지 않거나 에러가 발생할 때까지 반복해서 디코딩을 시도합니다."""
    current_text = text
    # 중첩된 깨짐(ÃƒÂƒ...)을 고려해 최대 10번 반복
    for _ in range(10):
        try:
            # 1바이트 문자열을 다시 바이트로 변환 후 UTF-8로 해석
            new_text = current_text.encode('latin1').decode('utf-8')
            if new_text == current_text:
                break
            current_text = new_text
        except (UnicodeEncodeError, UnicodeDecodeError):
            # 복구가 완료되어 한글 등 2바이트 이상 문자가 정상 등장하면 latin1 인코딩 시 에러 발생 -> 루프 종료
            break
            
    return current_text

def main():
    input_file = "./scripts/maintenance/import_review_design.py"
    output_file = "./scripts/import_review_design_fixed.py"

    print(f"[{input_file}] 파일을 읽어 다중 인코딩 복구를 시작합니다...")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        fixed_content = fix_mojibake(content)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
            
        print(f"완료되었습니다! 복구된 파이썬 스크립트가 [{output_file}]로 저장되었습니다.")
        print("파일을 열어 딕셔너리 내부의 한글(예: DC-DC 쵸퍼 등)이 정상적으로 보이는지 확인하세요.")
        
    except FileNotFoundError:
        print(f"오류: {input_file} 파일을 찾을 수 없습니다. 경로를 확인해 주세요.")
    except Exception as e:
        print(f"예기치 않은 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()
