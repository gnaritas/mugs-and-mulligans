#!/usr/bin/env python3
"""Mugs and Mulligans — template v2 T1 page generator (websites lane, 2026-11-23, t_6432ce1b).
All copy comes from the verified-facts card body + the shop's own published surfaces
(Facebook intro, Cash App order page, Google Maps listing) captured 2026-11-23.
Unknowns omitted (no phone published, no invented menu), never guessed.
Output: public/*.html + style.css + sitemap.xml + robots.txt. Canonical/OG pinned to the -demo host.
"""
import json, os

ORIGIN = "https://mugs-and-mulligans-demo.up.railway.app"
SITE = "Mugs and Mulligans"
LEGAL = "Mugs and Mulligans LLC"
FB = "https://www.facebook.com/profile.php?id=61591141137801"
MAIL = "mugsandmulligans@gmail.com"
CASH = "https://cash.app/$mugsandmulligans"
GEO_LAT, GEO_LON = 41.0622112, -75.9642927  # Google Maps place pin, 244 Sand Springs Dr #107B (read 2026-11-23)
MAPQ = "244+Sand+Springs+Dr+%23107B+Drums+PA+18222"
MAP_LINK = "https://maps.google.com/maps?q=" + MAPQ
ADDR1 = "244 Sand Springs Dr #107B"
BUILT = "<!-- BUILT-2026-11-23 -->"

MAP_EMBED = ('<iframe src="https://www.google.com/maps?q=' + MAPQ + '&output=embed" '
             'title="Map: Mugs and Mulligans, 244 Sand Springs Dr #107B, Drums, PA 18222" '
             'loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>')

MARK = ('<svg class="mark" viewBox="0 0 100 100" role="img" aria-label="Mugs and Mulligans emblem: a coffee mug with a putting flag">'
        '<rect x="14" y="42" width="52" height="40" rx="7" fill="none" stroke="currentColor" stroke-width="6"/>'
        '<path d="M66 50h9a10 10 0 0 1 0 20h-9" fill="none" stroke="currentColor" stroke-width="6"/>'
        '<path d="M39 40V12" stroke="currentColor" stroke-width="6" stroke-linecap="round"/>'
        '<path d="M39 12l22 8-22 8z" fill="#e0682b" stroke="none"/>'
        '<path d="M24 84c4-6 8-6 12 0s8 6 12 0 8-6 12 0" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" opacity=".7"/>'
        '</svg>')

# ---- hours exactly as posted on the owner's Cash App storefront + Google listing, captured 2026-11-23 ----
HOURS = [("Monday", "7 AM – 2 PM"), ("Tuesday", "7 AM – 2 PM"), ("Wednesday", "Closed"),
         ("Thursday", "Closed*"), ("Friday", "7 AM – 2 PM*"), ("Saturday", "8 AM – 1 PM"), ("Sunday", "8 AM – 1 PM")]
HOURS_CAPTION = ("Hours as posted on our Google listing and Cash App order page. "
                 "*Holiday weeks shift Thursday and Friday — closed Thanksgiving Day, open 7 AM–2 PM Black Friday.")

# ---- menu as published on the Cash App order page (cash.app/$mugsandmulligans, captured 2026-11-23) ----
MENU = [
    ("Featured", [
        ("Pumpkin Pie Latte", "$6.00–$8.00", "Latte with pumpkin-pie spice, steamed milk and espresso."),
        ("S'mores Cold Brew", "$6.00–$7.00", "Cold brew topped with smooth cold foam, flavored with marshmallow and chocolate.", True),
    ]),
    ("Signature", [
        ("The Bogey Booster", "$4.00–$4.50", "Peach-and-mint tea blended with lemonade and honey — fruity, citrusy, lightly sweet."),
        ("Shaken in the Rough", "$6.75", "Espresso shaken with brown sugar and oat milk — smooth, creamy, warm sweetness."),
        ("The Sweet Spot", "$6.00–$6.75", "Vanilla latte sweetened with rich caramel over espresso and steamed milk."),
        ("The Bun-ker", "$6.00–$6.75", "Cinnamon-bun latte: espresso, steamed milk and cinnamon-bun flavor."),
        ("The Nutty Caddie", "$6.00–$6.75", "Dark-chocolate latte with a nutty hazelnut finish, topped with steamed milk."),
        ("Frosted Cranberry", "$4.00", "Tart cranberry dirty soda with a sweet frosted coating."),
    ]),
    ("Build Your Own Coffee", [
        ("Hot Coffee", "$3.50–$4.00", "Rich, ready-to-enjoy cup — warm and comforting."),
        ("Cold Brew", "$5.00–$6.00", "Smooth cold brew, steeped slow. Convenient to take along.", True),
        ("Iced Coffee", "$4.50–$5.50", "Espresso base over ice, flash-chilled."),
        ("Latte", "$6.00–$6.75", "Espresso and steamed milk — balanced and creamy."),
        ("Americano", "$4.00–$4.50", "Espresso lengthened with hot water; take it black or add milk."),
        ("Mocha Latte", "$6.00–$6.75", "Espresso and chocolate with steamed milk — smooth with a hint of sweet."),
        ("Double Espresso", "$3.00", "Two shots — concentrated and strong."),
    ]),
    ("Non-Coffee Drinks", [
        ("Birdie Beverage", "$3.00", "12 oz iced lemonade or iced tea — your flavor of choice."),
        ("Fairway Fuel", "$6.00", "Ready-to-drink energy for early rounds and long shifts."),
        ("Dirty Alani", "$6.00", "Cotton-candy Alani topped with blue-raspberry cold foam."),
        ("Dirty Soda", "$4.00", "Fizzy mix with its own twist of flavor."),
        ("Hot Tea", "$2.50", "Soothing, warming cup all day."),
        ("Soda", "$1.50", "Can of soda."),
    ]),
    ("Food", [
        ("Italian Bagel Sandwich", "$5.99", "Ciabatta Italian — rustic, chewy, crisp crust."),
        ("Ham and Cheese Bagel", "$4.99", "Savory ham and melty cheese, toasted or not."),
        ("Bagel", "$2.50", "Toasted or not — with cream cheese, butter, or jelly."),
        ("Cinnamon Roll", "$4.50", "Warm, gooey center with sweet spiced flavor."),
        ("Jumbo Muffin", "$4.50", "Moist muffin, assorted flavors."),
        ("Apple Turnover", "$2.49", "Flaky crust, sweet apple filling, cinnamon-sugar dusting."),
        ("Scones", "$4.00", "Warm, flaky scone — a sidekick for your tea or coffee."),
    ]),
    ("Bottled Coffee Preorder · Pick-Up Wednesday 5–7 PM", [
        ("Tee\u2019d Up Latte", "$6.00", "Bottled cold latte — smooth coffee and creamy milk."),
        ("Tee\u2019d Up Cold Brew", "$5.00", "Bottled cold brew, brewed in-house for freshness."),
    ]),
    ("Other Merch", [
        ("Whole-Bean Coffee", "$15.00–$16.50", "Espresso roast with tasting notes of chocolate, caramel, and citrus."),
    ]),
]

