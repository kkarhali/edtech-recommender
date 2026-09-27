"""Regenerate Figure 5.2 (cold-start-refit Precision@10 relative gain, one point per presentation).

Reads   results/run_artifacts/u11_s5_run_main/results_<pres>.json
        splits.primary.cells["A|2"].models.<model>["P@10"].mean   (model = Hybrid, CBF, ItemKNN-CF)
Writes  thesis/figures/figure_5_2_coldstart_relative_gain_spread.png   (1220 x 932)

Relative gain = (hybrid - baseline) / baseline. A presentation counts as a tie when
|hybrid - baseline| < 1e-12 (correction E2, decisions.log 2026-09-26; same tolerance as
thesis/tables/table_5_2_coldstart_refit_slice.md and table_5_14_condition_a_vs_b.md), so
floating-point summation-order differences (EEE_2014J +6.9e-18, FFF_2014B -3.5e-18) are ties,
not a win and a loss.

Counts, medians and ranges are computed from the files. The Holm p-values and the phase 1 pilot
numbers in the footer are quoted from Table 5.2 (they are not in the per-presentation files).

The PNG is drawn as SVG and rasterised by headless Chrome/Edge (no matplotlib/PIL in this
environment). Run from anywhere:
    PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 python thesis/figures/make_figure_5_2.py
"""

import glob
import json
import os
import shutil
import statistics
import subprocess
import sys
import tempfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "results" / "run_artifacts" / "u11_s5_run_main"
OUT = Path(__file__).resolve().parent / "figure_5_2_coldstart_relative_gain_spread.png"
CELL = "A|2"
TIE_TOL = 1e-12
W, H = 1220, 932

# Quoted, not computed (source: thesis/tables/table_5_2_coldstart_refit_slice.md).
P_HOLM_CF = "0.000241"
P_HOLM_CBF = "0.000241"
PILOT_LINE = ("THIS INVERTS THE UNRECEIPTED PHASE 1 PILOT, WHICH BEAT CBF ON COLD START IN 22 OF 22 "
              "(MEDIAN +73.12%, RANGE +13.55% TO +163.85%) AND LOST TO CF IN 22 OF 22 (MEDIAN -17.90%).")

BLUE, ORANGE, GRID, STRIPE, CONNECT = "#2158a8", "#cc6214", "#dddddd", "#f4f4f4", "#c8c8c8"
FONT = "Consolas, 'Lucida Console', 'DejaVu Sans Mono', monospace"


def load():
    rows = []
    for f in sorted(glob.glob(str(SRC / "results_*_20*.json"))):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        c = d["splits"]["primary"]["cells"][CELL]
        m = c["models"]
        h = m["Hybrid"]["P@10"]["mean"]
        rows.append({"pres": d["pres"], "n": c["n_scored"],
                     "cbf": (h, m["CBF"]["P@10"]["mean"]),
                     "cf": (h, m["ItemKNN-CF"]["P@10"]["mean"])})
    if len(rows) != 22:
        sys.exit(f"expected 22 presentations, found {len(rows)}")
    return rows


def summarise(rows, key):
    gains, w, t, l = [], 0, 0, 0
    for r in rows:
        h, b = r[key]
        gains.append((h - b) / b * 100.0)
        if abs(h - b) < TIE_TOL:
            t += 1
        elif h > b:
            w += 1
        else:
            l += 1
    return gains, w, t, l


def txt(x, y, s, size, fill="#000", anchor="start", spacing=1.0, weight="normal"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
            f'letter-spacing="{spacing}" font-weight="{weight}">{escape(s.upper()).replace("  ", "   ")}</text>')


