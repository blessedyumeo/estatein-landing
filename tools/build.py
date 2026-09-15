# -*- coding: utf-8 -*-
"""Сборка статических HTML-страниц Estatein из общих партиалов."""
import os
from partials import page, eyebrow

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def write(name, html):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(html)


def icon(name, cls=""):
    c = f' class="{cls}"' if cls else ""
    return f'<svg{c} aria-hidden="true"><use href="#i-{name}"></use></svg>'


def sec_head(title, text, action=None, eyebrow_on=True):
    act = f'<div class="section-head__action">{action}</div>' if action else ""
    return f"""      <div class="section-head">
        {eyebrow() if eyebrow_on else ''}
        <div class="section-head__main">
          <h2>{title}</h2>
          <p class="lead">{text}</p>
        </div>
        {act}
      </div>"""


def slider_foot(total, extra_id=""):
    return f"""        <div class="slider-foot">
          <p class="slider-count"><b data-slider-current>01</b> of <span data-slider-total data-total="{total}">{total}</span></p>
          <div class="slider-nav">
            <button class="slider-btn" type="button" data-slider-prev aria-label="Previous">{icon('arrow-left')}</button>
            <button class="slider-btn" type="button" data-slider-next aria-label="Next">{icon('arrow-right')}</button>
          </div>
        </div>"""


# ---------------------------------------------------------------- данные
PROPERTIES = [
    dict(img="img/properties/seaside-serenity-villa.svg", title="Seaside Serenity Villa",
         tagline="Coastal Escapes - Where Waves Beckon",
         desc="A stunning 4-bedroom, 3-bathroom villa in a peaceful suburban neighborhood…",
         bed="4-Bedroom", bath="3-Bathroom", kind="Villa", price="$550,000", price2="$1,250,000"),
    dict(img="img/properties/metropolitan-haven.svg", title="Metropolitan Haven",
         tagline="Urban Oasis - Life in the Heart of the City",
         desc="A chic and fully-furnished 2-bedroom apartment with panoramic city views…",
         bed="2-Bedroom", bath="2-Bathroom", kind="Villa", price="$550,000", price2="$650,000"),
    dict(img="img/properties/rustic-retreat-cottage.svg", title="Rustic Retreat Cottage",
         tagline="Countryside Charm - Escape to Nature's Embrace",
         desc="An elegant 3-bedroom, 2.5-bathroom townhouse in a gated community…",
         bed="3-Bedroom", bath="3-Bathroom", kind="Villa", price="$550,000", price2="$350,000"),
    dict(img="img/properties/urban-oasis-loft.svg", title="Urban Oasis Loft",
         tagline="City Lights - Designed for Modern Living",
         desc="A bright 2-bedroom loft with floor-to-ceiling windows and a private terrace…",
         bed="2-Bedroom", bath="2-Bathroom", kind="Loft", price="$480,000", price2="$780,000"),
    dict(img="img/properties/coastal-escape-villa.svg", title="Coastal Escape Villa",
         tagline="Ocean Breeze - Wake Up to the Horizon",
         desc="A spacious 5-bedroom villa with an infinity pool and direct beach access…",
         bed="5-Bedroom", bath="4-Bathroom", kind="Villa", price="$920,000", price2="$1,480,000"),
    dict(img="img/properties/countryside-charm.svg", title="Countryside Charm House",
         tagline="Green Valley - Peace Just Outside the City",
         desc="A cosy 3-bedroom family house surrounded by gardens and quiet forest paths…",
         bed="3-Bedroom", bath="2-Bathroom", kind="House", price="$390,000", price2="$420,000"),
]


def property_card(p, with_tagline=False, price_key="price"):
    tagline = f'<span class="property__tagline">{p["tagline"]}</span>' if with_tagline else ""
    return f"""          <article class="property">
            <div class="property__media"><img src="{p['img']}" alt="{p['title']}" loading="lazy" width="800" height="600"></div>
            {tagline}
            <div class="property__body">
              <h3 class="property__title">{p['title']}</h3>
              <p class="property__desc">{p['desc']} <a href="property-details.html">Read More</a></p>
            </div>
            <ul class="tags">
              <li class="tag">{icon('bed')}{p['bed']}</li>
              <li class="tag">{icon('bath')}{p['bath']}</li>
              <li class="tag">{icon('villa')}{p['kind']}</li>
            </ul>
            <div class="property__foot">
              <p class="price"><span class="price__label">Price</span><span class="price__value">{p[price_key]}</span></p>
              <a class="btn btn--primary" href="property-details.html">View Property Details</a>
            </div>
          </article>"""


REVIEWS = [
    ("Exceptional Service!", "Our experience with Estatein was outstanding. Their team's dedication and "
     "professionalism made finding our dream home a breeze. Highly recommended!",
     "Wade Warren", "USA, California", "img/team/review-1.svg"),
    ("Efficient and Reliable", "Estatein provided us with top-notch service. They helped us sell our property "
     "quickly and at a great price. We couldn't be happier with the results.",
     "Emelie Thomson", "USA, Florida", "img/team/review-2.svg"),
    ("Trusted Advisors", "The Estatein team guided us through the entire buying process. Their knowledge and "
     "commitment to our needs were impressive. Thank you for your support!",
     "John Mans", "USA, Nevada", "img/team/review-3.svg"),
]


def review_card(r):
    title, text, name, place, ava = r
    stars = "".join(icon("star") for _ in range(5))
    return f"""          <article class="review">
            <div class="stars" aria-label="Rating: 5 out of 5">{stars}</div>
            <h3 class="h4">{title}</h3>
            <p class="review__text">{text}</p>
            <div class="review__author">
              <img class="review__avatar" src="{ava}" alt="" width="44" height="44" loading="lazy">
              <div>
                <p class="review__name">{name}</p>
                <p class="review__place">{place}</p>
              </div>
            </div>
          </article>"""