def items_of(cat_name):
    for name, items in MENU:
        if name.startswith(cat_name):
            return items
    return []

# ---------------------------------------------------------------- head/CSS

def head(path, title, desc):
    canonical = ORIGIN + ("" if path == "/" else path)
    return (
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<title>' + title + '</title>\n'
        '<meta name="description" content="' + desc + '">\n'
        '<meta name="robots" content="noindex, nofollow">\n'
        '<link rel="canonical" href="' + canonical + '">\n'
        '<meta property="og:title" content="' + title + '">\n'
        '<meta property="og:description" content="' + desc + '">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:url" content="' + canonical + '">\n'
        '<meta property="og:image" content="' + ORIGIN + '/og.png">\n'
        '<meta property="og:site_name" content="' + SITE + '">\n'
        '<meta name="twitter:card" content="summary_large_image">\n'
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
        '<link rel="stylesheet" href="/style.css">\n'
        + BUILT + '\n</head>\n'
    )

NAV = (
    '<header class="site"><a class="skip" href="#main">Skip to content</a>'
    '<a class="brand" href="/">' + MARK +
    '<span class="brandname">Mugs <em>&amp;</em> Mulligans</span></a>'
    '<nav><a href="/">Home</a><a href="/menu">Menu</a><a href="/coffee">Coffee</a>'
    '<a href="/eats">Eats</a><a href="/visit">Visit</a><a href="/contact">Contact</a></nav>'
    '<a class="btn btn-order" href="' + CASH + '">Order ahead</a></header>'
)

def footer():
    return (
        '<footer class="site"><div class="cols">'
        '<div class="col"><span class="fbrand">Mugs <em>&amp;</em> Mulligans</span>'
        '<p class="tag">Hand-crafted &nbsp;·&nbsp; Locally Roasted &nbsp;·&nbsp; Good Grounds, Good Rounds</p>'
        '<p class="mini">Coffee shop in the Sand Springs community — freshly open since fall 2026, '
        'ribbon-cutting on Nov. 20. Early regulars rate us 5.0 on Google (21 reviews).</p>'
        '<a class="fb" href="' + FB + '">Find us on Facebook</a></div>'
        '<div class="col"><h4>Menu</h4><p><a href="/menu">Full menu</a><br><a href="/coffee">Coffee &amp; cold brew</a><br>'
        '<a href="/eats">Breakfast &amp; baked goods</a><br><a href="/visit">Hours &amp; directions</a></p></div>'
        '<div class="col"><h4>Order &amp; contact</h4><p><a href="' + CASH + '">Order ahead on Cash App</a><br>'
        '<a href="mailto:' + MAIL + '">' + MAIL + '</a><br><a href="/contact">Send a message</a></p></div>'
        '</div>'
        '<p class="footline">' + LEGAL + ' · ' + ADDR1 + ', Drums, PA 18222 · <a href="mailto:' + MAIL + '">' + MAIL + '</a> · '
        '<a href="/privacy">Privacy</a> · © 2026</p></footer>'
    )

def ld(data):
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + '</script>\n'

def webpage(path, name, desc):
    return {"@type": "WebPage", "@id": ORIGIN + path, "name": name, "description": desc,
            "url": ORIGIN + path, "isPartOf": {"@id": ORIGIN + "/#business"}}

def crumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": ORIGIN + p}
        for i, (n, p) in enumerate(items)]}

def page(path, title, desc, body, extra_head=""):
    return head(path, title, desc) + extra_head + body + footer() + "\n</html>\n"

def cta_band(kicker, line, sub=""):
    s = ('<section class="ctaband"><div class="wrap">'
         '<p class="kicker">' + kicker + '</p><h2>' + line + '</h2>')
    if sub:
        s += '<p class="sub">' + sub + '</p>'
    s += ('<p class="btns"><a class="btn btn-order" href="' + CASH + '">Order on Cash App</a>'
          '<a class="btn btn-ghost" href="/visit">Hours &amp; directions</a></p></div></section>')
    return s

# ---------------------------------------------------------------- pages

