import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ── Page Configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Retail Sales Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS for a cleaner, more professional look ─────────────────────────
st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 700; margin-bottom: 0.2rem; }
    .sub-title  { font-size: 1rem; color: #888; margin-bottom: 1.5rem; }
    .insight-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border-left: 4px solid #4fc3f7;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0;
        color: #e0e0e0;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    .rq-tag {
        background: #4fc3f7;
        color: #0d0d0d;
        padding: 2px 10px;
        border-radius: 99px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: inline-block;
    }
    .section-divider { border-top: 1px solid #333; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data(file):
    df = pd.read_csv(file, encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date']  = pd.to_datetime(df['Ship Date'])
    df['Year']       = df['Order Date'].dt.year
    df['Month']      = df['Order Date'].dt.to_period('M').astype(str)
    return df

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛒 Retail Sales Analytics")
    st.markdown("---")

    # Project info
    st.markdown("**Project:** Sales Data Analysis and Visualization for Retail Business Decision-Making")
    st.markdown("**By:** Varsha Reddy Gangasani")
    st.markdown("---")

    # File upload
    st.markdown("### 📁 Upload Your Data")
    uploaded_file = st.sidebar.file_uploader(
        "Upload any retail sales CSV file",
        type=["csv"],
        help="Upload your own retail CSV dataset to analyze it instantly"
    )
    if uploaded_file:
        df = load_data(uploaded_file)
        st.success("✅ Your dataset loaded successfully!")
    else:
        df = load_data("superstore.csv")
        st.info("Using default Superstore dataset (Kaggle, 2021)")

    st.markdown("---")

    # Filters
    st.markdown("### 🔽 Filters")
    st.caption("Use these to explore specific segments of your data")
    years    = ["All"] + sorted(df['Year'].unique().tolist())
    segments = ["All"] + sorted(df['Segment'].unique().tolist())
    regions  = ["All"] + sorted(df['Region'].unique().tolist())

    sel_year    = st.selectbox("📅 Year",    years,    help="Filter all charts by a specific year")
    sel_segment = st.selectbox("👥 Segment", segments, help="Focus on a specific customer segment")
    sel_region  = st.selectbox("🌍 Region",  regions,  help="Focus on a specific geographic region")

    # Apply filters
    filtered = df.copy()
    if sel_year    != "All": filtered = filtered[filtered['Year']    == sel_year]
    if sel_segment != "All": filtered = filtered[filtered['Segment'] == sel_segment]
    if sel_region  != "All": filtered = filtered[filtered['Region']  == sel_region]

    st.markdown("---")

    # How to use
    with st.expander("ℹ️ How to Use This App"):
        st.markdown("""
**Getting started:**
1. Upload your own CSV file or use the default dataset
2. Use the filters above to focus on specific years, segments, or regions
3. Navigate through the tabs to explore different analyses

**Each tab answers a research question:**
- **Overview** → What does my sales data look like?
- **Segmentation** → How do customer groups perform?
- **Sales Trends** → How have sales changed over time?
- **RFM Analysis** → Who are my best and at-risk customers?
- **Visualization Impact** → Why does visualization matter?
- **Recommendations** → What should my business do next?
        """)

    st.markdown("---")
    st.caption("📊 Data Source: Vivek, R. (2021). Superstore Dataset. Kaggle. https://www.kaggle.com/datasets/vivek468/superstore-dataset-final")

# ── Navigation Tabs ───────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Overview",
    "👥 Customer Segmentation",
    "📈 Sales Trends",
    "🔬 RFM Analysis",
    "📊 Visualization Impact",
    "💡 Recommendations",
])

# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ═════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="main-title">🛒 Retail Sales Analytics Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Transforming raw retail data into clear, actionable business intelligence</div>', unsafe_allow_html=True)

    st.markdown("**What this tab shows:** A high-level summary of your retail sales performance including total revenue, orders, profit, and customer counts. Use the sidebar filters to explore specific years, segments, or regions.")
    st.markdown("---")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    total_sales   = filtered['Sales'].sum()
    total_orders  = filtered['Order ID'].nunique()
    total_profit  = filtered['Profit'].sum()
    total_cust    = filtered['Customer ID'].nunique()
    profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

    col1.metric("💰 Total Sales",   f"${total_sales:,.0f}")
    col2.metric("📦 Total Orders",  f"{total_orders:,}")
    col3.metric("💵 Total Profit",  f"${total_profit:,.0f}",
                delta=f"{profit_margin:.1f}% margin")
    col4.metric("👤 Customers",     f"{total_cust:,}")

    st.markdown("---")

    col_a, col_b = st.columns(2)
    with col_a:
        cat_sales = filtered.groupby('Category')['Sales'].sum().reset_index()
        fig = px.bar(cat_sales, x='Category', y='Sales',
                     title='Total Sales by Product Category',
                     color='Category',
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     labels={'Sales': 'Total Sales ($)', 'Category': 'Product Category'})
        fig.update_layout(showlegend=False, yaxis_tickprefix='$')
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        region_sales = filtered.groupby('Region')['Sales'].sum().reset_index()
        fig2 = px.pie(region_sales, names='Region', values='Sales',
                      title='Sales Distribution by Region',
                      color_discrete_sequence=px.colors.qualitative.Pastel,
                      hole=0.4)
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig2, use_container_width=True)



# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — CUSTOMER SEGMENTATION
# ═════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="main-title">👥 Customer Segmentation Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="rq-tag">RQ1 & RQ3</div>', unsafe_allow_html=True)
    st.markdown("**What this tab shows:** How the three customer segments (Consumer, Corporate, Home Office) compare across revenue, profit margin, purchase frequency, and average order value. This directly answers how customer segmentation impacts sales performance and profitability.")
    st.markdown("---")

    seg = filtered.groupby('Segment').agg(
        Total_Sales      = ('Sales',       'sum'),
        Total_Profit     = ('Profit',      'sum'),
        Total_Orders     = ('Order ID',    'nunique'),
        Unique_Customers = ('Customer ID', 'nunique'),
        Avg_Order_Value  = ('Sales',       'mean')
    ).reset_index()
    seg['Profit_Margin_%']     = (seg['Total_Profit'] / seg['Total_Sales'] * 100).round(2)
    seg['Avg_Orders_Per_Cust'] = (seg['Total_Orders'] / seg['Unique_Customers']).round(1)

    # Summary table
    st.subheader("📋 Full Segment Comparison — Revenue, Frequency & Profit")
    st.caption("This table shows all three sales metrics side by side: revenue, purchase frequency, and profitability — directly answering RQ3.")
    display_seg = seg[['Segment','Total_Sales','Total_Profit','Profit_Margin_%',
                        'Total_Orders','Avg_Orders_Per_Cust','Avg_Order_Value','Unique_Customers']].copy()
    display_seg.columns = ['Segment','Total Sales','Total Profit','Profit Margin %',
                           'Total Orders','Avg Orders/Customer','Avg Order Value','Customers']
    st.dataframe(display_seg.style.format({
        'Total Sales':       '${:,.0f}',
        'Total Profit':      '${:,.0f}',
        'Profit Margin %':   '{:.1f}%',
        'Avg Order Value':   '${:,.0f}',
        'Avg Orders/Customer': '{:.1f}'
    }), use_container_width=True)

    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        fig3 = px.bar(seg, x='Segment', y='Total_Sales',
                      title='Total Revenue by Customer Segment',
                      color='Segment',
                      color_discrete_sequence=['#636EFA','#EF553B','#00CC96'],
                      labels={'Total_Sales': 'Total Revenue ($)', 'Segment': 'Customer Segment'})
        fig3.update_layout(showlegend=False, yaxis_tickprefix='$')
        st.plotly_chart(fig3, use_container_width=True)

    with c2:
        fig4 = px.bar(seg, x='Segment', y='Profit_Margin_%',
                      title='Profit Margin % by Customer Segment',
                      color='Segment',
                      color_discrete_sequence=['#636EFA','#EF553B','#00CC96'],
                      labels={'Profit_Margin_%': 'Profit Margin (%)', 'Segment': 'Customer Segment'})
        fig4.add_hline(y=seg['Profit_Margin_%'].mean(),
                       line_dash="dash", line_color="gray",
                       annotation_text=f"Average: {seg['Profit_Margin_%'].mean():.1f}%")
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig_freq = px.bar(seg, x='Segment', y='Avg_Orders_Per_Cust',
                          title='Average Purchase Frequency per Customer',
                          color='Segment',
                          color_discrete_sequence=['#AB63FA','#FFA15A','#19D3F3'],
                          labels={'Avg_Orders_Per_Cust': 'Avg Orders per Customer', 'Segment': 'Customer Segment'})
        fig_freq.update_layout(showlegend=False)
        st.plotly_chart(fig_freq, use_container_width=True)

    with c4:
        heatmap_data = filtered.pivot_table(
            values='Sales', index='Segment', columns='Category', aggfunc='sum')
        fig5 = px.imshow(heatmap_data, text_auto=',.0f',
                         color_continuous_scale='Blues',
                         title='Sales Heatmap: Customer Segment vs Product Category',
                         labels={'color': 'Total Sales ($)'})
        st.plotly_chart(fig5, use_container_width=True)

    # Download button
    st.download_button(
        "⬇️ Download Segment Analysis as CSV",
        display_seg.to_csv(index=False),
        "segment_analysis.csv",
        "text/csv",
        help="Download this segment comparison table for use in reports"
    )