FAQS = [
    ("How do I search for properties on Estatein?",
     "Learn how to use our user-friendly search tools to find properties that match your criteria."),
    ("What documents do I need to sell my property through Estatein?",
     "Find out about the necessary documentation for listing your property with us."),
    ("How can I contact an Estatein agent?",
     "Discover the different ways you can get in touch with our experienced agents."),
]


def faq_card(f):
    q, a = f
    return f"""          <article class="faq">
            <h3 class="faq__q">{q}</h3>
            <p class="faq__a">{a}</p>
            <a class="btn btn--sm" href="#">Read More</a>
          </article>"""


FAQ_BTN = '<a class="btn" href="#">View All FAQ&rsquo;s</a>'


def faq_section():
    head = sec_head(
        "Frequently Asked Questions",
        "Find answers to common questions about Estatein's services, property listings, and the real estate "
        "process. We're here to provide clarity and assist you every step of the way.",
        FAQ_BTN)
    return f"""  <section class="section" id="faq">
    <div class="container">
{head}
      <div class="slider" data-slider>
        <div class="slider__track" data-slider-track>
{chr(10).join(faq_card(f) for f in FAQS)}
        </div>
{slider_foot(10)}
      </div>
    </div>
  </section>
"""


FEATURES = [
    ("shop", "Find Your Dream Home"),
    ("wallet", "Unlock Property Value"),
    ("building", "Effortless Property Management"),
    ("sun", "Smart Investments, Informed Decisions"),
]


def features_band():
    cards = "".join(f"""      <a class="feature" href="services.html">
        <span class="feature__icon">{icon(ic)}</span>
        <span class="feature__title">{label}</span>
        {icon('arrow-ur', 'feature__arrow')}
      </a>
""" for ic, label in FEATURES)
    return f"""  <section class="features" id="features">
{cards}  </section>
"""


# ---------------------------------------------------------------- 1. Главная
def build_home():
    featured_head = sec_head(
        "Featured Properties",
        "Explore our handpicked selection of featured properties. Each listing offers a glimpse into exceptional "
        "homes and investments available through Estatein. Click &ldquo;View Details&rdquo; for more information.",
        '<a class="btn" href="properties.html">View All Properties</a>')
    testimonials_head = sec_head(
        "What Our Clients Say",
        "Read the success stories and heartfelt testimonials from our valued clients. Discover why they chose "
        "Estatein for their real estate needs.",
        '<a class="btn" href="#">View All Testimonials</a>')
    cards = chr(10).join(property_card(p) for p in PROPERTIES)
    reviews = chr(10).join(review_card(r) for r in REVIEWS)
    body = f"""  <section class="hero" id="hero">
    <div class="hero__content">
      <h1 class="hero__title">Discover Your Dream Property with Estatein</h1>
      <p class="hero__text">Your journey to finding the perfect property begins here. Explore our listings to find the
        home that matches your dreams.</p>
      <div class="hero__actions">
        <a class="btn" href="about.html">Learn More</a>
        <a class="btn btn--primary" href="properties.html">Browse Properties</a>
      </div>
      <div class="hero__stats">
        <div class="stat"><p class="stat__value">200+</p><p class="stat__label">Happy Customers</p></div>
        <div class="stat"><p class="stat__value">10k+</p><p class="stat__label">Properties For Clients</p></div>
        <div class="stat"><p class="stat__value">16+</p><p class="stat__label">Years of Experience</p></div>
      </div>
    </div>

    <div class="hero__media">
      <img src="img/hero-building.svg" alt="Modern glass towers at dusk" width="900" height="900">
      <div class="hero__badge badge">
        <svg class="badge__ring" viewBox="0 0 100 100" aria-hidden="true">
          <defs><path id="badge-path" d="M50,50 m-37,0 a37,37 0 1,1 74,0 a37,37 0 1,1 -74,0"></path></defs>
          <text><textPath href="#badge-path" startOffset="0">Discover Your Dream Property •&nbsp;</textPath></text>
        </svg>
        {icon('arrow-ur', 'badge__arrow')}
      </div>
    </div>
  </section>

{features_band()}
  <section class="section" id="properties">
    <div class="container">
{featured_head}
      <div class="slider" data-slider>
        <div class="slider__track" data-slider-track>
{cards}
        </div>
{slider_foot(60)}
      </div>
    </div>
  </section>

  <section class="section" id="testimonials">
    <div class="container">
{testimonials_head}
      <div class="slider" data-slider>
        <div class="slider__track" data-slider-track>
{reviews}
        </div>
{slider_foot(10)}
      </div>
    </div>
  </section>

{faq_section()}"""
    write("index.html", page(
        "Estatein — Discover Your Dream Property",
        "Estatein — real estate agency. Explore featured properties, client stories and expert services.",
        "index.html", body))


# ---------------------------------------------------------------- 2. О нас
VALUES = [
    ("star", "Trust", "Trust is the cornerstone of every successful real estate transaction."),
    ("cap", "Excellence", "We set the bar high for ourselves. From the properties we list to the services we provide."),
    ("users", "Client-Centric", "Your dreams and needs are at the center of our universe. We listen, understand."),
    ("heart", "Our Commitment", "We are dedicated to providing you with the highest level of service, professionalism and support."),
]

ACHIEVEMENTS = [
    ("3+ Years of Excellence", "With over 3 years in the industry, we've amassed a wealth of knowledge and experience, "
     "becoming a go-to resource for all things real estate."),
    ("Happy Clients", "Our greatest achievement is the satisfaction of our clients. Their success stories fuel our "
     "passion for what we do."),
    ("Industry Recognition", "We've earned the respect of our peers and industry leaders, with accolades and awards "
     "that reflect our commitment to excellence."),
]