def page_home():
    feats = items_of("Featured")
    sig = items_of("Signature")
    def card(name, price, desc, sale=False):
        tag = '<span class="chip">Sale</span>' if sale else ''
        return ('<div class="itemcard"><div class="topline"><h3>' + name + '</h3>' + tag +
                '<span class="price">' + price + '</span></div><p>' + desc + '</p></div>')
    body = (
        '<main id="main"><section class="hero"><div class="wrap">'
        '<p class="eyebrow">Sand Springs · Drums, PA 18222 · Luzerne County</p>'
        '<h1>Good Grounds,<br><em>Good Rounds.</em></h1>'
        '<p class="lede">Hand-crafted, locally roasted coffee with a golf-side hangout at '
        + ADDR1 + ' — cold brew, bottled lattes, warm bagels, and cinnamon rolls in the Sand Springs community.</p>'
        '<p class="btns"><a class="btn btn-order" href="' + CASH + '">Order ahead on Cash App</a>'
        '<a class="btn btn-ghost" href="/menu">See the menu</a></p>'
        '<ul class="pills"><li>Hand-crafted</li><li>Locally roasted</li><li>Brewed in-house</li><li>Order ahead, pick up</li></ul>'
        '</div><div class="dimples" aria-hidden="true"></div></section>'
        '<section class="strip"><div class="wrap stripgrid">'
        '<div><p class="kicker">Cut to the chase</p><h2>A coffee shop that speaks golf.</h2>'
        '<p>Bogey Boosters and Nutty Caddies, Tee\u2019d Up cold brew and Shaken in the Rough — every drink on the board '
        'is hand-made to order, poured from locally roasted beans. Order on Cash App before you swing by; it\u2019s waiting '
        'when you get here.</p><p><a class="txtlink" href="/coffee">See the coffee program →</a> · '
        '<a class="txtlink" href="/eats">Breakfast board →</a></p></div>'
        '<div class="newnote"><p class="kicker">Just opened</p>'
        '<h2>Ribbon cut Nov. 20, 2026</h2>'
        '<p>Mugs and Mulligans opened its doors this fall in the Sand Springs area — '
        'the county health team cleared the build-out in October with zero violations, '
        'and the community came out for the Nov. 20 ribbon cutting.</p>'
        '<p class="rating"><strong>5.0 stars</strong> · 21 Google reviews · $1–10</p></div>'
        '</div></section>'
        '<section class="board"><div class="wrap">'
        '<p class="kicker">On the board today</p><h2 class="hcenter">The Featured Round</h2>'
        '<div class="itemgrid">' + card(*feats[0]) + card(*feats[1]) + '</div>'
        '<p class="fineprint">Prices as posted on our Cash App order page — sizes and add-ons change the total.</p>'
        '</div></section>'
        '<section class="board alt"><div class="wrap">'
        '<p class="kicker">From the scorecard</p><h2 class="hcenter">Signature Drinks</h2>'
        '<div class="itemgrid">' + ''.join(card(*it) for it in sig[:4]) + '</div>'
        '<p class="mini"><a class="txtlink" href="/menu">The full menu is here →</a></p>'
        '</div></section>'
        + cta_band("Before the first tee", "Skip the line — order ahead.",
                   "Order before you swing by — it\u2019s waiting at the counter. Bottled cold brew and lattes preorder for Wednesday pick-up, 5–7 PM.") +
        '<section class="visitmini"><div class="wrap vgrid">'
        '<div><p class="kicker">Find us</p><p class="addr">' + ADDR1 + '<br>Drums, PA 18222</p>'
        '<p class="mini">In the Sand Springs community, Luzerne County — look for the flag on the mug.</p>'
        '<p class="btns"><a class="btn btn-dark" href="' + MAP_LINK + '">Directions</a>'
        '<a class="btn btn-line" href="/visit">Hours &amp; details</a></p></div>'
        '<div class="map">' + MAP_EMBED + '</div></div></section></main>'
    )
    business = {
        "@context": "https://schema.org", "@type": "CafeOrCoffeeShop", "@id": ORIGIN + "/#business",
        "name": SITE, "url": ORIGIN + "/", "image": ORIGIN + "/og.png",
        "description": "Hand-crafted, locally roasted coffee shop in the Sand Springs community of Drums, PA — cold brew, bottled lattes, bagels and baked goods.",
        "address": {"@type": "PostalAddress", "streetAddress": "244 Sand Springs Drive, Unit 107B",
                    "addressLocality": "Drums", "addressRegion": "PA", "postalCode": "18222", "addressCountry": "US"},
        "geo": {"@type": "GeoCoordinates", "latitude": GEO_LAT, "longitude": GEO_LON},
        "priceRange": "$",
        "servesCuisine": ["Coffee", "Breakfast"],
        "openingHoursSpecification": [
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Monday", "opens": "07:00", "closes": "14:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Tuesday", "opens": "07:00", "closes": "14:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Friday", "opens": "07:00", "closes": "14:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "08:00", "closes": "13:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "08:00", "closes": "13:00"},
            {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Wednesday", "Thursday"], "opens": "00:00", "closes": "00:00"}
        ],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "21", "bestRating": "5"},
        "hasMenu": {"@type": "Menu", "name": "Mugs and Mulligans menu", "url": ORIGIN + "/menu"},
        "sameAs": [FB, CASH],
    }
    extra = ld(business) + ld({"@context": "https://schema.org", **webpage("/", "Mugs and Mulligans — Hand-Crafted Coffee in Drums, PA",
              "Golf-themed coffee shop at 244 Sand Springs Dr #107B, Drums, PA 18222. Locally roasted coffee, cold brew, bottled lattes, bagels and baked goods.")})
    return page("/", "Mugs and Mulligans — Hand-Crafted Coffee in Drums, PA",
                "Golf-themed coffee shop in the Sand Springs community — locally roasted coffee, cold brew, bottled lattes, and warm breakfast at 244 Sand Springs Dr #107B, Drums, PA 18222. Order ahead on Cash App.",
                NAV + body, extra)

def page_menu():
    rows = ''
    menu_items = []
    for cat, items in MENU:
        rowsh = ''
        for i, it in enumerate(items):
            name, price, desc = it[0], it[1], it[2]
            sale = len(it) > 3 and it[3]
            tag = '<span class="chip">Sale</span>' if sale else ''
            rowsh += ('<li class="scorerow"><span class="hole">' + str(i + 1) + '</span>'
                      '<div class="rowmain"><p class="rowtop"><strong>' + name + '</strong>' + tag +
                      '<span class="dots"></span><span class="price">' + price + '</span></p>'
                      '<p class="desc">' + desc + '</p></div></li>')
            menu_items.append({"@type": "MenuItem", "name": name, "description": desc,
                               "offers": {"@type": "Offer", "price": price.split("–")[0].strip("$"),
                                          "priceCurrency": "USD", "availability": "https://schema.org/InStock"}})
        rows += '<section class="cat"><h2>' + cat + '</h2><ol class="scorecard">' + rowsh + '</ol></section>'
    body = (
        '<section class="pagehero"><div class="wrap"><p class="eyebrow">The full card · ' + ADDR1 + ', Drums PA</p>'
        '<h1>The Scorecard</h1><p class="lede">Everything on the board — hand-crafted coffee, signature drinks, '
        'non-coffee picks, breakfast and baked goods, bottled brews and whole beans. Prices exactly as posted on '
        'our Cash App order page.</p>'
        '<p class="btns"><a class="btn btn-order" href="' + CASH + '">Order on Cash App</a></p></div></section>'
        '<main id="main" class="wrap menuwrap">' + rows +
        '<p class="fineprint">Cash App orders carry a posted 2.99% card surcharge. Bottled coffee preorders pick up Wednesday 5–7 PM. '
        'Menu rotates with the seasons — whatever\u2019s sold out, the barista will steer you somewhere good.</p></main>'
    )
    menu_ld = {
        "@context": "https://schema.org", "@type": "Menu", "@id": ORIGIN + "/menu#menu",
        "name": "Mugs and Mulligans menu", "url": ORIGIN + "/menu",
        "inCuisine": "American coffee-shop fare", "hasMenuItem": menu_items,
    }
    extra = ld(menu_ld) + ld({"@context": "https://schema.org", **webpage("/menu", "Coffee, Cold Brew & Food Menu — Mugs and Mulligans, Drums PA",
              "Hand-crafted coffee, signature drinks, breakfast and baked goods at Mugs and Mulligans in Drums, PA — prices as posted."  )}) \
        + ld({"@context": "https://schema.org", **crumbs([("Home", "/"), ("Menu", "/menu")])})
    return page("/menu", "Coffee, Cold Brew & Food Menu — Mugs and Mulligans, Drums PA",
                "The full menu at Mugs and Mulligans, Drums PA: hand-crafted coffee, signature golf-named drinks, breakfast bagels, baked goods, bottled cold brew and whole beans. Order ahead on Cash App.",
                NAV + body, extra)

