import streamlit as st
import pandas as pd
import json
from pathlib import Path
from io import BytesIO

# ============================================================
# OPTIONAL MODULES
# ============================================================

try:
    from pitch_deck import create_pitch_deck
except Exception:
    create_pitch_deck = None

try:
    from portfolio_pdf import create_portfolio_pdf
except Exception:
    create_portfolio_pdf = None


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Digital Entrepreneur Portfolio",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# FILE PATHS
# ============================================================

DATA_DIR = Path("saved_data")
DATA_DIR.mkdir(exist_ok=True)

DATA_FILE = DATA_DIR / "portfolio_data.json"


# ============================================================
# DEFAULT DATA
# ============================================================

DEFAULT_PROFILE = {
    "name": "",
    "bio": "",
    "email": "",
    "linkedin": "",
    "phone": "",
    "role": "",
    "skills": ""
}

DEFAULT_STARTUP = {
    "startup_name": "",
    "industry": "CleanTech",
    "problem": "",
    "solution": "",
    "target_market": "",
    "competitive_advantage": "",
    "revenue_model": "",
    "market_size": "",
    "funding_stage": "Idea Stage",
    "current_revenue": "",
    "growth_rate": ""
}

DEFAULT_PORTFOLIO = {
    "project_name": "",
    "project_description": "",
    "project_result": "",
    "achievements": "",
    "clients": "",
    "testimonials": "",
    "roadmap": ""
}


# ============================================================
# LOAD SAVED DATA
# ============================================================

def load_saved_data():

    if not DATA_FILE.exists():
        return {
            "profile": DEFAULT_PROFILE.copy(),
            "startup": DEFAULT_STARTUP.copy(),
            "portfolio": DEFAULT_PORTFOLIO.copy()
        }

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return {
            "profile": {
                **DEFAULT_PROFILE,
                **data.get("profile", {})
            },
            "startup": {
                **DEFAULT_STARTUP,
                **data.get("startup", {})
            },
            "portfolio": {
                **DEFAULT_PORTFOLIO,
                **data.get("portfolio", {})
            }
        }

    except Exception:
        return {
            "profile": DEFAULT_PROFILE.copy(),
            "startup": DEFAULT_STARTUP.copy(),
            "portfolio": DEFAULT_PORTFOLIO.copy()
        }


# ============================================================
# SAVE DATA
# ============================================================

def save_all_data():

    data = {
        "profile": st.session_state.profile,
        "startup": st.session_state.startup,
        "portfolio": st.session_state.portfolio
    }

    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )
    except Exception as e:
        st.error(f"Could not save data: {e}")


# ============================================================
# SESSION STATE
# ============================================================

if "data_loaded" not in st.session_state:

    saved = load_saved_data()

    st.session_state.profile = saved["profile"]
    st.session_state.startup = saved["startup"]
    st.session_state.portfolio = saved["portfolio"]

    st.session_state.ai_content = ""
    st.session_state.pitch_generated = False
    st.session_state.data_loaded = True


# ============================================================
# CSV DATA
# ============================================================

@st.cache_data
def load_startup_database():

    csv_file = Path("startup_data.csv")

    if csv_file.exists():

        try:
            return pd.read_csv(csv_file)

        except Exception:
            return pd.DataFrame()

    return pd.DataFrame()


df = load_startup_database()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🚀 Entrepreneur Builder")