STEPS = [
    ("Step 01", "Discover a World of Possibilities",
     "Your journey begins with exploring our carefully curated property listings. Use our intuitive search tools to "
     "filter properties based on your preferences, including location, type, size, and budget."),
    ("Step 02", "Narrowing Down Your Choices",
     "Once you've found properties that catch your eye, save them to your account or make a shortlist. This allows you "
     "to compare and revisit your favorites as you make your decision."),
    ("Step 03", "Personalized Guidance",
     "Have questions about a property or need more information? Our dedicated team of real estate experts is just a "
     "call or message away."),
    ("Step 04", "See It for Yourself",
     "Arrange viewings of the properties you're interested in. We'll coordinate with the property owners and accompany "
     "you to ensure you get a firsthand look at your potential new home."),
    ("Step 05", "Making Informed Decisions",
     "Before making an offer, our team will assist you with due diligence, including property inspections, legal "
     "checks, and market analysis. We want you to be fully informed and confident in your choice."),
    ("Step 06", "Getting the Best Deal",
     "We'll help you negotiate the best terms and prepare your offer. Our goal is to secure the property at the right "
     "price and on favorable terms."),
]

TEAM = [
    ("img/team/max-mitchell.svg", "Max Mitchell", "Founder"),
    ("img/team/sarah-johnson.svg", "Sarah Johnson", "Chief Real Estate Officer"),
    ("img/team/david-brown.svg", "David Brown", "Head of Property Management"),
    ("img/team/michael-turner.svg", "Michael Turner", "Legal Counsel"),
]

CLIENTS = [
    ("Since 2019", "ABC Corporation", "Commercial Real Estate", "Luxury Home Development",
     "Estatein's expertise in finding the perfect office space for our expanding operations was invaluable. "
     "They truly understand our business needs."),
    ("Since 2018", "GreenTech Enterprises", "Commercial Real Estate", "Retail Space",
     "Estatein's ability to identify prime retail locations helped us expand our brand presence. "
     "They are a trusted partner in our growth."),
    ("Since 2020", "Sunrise Ventures", "Residential Real Estate", "Urban Apartments",
     "From the first viewing to the closing table, the Estatein team kept everything transparent and on schedule."),
]


def build_about():
    values = "".join(f"""          <div class="value">
            <div class="value__head"><span class="value__icon">{icon(ic)}</span><h3 class="h5">{title}</h3></div>
            <p class="value__text">{text}</p>
          </div>
""" for ic, title, text in VALUES)

    achievements = "".join(f"""        <article class="card">
          <h3 class="h4">{title}</h3>
          <p class="lead mt-40" style="margin-top:14px">{text}</p>
        </article>
""" for title, text in ACHIEVEMENTS)

    steps = "".join(f"""        <article class="step">
          <span class="step__num">{num}</span>
          <h3 class="h5">{title}</h3>
          <p class="step__text">{text}</p>
        </article>
""" for num, title, text in STEPS)

    team = "".join(f"""        <article class="member">
          <div class="member__photo">
            <img src="{img}" alt="{name}" loading="lazy" width="420" height="520">
            <a class="member__social" href="#" aria-label="{name} on Twitter">{icon('tw')}</a>
          </div>
          <div>
            <p class="member__name">{name}</p>
            <p class="member__role">{role}</p>
          </div>
          <div class="member__hello">
            <span>Say Hello 👋</span>
            <a class="member__send" href="mailto:info@estatein.com" aria-label="Write to {name}">{icon('send')}</a>
          </div>
        </article>
""" for img, name, role in TEAM)

    clients = "".join(f"""          <article class="client">
            <div class="client__head">
              <div>
                <p class="client__since">{since}</p>
                <h3 class="client__name">{name}</h3>
              </div>
              <a class="btn btn--sm" href="#">Visit Website</a>
            </div>
            <dl class="client__meta">
              <div><dt>{icon('grid')}Domain</dt><dd>{domain}</dd></div>
              <div><dt>{icon('tag')}Category</dt><dd>{cat}</dd></div>
            </dl>
            <div class="client__quote">
              <span class="client__quote-label">What They Said 🤗</span>
              <p>{quote}</p>
            </div>
          </article>
""" for since, name, domain, cat, quote in CLIENTS)

    body = f"""  <section class="section" id="journey">
    <div class="container split">
      <div>
        {eyebrow()}
        <h1>Our Journey</h1>
        <p class="lead" style="margin-top:12px">Our story is one of continuous growth and evolution. We started as a
          small team with big dreams, determined to create a real estate platform that transcended the ordinary. Over
          the years, we've expanded our reach, forged valuable partnerships, and gained the trust of countless clients.</p>
        <div class="hero__stats" style="margin-top:28px">
          <div class="stat"><p class="stat__value">200+</p><p class="stat__label">Happy Customers</p></div>
          <div class="stat"><p class="stat__value">10k+</p><p class="stat__label">Properties For Clients</p></div>
          <div class="stat"><p class="stat__value">16+</p><p class="stat__label">Years of Experience</p></div>
        </div>
      </div>
      <div class="journey__media">
        <img src="img/about-house.svg" alt="A house model held in a hand" width="900" height="620">
      </div>
    </div>
  </section>

  <section class="section" id="values">
    <div class="container split split--media-left">
      <div class="panel">
        <div class="cards-grid cards-grid--2">
{values}        </div>
      </div>
      <div>
        {eyebrow()}
        <h2>Our Values</h2>
        <p class="lead" style="margin-top:12px">Our story is one of continuous growth and evolution. We started as a
          small team with big dreams, determined to create a real estate platform that transcended the ordinary.</p>
      </div>
    </div>
  </section>

  <section class="section" id="achievements">
    <div class="container">
{sec_head("Our Achievements",
          "Our story is one of continuous growth and evolution. We started as a small team with big dreams, determined "
          "to create a real estate platform that transcended the ordinary.")}
      <div class="cards-grid cards-grid--3">
{achievements}      </div>
    </div>
  </section>

  <section class="section" id="steps">
    <div class="container">
{sec_head("Navigating the Estatein Experience",
          "At Estatein, we've designed a straightforward process to help you find and purchase your dream property "
          "with ease. Here's a step-by-step guide to how it all works.")}
      <div class="cards-grid cards-grid--3">
{steps}      </div>
    </div>
  </section>

  <section class="section" id="team">
    <div class="container">
{sec_head("Meet the Estatein Team",
          "At Estatein, our success is driven by the dedication and expertise of our team. Get to know the people "
          "behind our mission to make your real estate dreams a reality.")}
      <div class="cards-grid cards-grid--4">
{team}      </div>
    </div>
  </section>

  <section class="section" id="clients">
    <div class="container">
{sec_head("Our Valued Clients",
          "At Estatein, we have had the privilege of working with a diverse range of clients across various "
          "industries. Here are some of the clients we've had the pleasure of serving.")}
      <div class="slider slider--2" data-slider>
        <div class="slider__track" data-slider-track>
{clients}        </div>
{slider_foot(10)}
      </div>
    </div>
  </section>
"""
    write("about.html", page(
        "About Us — Estatein",
        "Estatein's story, values, achievements, team and clients.",
        "about.html", body))


