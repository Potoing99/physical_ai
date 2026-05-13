import os


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
        print(f"[생성] 폴더: {path}")
    else:
        print(f"[유지] 폴더 이미 존재: {path}")


def write_text(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[생성] 파일: {path}")


def main():
    base = os.getcwd()

    # 1) 하위 폴더 만들기
    for d in ['posts', 'assets', 'drafts']:
        ensure_dir(os.path.join(base, d))

    # 2) index.md 작성
    index_md = """# 블로그 시리즈 목차 (3편)

## 시리즈 주제: CSV 데이터로 시작하는 데이터 시각화

1. **1편 - CSV 데이터 읽기와 전처리 기초**
   - CSV 구조 이해
   - 필요한 컬럼 선택
   - 결측치/형변환 처리

2. **2편 - 추이 그래프(line chart) 만들기**
   - 시간축 데이터 정렬
   - 시계열 시각화 구성
   - 그래프 해석 포인트

3. **3편 - 결과 공유와 리포트 작성**
   - 그래프 결과 정리
   - 인사이트 문장화
   - 재현 가능한 실행 방법 정리
"""
    write_text(os.path.join(base, 'index.md'), index_md)

    # 3) post1.md 작성
    post1_md = """# 1편 초안: CSV 데이터 읽기와 전처리 기초

## 들어가며
데이터 분석의 시작은 대부분 CSV 파일입니다. 이번 글에서는 CSV를 읽고,
그래프를 그리기 전에 꼭 필요한 전처리 과정을 간단히 정리합니다.

## 1) CSV 구조 파악
먼저 헤더(컬럼명)를 확인하고, 어떤 컬럼을 사용할지 결정합니다.
예를 들어 기온 추이 분석이라면 date, meantemp 컬럼이 핵심입니다.

## 2) 컬럼 선택과 타입 변환
date는 날짜형으로, meantemp는 숫자형으로 다루어야 합니다.
타입이 맞지 않으면 그래프가 깨지거나 계산 결과가 잘못될 수 있습니다.

## 3) 결측치/이상치 처리
빈 값이 있는 행은 제거하거나 보정합니다.
극단값이 있다면 기준을 정해 제외 여부를 판단합니다.

## 마무리
전처리는 분석 품질을 좌우합니다.
다음 편에서는 정리된 데이터를 바탕으로 추이 그래프를 실제로 만들어보겠습니다.
"""
    write_text(os.path.join(base, 'post1.md'), post1_md)

    print("\n[완료] 3개 작업을 순서대로 처리했습니다.")


if __name__ == '__main__':
    main()