def build_svg(rows):
    g_cbf, w_cbf, t_cbf, l_cbf = summarise(rows, "cbf")
    g_cf, w_cf, t_cf, l_cf = summarise(rows, "cf")
    med_cbf, med_cf = statistics.median(g_cbf), statistics.median(g_cf)
    n_total = sum(r["n"] for r in rows)
    print(f"vs CBF: median {med_cbf:+.2f}%  {w_cbf} W / {t_cbf} T / {l_cbf} L")
    print(f"vs CF : median {med_cf:+.2f}%  {w_cf} W / {t_cf} T / {l_cf} L")

    x0, x1, y0, row_h = 200, 1120, 150, 26
    y1 = y0 + row_h * len(rows) + 2
    allg = g_cbf + g_cf
    span = max(allg) - min(allg)
    lo, hi = min(allg) - 0.045 * span, max(allg) + 0.045 * span

    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="{FONT}" xml:space="preserve" style="white-space:pre">',
         f'<rect width="{W}" height="{H}" fill="#fff"/>']
    o.append(txt(22, 43, f"Figure 5.2  Cold-start-refit Precision@10 relative gain, one point per "
                 f"module presentation (N={len(rows)})", 19, spacing=1.35))
    o.append(txt(22, 62, f"OULAD, Precision@10, K=10, cold-start-refit slice at k=2 visible items "
                 f"(cell A|2, similarity model refitted without the held-out learners), {len(rows)} "
                 f"module presentations, {n_total} evaluated learners in total.", 9.5, spacing=0.55))
    o.append(txt(22, 81, "Source: results/run_artifacts/u11_s5_run_main/results_<pres>.json  -  "
                 "the slice and the medians that decide criteria C2 and C3 (Table 5.2).", 9.5, spacing=0.55))

    # plot frame, stripes, grid
    for i in range(len(rows)):
        if i % 2 == 0:
            o.append(f'<rect x="{x0}" y="{y0 + i * row_h}" width="{x1 - x0}" height="{row_h}" fill="{STRIPE}"/>')
    tick = int(lo // 40) * 40
    while tick <= hi:
        if tick >= lo:
            o.append(f'<line x1="{X(tick):.1f}" y1="{y0}" x2="{X(tick):.1f}" y2="{y1}" stroke="{GRID}"/>')
            o.append(txt(round(X(tick), 1), y1 + 17, f"{tick:+d}%" if tick else "0%", 10,
                         anchor="middle", spacing=0.8))
        tick += 40
    o.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="none" stroke="#999"/>')
    o.append(f'<line x1="{X(med_cbf):.1f}" y1="{y0}" x2="{X(med_cbf):.1f}" y2="{y1}" stroke="{BLUE}" '
             f'stroke-width="1.3" stroke-dasharray="4,3"/>')
    o.append(f'<line x1="{X(med_cf):.1f}" y1="{y0}" x2="{X(med_cf):.1f}" y2="{y1}" stroke="{ORANGE}" '
             f'stroke-width="1.3" stroke-dasharray="4,3"/>')
    o.append(f'<line x1="{X(0):.1f}" y1="{y0}" x2="{X(0):.1f}" y2="{y1}" stroke="#000" stroke-width="2"/>')

    # rows
    for i, r in enumerate(rows):
        cy = y0 + i * row_h + row_h / 2
        a, b = X(g_cbf[i]), X(g_cf[i])
        o.append(txt(22, cy + 6, r["pres"], 17, spacing=0.6))
        o.append(f'<line x1="{a:.1f}" y1="{cy}" x2="{b:.1f}" y2="{cy}" stroke="{CONNECT}"/>')
        o.append(f'<rect x="{a - 6:.1f}" y="{cy - 6}" width="12" height="12" fill="{BLUE}"/>')
        o.append(f'<polygon points="{b:.1f},{cy - 7} {b + 7:.1f},{cy} {b:.1f},{cy + 7} {b - 7:.1f},{cy}" '
                 f'fill="{ORANGE}"/>')

    # legend
    ly = y1 + 43
    o.append(f'<rect x="201" y="{ly - 9}" width="11" height="11" fill="{BLUE}"/>')
    o.append(txt(220, ly, f"Hybrid vs. CBF (blue square  dashed blue line = median {med_cbf:+.2f}%)", 10, spacing=0.8))
    o.append(f'<polygon points="670,{ly - 10} 677,{ly - 3} 670,{ly + 4} 663,{ly - 3}" fill="{ORANGE}"/>')
    o.append(txt(686, ly, f"Hybrid vs. ItemKNN-CF (orange diamond  dashed orange line = median {med_cf:+.2f}%)",
                 10, spacing=0.8))
    o.append(f'<line x1="206" y1="{ly + 9}" x2="206" y2="{ly + 21}" stroke="#000" stroke-width="2"/>')
    o.append(txt(220, ly + 18, "Solid black = 0% = the C2 threshold itself  C2 requires a positive median against "
                 "both baselines (pre-registered in plan.md, not moved)", 10, spacing=0.8))

    # footer (counts, medians and ranges computed above; p-values and pilot numbers quoted)
    ge_cbf_names = [r["pres"] for r in rows if r["cbf"][0] >= r["cbf"][1] - TIE_TOL]
    ge_cbf = len(ge_cbf_names)
    right_cf = w_cf
    on_zero = t_cf
    foot = [
        f"C2 is not met: it requires a positive median against both baselines. vs. CF the median is "
        f"{med_cf:+.2f}% ({w_cf} wins, {t_cf} ties, {l_cf} losses; tie = |diff| < 1e-12, correction E2; "
        f"p_holm {P_HOLM_CF})",
        f"vs. CBF it is {med_cbf:+.2f}% ({w_cbf} wins, {l_cbf} losses, p_holm {P_HOLM_CBF}), so the "
        f"both-baselines requirement fails on the threshold itself, not on significance.",
        f"The two series separate almost completely: the blue squares sit left of zero in {l_cbf} of 22 "
        f"presentations, the orange diamonds right of zero in {right_cf} of 22 and on it in {on_zero}.",
        f"C3 fails through the same conjunct: ge_cbf holds in only {ge_cbf} of 22 ({', '.join(ge_cbf_names)}), "
        f"while gt_mostpop, zero empty lists and coverage>=10% hold in 22 of 22.",
        PILOT_LINE,
        "(The often-quoted +190% is the pilot's warm gain over CBF, not a cold-start figure: correction E1, "
        "decisions.log 2026-09-24. Recomputed from inputs/prior_evidence/all_modules_metrics.json.)",
        "Absolute levels are low by construction: cold-start Precision@10 is 0.03-0.08 against a "
        "per-presentation ceiling_p10 of 0.648-0.943 (Table 5.2).",
    ]
    for k, line in enumerate(foot):
        o.append(txt(22, 826 + 15 * k, line, 9.5, spacing=0.6))
    o.append("</svg>")
    return "\n".join(o)


def find_browser():
    cands = [os.environ.get("CHROME"), shutil.which("chrome"), shutil.which("google-chrome"),
             shutil.which("chromium"), shutil.which("msedge"),
             r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"]
    for c in cands:
        if c and Path(c).exists():
            return c
    sys.exit("no Chrome/Edge found; set CHROME=<path>")


def main():
    svg = build_svg(load())
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "fig.html"
        page.write_text("<!doctype html><html><head><meta charset='utf-8'><style>html,body{margin:0;"
                        "padding:0;background:#fff;overflow:hidden}</style></head><body>" + svg +
                        "</body></html>", encoding="utf-8")
        shot = Path(tmp) / "shot.png"
        subprocess.run([find_browser(), "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--force-device-scale-factor=1", f"--user-data-dir={Path(tmp) / 'profile'}",
                        f"--window-size={W},{H}", f"--screenshot={shot}", page.as_uri()],
                       check=True, capture_output=True, timeout=120)
        shutil.copyfile(shot, OUT)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
