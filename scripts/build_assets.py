#!/usr/bin/env python3
"""Builds the README figures in assets/ for Thinker's Intelligence Laboratory.

Paper-and-ink style: every figure is a sheet of working notes, built in a light
and a dark variant (name.svg and name-dark.svg) for GitHub's two themes.
Standard library only. Run from anywhere:
    python scripts/build_assets.py
Edit the text below, re-run, commit the regenerated SVGs.
"""
import math
import os
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets")

SERIF = "Georgia,'Times New Roman',serif"
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"

THEMES = {
    "light": dict(PAPER="#f4efe4", INK="#1d1b17", SOFT="#6f695d", RULE="#cfc6b3", TINT="#e8e0cf",
                  RED="#c2362b", BLUE="#27508f", BLUSH="#f3d9d2"),
    "dark": dict(PAPER="#171613", INK="#ece6d8", SOFT="#a29a88", RULE="#3b382f", TINT="#26241e",
                 RED="#ee6f62", BLUE="#86aeea", BLUSH="#3d231f"),
}
PAPER = INK = SOFT = RULE = TINT = RED = BLUE = BLUSH = ""


def use(theme):
    """Select the palette. Figures are built once per theme."""
    globals().update(THEMES[theme])
    globals()["BASE_CSS"] = (
        f"text{{font-family:{SANS};fill:{INK}}}.serif{{font-family:{SERIF}}}.it{{font-style:italic}}"
        f".soft{{fill:{SOFT}}}.red{{fill:{RED}}}.blue{{fill:{BLUE}}}.caps{{letter-spacing:2.5px}}"
    )

BASE_CSS = ""


def sheet(title, height, body, css=""):
    t = escape(title, {'"': "&quot;"})
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="{height}" viewBox="0 0 1000 {height}" role="img" aria-label="{t}">\n'
        f"<title>{t}</title>\n"
        f'<defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r=".9" fill="{RULE}"/></pattern>'
        f'<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 1L10 5L0 9z" fill="{INK}"/></marker>'
        f'<marker id="arr-red" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 1L10 5L0 9z" fill="{RED}"/></marker></defs>\n'
        f"<style>{BASE_CSS}{css}</style>\n"
        f'<rect x=".5" y=".5" width="999" height="{height - 1}" rx="6" fill="{PAPER}" stroke="{RULE}"/>\n'
        f"{body}\n</svg>\n"
    )


def mindoo(x, y, scale):
    """MINDOO as an ink sketch (same proportions as the profile mascot)."""
    w = 2 / scale  # constant on-screen stroke
    return f"""<g transform="translate({x} {y}) scale({scale})" stroke="{INK}" stroke-width="{w:.2f}" stroke-linecap="round" stroke-linejoin="round">
<path d="M-26 140L-38 170M26 140L40 170" stroke-width="28"/><path d="M-26 140L-38 170M26 140L40 170" stroke="{TINT}" stroke-width="{28 - 2 * w:.2f}"/>
<ellipse cx="-43" cy="176" rx="26" ry="13" fill="{TINT}"/><ellipse cx="45" cy="176" rx="26" ry="13" fill="{TINT}"/>
<path d="M-45 76Q-87 70 -67 20M46 78L59 125" fill="none" stroke-width="21"/><path d="M-45 76Q-87 70 -67 20M46 78L59 125" fill="none" stroke="{TINT}" stroke-width="{21 - 2 * w:.2f}"/>
<rect x="-48" y="55" width="96" height="92" rx="37" fill="{TINT}"/>
<circle cy="87" r="12" fill="{PAPER}"/>
<g class="head"><rect x="-91" y="-43" width="182" height="106" rx="49" fill="{TINT}"/>
<rect x="-76" y="-30" width="152" height="78" rx="33" fill="{INK}" stroke="none"/>
<g class="eyes" fill="{PAPER}" stroke="none"><circle cx="-35" cy="9" r="8"/><circle cx="35" cy="9" r="8"/></g></g></g>"""