def page_coffee():
    byo = items_of("Build Your Own")
    bottled = items_of("Bottled")
    def row(name, price, desc, sale=False):
        tag = '<span class="chip">Sale</span>' if sale else ''
        return ('<li class="scorerow"><div class="rowmain"><p class="rowtop"><strong>' + name + '</strong>' + tag +
                '<span class="dots"></span><span class="price">' + price + '</span></p>'
                '<p class="desc">' + desc + '</p></div></li>')
    body = (
        '<section class="pagehero"><div class="wrap"><p class="eyebrow">Locally roasted · Brewed in-house</p>'
        '<h1>The Coffee Program</h1><p class="lede">Hand-crafted drinks built on locally roasted beans — hot, iced, '
        'cold brew, and bottled to grab for the round.</p>'
        '<p class="btns"><a class="btn btn-order" href="' + CASH + '">Order on Cash App</a></p></div></section>'
        '<main id="main" class="wrap">'
        '<section class="cat"><h2>Build Your Own Coffee</h2><p class="introline">Start with the base — hot coffee, cold brew, '
        'iced coffee, latte, Americano, mocha, or a straight double espresso — and the barista builds it your way.</p>'
        '<ol class="scorecard">' + ''.join(row(*it) for it in byo) + '</ol></section>'
        '<section class="split"><div class="splitcol">'
        '<h2>Bottled Preorder</h2><p class="introline">Brewed in-house, bottled to keep, waiting at the counter: '
        'pick-up every Wednesday, 5–7 PM.</p><ol class="scorecard">' + ''.join(row(*it) for it in bottled) + '</ol></div>'
        '<div class="splitcol card"><h2>Take the Roast Home</h2>'
        '<p>Whole-bean bags from the espresso roast we serve — tasting notes of chocolate, caramel, and citrus. '
        'Grind it fine for the Moka pot or coarse for cold brew at home.</p>'
        '<p class="pricebig">Whole-Bean Coffee · $15.00–$16.50</p>'
        '<p class="btns"><a class="btn btn-dark" href="' + CASH + '">Grab a bag on Cash App</a></p></div></section>'
        '</main>'
        + cta_band("First tee tomorrow", "Order ahead — it\u2019s hot when you arrive.")
    )
    svc = {"@context": "https://schema.org", "@type": "Service", "@id": ORIGIN + "/coffee#service",
           "name": "Locally roasted coffee, cold brew & bottled preorder", "url": ORIGIN + "/coffee",
           "description": "Hot coffee, cold brew, iced coffee, lattes and Americanos made to order, plus bottled cold brew and lattes for Wednesday pick-up.",
           "provider": {"@id": ORIGIN + "/#business"},
           "areaServed": {"@type": "City", "name": "Drums", "containedInPlace": {"@type": "AdministrativeArea", "name": "Luzerne County, PA"}}}
    extra = ld(svc) + ld({"@context": "https://schema.org", **webpage("/coffee", "Locally Roasted Coffee & Bottled Cold Brew — Mugs and Mulligans, Drums PA",
              "Build-your-own coffee program: hot coffee, cold brew, iced coffee, mocha and espresso — plus bottled Tee'd Up cold brew and lattes for Wednesday pick-up.")}) \
        + ld({"@context": "https://schema.org", **crumbs([("Home", "/"), ("Coffee", "/coffee")])})
    return page("/coffee", "Locally Roasted Coffee & Bottled Cold Brew — Mugs and Mulligans, Drums PA",
                "Hand-crafted coffee at Mugs and Mulligans, Drums PA: hot coffee from $3.50, cold brew, iced coffee, mocha, bottled Tee'd Up lattes and whole beans. Order ahead on Cash App.",
                NAV + body, extra)

def page_eats():
    food = items_of("Food")
    def row(name, price, desc):
        return ('<li class="scorerow"><div class="rowmain"><p class="rowtop"><strong>' + name + '</strong>'
                '<span class="dots"></span><span class="price">' + price + '</span></p>'
                '<p class="desc">' + desc + '</p></div></li>')
    body = (
        '<section class="pagehero"><div class="wrap"><p class="eyebrow">Breakfast board · Until the case runs out</p>'
        '<h1>Eats &amp; Bakes</h1><p class="lede">Toasted bagels stacked high, gooey cinnamon rolls, apple turnovers '
        'and jumbo muffins — the breakfast lineup that pairs with every pour.</p>'
        '<p class="btns"><a class="btn btn-order" href="' + CASH + '">Order on Cash App</a></p></div></section>'
        '<main id="main" class="wrap">'
        '<section class="cat"><h2>Sandwiches &amp; Bagels</h2><ol class="scorecard">' +
        ''.join(row(*it) for it in food[:3]) + '</ol></section>'
        '<section class="cat"><h2>Baked Goods</h2><p class="introline">Out of the case by mid-morning — order ahead to make sure yours is waiting.</p>'
        '<ol class="scorecard">' + ''.join(row(*it) for it in food[3:]) + '</ol></section>'
        '<p class="fineprint">The croissant ham &amp; cheese sandwich comes back when the baker bakes it — check the board at the counter.</p>'
        '</main>'
        + cta_band("Breakfast rounds daily", "Bagel, sandwich, or roll — reserve it on Cash App.")
    )
    svc = {"@context": "https://schema.org", "@type": "Service", "@id": ORIGIN + "/eats#service",
           "name": "Breakfast sandwiches, bagels & baked goods", "url": ORIGIN + "/eats",
           "description": "Italian bagel sandwiches, ham and cheese bagels, cinnamon rolls, muffins, apple turnovers and scones at Mugs and Mulligans.",
           "provider": {"@id": ORIGIN + "/#business"},
           "areaServed": {"@type": "City", "name": "Drums", "containedInPlace": {"@type": "AdministrativeArea", "name": "Luzerne County, PA"}}}
    extra = ld(svc) + ld({"@context": "https://schema.org", **webpage("/eats", "Bagels, Sandwiches & Baked Goods — Mugs and Mulligans, Drums PA",
              "Breakfast at Mugs and Mulligans, Drums PA: ciabatta Italian bagel sandwiches, ham and cheese bagels, cinnamon rolls, turnovers and scones.")}) \
        + ld({"@context": "https://schema.org", **crumbs([("Home", "/"), ("Eats", "/eats")])})
    return page("/eats", "Bagels, Sandwiches & Baked Goods — Mugs and Mulligans, Drums PA",
                "Breakfast board at Mugs and Mulligans, Drums PA: Italian bagel sandwiches from $5.99, cinnamon rolls, jumbo muffins, apple turnovers and scones. Order ahead on Cash App.",
                NAV + body, extra)