# ---------------------------------------------------------------- 3. Объекты
FILTERS = [
    ("pin", "Location", ["New York", "Los Angeles", "Miami", "Chicago"]),
    ("villa", "Property Type", ["Villa", "Apartment", "Loft", "Townhouse"]),
    ("wallet", "Pricing Range", ["$100k – $300k", "$300k – $600k", "$600k – $1M", "$1M+"]),
    ("area", "Property Size", ["Up to 1,000 sqft", "1,000 – 2,500 sqft", "2,500 sqft+"]),
    ("grid", "Build Year", ["2024", "2020 – 2023", "2010 – 2019", "Before 2010"]),
]


def build_properties():
    filters = "".join(f"""          <label class="control control--select">
            {icon(ic, 'control__icon')}
            <span class="visually-hidden">{label}</span>
            <select name="{label.lower().replace(' ', '-')}">
              <option value="">{label}</option>
{''.join(f'              <option>{o}</option>' + chr(10) for o in opts)}            </select>
            {icon('chevron', 'control__chevron')}
          </label>
""" for ic, label, opts in FILTERS)

    body = f"""  <section class="page-hero">
    <img class="page-hero__pattern" src="img/pattern-lines.svg" alt="" aria-hidden="true">
    <div class="container page-hero__inner">
      <h1>Find Your Dream Property</h1>
      <p class="page-hero__text">Welcome to Estatein, where your dream property awaits in every corner of our beautiful
        world. Explore our curated selection of properties, each offering a unique story and a chance to redefine your
        life. With categories to suit every dreamer, your journey starts here.</p>

      <form class="search" data-form novalidate>
        <div class="search__bar">
          <input type="search" name="q" placeholder="Search For A Property" aria-label="Search for a property">
          <button class="btn btn--primary btn--sm" type="submit">{icon('search', 'btn__icon')}Find Property</button>
        </div>
        <div class="search__filters">
{filters}        </div>
      </form>
    </div>
  </section>

  <section class="section" id="catalog">
    <div class="container">
{sec_head("Discover a World of Possibilities",
          "Our portfolio of properties is as diverse as your dreams. Explore the following categories to find the "
          "perfect property that resonates with your vision of home.")}
      <div class="slider" data-slider>
        <div class="slider__track" data-slider-track>
{chr(10).join(property_card(p, with_tagline=True, price_key='price2') for p in PROPERTIES)}
        </div>
{slider_foot(10)}
      </div>
    </div>
  </section>

  <section class="section" id="request">
    <div class="container">
{sec_head("Let's Make it Happen",
          "Ready to take the first step toward your dream property? Fill out the form below, and our real estate "
          "wizards will work their magic to find your perfect match. Don't wait, let's embark on this exciting "
          "journey together.")}
      <form class="form" data-form novalidate>
        <div class="form__grid form__grid--4">
          <label class="field"><span>First Name</span>
            <span class="control"><input type="text" name="first-name" placeholder="Enter First Name" required></span>
            <span class="field__error">Required field</span>
          </label>
          <label class="field"><span>Last Name</span>
            <span class="control"><input type="text" name="last-name" placeholder="Enter Last Name" required></span>
            <span class="field__error">Required field</span>
          </label>
          <label class="field"><span>Email</span>
            <span class="control"><input type="email" name="email" placeholder="Enter your Email" required></span>
            <span class="field__error">Enter a valid email</span>
          </label>
          <label class="field"><span>Phone</span>
            <span class="control"><input type="tel" name="phone" placeholder="Enter Phone Number"></span>
          </label>

          <label class="field"><span>Preferred Location</span>
            <span class="control control--select">
              <select name="location"><option value="">Select Location</option><option>New York</option><option>Los Angeles</option><option>Miami</option></select>
              {icon('chevron', 'control__chevron')}
            </span>
          </label>
          <label class="field"><span>Property Type</span>
            <span class="control control--select">
              <select name="type"><option value="">Select Property Type</option><option>Villa</option><option>Apartment</option><option>Loft</option></select>
              {icon('chevron', 'control__chevron')}
            </span>
          </label>
          <label class="field"><span>No. of Bathrooms</span>
            <span class="control control--select">
              <select name="bathrooms"><option value="">Select no. of Bathrooms</option><option>1</option><option>2</option><option>3+</option></select>
              {icon('chevron', 'control__chevron')}
            </span>
          </label>
          <label class="field"><span>No. of Bedrooms</span>
            <span class="control control--select">
              <select name="bedrooms"><option value="">Select no. of Bedrooms</option><option>1</option><option>2</option><option>3+</option></select>
              {icon('chevron', 'control__chevron')}
            </span>
          </label>
        </div>

        <div class="form__grid form__grid--2">
          <label class="field"><span>Budget</span>
            <span class="control control--select">
              <select name="budget"><option value="">Select Budget</option><option>$100k – $300k</option><option>$300k – $600k</option><option>$600k+</option></select>
              {icon('chevron', 'control__chevron')}
            </span>
          </label>
          <div class="field"><span>Preferred Contact Method</span>
            <div class="form__grid form__grid--2">
              <span class="control">{icon('phone', 'control__icon')}<input type="tel" name="contact-phone" placeholder="Enter Your Number"></span>
              <span class="control">{icon('mail', 'control__icon')}<input type="email" name="contact-email" placeholder="Enter Your Email"></span>
            </div>
          </div>
        </div>

        <label class="field field--full"><span>Message</span>
          <span class="control"><textarea name="message" placeholder="Enter your Message here.."></textarea></span>
        </label>

        <div class="form__foot">
          <label class="checkbox">
            <input type="checkbox" name="agree" required>
            <span>I agree with <a href="#">Terms of Use</a> and <a href="#">Privacy Policy</a></span>
          </label>
          <button class="btn btn--primary" type="submit">Send Your Message</button>
        </div>
        <p class="form__status" data-form-status role="status"></p>
      </form>
    </div>
  </section>
"""
    write("properties.html", page(
        "Properties — Estatein",
        "Browse Estatein property listings: villas, apartments, lofts and family houses.",
        "properties.html", body))


