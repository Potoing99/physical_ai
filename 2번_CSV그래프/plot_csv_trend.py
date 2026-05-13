import csv
import os
from datetime import datetime

INPUT_CANDIDATES = [
    "DailyDelhiClimateTrain.csv",
    "sample_daily_delhi_climate.csv",
]


def resolve_csv_path(arg_path=None):
    if arg_path and os.path.exists(arg_path):
        return arg_path
    for p in INPUT_CANDIDATES:
        if os.path.exists(p):
            return p
    for name in os.listdir('.'):
        if name.lower().endswith('.csv'):
            return name
    raise FileNotFoundError("CSV 파일을 찾을 수 없습니다.")


def read_rows(csv_path):
    rows = []
    with open(csv_path, 'r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        if 'date' not in reader.fieldnames or 'meantemp' not in reader.fieldnames:
            raise ValueError("필수 컬럼(date, meantemp)이 필요합니다.")
        for r in reader:
            try:
                d = datetime.fromisoformat(r['date'].strip())
                t = float(r['meantemp'])
                rows.append((d, t))
            except Exception:
                continue
    rows.sort(key=lambda x: x[0])
    if not rows:
        raise ValueError("유효한 데이터가 없습니다.")
    return rows


def create_svg(rows, out_svg):
    width, height = 1000, 420
    m = 50
    xs = [r[0] for r in rows]
    ys = [r[1] for r in rows]

    min_y, max_y = min(ys), max(ys)
    if min_y == max_y:
        min_y -= 1
        max_y += 1

    def px(i):
        if len(rows) == 1:
            return m
        return m + (width - 2 * m) * (i / (len(rows) - 1))

    def py(v):
        return height - m - (height - 2 * m) * ((v - min_y) / (max_y - min_y))

    points = " ".join(f"{px(i):.2f},{py(v):.2f}" for i, (_, v) in enumerate(rows))

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">')
    svg.append('<rect width="100%" height="100%" fill="white" />')
    svg.append(f'<text x="{m}" y="30" font-size="20" font-family="Arial">CSV 평균기온 추이 (meantemp)</text>')

    # axes
    svg.append(f'<line x1="{m}" y1="{height-m}" x2="{width-m}" y2="{height-m}" stroke="black"/>')
    svg.append(f'<line x1="{m}" y1="{m}" x2="{m}" y2="{height-m}" stroke="black"/>')

    # y ticks
    for i in range(6):
        v = min_y + (max_y - min_y) * i / 5
        y = py(v)
        svg.append(f'<line x1="{m-5}" y1="{y:.2f}" x2="{m}" y2="{y:.2f}" stroke="black"/>')
        svg.append(f'<text x="8" y="{y+4:.2f}" font-size="11" font-family="Arial">{v:.1f}</text>')

    # x labels (5개만)
    idxs = sorted(set([0, len(rows)//4, len(rows)//2, (len(rows)*3)//4, len(rows)-1]))
    for idx in idxs:
        x = px(idx)
        label = xs[idx].strftime('%Y-%m-%d')
        svg.append(f'<line x1="{x:.2f}" y1="{height-m}" x2="{x:.2f}" y2="{height-m+5}" stroke="black"/>')
        svg.append(f'<text x="{x-35:.2f}" y="{height-m+20}" font-size="10" font-family="Arial">{label}</text>')

    svg.append(f'<polyline fill="none" stroke="#2563eb" stroke-width="2" points="{points}"/>')
    svg.append('</svg>')

    with open(out_svg, 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))


def main():
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    csv_path = resolve_csv_path(arg)
    rows = read_rows(csv_path)
    out_svg = 'trend.svg'
    create_svg(rows, out_svg)
    print(f"[완료] 그래프 생성: {os.path.abspath(out_svg)}")
    print(f"[정보] CSV: {os.path.abspath(csv_path)}")
    print(f"[정보] 데이터 건수: {len(rows)}")


if __name__ == '__main__':
    main()
