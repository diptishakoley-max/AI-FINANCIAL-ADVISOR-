# Visualization Module
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns


# Visualization: Detailed Advised Financial Health
def plot_advised_financial_overview(user_data, analysis_data):

    expenses = user_data["expenses"]
    savings = analysis_data["savings"]
    emergency_fund_monthly = analysis_data["emergency_fund_monthly"]

    investment_allocation = analysis_data["recommended_investment_allocation"]
    high_interest = investment_allocation.get("High-Interest Savings / RD", 0)
    stocks = investment_allocation.get("Stocks / Equity Funds", 0)
    etfs = investment_allocation.get("ETFs / Balanced Funds", 0)
    risk_free = investment_allocation.get("Debt Mutual Funds / Bonds", 0)

    total_investments = high_interest + stocks + etfs + risk_free
    remaining_savings = max(0, savings - (emergency_fund_monthly + total_investments))

    labels = [
        "Emergency Fund",
        "High-Interest Savings / RD",
        "Stocks / Equity Funds",
        "ETFs / Balanced Funds",
        "Debt Mutual Funds / Bonds",
        "Remaining Savings"
    ]
    values = [
        emergency_fund_monthly,
        high_interest,
        stocks,
        etfs,
        risk_free,
        remaining_savings
    ]

    # Filter out zero values
    filtered = [(l, v) for l, v in zip(labels, values) if v > 0]
    if filtered:
        labels, values = zip(*filtered)
        labels = list(labels)
        values = list(values)
    else:
        labels = ["No Savings"]
        values = [1]

    colors = sns.color_palette("pastel", len(values))

    fig, ax = plt.subplots(1, 2, figsize=(14, 6))
    fig.patch.set_facecolor("#F9FAFB")

    wedges, texts, autotexts = ax[0].pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        startangle=140,
        colors=colors,
        pctdistance=0.85,
        wedgeprops=dict(edgecolor="white", linewidth=1.5)
    )
    for text in texts:
        text.set_fontsize(9)
        text.set_color("#333333")
    for autotext in autotexts:
        autotext.set_fontsize(8)
        autotext.set_color("#333333")
        autotext.set_fontweight("bold")
    ax[0].set_title("Savings & Investment Distribution", pad=35, fontweight="bold", fontsize=11, color="#222222")

    sns.set_style("whitegrid")
    sns.barplot(
        x=labels,
        y=values,
        hue=labels,
        palette=colors,
        legend=False,
        ax=ax[1]
    )
    ax[1].set_facecolor("#FFFFFF")
    ax[1].grid(axis="y", linestyle="--", alpha=0.5)
    ax[1].set_ylabel("Amount (₹)", fontsize=10, fontweight="bold", color="#222222")
    ax[1].tick_params(axis="x", rotation=90, labelsize=9)
    ax[1].set_title("Component-wise Financial Impact", pad=35, fontweight="bold", fontsize=11, color="#222222")

    for i, value in enumerate(values):
        ax[1].text(
            i, value + max(values) * 0.02,
            f'₹{value:,.0f}',
            ha='center', fontsize=9, fontweight='bold', color="#222222"
        )

    plt.tight_layout(rect=[0.05, 0.1, 0.95, 0.95])
    plt.subplots_adjust(wspace=0.4)

    return fig