# ---------------------------------------------------------------- 4. Карточка объекта
AMENITIES = [
    "Expansive oceanfront terrace for outdoor entertaining",
    "Gourmet kitchen with top-of-the-line appliances",
    "Private beach access for morning strolls and sunset views",
    "Master suite with a spa-inspired bathroom and ocean-facing balcony",
    "Private garage and ample storage space",
]

ADDITIONAL_FEES = [
    ("Property Transfer Tax", "$25,000", "Based on the sale price and local regulations"),
    ("Legal Fees", "$3,000", "Approximate cost for legal services, including title transfer"),
    ("Home Inspection", "$500", "Recommended for due diligence"),
    ("Property Insurance", "$1,200", "Annual cost for comprehensive property insurance"),
    ("Mortgage Fees", "Varies", "If applicable, consult your lender for specific details"),
]

MONTHLY_COSTS = [
    ("Property Taxes", "$1,250", "Approximate monthly property tax based on the sale price and local rates"),
    ("Homeowners' Association Fee", "$300", "Monthly fee for common area maintenance and security"),
]

TOTAL_INITIAL = [
    ("Listing Price", "$1,250,000", ""),
    ("Additional Fees", "$29,700", "Property transfer tax, legal fees, inspection, insurance"),
    ("Down Payment", "$250,000", "20%"),
    ("Mortgage Amount", "$1,000,000", "If applicable"),
]

MONTHLY_EXPENSES = [
    ("Property Taxes", "$1,250", ""),
    ("Homeowners' Association Fee", "$300", ""),
    ("Mortgage Payment", "Varies based on terms and interest rate", "If applicable"),
    ("Property Insurance", "$100", "Approximate monthly cost"),
]


def fees_block(title, rows, cols=2):
    items = "".join(f"""            <div class="fee">
              <p class="fee__label">{label}</p>
              <p class="fee__value"><b>{value}</b>{f'<span class="fee__hint">{hint}</span>' if hint else ''}</p>
            </div>
""" for label, value, hint in rows)
    return f"""        <div class="panel">
          <div class="pricing__block-head">
            <h3 class="h5">{title}</h3>
            <a class="btn btn--sm" href="#">Learn More</a>
          </div>
          <div class="fees fees--{cols}">
{items}          </div>
        </div>
"""


