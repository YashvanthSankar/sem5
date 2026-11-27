"""After filling experiments.csv, run: python3 make_graphs.py (no extra packages)."""
import csv
from pathlib import Path

HERE = Path(__file__).parent
with open(HERE / "experiments.csv", newline="") as file:
    rows = [{key: float(value) for key, value in row.items()}
            for row in csv.DictReader(file)]

if len(rows) < 4:
    raise SystemExit("Record at least 4 real transfers in experiments.csv first")

for row in rows:
    row["server_loss"] = row["packets_sent"] - row["packets_server"]
    row["receiver_loss"] = row["packets_server"] - row["packets_receiver"]
    row["overall_loss"] = row["packets_sent"] - row["packets_receiver"]

OUT = HERE / "graphs"
OUT.mkdir(exist_ok=True)


def graph(filename, title, x_name, series):
    width, height = 700, 420
    left, right, top, bottom = 80, 35, 55, 65
    xs = [row[x_name] for row in rows]
    ys = [row[y_name] for row in rows for y_name, _ in series]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(0, min(ys)), max(ys)
    x_span = x_max - x_min or 1
    y_span = y_max - y_min or 1

    def pos(row, y_name):
        x = left + (row[x_name] - x_min) / x_span * (width - left - right)
        y = height - bottom - (row[y_name] - y_min) / y_span * (height - top - bottom)
        return round(x, 1), round(y, 1)

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<text x="{width/2}" y="28" text-anchor="middle" font-size="18">{title}</text>',
             f'<path d="M{left} {top}V{height-bottom}H{width-right}" stroke="black" fill="none"/>',
             f'<text x="{width/2}" y="{height-15}" text-anchor="middle">{x_name}</text>',
             f'<text x="{left}" y="{height-bottom+20}">{x_min:g}</text>',
             f'<text x="{width-right-35}" y="{height-bottom+20}">{x_max:g}</text>',
             f'<text x="{left-55}" y="{top+5}">{y_max:g}</text>',
             f'<text x="{left-55}" y="{height-bottom}">{y_min:g}</text>']
    colors = ["#1f77b4", "#d62728", "#2ca02c"]
    for index, (y_name, label) in enumerate(series):
        ordered = sorted(rows, key=lambda row: row[x_name])
        points = " ".join(f"{x},{y}" for x, y in (pos(row, y_name) for row in ordered))
        color = colors[index]
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"/>')
        for row in ordered:
            x, y = pos(row, y_name)
            parts.append(f'<circle cx="{x}" cy="{y}" r="3" fill="{color}"/>')
        parts.append(f'<text x="{left+index*190}" y="{top+20}" fill="{color}">{label}</text>')
    parts.append("</svg>")
    (OUT / filename).write_text("\n".join(parts))


loss = [("server_loss", "server loss"), ("receiver_loss", "receiver loss"),
        ("overall_loss", "overall loss")]
graph("packet_size_loss.svg", "Packet size vs packet loss", "packet_size", loss)
graph("delay_loss.svg", "Delay vs packet loss", "delay_s", loss)
graph("packet_size_received.svg", "Packet size vs received file size", "packet_size",
      [("received_bytes", "received bytes")])
graph("delay_received.svg", "Delay vs received file size", "delay_s",
      [("received_bytes", "received bytes")])
graph("packet_size_time.svg", "Packet size vs transmission time", "packet_size",
      [("seconds", "seconds")])
print("Saved 5 graphs in", OUT)
