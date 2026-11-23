#!/usr/bin/env python3
"""Render the front page for the make.fun news-image-20261123 entry.

The picture sums up Sunday 23 November 2026 in one 1024x1024 PNG:
a masthead, one lead story, thirty stories grouped in seven region
sections, and a numbers strip whose figures all come from the
stories above it.  Rendering is deterministic - fixed data, fixed
fonts, no clock, no network - so entry.png is byte-stable.

Story selection: cross-checked against public reporting for
23 Nov 2026 (AP, Reuters, BBC, CNN, France 24, Xinhua, Oxfam/CEOBS,
Lean/Mathlib communities, Korea JoongAng Daily, UKMTO via CNN/ABC).
Single-source or earlier-dated items were dropped (the EU-Rwanda
return-centre plan of 16 Nov, Korea's $1tn export milestone of
19 Nov, the Shenzhen summit declaration of 19-20 Nov).  Where
reports disagreed the conservative figure is used: Khartoum
deaths (Al Jazeera 4, Radio Dabanga 5 children) and the Indonesia
missing (AP 34, Reuters about 30).  The Riemann item notes the
Lean certification and the published critique of one step.
"""

from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
MARGIN = 28
GUTTER = 16
PAPER = "#fdf6e3"
INK = "#111111"
GREY = "#444444"
RULE = "#d5cba8"
ACCENT = "#7b241c"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = FONT_DIR + "/DejaVuSerif-Bold.ttf"
SANS_BOLD = FONT_DIR + "/DejaVuSans-Bold.ttf"
SANS_PLAIN = FONT_DIR + "/DejaVuSans.ttf"


def load_font(path, size):
    return ImageFont.truetype(path, size)


# Each region: a banner title, its colour, and (headline, dek) pairs.
REGIONS = [
    dict(name="CLIMATE & DIPLOMACY", colour="#1a5276", items=[
        dict(h="COP31 ends with no deal",
             d="Antalya talks collapse after overtime rows over fossil fuels and finance."),
        dict(h="EU and 130 nations reject text",
             d="Draft without fossil-fuel language is refused; talks end in failure."),
        dict(h="Trump 'inclined' to strike Iran",
             d="President says he may resume strikes next year if no deal is reached."),
        dict(h="Thousands rally in Istanbul",
             d="March for press freedom after Sozcu TV raid, third media takeover in a year."),
    ]),
    dict(name="EUROPE & UKRAINE", colour="#7b241c", items=[
        dict(h="Dymer toll rises to 11",
             d="Drone strike on flats north of Kyiv; a teenager among the dead."),
        dict(h="Russian corvette sinks at Benghazi",
             d="Merkury capsizes after suspected Ukrainian sea-drone attack in Libya."),
        dict(h="Finland: war is spilling over",
             d="Sparta II towed out after Baltic drone fire; crew evacuated."),
        dict(h="Belgian airports shut",
             d="Controllers join anti-austerity strike; 429 flights cancelled."),
        dict(h="Drone debris falls on Kyiv schools",
             d="Early-morning attack; no casualties reported at the schools."),
    ]),
    dict(name="MIDDLE EAST", colour="#7e5109", items=[
        dict(h="Houthis claim Rabigh refinery strike",
             d="Group says it hit Saudi refinery and radar site; Riyadh silent."),
        dict(h="Hormuz attacks hit record high",
             d="31 attacks in October, 22 more by 22 Nov; three tankers struck."),
        dict(h="Gaza a 'toxic wasteland'",
             d="Oxfam report finds contamination signs across more than 99% of Gaza."),
        dict(h="Settlers torch cars in West Bank",
             d="Eisenkot calls overnight arson 'Jewish terrorism'."),
    ]),
    dict(name="ASIA-PACIFIC", colour="#145a32", items=[
        dict(h="Indonesia factory fire: 24 dead",
             d="Blaze at Banten candy factory; about 30 workers still missing."),
        dict(h="Taiwan bans short selling",
             d="Curbs take effect as TAIEX suffers its worst week in 35 years."),
        dict(h="AI sell-off rattles markets",
             d="S&P 500 falls 3.7%, Nikkei 5.06% on AI valuation fears."),
        dict(h="Korea minister quits over AI cheating",
             d="Education chief resigns after exam anti-cheating chaos; 111 caught."),
        dict(h="Asian governments rush market rescues",
             d="China cuts margins, Korea readies funds as AI rout spreads."),
    ]),
    dict(name="AMERICAS", colour="#4a235a", items=[
        dict(h="Democrats clinch 258 House seats",
             d="AP calls North Carolina race; largest majority since 1992."),
        dict(h="Delta delays 1,000+ flights",
             d="Weight-and-balance failure snarls Atlanta hub before Thanksgiving."),
        dict(h="Army to detonate lead azide in Iowa",
             d="68 barrels to be blown up despite court stay; 10,000 lbs at risk."),
        dict(h="Bolsonaro in intensive care",
             d="Ex-president stable with bowel obstruction; no discharge date set."),
    ]),
    dict(name="AFRICA", colour="#935116", items=[
        dict(h="Sudan drones hit Khartoum",
             d="Strikes hit homes and a UN building; at least 4 killed, children among them."),
        dict(h="South Sudan attack kills 24",
             d="Opposition raid on cattle camp in Warrap; 7 children among the dead."),
        dict(h="Ebola team trapped in DR Congo",
             d="Fighting traps WHO team in Ituri hospital; 5,678 dead in outbreak."),
    ]),
    dict(name="WORLD & CULTURE", colour="#1b4f72", items=[
        dict(h="Alcaraz wins first ATP Finals",
             d="Beats Zverev 6-2, 7-6 in Turin on Sunday."),
        dict(h="Márquez wins 8th MotoGP title",
             d="Equals Agostini's record with a round to spare."),
        dict(h="Liverpool thrash Man Utd 4-0",
             d="Pochettino's first match ends in humbling at Anfield."),
        dict(h="Riemann proof certified",
             d="Lean community certifies Alpöge's proof; a critique questions one step."),
        dict(h="Drug may 'cure' hormone blood pressure",
             d="Baxdrostat benefits last up to two years after treatment, study finds."),
    ]),
]