def build_details():
    thumbs = "".join(f"""          <button type="button" data-viewer-thumb data-full="img/interior/interior-{i}.svg"
            data-alt="Interior view {i}" aria-label="Photo {i}">
            <img src="img/interior/interior-{i}.svg" alt="" loading="lazy" width="800" height="600">
          </button>
""" for i in range(1, 9))

    dots = "".join('<span></span>' for _ in range(4))
    amenities = "".join(f'            <li>{icon("bolt")}{a}</li>\n' for a in AMENITIES)

    body = f"""  <section class="container property-head">
    <div class="property-head__title">
      <h1 class="h2">Seaside Serenity Villa</h1>
      <span class="property-head__loc">{icon('pin')}Malibu, California</span>
    </div>
    <p class="property-head__price price">
      <span class="price__label">Price</span>
      <span class="price__value h3">$1,250,000</span>
    </p>
  </section>

  <section class="container">
    <div class="viewer" data-viewer>
      <div class="viewer__thumbs">
{thumbs}      </div>
      <div class="viewer__stage" data-viewer-stage>
        <img src="img/interior/interior-1.svg" alt="Interior view" width="800" height="600">
        <img src="img/interior/interior-2.svg" alt="Interior view" width="800" height="600">
      </div>
      <div class="viewer__controls">
        <button class="slider-btn" type="button" data-viewer-prev aria-label="Previous photos">{icon('arrow-left')}</button>
        <div class="dots" data-viewer-dots>{dots}</div>
        <button class="slider-btn" type="button" data-viewer-next aria-label="Next photos">{icon('arrow-right')}</button>
      </div>
    </div>
  </section>

  <section class="section section--tight">
    <div class="container cards-grid cards-grid--2">
      <article class="panel">
        <h2 class="h5">Description</h2>
        <p class="lead" style="margin:14px 0 24px">Discover your own piece of paradise with the Seaside Serenity Villa.
          With an open floor plan, breathtaking ocean views from every room, and direct access to a pristine sandy
          beach, this property is the epitome of coastal living.</p>
        <dl class="specs">
          <div><dt>{icon('bed')}Bedrooms</dt><dd>04</dd></div>
          <div><dt>{icon('bath')}Bathrooms</dt><dd>03</dd></div>
          <div><dt>{icon('area')}Area</dt><dd>2,500 Square Feet</dd></div>
        </dl>
      </article>

      <article class="panel">
        <h2 class="h5" style="margin-bottom:20px">Key Features and Amenities</h2>
        <ul class="features-list">
{amenities}        </ul>
      </article>
    </div>
  </section>

  <section class="section" id="inquire">
    <div class="container split">
      <div>
        {eyebrow()}
        <h2>Inquire About Seaside Serenity Villa</h2>
        <p class="lead" style="margin-top:12px">Interested in this property? Fill out the form below, and our real
          estate experts will get back to you with more details, including scheduling a viewing and answering any
          questions you may have.</p>
      </div>

      <form class="form" data-form novalidate>
        <div class="form__grid form__grid--2">
          <label class="field"><span>First Name</span>
            <span class="control"><input type="text" name="first-name" placeholder="Enter First Name" required></span>
            <span class="field__error">Required field</span>
          </label>
          <label class="field"><span>Last Name</span>
            <span class="control"><input type="text" name="last-name" placeholder="Enter Last Name" required></span>
            <span class="field__error">Required field</span>
          </label>
          <label class="field"><span>Email</span>
            <span class="control"><input type="email" name="email" placeholder="Enter your Email" required></span>
            <span class="field__error">Enter a valid email</span>
          </label>
          <label class="field"><span>Phone</span>
            <span class="control"><input type="tel" name="phone" placeholder="Enter Phone Number"></span>
          </label>
        </div>
        <label class="field"><span>Selected Property</span>
          <span class="control"><input type="text" name="property" value="Seaside Serenity Villa, Malibu, California" readonly>{icon('pin', 'control__icon')}</span>
        </label>
        <label class="field"><span>Message</span>
          <span class="control"><textarea name="message" placeholder="Enter your Message here.."></textarea></span>
        </label>
        <div class="form__foot">
          <label class="checkbox">
            <input type="checkbox" name="agree" required>
            <span>I agree with <a href="#">Terms of Use</a> and <a href="#">Privacy Policy</a></span>
          </label>
          <button class="btn btn--primary" type="submit">Send Your Message</button>
        </div>
        <p class="form__status" data-form-status role="status"></p>
      </form>
    </div>
  </section>

  <section class="section" id="pricing">
    <div class="container">
{sec_head("Comprehensive Pricing Details",
          "At Estatein, transparency is key. We want you to have a clear understanding of all costs associated with "
          "your property investment. Below, we break down the pricing for Seaside Serenity Villa to help you make an "
          "informed decision.")}
      <p class="note"><b>Note</b><span>The figures provided above are estimates and may vary depending on the property,
        location, and individual circumstances.</span></p>

      <div class="pricing">
        <div>
          <p class="price__label">Listing Price</p>
          <p class="h2">$1,250,000</p>
        </div>
        <div class="pricing__blocks">
{fees_block("Additional Fees", ADDITIONAL_FEES)}{fees_block("Monthly Costs", MONTHLY_COSTS, 1)}{fees_block("Total Initial Costs", TOTAL_INITIAL)}{fees_block("Monthly Expenses", MONTHLY_EXPENSES)}        </div>
      </div>
    </div>
  </section>

{faq_section()}"""
    write("property-details.html", page(
        "Seaside Serenity Villa — Estatein",
        "Seaside Serenity Villa in Malibu, California: photos, features, pricing details and inquiry form.",
        "properties.html", body))


# ---------------------------------------------------------------- 5. Услуги
SELLING = [
    ("chart", "Valuation Mastery", "Discover the true worth of your property with our expert valuation services."),
    ("target", "Strategic Marketing", "Selling a property requires more than just a listing. It demands a strategic marketing approach."),
    ("layers", "Negotiation Wizardry", "Negotiating the best deal is an art, and our negotiation experts are masters of it."),
    ("key", "Closing Success", "A successful sale is not complete until the closing. We guide you through the intricate closing process."),
]

MANAGEMENT = [
    ("users", "Tenant Harmony", "Our Tenant Management services ensure that your tenants have a smooth and reducing vacancies."),
    ("wrench", "Maintenance Ease", "Say goodbye to property maintenance headaches. We handle all aspects of property upkeep."),
    ("wallet", "Financial Peace of Mind", "Managing property finances can be complex. Our financial experts take care of rent collection."),
    ("shield", "Legal Guardian", "Stay compliant with property laws and regulations effortlessly."),
]

INVEST = [
    ("chart", "Market Insight", "Stay ahead of market trends with our expert Market Analysis. We provide in-depth insights into real estate market conditions."),
    ("target", "ROI Assessment", "Make investment decisions with confidence. Our ROI Assessment services evaluate the potential returns on your investments."),
    ("bolt", "Customized Strategies", "Every investor is unique, and so are their goals. We develop Customized Investment Strategies tailored to your specific needs."),
    ("layers", "Diversification Mastery", "Diversify your real estate portfolio effectively. Our experts guide you in spreading your investments across various property types and locations."),
]