def density(components, x0, x1, base, n=160):
    """Path for a sum of Gaussian bumps; components = (centre 0..1, sd, height in px)."""
    pts = []
    for i in range(n + 1):
        g = i / n
        h = sum(a * math.exp(-0.5 * ((g - m) / s) ** 2) for m, s, a in components)
        pts.append(f"{x0 + g * (x1 - x0):.1f} {base - h:.1f}")
    return "M" + "L".join(pts)


# ------------------------------------------------------------------ banner
def banner():
    css = (
        ".head{animation:tilt 9s ease-in-out infinite;transform-box:fill-box;transform-origin:center}"
        ".eyes{animation:blink 5s infinite;transform-box:fill-box;transform-origin:center}"
        "@keyframes tilt{0%,45%,100%{transform:rotate(0deg)}60%,85%{transform:rotate(-9deg)}}"
        "@keyframes blink{0%,90%,96%,100%{transform:scaleY(1)}93%{transform:scaleY(.12)}}"
        ".c{fill:none;stroke-dasharray:1;stroke-dashoffset:1;animation:16s ease-in-out infinite}"
        ".c1{animation-name:d1}.c2{animation-name:d2}.c3{animation-name:d3}"
        "@keyframes d1{0%,2%{stroke-dashoffset:1}14%,94%{stroke-dashoffset:0;opacity:1}99%,100%{stroke-dashoffset:0;opacity:0}}"
        "@keyframes d2{0%,20%{stroke-dashoffset:1}36%,94%{stroke-dashoffset:0;opacity:1}99%,100%{stroke-dashoffset:0;opacity:0}}"
        "@keyframes d3{0%,46%{stroke-dashoffset:1}60%,94%{stroke-dashoffset:0;opacity:1}99%,100%{stroke-dashoffset:0;opacity:0}}"
        ".l{opacity:0;animation:16s infinite}.l1{animation-name:l1}.l2{animation-name:l2}.l3{animation-name:l3}"
        "@keyframes l1{0%,12%{opacity:0}16%,94%{opacity:1}99%,100%{opacity:0}}"
        "@keyframes l2{0%,34%{opacity:0}38%,94%{opacity:1}99%,100%{opacity:0}}"
        "@keyframes l3{0%,58%{opacity:0}63%,94%{opacity:1}99%,100%{opacity:0}}"
        "@media(prefers-reduced-motion:reduce){.head,.eyes{animation:none}.c{animation:none;stroke-dashoffset:0}.l{animation:none;opacity:1}}"
    )
    x0, x1, base = 600, 870, 360
    prior = density([(.5, .30, 46)], x0, x1, base)
    after_u = density([(.30, .085, 112), (.63, .10, 96)], x0, x1, base)
    after_q = density([(.30, .042, 226), (.63, .10, 8)], x0, x1, base)
    b = f"""<text x="40" y="45" font-size="12" class="caps" font-weight="700">THINKER’S INTELLIGENCE LABORATORY</text>
<text x="960" y="45" font-size="12" class="caps soft" text-anchor="end">WORKING NOTES · VOL. 0 · NOV 2026</text>
<path d="M40 58H960" stroke="{INK}" stroke-width="2"/><path d="M40 63H960" stroke="{INK}" stroke-width=".6"/>
<text x="38" y="140" font-size="48" class="serif">On learning what</text>
<text x="38" y="196" font-size="48" class="serif">a person <tspan class="it">means</tspan></text>
<text x="40" y="240" font-size="18" class="serif it soft">Notes on mathematics, learning machines,</text>
<text x="40" y="264" font-size="18" class="serif it soft">and the inference of human intent.</text>
<text x="40" y="308" font-size="13">Nguyen Thanh An <tspan class="soft">(thinker), with MINDOO</tspan></text>
<text x="40" y="346" font-size="11" class="caps soft">KEYWORDS</text>
<text x="40" y="366" font-size="12.5">machine learning · deep learning · mathematics</text>
<text x="40" y="384" font-size="12.5">theory of mind · pragmatics · calibration</text>
<rect x="580" y="84" width="380" height="304" fill="url(#dots)"/>
<text x="618" y="104" font-size="11" class="caps soft">FIG. 0</text><text x="668" y="104" font-size="12" class="serif it soft">belief over intent g</text>
<path d="M{x0 - 8} {base}H{x1 + 14}" stroke="{INK}" stroke-width="1.2" marker-end="url(#arr)"/>
<path d="M{x0} {base + 4}V{base - 250}" stroke="{INK}" stroke-width="1.2" marker-end="url(#arr)"/>
<text x="{x1 + 10}" y="{base + 20}" font-size="14" class="serif it">g</text>
<path class="c c1" pathLength="1" d="{prior}" stroke="{SOFT}" stroke-width="1.4"/>
<path class="c c2" pathLength="1" d="{after_u}" stroke="{BLUE}" stroke-width="1.8"/>
<path class="c c3" pathLength="1" d="{after_q}" stroke="{RED}" stroke-width="2.2"/>
<text class="l l1 serif it soft" x="822" y="328" font-size="13">prior</text>
<text class="l l2 serif it blue" x="792" y="252" font-size="13">after the request</text>
<g class="l l3"><text class="serif it red" x="716" y="148" font-size="14">after one question</text><path d="M712 144Q700 142 692 148" fill="none" stroke="{RED}" stroke-width="1.2" marker-end="url(#arr-red)"/></g>
{mindoo(926, 288, .38)}
<path d="M40 412H960" stroke="{INK}" stroke-width=".6"/>
<text x="40" y="438" font-size="14" class="serif it">Derive it. Build it. Break it. Ask the person.</text>
<text x="960" y="438" font-size="11" class="caps soft" text-anchor="end">TIL · TODAY I LEARNED</text>"""
    return sheet(
        "Thinker's Intelligence Laboratory, working notes. On learning what a person means: notes on mathematics, "
        "learning machines, and the inference of human intent. Figure: a belief over intent drawn as three curves, "
        "flat at first, two-peaked after the request, and sharp after one question. MINDOO watches from the corner.",
        460, b, css)