LEAD_HEAD = "COP31 COLLAPSES"
LEAD_DEK = "No deal in Antalya — fossil fuels sink the climate talks"
LEAD_LINE = ("Antalya, Turkey — after two days of overtime, "
             "nearly 200 countries left without an agreement.")
DATELINE = "Sunday 23 November 2026  •  30 stories  •  7 regions  •  All times UTC"

NUMBERS = [
    ("200", "countries at COP31"),
    ("258", "House seats for Democrats"),
    ("24", "dead in Indonesia fire"),
    ("11", "killed in Dymer strike"),
    ("429", "flights cut in Belgium"),
    ("99%", "of Gaza contaminated"),
]

# Which regions go in which column, chosen so the columns balance.
COLUMN_PLAN = [[0, 1], [2, 6, 5], [3, 4]]


class FrontPage:
    """Draws the whole page onto a fresh PIL image."""

    def __init__(self):
        self.img = Image.new("RGB", (PAGE, PAGE), PAPER)
        self.pen = ImageDraw.Draw(self.img)
        self.head_font = load_font(SANS_BOLD, 13)
        self.dek_font = load_font(SANS_PLAIN, 11)
        self.banner_font = load_font(SANS_BOLD, 12)

    def wrap(self, text, font, width):
        """Greedy word wrap measured with textbbox."""
        out, current = [], ""
        for word in text.split():
            trial = (current + " " + word).strip()
            box = self.pen.textbbox((0, 0), trial, font=font)
            if box[2] - box[0] <= width:
                current = trial
            else:
                if current:
                    out.append(current)
                current = word
        if current:
            out.append(current)
        return out

    def masthead(self):
        pen = self.pen
        pen.rectangle([0, 0, PAGE, 86], fill=INK)
        pen.text((MARGIN, 10), "THE WORLD", font=load_font(SERIF_BOLD, 46), fill=PAPER)
        pen.text((PAGE - MARGIN, 22), "IN ONE PICTURE",
                 font=load_font(SANS_BOLD, 20), fill="#f4d03f", anchor="ra")
        pen.text((PAGE - MARGIN, 50), "SUNDAY 23 NOVEMBER 2026",
                 font=load_font(SANS_BOLD, 14), fill=PAPER, anchor="ra")
        pen.text((MARGIN, 62), DATELINE, font=load_font(SANS_PLAIN, 12), fill="#bbbbbb")

    def lead(self, top):
        pen = self.pen
        pen.rectangle([MARGIN, top, PAGE - MARGIN, top + 104], outline=INK, width=2)
        pen.rectangle([MARGIN, top, MARGIN + 6, top + 104], fill=ACCENT)
        pen.text((MARGIN + 14, top + 6), LEAD_HEAD, font=load_font(SERIF_BOLD, 36), fill=ACCENT)
        pen.text((MARGIN + 14, top + 54), LEAD_DEK, font=load_font(SANS_BOLD, 17), fill=INK)
        pen.text((MARGIN + 14, top + 78), LEAD_LINE, font=load_font(SANS_PLAIN, 13), fill="#333333")
        return top + 118

    def region_block(self, x, y, width, region):
        pen = self.pen
        pen.rectangle([x, y, x + width, y + 26], fill=region["colour"])
        pen.text((x + 8, y + 5), region["name"], font=self.banner_font, fill="white")
        y += 32
        for item in region["items"]:
            for line in self.wrap(item["h"], self.head_font, width - 4):
                pen.text((x + 2, y), line, font=self.head_font, fill=INK)
                y += 15
            for line in self.wrap(item["d"], self.dek_font, width - 4):
                pen.text((x + 2, y), line, font=self.dek_font, fill=GREY)
                y += 13
            y += 4
            pen.line([x, y - 3, x + width, y - 3], fill=RULE, width=1)
        return y + 4

    def columns(self, top):
        width = (PAGE - 2 * MARGIN - 2 * GUTTER) // 3
        for index, plan in enumerate(COLUMN_PLAN):
            x = MARGIN + index * (width + GUTTER)
            y = top
            for region_no in plan:
                y = self.region_block(x, y, width, REGIONS[region_no])

    def numbers_strip(self, top):
        pen = self.pen
        pen.rectangle([MARGIN, top, PAGE - MARGIN, top + 96], outline=INK, width=2)
        pen.text((MARGIN + 12, top + 8), "THE DAY IN NUMBERS",
                 font=load_font(SANS_BOLD, 13), fill=INK)
        cell = (PAGE - 2 * MARGIN - 24) // 6
        label_font = load_font(SANS_PLAIN, 10)
        for i, (figure, label) in enumerate(NUMBERS):
            x = MARGIN + 12 + i * cell
            if i:
                pen.line([x - 9, top + 30, x - 9, top + 84], fill=RULE, width=1)
            pen.text((x, top + 30), figure, font=load_font(SERIF_BOLD, 26), fill=ACCENT)
            for row, line in enumerate(self.wrap(label, label_font, cell - 8)):
                pen.text((x, top + 62 + row * 12), line, font=label_font, fill=GREY)

    def footer(self):
        pen = self.pen
        y = PAGE - 26
        pen.line([MARGIN, y - 6, PAGE - MARGIN, y - 6], fill=INK, width=1)
        pen.text((MARGIN, y),
                 "Compiled from public reporting on 23 Nov 2026  •  COP31 Antalya  •  Benghazi  •  Hormuz  •  Turin",
                 font=load_font(SANS_PLAIN, 11), fill="#555555")
        pen.text((PAGE - MARGIN, y), "30 stories",
                 font=load_font(SANS_BOLD, 11), fill="#555555", anchor="ra")

    def render(self, path):
        self.masthead()
        body_top = self.lead(100)
        self.columns(body_top)
        self.numbers_strip(878)
        self.footer()
        self.img.save(path, format="PNG", optimize=True)


if __name__ == "__main__":
    FrontPage().render("entry.png")