def page_visit():
    hrs = ''.join('<tr><th scope="row">' + d + '</th><td>' + h + '</td></tr>' for d, h in HOURS)
    faqs = [
        ("What\u2019s the fastest way to order?",
         "Order ahead on <a href=\"" + CASH + "\">Cash App</a> — pick it up at the counter. Bottled cold brew and lattes preorder for Wednesday pick-up, 5–7 PM."),
        ("Do you roast your own coffee?",
         "Everything is hand-crafted and locally roasted. Bottled cold brew and lattes are brewed in-house, and the espresso roast is sold whole-bean by the bag."),
        ("Where exactly is the shop?",
         "244 Sand Springs Drive, Unit 107B in Drums, PA — the Sand Springs community in Luzerne County. Look for the mug-and-flag sign."),
        ("Is there a surcharge on card orders?",
         "Cash App orders carry a posted 2.99% card surcharge, per our order page policy."),
    ]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "@id": ORIGIN + "/visit#faq",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer",
                "text": a.replace('<a href="' + CASH + '">', '').replace('</a>', '')}} for q, a in faqs]}
    body = (
        '<section class="pagehero"><div class="wrap"><p class="eyebrow">Sand Springs Community · Luzerne County</p>'
        '<h1>Come Say Hi</h1><p class="lede">Corner-unit coffee shop at 244 Sand Springs Dr #107B — '
        'in and out fast between rounds, or settle in with a cinnamon roll and stay a while.</p>'
        '<p class="btns"><a class="btn btn-dark" href="' + MAP_LINK + '">Get directions</a>'
        '<a class="btn btn-order" href="' + CASH + '">Order on Cash App</a></p></div></section>'
        '<main id="main" class="wrap">'
        '<section class="visitgrid"><div class="card hourscard"><h2>This week\u2019s board</h2>'
        '<table class="hours"><tbody>' + hrs + '</tbody></table>'
        '<p class="fineprint">' + HOURS_CAPTION + '</p>'
        '<p class="rating"><strong>5.0 stars</strong> · 21 Google reviews · $1–10 per visit</p></div>'
        '<div class="card"><h2>The address</h2><p class="addr">' + ADDR1 + '<br>Drums, PA 18222-5501</p>'
        '<p class="mini">In the Sand Springs community, Luzerne County — the flag-on-mug sign marks the door. '
        'Questions before you drive? <a class="txtlink" href="mailto:' + MAIL + '">' + MAIL + '</a>.</p>'
        '<p class="btns"><a class="btn btn-line" href="' + FB + '">Our Facebook page</a></p></div></section>'
        '<section class="mapfull">' + MAP_EMBED + '</section>'
        '<section class="cat"><h2>Good questions</h2><dl class="faq">'
        + ''.join('<dt>' + q + '</dt><dd>' + a + '</dd>' for q, a in faqs) +
        '</dl></section>'
        '</main>'
        + cta_band("Coffee runs strong", "Order ahead, skip the line.", "Every drink hand-made — Cash App checkout means it's up when you pull up.")
    )
    svc = {"@context": "https://schema.org", "@type": "Service", "@id": ORIGIN + "/visit#service",
           "name": "Coffee shop & golf-side hangout", "url": ORIGIN + "/visit",
           "description": "Visit Mugs and Mulligans at 244 Sand Springs Dr #107B, Drums, PA 18222 — hours, directions and FAQs.",
           "provider": {"@id": ORIGIN + "/#business"},
           "areaServed": [{"@type": "City", "name": "Drums"}, {"@type": "City", "name": "Hazleton"}]}
    extra = ld(svc) + ld(faq_ld) + ld({"@context": "https://schema.org", **webpage("/visit", "Visit Mugs and Mulligans — 244 Sand Springs Dr, Drums, PA 18222",
              "Hours, directions and answers for Mugs and Mulligans, the golf-themed coffee shop in the Sand Springs community of Drums, PA.")}) \
        + ld({"@context": "https://schema.org", **crumbs([("Home", "/"), ("Visit", "/visit")])})
    return page("/visit", "Visit Mugs and Mulligans — 244 Sand Springs Dr, Drums, PA 18222",
                "Mugs and Mulligans at 244 Sand Springs Dr #107B, Drums, PA 18222: current hours, map, directions and FAQs. Order ahead on Cash App.",
                NAV + body, extra)

def page_contact():
    body = (
        '<section class="pagehero"><div class="wrap"><p class="eyebrow">Talk to the shop</p>'
        '<h1>Say Something</h1><p class="lede">Questions, catering rounds, big bottled orders — drop a note below, '
        'email us direct, or order on Cash App for anything you want to pick up.</p></div></section>'
        '<main id="main" class="wrap contactgrid">'
        '<form class="card form" method="post" action="/contact">'
        '<p class="field"><label for="f-name">Your name</label><input id="f-name" name="name" required maxlength="120"></p>'
        '<p class="field"><label for="f-phone">Phone (optional)</label><input id="f-phone" name="phone" type="tel" maxlength="60"></p>'
        '<p class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" maxlength="120"></p>'
        '<p class="field"><label for="f-msg">Message</label><textarea id="f-msg" name="message" required maxlength="4000" rows="6"></textarea></p>'
        '<p><button class="btn btn-order" type="submit">Send message</button></p>'
        '<p class="fineprint">We read every note. For orders, Cash App answers fastest.</p></form>'
        '<div class="side">'
        '<div class="card"><h2>Direct</h2><p><a class="txtlink" href="mailto:' + MAIL + '">' + MAIL + '</a><br>'
        '<a class="txtlink" href="' + CASH + '">Order on Cash App</a><br><a class="txtlink" href="' + FB + '">Facebook page</a></p></div>'
        '<div class="card"><h2>The shop</h2><p class="addr">' + ADDR1 + '<br>Drums, PA 18222</p>'
        '<p class="mini">' + HOURS_CAPTION + '</p></div>'
        '<div class="card map-mini">' + MAP_EMBED + '</div></div>'
        '</main>'
    )
    extra = ld({"@context": "https://schema.org", **webpage("/contact", "Contact — Mugs and Mulligans, Drums PA",
              "Contact Mugs and Mulligans in Drums, PA: message form, email, Cash App ordering, and the address at 244 Sand Springs Dr #107B.")}) \
        + ld({"@context": "https://schema.org", **crumbs([("Home", "/"), ("Contact", "/contact")])})
    return page("/contact", "Contact — Mugs and Mulligans, Drums PA",
                "Contact Mugs and Mulligans, Drums PA — send a message, email mugsandmulligans@gmail.com, or order ahead on Cash App.",
                NAV + body, extra)