def service_card(ic, title, text):
    return f"""        <article class="service">
          <div class="service__head"><span class="value__icon">{icon(ic)}</span><h3 class="h5">{title}</h3></div>
          <p class="service__text">{text}</p>
        </article>
"""


def promo(title, text):
    return f"""        <article class="service-promo">
          <img class="service-promo__pattern" src="img/pattern-lines.svg" alt="" aria-hidden="true">
          <div class="service-promo__head">
            <h3 class="h4">{title}</h3>
            <a class="btn btn--sm" href="contact.html">Learn More</a>
          </div>
          <p class="service__text">{text}</p>
        </article>
"""


def build_services():
    body = f"""  <section class="page-hero">
    <img class="page-hero__pattern" src="img/pattern-lines.svg" alt="" aria-hidden="true">
    <div class="container page-hero__inner">
      <h1>Elevate Your Real Estate Experience</h1>
      <p class="page-hero__text">Welcome to Estatein, where your real estate aspirations meet expert guidance. Explore
        our comprehensive range of services, each designed to cater to your unique needs and dreams.</p>
    </div>
  </section>

{features_band()}
  <section class="section" id="selling">
    <div class="container">
{sec_head("Unlock Property Value",
          "Selling your property should be a rewarding experience, and at Estatein, we make sure it is. Our Property "
          "Selling Service is designed to maximize the value of your property, ensuring you get the best deal "
          "possible. Explore the categories below to see how we can help you at every step of your selling journey.")}
      <div class="services-grid">
{''.join(service_card(*s) for s in SELLING[:3])}{service_card(*SELLING[3])}{promo("Unlock the Value of Your Property Today", "Ready to unlock the true value of your property? Explore our Property Selling Service categories and let us help you achieve the best deal possible for your valuable asset.")}      </div>
    </div>
  </section>

  <section class="section" id="management">
    <div class="container">
{sec_head("Effortless Property Management",
          "Owning a property should be a pleasure, not a hassle. Estatein's Property Management Service takes the "
          "stress out of property ownership, offering comprehensive solutions tailored to your needs. Explore the "
          "categories below to see how we can make property management effortless for you.")}
      <div class="services-grid">
{''.join(service_card(*s) for s in MANAGEMENT[:3])}{service_card(*MANAGEMENT[3])}{promo("Experience Effortless Property Management", "Ready to experience hassle-free property management? Explore our Property Management Service categories and let us handle the complexities while you enjoy the benefits of property ownership.")}      </div>
    </div>
  </section>

  <section class="section" id="investments">
    <div class="container split">
      <div>
        {eyebrow()}
        <h2>Smart Investments, Informed Decisions</h2>
        <p class="lead" style="margin-top:12px">Building a real estate portfolio requires a strategic approach.
          Estatein's Investment Advisory Service empowers you to make smart investments and informed decisions.</p>
        <div class="panel" style="margin-top:26px">
          <h3 class="h5">Unlock Your Investment Potential</h3>
          <p class="service__text" style="margin:12px 0 18px">Explore our Property Management Service categories and
            let us handle the complexities while you enjoy the benefits of property ownership.</p>
          <a class="btn btn--block" href="contact.html">Learn More</a>
        </div>
      </div>
      <div class="cards-grid cards-grid--2">
{''.join(service_card(*s) for s in INVEST)}      </div>
    </div>
  </section>
"""
    write("services.html", page(
        "Services — Estatein",
        "Property selling, property management and investment advisory services by Estatein.",
        "services.html", body))


# ---------------------------------------------------------------- 6. Контакты
OFFICES = [
    ("main", "Main Headquarters", "123 Estatein Plaza, City Center, Metropolis",
     "Our main headquarters serve as the heart of Estatein. Located in the bustling city center, this is where our core "
     "team of experts operates, driving the excellence and innovation that define us.",
     "info@estatein.com", "+1 (123) 456-7890", "Metropolis"),
    ("regional", "Regional Offices", "456 Urban Avenue, Downtown District, Metropolis",
     "Estatein's presence extends to multiple regions, each with its own dynamic real estate landscape. Discover our "
     "regional offices, staffed by local experts who understand the nuances of their respective markets.",
     "info@restatein.com", "+1 (123) 628-7890", "Metropolis"),
    ("international", "International Offices", "789 Skyline Boulevard, Harbour Quarter, Port City",
     "Our international teams help clients buy and sell across borders, combining global reach with local knowledge in "
     "every market we serve.",
     "global@estatein.com", "+1 (123) 987-6543", "Port City"),
]