st.sidebar.caption(
    "Digital Entrepreneur Portfolio & Pitch Deck Builder"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "👤 Entrepreneur Profile",
        "💡 Startup Details",
        "📁 Portfolio Builder",
        "📊 Startup Database",
        "🤖 AI Content Assistant",
        "🎯 Pitch Deck Builder"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Build your entrepreneur profile, startup portfolio "
    "and investor-ready pitch deck."
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.title(
        "🚀 Digital Entrepreneur Portfolio & Pitch Deck Builder"
    )

    st.write(
        "Create a professional entrepreneur portfolio "
        "and investor-ready pitch deck."
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "👤 Profile",
            "Created"
            if st.session_state.profile.get("name")
            else "Pending"
        )

    with col2:
        st.metric(
            "💡 Startup",
            "Created"
            if st.session_state.startup.get("startup_name")
            else "Pending"
        )

    with col3:
        st.metric(
            "📁 Portfolio",
            "Created"
            if st.session_state.portfolio.get("project_name")
            else "Pending"
        )

    with col4:
        st.metric(
            "🎯 Pitch Deck",
            "Ready"
            if st.session_state.pitch_generated
            else "Pending"
        )

    st.divider()

    st.subheader("How the Platform Works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            "### 👤 Profile\n"
            "Enter entrepreneur and professional information."
        )

    with col2:
        st.success(
            "### 💡 Startup\n"
            "Describe the problem, solution, market and business model."
        )

    with col3:
        st.warning(
            "### 🎯 Pitch Deck\n"
            "Generate a professional investor-ready presentation."
        )

    st.divider()

    st.subheader("Project Workflow")

    st.markdown(
        """
        **Founder Profile**
        →
        **Startup Details**
        →
        **Portfolio**
        →
        **AI Content**
        →
        **Pitch Deck**
        →
        **Export**
        """
    )

    st.divider()

    st.subheader("📌 Project Features")

    features = [
        "👤 Entrepreneur Profile",
        "🚀 Startup Information",
        "📁 Portfolio & Case Studies",
        "📊 Startup Database",
        "🤖 AI Content Suggestions",
        "📄 Portfolio PDF",
        "🎯 Investor Pitch Deck"
    ]

    cols = st.columns(4)

    for i, feature in enumerate(features):

        with cols[i % 4]:
            st.markdown(
                f"""
                <div style="
                    padding:18px;
                    border-radius:12px;
                    background:#f3f6fa;
                    margin-bottom:15px;
                    text-align:center;
                ">
                <b>{feature}</b>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# ENTREPRENEUR PROFILE
# ============================================================

elif page == "👤 Entrepreneur Profile":

    st.header("👤 Entrepreneur Profile")

    profile = st.session_state.profile

    with st.form("profile_form"):

        name = st.text_input(
            "Full Name",
            value=profile.get("name", ""),
            placeholder="Example: Thirumalini E"
        )

        bio = st.text_area(
            "Professional Bio",
            value=profile.get("bio", ""),
            placeholder="Write a short professional introduction..."
        )

        col1, col2 = st.columns(2)

        with col1:

            email = st.text_input(
                "Email",
                value=profile.get("email", ""),
                placeholder="example@gmail.com"
            )

            phone = st.text_input(
                "Contact Number",
                value=profile.get("phone", ""),
                placeholder="+91 XXXXX XXXXX"
            )

            role = st.text_input(
                "Current Role",
                value=profile.get("role", ""),
                placeholder="Founder / MBA Student"
            )

        with col2:

            linkedin = st.text_input(
                "LinkedIn Profile",
                value=profile.get("linkedin", ""),
                placeholder="https://linkedin.com/in/yourname"
            )

            skills = st.text_input(
                "Key Skills",
                value=profile.get("skills", ""),
                placeholder="Analytics, Finance, Marketing"
            )

        submitted = st.form_submit_button(
            "💾 Save Entrepreneur Profile",
            use_container_width=True
        )

    if submitted:

        if not name or not bio or not email:

            st.error(
                "Please enter Name, Bio and Email."
            )

        else:

            st.session_state.profile = {
                "name": name,
                "bio": bio,
                "email": email,
                "linkedin": linkedin,
                "phone": phone,
                "role": role,
                "skills": skills
            }

            save_all_data()

            st.success(
                "✅ Entrepreneur profile saved!"
            )

    if st.session_state.profile.get("name"):

        st.divider()

        st.subheader("👀 Profile Preview")

        profile = st.session_state.profile

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"## {profile.get('name', '')}"
            )

            st.write(
                f"**Role:** {profile.get('role', '')}"
            )

            st.write(
                profile.get("bio", "")
            )

        with col2:

            st.write(
                f"📧 {profile.get('email', '')}"
            )

            st.write(
                f"📞 {profile.get('phone', '')}"
            )

            st.write(
                f"🔗 {profile.get('linkedin', '')}"
            )

            st.write(
                f"🛠️ {profile.get('skills', '')}"
            )


# ============================================================
# STARTUP DETAILS
# ============================================================

elif page == "💡 Startup Details":

    st.header("💡 Startup Details")

    startup = st.session_state.startup

    industry_options = [
        "CleanTech",
        "EdTech",
        "HealthTech",
        "AgriTech",
        "FinTech",
        "FoodTech",
        "FashionTech",
        "TravelTech",
        "BusinessTech",
        "Other"
    ]

    funding_options = [
        "Idea Stage",
        "Bootstrapped",
        "Pre-Seed",
        "Seed Funding",
        "Angel Investment",
        "Series A",
        "Series B",
        "Other"
    ]

    saved_industry = startup.get(
        "industry",
        "CleanTech"
    )

    if saved_industry not in industry_options:
        saved_industry = "CleanTech"

    saved_funding = startup.get(
        "funding_stage",
        "Idea Stage"
    )

    if saved_funding not in funding_options:
        saved_funding = "Idea Stage"

    with st.form("startup_form"):

        startup_name = st.text_input(
            "Startup Name",
            value=startup.get("startup_name", ""),
            placeholder="Example: EcoCharge"
        )

        industry = st.selectbox(
            "Industry",
            industry_options,
            index=industry_options.index(saved_industry)
        )

        problem = st.text_area(
            "🎯 Problem Statement",
            value=startup.get("problem", ""),
            placeholder="What problem does your startup solve?"
        )

        solution = st.text_area(
            "💡 Solution",
            value=startup.get("solution", ""),
            placeholder="How does your startup solve the problem?"
        )

        target_market = st.text_area(
            "🎯 Target Market",
            value=startup.get("target_market", ""),
            placeholder="Who are your customers?"
        )

        competitive_advantage = st.text_area(
            "🏆 Competitive Advantage",
            value=startup.get("competitive_advantage", ""),
            placeholder="What makes your startup different?"
        )

        revenue_model = st.text_area(
            "💰 Revenue Model",
            value=startup.get("revenue_model", ""),
            placeholder="Example: Subscription + Hardware Sales"
        )

        col1, col2 = st.columns(2)

        with col1:

            market_size = st.text_input(
                "📊 Market Size",
                value=startup.get("market_size", ""),
                placeholder="Example: ₹25 lakh"
            )

            current_revenue = st.text_input(
                "💵 Current Revenue",
                value=startup.get("current_revenue", ""),
                placeholder="Example: ₹8 lakh"
            )

        with col2:

            growth_rate = st.text_input(
                "📈 Expected Growth Rate",
                value=startup.get("growth_rate", ""),
                placeholder="Example: 12%"
            )

            funding_stage = st.selectbox(
                "💼 Funding Stage",
                funding_options,
                index=funding_options.index(saved_funding)
            )

        submitted = st.form_submit_button(
            "💾 Save Startup Details",
            use_container_width=True
        )

    if submitted:

        if not startup_name or not problem or not solution:

            st.error(
                "Please enter Startup Name, Problem and Solution."
            )

        else:

            st.session_state.startup = {

                "startup_name": startup_name,

                "industry": industry,

                "problem": problem,

                "solution": solution,

                "target_market": target_market,

                "competitive_advantage":
                    competitive_advantage,

                "revenue_model":
                    revenue_model,

                "market_size":
                    market_size,

                "funding_stage":
                    funding_stage,

                "current_revenue":
                    current_revenue,

                "growth_rate":
                    growth_rate
            }

            save_all_data()

            st.success(
                "✅ Startup details saved!"
            )

    if st.session_state.startup.get("startup_name"):

        st.divider()

        st.subheader("🚀 Startup Preview")

        startup = st.session_state.startup

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"## {startup.get('startup_name', '')}"
            )

            st.write(
                "**Industry:**",
                startup.get("industry", "")
            )

            st.write(
                "**Problem:**",
                startup.get("problem", "")
            )

            st.write(
                "**Target Market:**",
                startup.get("target_market", "")
            )

            st.write(
                "**Market Size:**",
                startup.get("market_size", "")
            )

        with col2:

            st.write(
                "**Solution:**",
                startup.get("solution", "")
            )

            st.write(
                "**Competitive Advantage:**",
                startup.get("competitive_advantage", "")
            )

            st.write(
                "**Revenue Model:**",
                startup.get("revenue_model", "")
            )

            st.write(
                "**Funding Stage:**",
                startup.get("funding_stage", "")
            )


# ============================================================
# PORTFOLIO BUILDER
# ============================================================

elif page == "📁 Portfolio Builder":

    st.header("📁 Entrepreneur Portfolio Builder")

    portfolio = st.session_state.portfolio

    with st.form("portfolio_form"):

        project_name = st.text_input(
            "Project / Product Name",
            value=portfolio.get("project_name", "")
        )

        project_description = st.text_area(
            "Project Description",
            value=portfolio.get("project_description", "")
        )

        project_result = st.text_area(
            "Project Result / Achievement",
            value=portfolio.get("project_result", "")
        )

        achievements = st.text_area(
            "🏆 Major Achievements",
            value=portfolio.get("achievements", "")
        )

        clients = st.text_area(
            "🤝 Clients / Users",
            value=portfolio.get("clients", "")
        )

        testimonials = st.text_area(
            "💬 Testimonials",
            value=portfolio.get("testimonials", "")
        )

        roadmap = st.text_area(
            "🗺️ Future Roadmap",
            value=portfolio.get("roadmap", "")
        )

        submitted = st.form_submit_button(
            "💾 Save Portfolio",
            use_container_width=True
        )

    if submitted:

        if not project_name or not project_description:

            st.error(
                "Please enter Project Name and Description."
            )

        else:

            st.session_state.portfolio = {

                "project_name":
                    project_name,

                "project_description":
                    project_description,

                "project_result":
                    project_result,

                "achievements":
                    achievements,

                "clients":
                    clients,

                "testimonials":
                    testimonials,

                "roadmap":
                    roadmap
            }

            save_all_data()

            st.success(
                "✅ Portfolio information saved!"
            )

    if st.session_state.portfolio.get("project_name"):

        st.divider()

        st.subheader("📄 Portfolio Preview")

        portfolio = st.session_state.portfolio

        st.markdown(
            f"## {portfolio.get('project_name', '')}"
        )

        st.write(
            portfolio.get("project_description", "")
        )

        st.write(
            "**Result:**",
            portfolio.get("project_result", "")
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write("### 🏆 Achievements")

            st.write(
                portfolio.get("achievements", "")
            )

            st.write("### 🤝 Clients / Users")

            st.write(
                portfolio.get("clients", "")
            )

        with col2:

            st.write("### 💬 Testimonials")

            st.write(
                portfolio.get("testimonials", "")
            )

            st.write("### 🗺️ Future Roadmap")

            st.write(
                portfolio.get("roadmap", "")
            )


# ============================================================
# STARTUP DATABASE
# ============================================================

elif page == "📊 Startup Database":

    st.header("📊 Startup Database")

    if df.empty:

        st.warning(
            "startup_data.csv was not found."
        )

        st.info(
            "Place startup_data.csv in the same folder as app.py."
        )

    else:

        selected_industry = st.selectbox(
            "🏭 Select Industry",
            ["All"]
            + sorted(
                df["Industry"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )
        )

        if selected_industry == "All":

            filtered_df = df

        else:

            filtered_df = df[
                df["Industry"] == selected_industry
            ]

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🚀 Startups",
                len(filtered_df)
            )

        with col2:

            st.metric(
                "🏭 Industries",
                filtered_df["Industry"].nunique()
            )

        with col3:

            st.metric(
                "💼 Funding Stages",
                filtered_df["Funding Stage"].nunique()
                if "Funding Stage" in filtered_df.columns
                else 0
            )

        with col4:

            st.metric(
                "💵 Revenue Records",
                filtered_df["Current Revenue"].notna().sum()
                if "Current Revenue" in filtered_df.columns
                else 0
            )

        st.divider()

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        st.subheader("📊 Industry Distribution")

        if "Industry" in df.columns:

            industry_counts = (
                filtered_df["Industry"]
                .value_counts()
            )

            st.bar_chart(industry_counts)


# ============================================================
# AI CONTENT ASSISTANT
# ============================================================

elif page == "🤖 AI Content Assistant":

    st.header("🤖 AI Content Assistant")

    startup = st.session_state.startup

    if not startup.get("startup_name"):

        st.warning(
            "⚠️ Complete Startup Details first."
        )

    else:

        st.write(
            "Use AI to generate professional startup content."
        )

        content_type = st.selectbox(
            "Choose Content Type",
            [
                "🎯 Problem Statement",
                "💡 Solution Description",
                "📊 Market Opportunity",
                "🏆 Competitive Advantage",
                "💰 Business Model",
                "✨ Startup Tagline"
            ]
        )

        if content_type == "🎯 Problem Statement":

            default_content = startup.get(
                "problem", ""
            )

        elif content_type == "💡 Solution Description":

            default_content = startup.get(
                "solution", ""
            )

        elif content_type == "📊 Market Opportunity":

            default_content = startup.get(
                "target_market", ""
            )

        elif content_type == "🏆 Competitive Advantage":

            default_content = startup.get(
                "competitive_advantage", ""
            )

        elif content_type == "💰 Business Model":

            default_content = startup.get(
                "revenue_model", ""
            )

        else:

            default_content = (
                f"{startup.get('startup_name', '')} "
                f"is a startup in the "
                f"{startup.get('industry', '')} industry."
            )

        content = st.text_area(
            "Your Content",
            value=default_content,
            height=180
        )

        if st.button(
            "✨ Generate AI Content",
            use_container_width=True
        ):

            try:

                from ai_assistant import generate_ai_content

                with st.spinner(
                    "🤖 AI is generating..."
                ):

                    result = generate_ai_content(
                        content_type,
                        startup.get("startup_name", ""),
                        startup.get("industry", ""),
                        content
                    )

                st.session_state.ai_content = result

                st.subheader(
                    "✨ AI-Generated Content"
                )

                st.success(result)

            except Exception as e:

                st.error(
                    "AI generation failed."
                )

                st.code(str(e))


# ============================================================
# PITCH DECK BUILDER
# ============================================================

elif page == "🎯 Pitch Deck Builder":

    st.header(
        "🎯 Investor Pitch Deck Builder"
    )

    startup = st.session_state.startup
    profile = st.session_state.profile
    portfolio = st.session_state.portfolio

    if not startup.get("startup_name"):

        st.warning(
            "⚠️ Complete Startup Details first."
        )

    else:

        st.subheader(
            "📋 Pitch Deck Summary"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Startup",
                startup.get("startup_name", "")
            )

        with col2:

            st.metric(
                "Industry",
                startup.get("industry", "")
            )

        with col3:

            st.metric(
                "Funding",
                startup.get("funding_stage", "")
            )

        with col4:

            st.metric(
                "Growth",
                startup.get("growth_rate", "N/A")
            )

        st.divider()

        st.subheader("📑 Pitch Deck Slides")

        slides = [
            ("01", "Startup Cover"),
            ("02", "Problem"),
            ("03", "Solution"),
            ("04", "Market Opportunity"),
            ("05", "Business Model"),
            ("06", "Competitive Advantage"),
            ("07", "Traction & Financial Snapshot"),
            ("08", "Founder & Team"),
            ("09", "Future Roadmap"),
            ("10", "Closing")
        ]

        cols = st.columns(2)

        for i, (number, title) in enumerate(slides):

            with cols[i % 2]:

                st.info(
                    f"**{number}. {title}**"
                )

        st.divider()

        # ----------------------------------------------------
        # PPTX
        # ----------------------------------------------------

        st.subheader(
            "📊 PowerPoint Pitch Deck"
        )

        if create_pitch_deck is None:

            st.error(
                "pitch_deck.py could not be loaded."
            )

        else:

            if st.button(
                "🎯 Generate Pitch Deck",
                use_container_width=True
            ):

                try:

                    with st.spinner(
                        "Creating professional pitch deck..."
                    ):

                        ppt_file = create_pitch_deck(
                            profile,
                            startup,
                            portfolio
                        )

                    st.session_state.pitch_generated = True

                    st.success(
                        "✅ Pitch deck created successfully!"
                    )

                    st.download_button(
                        "⬇️ Download PowerPoint",
                        data=ppt_file.getvalue(),
                        file_name=(
                            f"{startup.get('startup_name', 'Startup')}"
                            "_Pitch_Deck.pptx"
                        ),
                        mime=(
                            "application/vnd.openxmlformats-"
                            "officedocument.presentationml.presentation"
                        ),
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        "Pitch deck generation failed."
                    )

                    st.exception(e)

        st.divider()

        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------

        st.subheader(
            "📄 Entrepreneur Portfolio PDF"
        )

        if create_portfolio_pdf is None:

            st.error(
                "portfolio_pdf.py could not be loaded."
            )

        else:

            if st.button(
                "📄 Generate Portfolio PDF",
                use_container_width=True
            ):

                try:

                    with st.spinner(
                        "Creating portfolio PDF..."
                    ):

                        pdf_file = create_portfolio_pdf(
                            profile,
                            startup,
                            portfolio,
                            st.session_state.get(
                                "ai_content",
                                ""
                            )
                        )

                    st.success(
                        "✅ Portfolio PDF created successfully!"
                    )

                    st.download_button(
                        "⬇️ Download Portfolio PDF",
                        data=pdf_file.getvalue(),
                        file_name=(
                            f"{startup.get('startup_name', 'Startup')}"
                            "_Entrepreneur_Portfolio.pdf"
                        ),
                        mime="application/pdf",
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        "Portfolio PDF generation failed."
                    )

                    st.exception(e)

        st.divider()

        st.success(
            "Your portfolio and investor pitch materials "
            "are ready to export."
        )