def page_privacy():
    body = (
        '<section class="pagehero"><div class="wrap"><p class="eyebrow">Straight talk</p>'
        '<h1>Privacy</h1><p class="lede">Short, honest, and readable — what this site knows and what it does with it.</p></div></section>'
        '<main id="main" class="wrap prose">'
        '<h2>What we collect</h2><p>This site only collects what you send through the contact form: your name, '
        'an optional phone number, your email, and your message. It goes straight to the shop\u2019s inbox '
        '(<a href="mailto:' + MAIL + '">' + MAIL + '</a>) so a person can answer you.</p>'
        '<h2>What we don\u2019t do</h2><p>No advertising trackers, no analytics cookies, no pop-ups, no mailing-list '
        'sign-ups hiding in the footer. The interactive map uses Google\u2019s map embed, which may set its own cookies '
        'under Google\u2019s policy once you interact with it.</p>'
        '<h2>Your notes</h2><p>Messages are kept only as long as needed to answer you. To ask for a copy or a delete, '
        'email <a href="mailto:' + MAIL + '">' + MAIL + '</a> with "privacy" in the subject.</p>'
        '<h2>Who runs this page</h2><p>This website presents ' + LEGAL + ', ' + ADDR1 + ', Drums, PA 18222. '
        'Questions about this site or these terms: same email address.</p>'
        '<p class="fineprint">Effective November 2026.</p>'
        '</main>'
    )
    extra = ld({"@context": "https://schema.org", **webpage("/privacy", "Privacy Policy — Mugs and Mulligans, Drums PA",
              "Privacy for mugsandmulligans-demo.up.railway.app: what the contact form collects and what it never does.")}) \
        + ld({"@context": "https://schema.org", **crumbs([("Home", "/"), ("Privacy", "/privacy")])})
    return page("/privacy", "Privacy Policy — Mugs and Mulligans, Drums PA",
                "Privacy policy for the Mugs and Mulligans website: contact-form data only, no ad trackers, email the shop anytime.",
                NAV + body, extra)

def page_404():
    body = ('<a class="skip" href="#main">Skip to content</a><main id="main"><section class="lost"><div class="wrap">'
            '<p class="eyebrow">Out of bounds</p>'
            '<h1>404 — that page took a wrong swing.</h1>'
            '<p class="lede">The ball\u2019s in the trees somewhere. Back off to the fairway:</p>'
            '<p class="btns"><a class="btn btn-order" href="/">Home</a><a class="btn btn-line onpine" href="/menu">Menu</a>'
            '<a class="btn btn-line onpine" href="/contact">Contact the shop</a></p></div></section></main>' + footer())
    return head("/404", "Not found — Mugs and Mulligans, Drums PA", "Page not found at the Mugs and Mulligans site.") + body + "\n</html>\n"

def page_thanks():
    body = ('<a class="skip" href="#main">Skip to content</a><main id="main"><section class="lost"><div class="wrap">'
            '<p class="eyebrow">Message sent</p>'
            '<h1>Shot away, straight at the pin.</h1>'
            '<p class="lede">Your note is on its way to the shop inbox. If you\u2019re in a hurry, Cash App orders get '
            'answered fastest: <a class="txtlink" href="' + CASH + '">cash.app/$mugsandmulligans</a>.</p>'
            '<p class="btns"><a class="btn btn-order" href="/">Back to the menu</a>'
            '<a class="btn btn-line onpine" href="/contact">Send another note</a></p></div></section></main>' + footer())
    return head("/thanks", "Message sent — Mugs and Mulligans, Drums PA", "Your message was sent to Mugs and Mulligans.") + body + "\n</html>\n"

# ---------------------------------------------------------------- style