def build_contact():
    offices = "".join(f"""        <article class="office" data-tab-item="{kind}">
          <p class="office__kind">{label}</p>
          <h3 class="office__title">{addr}</h3>
          <p class="office__text">{text}</p>
          <ul class="office__meta">
            <li class="tag">{icon('mail')}{mail}</li>
            <li class="tag">{icon('phone')}{phone}</li>
            <li class="tag">{icon('pin')}{city}</li>
          </ul>
          <a class="btn btn--primary btn--block" href="#">Get Direction</a>
        </article>
""" for kind, label, addr, text, mail, phone, city in OFFICES)

    gallery = "".join(f"""        <img src="img/gallery/office-{i}.svg" alt="Estatein office life" loading="lazy" width="800" height="520">
""" for i in range(1, 6))

    body = f"""  <section class="page-hero">
    <img class="page-hero__pattern" src="img/pattern-lines.svg" alt="" aria-hidden="true">
    <div class="container page-hero__inner">
      <h1>Get in Touch with Estatein</h1>
      <p class="page-hero__text">Welcome to Estatein's Contact Us page. We're here to assist you with any inquiries,
        requests, or feedback you may have. Whether you're looking to buy or sell a property, explore investment
        opportunities, or simply want to connect, we're just a message away. Reach out to us, and let's start a
        conversation.</p>
    </div>
  </section>

  <section class="features">
    <div class="contact-card">
      <span class="contact-card__icon">{icon('mail')}</span>
      <a class="contact-card__value" href="mailto:info@estatein.com">info@estatein.com</a>
      {icon('arrow-ur', 'feature__arrow')}
    </div>
    <div class="contact-card">
      <span class="contact-card__icon">{icon('phone')}</span>
      <a class="contact-card__value" href="tel:+11234567890">+1 (123) 456-7890</a>
      {icon('arrow-ur', 'feature__arrow')}
    </div>
    <div class="contact-card">
      <span class="contact-card__icon">{icon('pin')}</span>
      <span class="contact-card__value">Main Headquarters</span>
      {icon('arrow-ur', 'feature__arrow')}
    </div>
    <div class="contact-card">
      <span class="contact-card__icon">{icon('logo')}</span>
      <span class="contact-card__links">
        <a href="#">Instagram</a><a href="#">LinkedIn</a><a href="#">Facebook</a>
      </span>
      {icon('arrow-ur', 'feature__arrow')}
    </div>
  </section>

  <section class="section" id="connect">
    <div class="container">
{sec_head("Let's Connect",
          "We're excited to connect with you and learn more about your real estate goals. Use the form below to get in "
          "touch with Estatein. Whether you're a prospective client, partner, or simply curious about our services, "
          "we're here to answer your questions and provide the assistance you need.")}
      <form class="form" data-form novalidate>
        <div class="form__grid form__grid--3">
          <label class="field"><span>First Name</span>
            <span class="control"><input type="text" name="first-name" placeholder="Enter First Name" required></span>
            <span class="field__error">Required field</span>
          </label>
          <label class="field"><span>Last Name</span>
            <span class="control"><input type="text" name="last-name" placeholder="Enter Last Name" required></span>
            <span class="field__error">Required field</span>
          </label>
          <label class="field"><span>Email</span>
            <span class="control"><input type="email" name="email" placeholder="Enter your Email" required></span>
            <span class="field__error">Enter a valid email</span>
          </label>
          <label class="field"><span>Phone</span>
            <span class="control"><input type="tel" name="phone" placeholder="Enter Phone Number"></span>
          </label>
          <label class="field"><span>Inquiry Type</span>
            <span class="control control--select">
              <select name="inquiry"><option value="">Select Inquiry Type</option><option>Buying a property</option><option>Selling a property</option><option>Investment advisory</option></select>
              {icon('chevron', 'control__chevron')}
            </span>
          </label>
          <label class="field"><span>How Did You Hear About Us?</span>
            <span class="control control--select">
              <select name="source"><option value="">Select</option><option>Search engine</option><option>Social media</option><option>Friend or colleague</option></select>
              {icon('chevron', 'control__chevron')}
            </span>
          </label>
        </div>
        <label class="field field--full"><span>Message</span>
          <span class="control"><textarea name="message" placeholder="Enter your Message here.."></textarea></span>
        </label>
        <div class="form__foot">
          <label class="checkbox">
            <input type="checkbox" name="agree" required>
            <span>I agree with <a href="#">Terms of Use</a> and <a href="#">Privacy Policy</a></span>
          </label>
          <button class="btn btn--primary" type="submit">Send Your Message</button>
        </div>
        <p class="form__status" data-form-status role="status"></p>
      </form>
    </div>
  </section>

  <section class="section" id="offices">
    <div class="container">
{sec_head("Discover Our Office Locations",
          "Estatein is here to serve you across multiple locations. Whether you're looking to meet our team, discuss "
          "real estate opportunities, or simply drop by for a chat, we have offices conveniently located to serve your "
          "needs. Explore the categories below to find the Estatein office nearest to you.")}
      <div class="tabs" role="tablist" data-tabs="#offices-list">
        <button type="button" class="is-active" role="tab" aria-selected="true" data-tab="all">All</button>
        <button type="button" role="tab" aria-selected="false" data-tab="regional">Regional</button>
        <button type="button" role="tab" aria-selected="false" data-tab="international">International</button>
      </div>
      <div class="cards-grid cards-grid--2" id="offices-list">
{offices}      </div>
    </div>
  </section>

  <section class="section section--tight" id="world">
    <div class="container">
      <div class="panel">
        <div class="gallery">
{gallery}          <div class="gallery__caption">
            {eyebrow()}
            <h2 class="h3">Explore Estatein's World</h2>
            <p class="service__text">Step inside the world of Estatein, where professionalism meets warmth, and
              expertise meets passion. Our gallery offers a glimpse into our team and workspaces, inviting you to get
              to know us better.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
"""
    write("contact.html", page(
        "Contact Us — Estatein",
        "Contact Estatein: offices, phone, email and a form to start a conversation.",
        "contact.html", body))


# ---------------------------------------------------------------- favicon
FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <rect width="32" height="32" rx="7" fill="#141414"/>
  <path fill="#703BF7" d="M7 9.2C7 7.9 8 7 9.2 7c.9 0 1.7.5 2 1.3l1.2 2.5V9.2C12.4 7.9 13.4 7 14.6 7h7.2C23 7 24 7.9 24 9.2v7.6C24 21.9 20 26 15 26S7 21.9 7 16.8V9.2z"/>
</svg>
"""


if __name__ == "__main__":
    with open(os.path.join(OUT, "img", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(FAVICON)
    build_home()
    build_about()
    build_properties()
    build_details()
    build_services()
    build_contact()
    print("built: index, about, properties, property-details, services, contact")