# ═════════════════════════════════════════════════════════════════════════════
# TAB 3 — SALES TRENDS
# ═════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="main-title">📈 Sales & Profit Trends Over Time</div>', unsafe_allow_html=True)
    st.markdown("**What this tab shows:** How sales and profit have changed month by month, which sub-categories generate the most revenue, and how discounts affect profitability. Identifies seasonal patterns and pricing risks.")
    st.markdown("---")

    monthly = filtered.groupby('Month').agg(
        Sales  = ('Sales',  'sum'),
        Profit = ('Profit', 'sum')
    ).reset_index()

    fig6 = px.line(monthly, x='Month', y=['Sales','Profit'],
                   title='Monthly Sales vs Profit Trend (2014–2017)',
                   markers=True,
                   color_discrete_map={'Sales':'#636EFA','Profit':'#00CC96'},
                   labels={'value': 'Amount ($)', 'Month': 'Month', 'variable': 'Metric'})
    fig6.update_layout(
        yaxis_title='Amount ($)',
        xaxis_title='Month',
        legend_title='Metric',
        yaxis_tickprefix='$'
    )
    fig6.update_xaxes(tickangle=45)
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("---")
    c3, c4 = st.columns(2)
    with c3:
        sub_sales = filtered.groupby('Sub-Category')['Sales'].sum()\
                            .sort_values(ascending=False).head(10).reset_index()
        fig7 = px.bar(sub_sales, x='Sales', y='Sub-Category',
                      orientation='h',
                      title='Top 10 Sub-Categories by Total Sales',
                      color='Sales',
                      color_continuous_scale='Blues',
                      labels={'Sales': 'Total Sales ($)', 'Sub-Category': 'Product Sub-Category'})
        fig7.update_layout(xaxis_tickprefix='$', coloraxis_showscale=False)
        st.plotly_chart(fig7, use_container_width=True)

    with c4:
        disc_profit = filtered.groupby('Discount')['Profit'].mean().reset_index()
        fig8 = px.scatter(disc_profit, x='Discount', y='Profit',
                          title='Impact of Discount Rate on Average Profit',
                          trendline='ols',
                          color_discrete_sequence=['#EF553B'],
                          labels={'Discount': 'Discount Rate', 'Profit': 'Average Profit ($)'})
        fig8.add_vline(x=0.3, line_dash="dash", line_color="orange",
                       annotation_text="30% threshold", annotation_position="top right")
        fig8.update_layout(yaxis_tickprefix='$')
        st.plotly_chart(fig8, use_container_width=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 4 — RFM ANALYSIS
# ═════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="main-title">🔬 RFM Customer Segmentation Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="rq-tag">RQ2</div>', unsafe_allow_html=True)
    st.markdown("**What this tab shows:** RFM Analysis automatically groups your customers into 5 behavioral segments based on their actual purchasing patterns — no manual categorization needed. This answers what distinct customer segments exist in your data.")
    st.markdown("---")

    # Plain English RFM explanation
    with st.expander("📖 What is RFM Analysis? (Click to learn)"):
        st.markdown("""
**RFM stands for Recency, Frequency, and Monetary value** — three measures of customer purchasing behavior:

| Measure | What it means | Better score means... |
|---|---|---|
| **Recency (R)** | How recently did the customer last purchase? | They bought very recently |
| **Frequency (F)** | How many times have they purchased? | They buy often |
| **Monetary (M)** | How much have they spent in total? | They spend a lot |

Each customer receives a score of 1–4 on each dimension, giving a combined score from 3–12.
The higher the score, the more valuable the customer.

**The 5 segments this creates:**
- 🏆 **Champions** — Bought recently, buy often, spend the most
- 💙 **Loyal Customers** — Buy regularly with good monetary value
- 🌱 **Potential Loyalists** — Recent buyers with moderate frequency
- ⚠️ **At Risk** — Used to buy but haven't recently
- ❌ **Lost Customers** — Haven't purchased in a long time
        """)

    # RFM Calculation
    snapshot_date = df['Order Date'].max() + pd.Timedelta(days=1)
    rfm = df.groupby('Customer ID').agg(
        Recency   = ('Order Date',  lambda x: (snapshot_date - x.max()).days),
        Frequency = ('Order ID',    'nunique'),
        Monetary  = ('Sales',       'sum')
    ).reset_index()

    rfm['R_Score'] = pd.qcut(rfm['Recency'],   q=4, labels=[4,3,2,1]).astype(int)
    rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), q=4, labels=[1,2,3,4]).astype(int)
    rfm['M_Score'] = pd.qcut(rfm['Monetary'],  q=4, labels=[1,2,3,4]).astype(int)
    rfm['RFM_Score'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']

    def rfm_segment(score):
        if score >= 10:   return 'Champions'
        elif score >= 8:  return 'Loyal Customers'
        elif score >= 6:  return 'Potential Loyalists'
        elif score >= 4:  return 'At Risk'
        else:             return 'Lost Customers'

    rfm['RFM_Segment'] = rfm['RFM_Score'].apply(rfm_segment)

    seg_colors = {
        'Champions':          '#00CC96',
        'Loyal Customers':    '#636EFA',
        'Potential Loyalists':'#FFA15A',
        'At Risk':            '#EF553B',
        'Lost Customers':     '#AB63FA'
    }

    col_a, col_b = st.columns(2)
    with col_a:
        seg_count = rfm['RFM_Segment'].value_counts().reset_index()
        seg_count.columns = ['RFM_Segment','Count']
        fig_rfm1 = px.pie(seg_count, names='RFM_Segment', values='Count',
                          title='Customer Distribution by RFM Segment',
                          color='RFM_Segment',
                          color_discrete_map=seg_colors,
                          hole=0.4)
        fig_rfm1.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_rfm1, use_container_width=True)

    with col_b:
        seg_monetary = rfm.groupby('RFM_Segment')['Monetary'].mean().reset_index()
        fig_rfm2 = px.bar(seg_monetary, x='RFM_Segment', y='Monetary',
                          title='Average Spending by RFM Segment',
                          color='RFM_Segment',
                          color_discrete_map=seg_colors,
                          labels={'Monetary': 'Average Spending ($)', 'RFM_Segment': 'Customer Segment'})
        fig_rfm2.update_layout(showlegend=False, yaxis_tickprefix='$')
        st.plotly_chart(fig_rfm2, use_container_width=True)

    col_c, col_d = st.columns(2)
    with col_c:
        fig_rfm3 = px.scatter(rfm, x='Frequency', y='Monetary',
                              color='RFM_Segment', size='Monetary',
                              title='Purchase Frequency vs Total Spending by Segment',
                              color_discrete_map=seg_colors,
                              labels={'Frequency': 'Purchase Frequency (orders)', 'Monetary': 'Total Spending ($)', 'RFM_Segment': 'Segment'},
                              hover_data=['Customer ID'])
        fig_rfm3.update_layout(yaxis_tickprefix='$')
        st.plotly_chart(fig_rfm3, use_container_width=True)

    with col_d:
        seg_freq = rfm.groupby('RFM_Segment')['Frequency'].mean().reset_index()
        fig_rfm4 = px.bar(seg_freq, x='RFM_Segment', y='Frequency',
                          title='Average Purchase Frequency by RFM Segment',
                          color='RFM_Segment',
                          color_discrete_map=seg_colors,
                          labels={'Frequency': 'Avg Purchase Frequency', 'RFM_Segment': 'Customer Segment'})
        fig_rfm4.update_layout(showlegend=False)
        st.plotly_chart(fig_rfm4, use_container_width=True)

    # RFM Summary Table
    st.markdown("---")
    st.subheader("📋 RFM Segment Summary Table")
    rfm_summary = rfm.groupby('RFM_Segment').agg(
        Customers     = ('Customer ID', 'count'),
        Avg_Recency   = ('Recency',     'mean'),
        Avg_Frequency = ('Frequency',   'mean'),
        Avg_Spending  = ('Monetary',    'mean'),
        Total_Revenue = ('Monetary',    'sum')
    ).reset_index().round(1)
    rfm_summary.columns = ['Segment','Customers','Avg Days Since Purchase','Avg Orders','Avg Spending ($)','Total Revenue ($)']
    st.dataframe(rfm_summary.style.format({
        'Avg Spending ($)':   '${:,.0f}',
        'Total Revenue ($)':  '${:,.0f}',
    }), use_container_width=True)

    # Download button
    st.download_button(
        "⬇️ Download Full RFM Results as CSV",
        rfm[['Customer ID','Recency','Frequency','Monetary','R_Score','F_Score','M_Score','RFM_Score','RFM_Segment']].to_csv(index=False),
        "rfm_customer_segments.csv",
        "text/csv",
        help="Download individual customer RFM scores for CRM or marketing use"
    )

