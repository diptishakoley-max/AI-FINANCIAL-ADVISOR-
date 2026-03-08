import streamlit as st
from finance_analysis import analyze_finances
from ai_advisor import generate_financial_advice, generate_goal_plan, finance_chatbot_response
from visualization import plot_advised_financial_overview
from utils import split_advice_sections, split_goal_sections

# Page configuration
st.set_page_config(
    page_title="AI Financial Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS from file
def load_css():
    with open('styles.css', 'r') as f:
        css = f.read()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

load_css()

# Initialize Session State
if "user_data" not in st.session_state:
    st.session_state.user_data = None
if "analysis_data" not in st.session_state:
    st.session_state.analysis_data = None
if "generated_advice" not in st.session_state:
    st.session_state.generated_advice = None
if "goal_plan" not in st.session_state:
    st.session_state.goal_plan = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

# HEADER SECTION
st.markdown('<div class="main-header">💰 AI Financial Advisor</div>', unsafe_allow_html=True)
st.markdown('<div class="subheader">Your Personal AI-Powered Financial Planning Assistant</div>', unsafe_allow_html=True)

st.markdown("""
<div class='hero-section' style='text-align: center;'>
    <h2 style='color: white; font-size: 2.5rem; margin-bottom: 1rem;'>Take Control of Your Financial Future</h2>
    <p style='font-size: 1.2rem; color: #f0f0f0; margin-bottom: 0.5rem;'>
    Get personalized financial advice, investment strategies, and goal planning powered by AI
    </p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR INPUTS
with st.sidebar:
    st.markdown(" ")
    profile = st.selectbox(
        "Profile Type",
        ["Student", "Professional", "Other"],
        help="Select your current profile type"
    )

    if profile == "Student":
        income = st.number_input(
            "Monthly Allowance / Stipend (₹)",
            min_value=0, value=10000, step=500,
            help="Enter your monthly allowance or stipend"
        )
        part_time = st.selectbox(
            "Do you have part-time income?",
            ["No", "Yes"],
            help="Select if you have additional income from part-time work"
        )
        if part_time == "Yes":
            extra_income = st.number_input(
                "Part-time Income (₹)",
                min_value=0, value=5000, step=500,
                help="Enter your monthly part-time income"
            )
            income += extra_income
    elif profile == "Professional":
        income = st.number_input(
            "Monthly Salary (₹)",
            min_value=0, value=50000, step=1000,
            help="Enter your monthly salary after tax"
        )
    else:
        income = st.number_input(
            "Monthly Income (₹)",
            min_value=0, value=30000, step=1000,
            help="Enter your total monthly income"
        )

    expenses = st.number_input(
        "Monthly Expenses (₹)",
        min_value=0, value=20000, step=1000,
        help="Enter your total monthly expenses"
    )

    existing_savings = st.number_input(
        "Existing Savings & Investments (₹)",
        min_value=0, value=50000, step=5000,
        help="Enter your total existing savings and investments"
    )

    debts = st.number_input(
        "Total Debts (₹)",
        min_value=0, value=10000, step=1000,
        help="Enter your total outstanding debts"
    )

    goals_input = st.text_area(
        "Financial Goals (comma-separated)",
        value="Emergency Fund, Retirement",
        help="Enter your financial goals separated by commas"
    )
    goals = [goal.strip() for goal in goals_input.split(",") if goal.strip()]

    risk_tolerance = st.selectbox(
        "Risk Tolerance",
        ["Low", "Medium", "High"],
        help="Select your risk tolerance level"
    )

    st.session_state.user_data = {
        "profile": profile,
        "income": income,
        "expenses": expenses,
        "debts": debts,
        "existing_savings": existing_savings,
        "risk_tolerance": risk_tolerance,
        "goals": goals
    }

    generate_btn = st.button("Financial Analysis & Advice")

# Process when button is clicked
if generate_btn:
    user_data = st.session_state.user_data
    st.session_state.analysis_data = analyze_finances(user_data)

    with st.spinner("🤖 Generating personalized financial advice..."):
        st.session_state.generated_advice = generate_financial_advice(user_data, st.session_state.analysis_data)

    st.session_state.goal_plan = None
    st.session_state.chat_history = []

# MAIN CONTENT AREA
if st.session_state.user_data and st.session_state.user_data['income'] > 0:

    st.markdown("""
    <div class='hero-section' style='text-align: center;'>
        <h2 style='color: white; font-size: 1.8rem; margin-bottom: 0.5rem;'>📊 Your Financial Summary & Analysis</h2>
        <p style='font-size: 1rem; color: #f0f0f0;'>Comprehensive overview of your financial health</p>
    </div>
    """, unsafe_allow_html=True)

    if generate_btn:
        st.session_state.analysis_data = analyze_finances(st.session_state.user_data)
        st.session_state.generated_advice = generate_financial_advice(
            st.session_state.user_data,
            st.session_state.analysis_data
        )

    if st.session_state.analysis_data:
        ad = st.session_state.analysis_data

        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>₹{ad['savings']:,.0f}</div>
                <div class='metric-label'>Monthly Savings</div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>₹{ad['investment_capacity']:,.0f}</div>
                <div class='metric-label'>Investment Capacity</div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>₹{ad['emergency_fund']:,.0f}</div>
                <div class='metric-label'>Emergency Fund Target</div>
            </div>""", unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class='metric-card'>
                <div class='metric-value'>₹{ad['total_net_worth']:,.0f}</div>
                <div class='metric-label'>Total Net Worth</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(" ")
        st.markdown(" ")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>💰 Savings Ratio</div>
                <div class='card-content'>
                    <div class='metric-value'>{ad['savings_ratio']*100:.1f}%</div>
                    <p>Of your income goes to savings</p>
                </div>
            </div>""", unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>💳 Debt-to-Income</div>
                <div class='card-content'>
                    <div class='metric-value'>{ad['debt_to_income_ratio']*100:.1f}%</div>
                    <p>{"⚠️ High - prioritize repayment" if ad['high_debt_alert'] else "✅ Within healthy range"}</p>
                </div>
            </div>""", unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>📊 Expense Ratio</div>
                <div class='card-content'>
                    <div class='metric-value'>{ad['expense_ratio']*100:.1f}%</div>
                    <p>Of your income goes to expenses</p>
                </div>
            </div>""", unsafe_allow_html=True)

        # Progress Indicators
        st.markdown(" ")
        st.markdown(" ")
        st.markdown("#### Financial Health Indicators")
        col1, col2 = st.columns(2)

        with col1:
            savings_pct = min(ad['savings_ratio'] * 100, 100)
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>🏦 Savings Progress</div>
                <div class='card-content'>
                    <p>Savings Rate: <strong>{savings_pct:.1f}%</strong> of income</p>
                    <div style='background:#e9ecef; border-radius:8px; height:20px; margin:8px 0;'>
                        <div style='background:linear-gradient(90deg,#2e7d32,#4caf50); width:{savings_pct}%; height:100%; border-radius:8px;'></div>
                    </div>
                    <p style='font-size:0.85rem; color:#666;'>Target: 20-30% of income</p>
                    <p>Emergency Fund Shortfall: <strong>₹{ad['emergency_fund_shortfall']:,.0f}</strong></p>
                    <p>Monthly Contribution Needed: <strong>₹{ad['emergency_fund_monthly']:,.0f}</strong></p>
                </div>
            </div>""", unsafe_allow_html=True)

        with col2:
            debt_pct = min(ad['debt_to_income_ratio'] * 100, 100)
            debt_color = "#e65100" if ad['high_debt_alert'] else "#1565c0"
            st.markdown(f"""
            <div class='card'>
                <div class='card-title'>💳 Debt Health</div>
                <div class='card-content'>
                    <p>Debt-to-Income: <strong>{debt_pct:.1f}%</strong></p>
                    <div style='background:#e9ecef; border-radius:8px; height:20px; margin:8px 0;'>
                        <div style='background:{debt_color}; width:{debt_pct}%; height:100%; border-radius:8px;'></div>
                    </div>
                    <p style='font-size:0.85rem; color:#666;'>{"⚠️ Above 40% - High Risk" if ad['high_debt_alert'] else "✅ Below 40% - Healthy"}</p>
                    <p>Debt-to-Savings Ratio: <strong>{ad['debt_to_savings_ratio']:.2f}</strong></p>
                    <p>Existing Savings: <strong>₹{ad['existing_savings']:,.0f}</strong></p>
                </div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # Tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Financial Advice", "📊 Visualizations", "🎯 Goal Planner", "💬 Financial Chatbot"])

        # TAB 1: Financial Advice
        with tab1:
            if st.session_state.generated_advice:
                sections = split_advice_sections(st.session_state.generated_advice)
                if sections:
                    for title, content_html in sections:
                        st.markdown(f"""
                        <div class='card'>
                            <div class='card-title'>{title}</div>
                            <div class='card-content'>{content_html}</div>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='card'>
                        <div class='card-content'>{st.session_state.generated_advice}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("Click 'Financial Analysis & Advice' to generate your personalized financial plan.")

        # TAB 2: Visualizations
        with tab2:
            st.markdown("### 📊 Savings & Investment Distribution")
            fig = plot_advised_financial_overview(st.session_state.user_data, ad)
            st.pyplot(fig)

            st.markdown("### 📋 Detailed Breakdown")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                <div class='card'>
                    <div class='card-title'>💵 Income & Expenses</div>
                    <div class='card-content'>
                        <ul style='margin:0; padding-left:18px;'>
                            <li>Monthly Income: ₹{st.session_state.user_data['income']:,.0f}</li>
                            <li>Monthly Expenses: ₹{st.session_state.user_data['expenses']:,.0f}</li>
                            <li>Expense Ratio: {ad['expense_ratio']*100:.1f}%</li>
                            <li>Monthly Savings: ₹{ad['savings']:,.0f}</li>
                        </ul>
                    </div>
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='card'>
                    <div class='card-title'>🏦 Savings & Emergency Fund</div>
                    <div class='card-content'>
                        <ul style='margin:0; padding-left:18px;'>
                            <li>Existing Savings: ₹{st.session_state.user_data['existing_savings']:,.0f}</li>
                            <li>Emergency Fund Target: ₹{ad['emergency_fund']:,.0f}</li>
                            <li>Emergency Fund Shortfall: ₹{ad['emergency_fund_shortfall']:,.0f}</li>
                            <li>Monthly Emergency Contribution: ₹{ad['emergency_fund_monthly']:,.0f}</li>
                        </ul>
                    </div>
                </div>""", unsafe_allow_html=True)

        # TAB 3: Goal Planner
        with tab3:
            pass

        # Advanced Planning Input
        st.markdown("---")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 1.5rem;
                    border-radius: 15px;
                    text-align: center;
                    margin-bottom: 2rem;
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);'>
            <h1 style='font-size: 2rem; font-weight: 700; color: white; margin-bottom: 0.3rem;'>
                🔮 Goal-Oriented Planning
            </h1>
        </div>
        """, unsafe_allow_html=True)

        user_instructions = st.text_area(
            "Your Specific Instructions:",
            placeholder="e.g., I want to save 30% of income directly, Pay debt as fast as possible, Reach goal in 2 years, Invest only in stocks, etc.",
            height=80,
            help="Enter your specific financial instructions that will be prioritized above all else"
        )

        advanced_plan_btn = st.button("🔮 Generate Advanced Goal Plan", use_container_width=True)

        if advanced_plan_btn:
            if not user_instructions.strip():
                st.warning("Please enter your specific instructions for advanced planning")
            else:
                with st.spinner("Creating advanced plan with your specific instructions..."):
                    st.session_state.goal_plan = generate_goal_plan(
                        st.session_state.user_data,
                        st.session_state.analysis_data,
                        user_instructions
                    )

        if st.session_state.goal_plan:

            st.markdown("---")
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 1.5rem;
                        border-radius: 15px;
                        text-align: center;
                        margin-bottom: 2rem;
                        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);'>
                <h1 style='font-size: 2rem; font-weight: 700; color: white; margin-bottom: 0.3rem;'>
                    🔮 Goal-Oriented Planning
                </h1>
            </div>
            """, unsafe_allow_html=True)

            sections = split_goal_sections(st.session_state.goal_plan)

            col1, col2 = st.columns(2)

            for i, (title, content_html) in enumerate(sections):
                with col1 if i % 2 == 0 else col2:
                    st.markdown(f"""
                    <div class='goal-card'>
                        {f"<h4 style='color: #667eea; margin-bottom: 10px;'>{title}</h4>" if title else ""}
                        {content_html}
                    </div>
                    """, unsafe_allow_html=True)

        # TAB 4: Financial Chatbot
        with tab4:
            pass

        # CHATBOT SECTION
        st.markdown("---")
        st.markdown("""
        <div class='hero-section' style='text-align: center;'>
            <h2 style='color: white; font-size: 1.8rem; margin-bottom: 0.5rem;'>💬 Financial Chatbot</h2>
            <p style='font-size: 1rem; color: #f0f0f0;'>Ask any finance-related question and get personalized advice</p>
        </div>
        """, unsafe_allow_html=True)

        chat_col1, chat_col2 = st.columns([2, 1])

        with chat_col1:

            chat_container = st.container()
            with chat_container:
                for msg in st.session_state.chat_history:
                    if msg['user']:
                        st.markdown(f'<div class="chat-user">{msg["user"]}</div>', unsafe_allow_html=True)
                    if msg['bot']:
                        st.markdown(f'<div class="chat-bot">{msg["bot"]}</div>', unsafe_allow_html=True)

            # Chat Input
            st.session_state.user_query = st.text_area(
                "Ask your financial question...",
                value="",
                height=100,
                placeholder="e.g., Should I invest in SIPs or FDs? How can I reduce my expenses?",
                key="chat_input"
            )

            ask_col1, ask_col2, ask_col3 = st.columns([1, 2, 1])
            with ask_col2:
                ask_btn = st.button("📩 Send Message", use_container_width=True)

            if ask_btn:
                if st.session_state.user_query.strip():
                    with st.spinner("🤖 Thinking..."):
                        response = finance_chatbot_response(
                            st.session_state.user_data, ad, st.session_state.user_query
                        )
                    st.session_state.chat_history.append({
                        "user": st.session_state.user_query,
                        "bot": response
                    })
                    st.rerun()
                else:
                    st.warning("Please type a question.")

        with chat_col2:
            st.markdown("""
            <div class='card'>
                <h4>💡 Chat Tips</h4>
                <ul style='font-size: 0.9rem;'>
                    <li>Ask about investments</li>
                    <li>Get budgeting advice</li>
                    <li>Discuss debt management</li>
                    <li>Plan for specific goals</li>
                    <li>Understand financial terms</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div style='text-align: center; padding: 3rem; color: #666;'>
        <h3>👈 Fill in your financial details in the sidebar and click "Financial Analysis & Advice" to get started!</h3>
    </div>""", unsafe_allow_html=True)