CSS = """:root{
  --pine:#0b1f14; --fairway:#17492e; --turf:#1f6a40; --cut:#3f8f5c;
  --cream:#f7f2e4; --paper:#fffdf6; --ink:#1e2a1f; --soft:#51614f;
  --line:#d9d0b6; --brass:#b9924e; --ball:#e0682b; --hole:#0e2a1a;
  --disp:Georgia,"Times New Roman",serif;
  --body:-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,"SF Mono",Consolas,"Courier New",monospace;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
.skip{position:absolute;left:-9999px;top:0;background:var(--fairway);color:var(--cream);padding:10px 18px;border-radius:0 0 10px 10px;z-index:99;font-family:var(--mono);font-size:13px}
.skip:focus{left:8px}
body{font-family:var(--body);color:var(--ink);background:
  repeating-linear-gradient(45deg,rgba(23,73,46,.035) 0 2px,transparent 2px 9px),var(--cream);
  line-height:1.55;font-size:17px}
a{color:var(--fairway)}
.wrap{max-width:1080px;margin:0 auto;padding:0 22px}
.kicker{font-family:var(--mono);font-size:12.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--turf);font-weight:700;margin-bottom:10px}
h1,h2,h3{font-family:var(--disp);line-height:1.08;letter-spacing:.01em}
h1{font-size:clamp(40px,6.4vw,72px)}
h2{font-size:clamp(26px,3.4vw,38px)}
h3{font-size:21px}
.btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}
.btn{display:inline-block;font-family:var(--mono);font-size:14px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
  padding:14px 24px;border-radius:999px;text-decoration:none;border:2px solid transparent;line-height:1}
.btn-order{background:var(--ball);color:#fff;border-color:var(--ball)}
.btn-order:hover{background:#c85a22;border-color:#c85a22}
.btn-ghost{background:transparent;color:var(--cream);border-color:rgba(247,242,228,.6)}
.btn-ghost:hover{border-color:var(--cream)}
.btn-dark{background:var(--fairway);color:var(--cream);border-color:var(--fairway)}
.btn-dark:hover{background:var(--turf);border-color:var(--turf)}
.btn-line{background:transparent;color:var(--fairway);border-color:var(--fairway)}
.btn-line:hover{background:var(--fairway);color:var(--cream)}
.btn-line.onpine{color:var(--cream);border-color:rgba(247,242,228,.6)}.btn-line.onpine:hover{background:var(--cream);color:var(--pine)}
.txtlink{font-weight:600;color:var(--turf);text-decoration:underline;text-decoration-color:rgba(31,106,64,.45);text-underline-offset:3px}

/* header */
header.site{position:sticky;top:0;z-index:40;display:flex;align-items:center;gap:18px;flex-wrap:wrap;
  background:rgba(247,242,228,.94);backdrop-filter:blur(8px);border-bottom:2px solid var(--fairway);padding:10px 22px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--pine)}
.mark{width:44px;height:44px;color:var(--fairway);flex:none}
.brandname{font-family:var(--disp);font-size:23px;font-weight:700;letter-spacing:.02em}
.brandname em{font-style:normal;color:var(--brass)}
nav{display:flex;gap:2px;flex-wrap:wrap;margin-left:auto}
nav a{font-family:var(--mono);font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;
  color:var(--ink);padding:9px 11px;border-radius:8px}
nav a:hover{background:rgba(31,106,64,.12);color:var(--fairway)}
header .btn-order{padding:11px 18px;font-size:12.5px}

/* hero */
.hero{position:relative;background:
  radial-gradient(1100px 480px at 85% -8%,rgba(63,143,92,.25),transparent 62%),
  radial-gradient(700px 420px at -5% 108%,rgba(224,104,43,.16),transparent 60%),
  var(--pine);color:var(--cream);overflow:hidden;border-bottom:6px solid var(--cut)}
.hero .wrap{position:relative;z-index:2;padding:84px 22px 76px;max-width:1080px}
.hero h1{color:var(--cream)}
.hero h1 em{color:#ffd98a;font-style:italic}
.eyebrow{font-family:var(--mono);font-size:12.5px;letter-spacing:.22em;text-transform:uppercase;color:#8fbf9f;margin-bottom:14px}
.lede{font-size:19.5px;max-width:640px;margin-top:20px;color:rgba(247,242,228,.92)}
.hero .lede{color:rgba(247,242,228,.9)}
.dimples{position:absolute;inset:0;opacity:.5;background-image:
  radial-gradient(circle at 25% 30%,rgba(255,255,255,.14) 0 2.2px,transparent 3px),
  radial-gradient(circle at 70% 62%,rgba(255,255,255,.10) 0 2.2px,transparent 3px);
  background-size:34px 34px,47px 47px;pointer-events:none}
.pills{list-style:none;display:flex;gap:9px;flex-wrap:wrap;margin-top:26px}
.pills li{font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase;
  border:1px solid rgba(185,146,78,.55);color:#ffd98a;border-radius:999px;padding:8px 15px}

/* page hero */
.pagehero{background:linear-gradient(180deg,var(--pine),var(--fairway));color:var(--cream);border-bottom:5px solid var(--cut);padding:54px 0 46px}
.pagehero h1{color:var(--cream)}
.pagehero .lede{color:rgba(247,242,228,.88)}

/* strips & boards */
.strip{background:var(--paper);border-bottom:1px solid var(--line);padding:54px 0}
.stripgrid{display:grid;grid-template-columns:1.25fr .85fr;gap:40px;align-items:start}
.newnote{background:var(--cream);border:1px solid var(--line);border-top:4px solid var(--brass);border-radius:12px;padding:24px 24px 20px}
.rating{font-size:15.5px;color:var(--soft)}
.rating strong{color:var(--brass);font-family:var(--disp);font-size:20px}
.board{padding:58px 0}
.board.alt{background:var(--paper);border-block:1px solid var(--line)}
.hcenter{text-align:center}
.itemgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px;margin-top:26px}
.itemcard{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:20px;box-shadow:0 2px 0 rgba(14,42,26,.06)}
.board.alt .itemcard,.menuwrap .itemcard{background:var(--cream)}
.itemcard .topline{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.itemcard h3{flex:1 1 auto}
.price{font-family:var(--mono);font-size:14.5px;font-weight:700;color:var(--fairway);white-space:nowrap}
.chip{font-family:var(--mono);font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;background:var(--ball);color:#fff;padding:3px 8px;border-radius:999px}
.itemcard p{font-size:15px;color:var(--soft);margin-top:8px}
.fineprint{font-size:13.5px;color:var(--soft);margin-top:16px}
.mini{font-size:14.5px;color:var(--soft)}

/* scorecard menu */
.menuwrap{padding:38px 22px 46px}
.cat{margin:34px 0 0}
.cat h2{color:var(--pine);border-bottom:2px solid var(--cut);padding-bottom:8px;display:flex;align-items:baseline;gap:12px}
.introline{color:var(--soft);font-size:15.5px;margin-top:10px}
.scorecard{list-style:none;margin-top:18px;background:var(--paper);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.scorerow{display:flex;gap:0;border-bottom:1px dashed var(--line)}
.scorerow:last-child{border-bottom:none}
.hole{flex:none;width:46px;display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:12px;font-weight:700;
  color:var(--cream);background:radial-gradient(circle,var(--hole) 55%,var(--fairway) 56%);margin:0;background:var(--pine)}
.rowmain{flex:1;padding:16px 18px}
.rowtop{display:flex;align-items:baseline;gap:10px;flex-wrap:wrap}
.rowtop strong{font-family:var(--disp);font-size:18.5px}
.dots{flex:1 1 40px;border-bottom:2px dotted var(--line);transform:translateY(-5px);min-width:30px}
.desc{font-size:14.5px;color:var(--soft);margin-top:5px}

/* split & cards */
main.wrap .split{display:grid;grid-template-columns:1.2fr .8fr;gap:24px;margin-top:38px;align-items:start}
.card{background:var(--paper);border:1px solid var(--line);border-radius:14px;padding:24px;box-shadow:0 2px 0 rgba(14,42,26,.05)}
.card h2{font-size:24px;margin-bottom:10px}
.pricebig{font-family:var(--mono);font-weight:700;color:var(--fairway);margin-top:14px;font-size:16px}
.addr{font-family:var(--disp);font-size:21px;line-height:1.35;color:var(--pine)}

/* visit */
.visitgrid{display:grid;grid-template-columns:1.1fr .9fr;gap:24px;margin-top:38px;align-items:start}
.hours{width:100%;border-collapse:collapse;margin-top:14px}
.hours th{text-align:left;font-family:var(--body);font-weight:600;color:var(--ink);padding:10px 6px;border-bottom:1px dashed var(--line)}
.hours td{text-align:right;font-family:var(--mono);font-size:14.5px;font-weight:700;color:var(--fairway);padding:10px 6px;border-bottom:1px dashed var(--line)}
.hours tr:last-child th,.hours tr:last-child td{border-bottom:none}
.mapfull{margin-top:26px;border-radius:16px;overflow:hidden;border:3px solid var(--fairway)}
.mapfull iframe{width:100%;height:420px;border:0;display:block}
.map iframe{width:100%;height:260px;border:0;display:block;border-radius:12px}
.map-mini{padding:10px}
.faq{margin-top:16px}
.faq dt{font-family:var(--disp);font-size:19px;font-weight:700;color:var(--pine);margin-top:20px}
.faq dd{color:var(--soft);margin-top:6px}
.visitmini{padding:56px 0;background:var(--paper);border-top:1px solid var(--line)}
.vgrid{display:grid;grid-template-columns:1fr 1.1fr;gap:30px;align-items:center}

/* cta band */
.ctaband{background:
  radial-gradient(760px 320px at 90% 0%,rgba(63,143,92,.35),transparent 60%),
  var(--pine);color:var(--cream);border-block:6px solid var(--cut);padding:52px 0;text-align:center}
.ctaband h2{color:var(--cream)}
.ctaband .kicker{color:#8fbf9f}
.ctaband .sub{color:rgba(247,242,228,.85);max-width:560px;margin:12px auto 0;font-size:16.5px}
.ctaband .btns{justify-content:center}

/* contact */
.contactgrid{display:grid;grid-template-columns:1.2fr .8fr;gap:24px;padding:38px 22px 48px;align-items:start}
.form .field{margin-bottom:16px}
.form label{display:block;font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--soft);margin-bottom:7px}
.form input,.form textarea{width:100%;font:inherit;font-size:16px;padding:12px 14px;border:1.5px solid var(--line);border-radius:10px;background:#fff;color:var(--ink)}
.form input:focus,.form textarea:focus{outline:2px solid var(--cut);border-color:var(--cut)}
.side .card{margin-bottom:18px}

/* prose */
.prose{padding:34px 22px 50px;max-width:760px}
.prose h2{font-size:24px;margin-top:30px;color:var(--pine)}
.prose p{margin-top:10px}

/* 404 / thanks */
.lost{background:var(--pine);color:var(--cream);padding:90px 0 84px;border-bottom:6px solid var(--cut)}
.lost h1{color:var(--cream);font-size:clamp(32px,5vw,54px)}
.lost .lede{color:rgba(247,242,228,.9)}
.lost a:not(.btn){color:#ffd98a}

/* footer */
footer.site{background:var(--pine);color:rgba(247,242,228,.85);margin-top:6px;border-top:6px solid var(--cut);padding:48px 22px 26px}
footer.site .cols{max-width:1080px;margin:0 auto;display:grid;grid-template-columns:1.4fr .8fr 1fr;gap:34px}
footer.site h4{font-family:var(--mono);font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:#8fbf9f;margin-bottom:12px}
footer.site p{font-size:15px}
footer.site a{color:#ffd98a;text-decoration:none}
footer.site a:hover{text-decoration:underline}
.fbrand{font-family:var(--disp);font-size:24px;color:var(--cream);display:block;margin-bottom:8px}
.fbrand em{font-style:normal;color:var(--brass)}
.tag{font-family:var(--disp);font-style:italic;color:#cfe3d3;margin-bottom:10px}
.fb{display:inline-block;margin-top:10px;font-family:var(--mono);font-size:12.5px;letter-spacing:.1em;text-transform:uppercase;border:1px solid rgba(247,242,228,.35);padding:9px 16px;border-radius:999px;color:var(--cream)!important}
.footline{max-width:1080px;margin:34px auto 0;padding-top:18px;border-top:1px solid rgba(247,242,228,.18);font-size:13px;font-family:var(--mono);color:rgba(247,242,228,.6);text-align:center}
.footline a{color:#ffd98a}

/* responsive */
@media (max-width:560px){
  .dots{display:none}
  .rowtop{flex-wrap:wrap}
  .price{margin-left:auto}
  .itemcard .topline .price{margin-left:auto}
}
@media (max-width:880px){
  .stripgrid,.visitgrid,.contactgrid,.split,.vgrid{grid-template-columns:1fr}
  footer.site .cols{grid-template-columns:1fr}
  header .btn-order{display:none}
  nav{margin-left:0}
  .hero .wrap{padding:62px 22px 56px}
  .mapfull iframe{height:300px}
}
"""

# ---------------------------------------------------------------- main

def w(name, content):
    with open(os.path.join("public", name), "w", encoding="utf-8") as f:
        f.write(content)

def main():
    os.makedirs("public", exist_ok=True)
    pages = [
        ("index.html", page_home()),
        ("menu.html", page_menu()),
        ("coffee.html", page_coffee()),
        ("eats.html", page_eats()),
        ("visit.html", page_visit()),
        ("contact.html", page_contact()),
        ("privacy.html", page_privacy()),
        ("404.html", page_404()),
        ("thanks.html", page_thanks()),
    ]
    for n, c in pages:
        w(n, c)
    w("style.css", CSS)
    paths = ["/", "/menu", "/coffee", "/eats", "/visit", "/contact", "/privacy"]
    sm = ("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
          "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
          + "".join("<url><loc>" + ORIGIN + p + "</loc><lastmod>2026-11-23</lastmod></url>\n" for p in paths)
          + "</urlset>\n")
    w("sitemap.xml", sm)
    w("robots.txt", "User-agent: *\nDisallow:\n\nSitemap: " + ORIGIN + "/sitemap.xml\n")
    print("built:", ", ".join(n for n, _ in pages), "| css | sitemap | robots")

if __name__ == "__main__":
    main()