# ------------------------------------------------------------------ figure 1: strata
def research_map():
    layers = [  # top to bottom
        ("§7", "Human intent", "theory of mind · inverse planning · pragmatics", True),
        ("§6", "Acting under uncertainty", "MDP · POMDP · reinforcement learning · agents", False),
        ("§5", "Representations", "autograd · attention · training dynamics · probing", False),
        ("§4", "Learning from data", "risk minimization · kernels · Bayesian inference", False),
        ("§3", "Mathematics", "linear algebra · probability · optimization", False),
    ]
    cx, h, top = 350, 56, 58
    b = '<text x="40" y="38" font-size="11" class="caps soft">FIG. 1</text>'
    for i, (sec, name, kw, accent) in enumerate(layers):
        w = 250 + i * 80
        x, y = cx - w / 2, top + i * h
        fill = BLUSH if accent else (TINT if i % 2 else PAPER)
        b += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="1.2"/>'
        b += f'<text x="{cx}" y="{y + 34}" font-size="18" class="serif" text-anchor="middle">{escape(name)}</text>'
        b += f'<text x="{x - 14}" y="{y + 33}" font-size="13" class="{"red" if accent else "soft"}" text-anchor="end">{sec}</text>'
        b += f'<path d="M{x + w + 6} {y + h / 2}H664" stroke="{RULE}" stroke-width="1"/><circle cx="{x + w + 6}" cy="{y + h / 2}" r="2" fill="{SOFT}"/>'
        b += f'<text x="672" y="{y + 32}" font-size="12.5" class="soft">{escape(kw)}</text>'
    yb = top + 5 * h
    b += f'<path d="M22 {yb - 6}V{top + 10}" stroke="{RED}" stroke-width="1.2" marker-end="url(#arr-red)"/>'
    b += f'<text transform="translate(16 {yb - 60}) rotate(-90)" font-size="12" class="serif it red">each layer rests on the ones below</text>'
    return sheet(
        "Figure 1. Five strata stacked like a cross-section: mathematics at the base, then learning from data, "
        "representations, acting under uncertainty, and human intent at the top. Each layer rests on the ones below.",
        top + 5 * h + 30, b)