# ═════════════════════════════════════════════════════════════════════════════
# TAB 5 — VISUALIZATION IMPACT
# ═════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="main-title">📊 How Visualization Improves Decision-Making</div>', unsafe_allow_html=True)
    st.markdown('<div class="rq-tag">RQ4 — Main Research Question</div>', unsafe_allow_html=True)
    st.markdown("**What this tab shows:** A direct, side-by-side demonstration that data visualization transforms raw numbers into instant, actionable insights. This tab answers the main research question by showing the same data in two formats — raw vs. visual.")
    st.markdown("---")

    st.subheader("🔴 Without Visualization — Raw Data Only")
    st.caption("Look at this table and try to answer: Which segment is most profitable? Which region underperforms? How are discounts affecting margins?")
    raw = filtered[['Order Date','Segment','Region','Category','Sales','Profit','Discount','Quantity']].head(20)
    st.dataframe(raw, use_container_width=True)
    st.error("❌ It is difficult and time-consuming to identify patterns, trends, or actionable insights from raw numbers alone. A business decision-maker would need minutes — or longer — to reach any conclusion from this table.")

    st.markdown("---")
    st.subheader("🟢 With Visualization — Instant Insights")
    st.caption("The exact same data, visualized. Patterns that were invisible above become immediately obvious.")

    v1, v2 = st.columns(2)
    with v1:
        seg_vis = filtered.groupby('Segment').agg(
            Sales  = ('Sales',  'sum'),
            Profit = ('Profit', 'sum')
        ).reset_index()
        fig_v1 = px.bar(seg_vis, x='Segment', y=['Sales','Profit'],
                        title='Sales vs Profit by Segment — Instantly Comparable',
                        barmode='group',
                        color_discrete_map={'Sales':'#636EFA','Profit':'#00CC96'},
                        labels={'value': 'Amount ($)', 'Segment': 'Customer Segment', 'variable': 'Metric'})
        fig_v1.update_layout(yaxis_tickprefix='$', yaxis_title='Amount ($)')
        st.plotly_chart(fig_v1, use_container_width=True)

    with v2:
        region_vis = filtered.groupby('Region').agg(
            Sales  = ('Sales',  'sum'),
            Profit = ('Profit', 'sum')
        ).reset_index()
        fig_v2 = px.bar(region_vis, x='Region', y=['Sales','Profit'],
                        title='Regional Performance — Underperformers Visible Instantly',
                        barmode='group',
                        color_discrete_map={'Sales':'#636EFA','Profit':'#00CC96'},
                        labels={'value': 'Amount ($)', 'Region': 'Sales Region', 'variable': 'Metric'})
        fig_v2.update_layout(yaxis_tickprefix='$', yaxis_title='Amount ($)')
        st.plotly_chart(fig_v2, use_container_width=True)

    st.success("✅ In under 5 seconds, you can see which segment leads in profit margin and which region underperforms — insights that would take minutes to find in the raw table above.")

    st.markdown("---")
    st.subheader("⚡ The Power of Interactive Filtering")
    st.caption("Use the sidebar filters right now — change Segment from All to Consumer. Watch every chart across all tabs update instantly. This is the core value of this dashboard.")

    v3, v4 = st.columns(2)
    with v3:
        monthly_vis = filtered.groupby('Month')['Sales'].sum().reset_index()
        fig_v3 = px.line(monthly_vis, x='Month', y='Sales',
                         title='Sales Trend — Seasonality Visible at a Glance',
                         markers=True,
                         color_discrete_sequence=['#636EFA'],
                         labels={'Sales': 'Total Sales ($)', 'Month': 'Month'})
        fig_v3.update_xaxes(tickangle=45)
        fig_v3.update_layout(yaxis_tickprefix='$')
        st.plotly_chart(fig_v3, use_container_width=True)

    with v4:
        cat_vis = filtered.groupby(['Category','Segment'])['Profit'].sum().reset_index()
        fig_v4 = px.bar(cat_vis, x='Category', y='Profit', color='Segment',
                        title='Profit by Category & Segment — Multi-Dimensional Insight',
                        barmode='group',
                        labels={'Profit': 'Total Profit ($)', 'Category': 'Product Category', 'Segment': 'Customer Segment'})
        fig_v4.update_layout(yaxis_tickprefix='$')
        st.plotly_chart(fig_v4, use_container_width=True)