# ------------------------------------------------------------------ figure 2: intent
def intent():
    rows = [("cut total length by half", .38, .86), ("tighten the wording", .34, .08),
            ("turn it into bullets", .18, .04), ("shorten only the intro", .10, .02)]
    W = 230
    b = '<text x="40" y="38" font-size="11" class="caps soft">FIG. 2</text>'
    for lab, x in (("a", 40), ("b", 320), ("c", 680)):
        b += f'<text x="{x}" y="76" font-size="15" font-weight="700">{lab}</text>'
    b += f'<path d="M296 62V332M656 62V332" stroke="{RULE}"/>'
    # a
    b += '<text x="62" y="76" font-size="11" class="caps soft">REQUEST AND CONTEXT</text>'
    b += '<text x="40" y="124" font-size="23" class="serif it">“Can you make it</text><text x="40" y="154" font-size="23" class="serif it">shorter?”</text>'
    for i, t in enumerate(["900-word draft", "deadline is today", "said earlier: “the intro drags”"]):
        b += f'<text x="40" y="{204 + i * 24}" font-size="13" class="soft">–  {escape(t)}</text>'
    # b
    b += '<text x="342" y="76" font-size="11" class="caps soft">BELIEF OVER INTENTS</text>'
    for i, (name, before, after) in enumerate(rows):
        y = 108 + i * 52
        b += f'<text x="320" y="{y}" font-size="13">{escape(name)}</text>'
        b += f'<rect x="320.5" y="{y + 8.5}" width="{W * before:.1f}" height="8" fill="{PAPER}" stroke="{INK}"/>'
        b += f'<rect x="320" y="{y + 21}" width="{max(W * after, 2):.1f}" height="9" fill="{BLUE}"/>'
        b += f'<text x="{326 + W * before:.1f}" y="{y + 17}" font-size="11" class="soft">{before:.2f}</text>'
        b += f'<text x="{326 + max(W * after, 2):.1f}" y="{y + 30}" font-size="11" class="blue">{after:.2f}</text>'
    b += f'<rect x="320.5" y="313.5" width="14" height="8" fill="{PAPER}" stroke="{INK}"/><text x="342" y="322" font-size="11.5" class="soft">before asking</text>'
    b += f'<rect x="440" y="313" width="14" height="9" fill="{BLUE}"/><text x="462" y="322" font-size="11.5" class="soft">after the answer</text>'
    # c
    b += '<text x="702" y="76" font-size="11" class="caps soft">DECISION</text>'

    def node(y, label):
        return (f'<rect x="680.5" y="{y}.5" width="170" height="36" rx="18" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/>'
                f'<text x="765" y="{y + 23}" font-size="13.5" class="serif it" text-anchor="middle">{escape(label)}</text>')

    def leaf(x, y, label, note=None):
        s = f'<text x="{x}" y="{y}" font-size="13" font-weight="700" letter-spacing="1.5">{label}</text>'
        if note:
            s += f'<text x="{x}" y="{y + 18}" font-size="12.5" class="serif it red">{note}</text>'
        return s

    b += node(100, "max P(g | u, c) ≥ τ ?") + node(196, "EIG(q*) > κ ?")
    b += f'<path d="M854 118H892" stroke="{INK}" stroke-width="1.2" marker-end="url(#arr)"/><text x="872" y="111" font-size="11" class="soft" text-anchor="middle">yes</text>'
    b += f'<path d="M854 214H892" stroke="{INK}" stroke-width="1.2" marker-end="url(#arr)"/><text x="872" y="207" font-size="11" class="soft" text-anchor="middle">yes</text>'
    b += f'<path d="M765 138V192" stroke="{INK}" stroke-width="1.2" marker-end="url(#arr)"/><text x="775" y="169" font-size="11" class="soft">no</text>'
    b += f'<path d="M765 234V280" stroke="{INK}" stroke-width="1.2" marker-end="url(#arr)"/><text x="775" y="261" font-size="11" class="soft">no</text>'
    b += leaf(900, 122, "INFER", "after") + leaf(900, 218, "ASK", "before")
    b += '<text x="765" y="302" font-size="13" font-weight="700" letter-spacing="1.5" text-anchor="middle">ABSTAIN</text>'
    b += '<text x="765" y="320" font-size="11.5" class="soft" text-anchor="middle">say “I don’t know”</text>'
    return sheet(
        "Figure 2. (a) The request 'Can you make it shorter?' with its context. (b) Belief over four candidate intents "
        "before asking (0.38, 0.34, 0.18, 0.10) and after the answer (0.86, 0.08, 0.04, 0.02). (c) Decision tree: "
        "infer if the top belief clears a threshold, otherwise ask if the question is worth its cost, otherwise abstain.",
        352, b)