# ═════════════════════════════════════════════════════════════════════════════
# TAB 6 — RECOMMENDATIONS
# ═════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="main-title">💡 Automated Business Recommendations</div>', unsafe_allow_html=True)
    st.markdown("**What this tab shows:** Automated, data-driven business recommendations generated directly from your filtered data. These recommendations update whenever you change the sidebar filters — making this a reusable decision-support tool for any retail dataset.")
    st.markdown("---")

    # Recalculate for recommendations
    seg2           = filtered.groupby('Segment').agg(
                         Total_Sales=('Sales','sum'), Total_Profit=('Profit','sum'),
                         Total_Orders=('Order ID','nunique'), Unique_Customers=('Customer ID','nunique')
                     ).reset_index()
    seg2['Profit_Margin_%'] = (seg2['Total_Profit'] / seg2['Total_Sales'] * 100).round(2)

    top_seg        = seg2.loc[seg2['Total_Sales'].idxmax(), 'Segment']
    top_profit_seg = seg2.loc[seg2['Profit_Margin_%'].idxmax(), 'Segment']
    top_margin_val = seg2['Profit_Margin_%'].max()
    top_cat        = filtered.groupby('Category')['Sales'].sum().idxmax()
    top_region     = filtered.groupby('Region')['Sales'].sum().idxmax()
    low_region     = filtered.groupby('Region')['Sales'].sum().idxmin()
    high_disc      = filtered[filtered['Discount'] > 0.3]
    discount_loss  = high_disc[high_disc['Profit'] < 0].shape[0]
    champions_n    = rfm[rfm['RFM_Segment']=='Champions'].shape[0]
    at_risk_n      = rfm[rfm['RFM_Segment']=='At Risk'].shape[0]

    st.subheader("📌 Strategic Recommendations")

    col1, col2 = st.columns(2)
    with col1:
        st.success(f"**1. Double down on {top_seg} customers**\n\nThis segment generates the highest total revenue. Invest in loyalty programs, personalized promotions, and retention campaigns targeted at {top_seg} customers to protect and grow your largest revenue source.")
        st.info(f"**2. Grow your {top_profit_seg} segment**\n\nWith the highest profit margin at {top_margin_val:.1f}%, the {top_profit_seg} segment generates the best return per dollar of sales. Consider premium product bundles, dedicated account management, or B2B outreach to grow this segment.")
        st.success(f"**3. Prioritize {top_cat} inventory**\n\nThis is your top-performing product category. Ensure strong stock levels at all times and explore upselling and cross-selling opportunities within this category to maximize revenue per transaction.")

    with col2:
        st.info(f"**4. Replicate {top_region} success in {low_region}**\n\nThe {top_region} region leads in total sales. Analyze what marketing, pricing, and product strategies are working there and apply the same approach to improve performance in the underperforming {low_region} region.")
        st.success(f"**5. Re-engage your {champions_n} Champion customers**\n\nThese are your highest-value customers based on RFM analysis. Reward them with exclusive early access to new products, VIP discounts, or loyalty rewards to maintain their high engagement and spending.")
        if at_risk_n > 0:
            st.warning(f"**⚠️ 6. Urgently re-engage {at_risk_n} At-Risk customers**\n\nThese customers have not purchased recently and are at high risk of churning. Launch a targeted win-back campaign with personalized offers immediately — waiting longer significantly reduces the chance of recovery.")
        if discount_loss > 0:
            st.warning(f"**⚠️ 7. Reform your discount policy — {discount_loss:,} loss-making orders**\n\nOrders with discounts above 30% consistently result in financial losses. Implementing a maximum discount cap of 20–25% would eliminate these losses while still supporting promotional sales activity.")

    st.markdown("---")
    st.subheader("🔍 Explore the Underlying Data")
    st.caption("Browse and search the raw transaction data behind these recommendations")
    st.dataframe(
        filtered[['Order Date','Segment','Category','Sub-Category',
                  'Region','Sales','Profit','Discount','Quantity']].reset_index(drop=True),
        use_container_width=True
    )
    st.download_button(
        "⬇️ Download Filtered Data as CSV",
        filtered.to_csv(index=False),
        "filtered_sales_data.csv",
        "text/csv",
        help="Download the current filtered dataset for further analysis"
    )

    st.markdown("---")
    st.caption("Built by Varsha Reddy Gangasani | IT Final Project 2026 | Retail Sales Analytics Dashboard")