# ------------------------------------------------------------------ figure 3: the loop
def method():
    steps = [("Question", "a claim that could be false"), ("Derive", "by hand, assumptions named"),
             ("Implement", "minimal, from scratch"), ("Experiment", "seeds, baselines, spread"),
             ("Break", "find where it fails"), ("Write", "a note worth keeping")]
    cx, cy, rx, ry = 500, 200, 250, 112
    b = '<text x="40" y="38" font-size="11" class="caps soft">FIG. 3</text>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="{INK}" stroke-width="1.2"/>'
    for k in range(6):  # direction arrows between nodes
        t = math.radians(-120 + 60 * k)
        x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
        ang = math.degrees(math.atan2(ry * math.cos(t), -rx * math.sin(t)))
        b += f'<path transform="translate({x:.1f} {y:.1f}) rotate({ang:.1f})" d="M-6 -4.5L5 0L-6 4.5z" fill="{INK}"/>'
    for k, (name, cap) in enumerate(steps):
        t = math.radians(-150 + 60 * k)
        x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
        brk = name == "Break"
        col = RED if brk else INK
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{PAPER}" stroke="{col}" stroke-width="1.4"/>'
        b += f'<text x="{x:.1f}" y="{y + 4.5:.1f}" font-size="12.5" font-weight="700" text-anchor="middle" fill="{col}">{k + 1}</text>'
        if k in (1, 4):  # top / bottom
            ty = y - 44 if k == 1 else y + 40
            tx, anchor = x, "middle"
        else:
            right = k in (2, 3)
            tx, anchor, ty = (x + 26, "start", y - 1) if right else (x - 26, "end", y - 1)
        b += f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="19" class="serif" text-anchor="{anchor}" fill="{col}">{name}</text>'
        b += f'<text x="{tx:.1f}" y="{ty + 18:.1f}" font-size="12" class="soft" text-anchor="{anchor}">{cap}</text>'
    b += f'<text x="{cx}" y="{cy - 4}" font-size="16" class="serif it" text-anchor="middle">one study</text>'
    b += f'<text x="{cx}" y="{cy + 18}" font-size="12.5" class="serif it red" text-anchor="middle">every note ends in a question</text>'
    return sheet("Figure 3. One study as a loop of six steps: question, derive, implement, experiment, break, write. "
                 "The written note raises the next question.", 400, b)


def divider():
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="24" viewBox="0 0 1200 24" role="img" aria-label="Section break">'
        '<path d="M380 12H560M640 12H820" stroke="#8a8474" stroke-width="1"/>'
        '<g fill="#8a8474"><circle cx="584" cy="12" r="2.2"/><circle cx="600" cy="12" r="2.2"/><circle cx="616" cy="12" r="2.2"/></g></svg>\n'
    )


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    built = []
    for theme, suffix in (("light", ""), ("dark", "-dark")):
        use(theme)
        figures = {"banner": banner(), "research-map": research_map(), "intent": intent(), "method": method()}
        for name, svg in figures.items():
            with open(os.path.join(OUT, f"{name}{suffix}.svg"), "w", encoding="utf-8", newline="\n") as f:
                f.write(svg)
            built.append(f"{name}{suffix}.svg")
    with open(os.path.join(OUT, "divider.svg"), "w", encoding="utf-8", newline="\n") as f:
        f.write(divider())
    print("Built " + ", ".join(built + ["divider.svg"]))
