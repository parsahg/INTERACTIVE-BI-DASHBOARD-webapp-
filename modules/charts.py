import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import time
from modules.utils import translate_country_name
# Shared color palette
COLOR_PALETTE = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
    '#bcbd22', '#17becf'
]

# Shared date order
DATE_ORDER = [
    f"{m} 1402" for m in ["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"]
] + [
    f"{m} 1403" for m in ["فروردین","اردیبهشت","خرداد","تیر","مرداد","شهریور","مهر","آبان","آذر","دی","بهمن","اسفند"]
]


# --------------------------------------------------------------------
def show_treemap(sader1402, sader1403, matched):
    st.header("📊 نمودار تری‌مپ")
    dataset_options = {"دیتای 1402 تا 1403": pd.concat([sader1402, sader1403]), "دیتای مقایسه دو سال": matched}
    selected = st.radio("📂 دیتاست را انتخاب کنید", list(dataset_options.keys()), key="treemap_dataset")
    df = dataset_options[selected]

    cat_cols = df.select_dtypes(include='object').columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()

    category_col = st.selectbox("📌 متغیر کیفی", cat_cols)
    subcat1_col = st.selectbox("📌 زیرشاخه اول", cat_cols)
    subcat2_col = st.selectbox("📌 زیرشاخه دوم", cat_cols)
    value_col = st.selectbox("📌 متغیر کمی", num_cols)

    if st.button("ایجاد نمودار", key="treemap_btn"):
        if len({category_col, subcat1_col, subcat2_col, value_col}) < 4:
            st.error("❌ همه متغیرها را انتخاب کنید.")
            return

        df = df[[category_col, subcat1_col, subcat2_col, value_col]].dropna()
        total_value = df[value_col].sum()
        df['percentage'] = (df[value_col] / total_value) * 100

        fig = px.treemap(
            df, path=[category_col, subcat1_col, subcat2_col],
            values=value_col, color=category_col,
            color_discrete_sequence=COLOR_PALETTE,
            hover_data={'percentage': ':.2f'}
        )
        fig.update_layout(title="Treemap", title_font_size=28)
        st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------------------
def show_line_chart(sader1402, sader1403, matched):
    st.header("📈 نمودار خطی")
    dataset_options = {"دیتای اول": pd.concat([sader1402, sader1403]), "دیتای تفاضل‌گیری شده": matched}
    selected = st.radio("📂 دیتاست را انتخاب کنید", list(dataset_options.keys()), key="line_dataset")
    df = dataset_options[selected]

    cat_cols = df.select_dtypes(include='object').columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()

    category = st.selectbox("📌 متغیر کیفی", cat_cols)
    value = st.selectbox("📌 متغیر کمی", num_cols)
    subcategories = df[category].unique()

    selected_subcats = st.multiselect("زیرشاخه‌ها", ["All"] + list(subcategories), default=["All"])
    if st.button("ایجاد نمودار", key="line_btn"):
        grouped = df.groupby(['ماه ارسال', category])[value].sum().reset_index().sort_values('ماه ارسال')
        if "All" not in selected_subcats:
            grouped = grouped[grouped[category].isin(selected_subcats)]

        fig = px.line(
            grouped, x='ماه ارسال', y=value,
            color=category if "All" not in selected_subcats else None,
            markers=True, template='plotly_dark'
        )
        st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------------------
def show_bar_chart(sader1402, sader1403, matched):
    st.header("📊 نمودار میله‌ای")
    dataset_options = {"دیتای 1402 تا 1403": pd.concat([sader1402, sader1403]), "دیتای مقایسه دو سال": matched}
    selected = st.radio("📂 دیتاست را انتخاب کنید", list(dataset_options.keys()), key="bar_dataset")
    df = dataset_options[selected]

    cat_cols = df.select_dtypes(include='object').columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()

    category = st.selectbox("📌 متغیر کیفی اول", cat_cols)
    subcategory = st.selectbox("📌 متغیر کیفی دوم", cat_cols)
    value = st.selectbox("📌 متغیر کمی", num_cols)

    if st.button("ایجاد نمودار", key="bar_btn"):
        fig = px.bar(df, x=category, y=value, color=subcategory, barmode='group', log_y=True)
        st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------------------
def show_pie_chart(sader1402, sader1403, matched):
    st.header("🥧 نمودار پای چارت")
    dataset_options = {"دیتای 1402 تا 1403": pd.concat([sader1402, sader1403]), "دیتای مقایسه دو سال": matched}
    selected = st.radio("📂 دیتاست را انتخاب کنید", list(dataset_options.keys()), key="pie_dataset")
    df = dataset_options[selected]

    cat_cols = df.select_dtypes(include='object').columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()
    value = st.selectbox("📌 متغیر کمی", num_cols)
    category = st.selectbox("📌 متغیر کیفی", cat_cols)

    if st.button("ایجاد نمودار", key="pie_btn"):
        grouped = df.groupby(category)[value].sum()
        total = grouped.sum()
        filtered = grouped[grouped / total >= 0.02]
        if (grouped / total < 0.02).any():
            filtered["سایر"] = grouped[grouped / total < 0.02].sum()

        fig, ax = plt.subplots()
        ax.pie(filtered, labels=[(lbl) for lbl in filtered.index], autopct='%1.1f%%', startangle=140)
        ax.axis('equal')
        st.pyplot(fig)


# --------------------------------------------------------------------
def show_map(sader1402, sader1403, matched):
    st.header("🗺️ نقشه جغرافیایی")
    dataset_options = {"دیتای 1402 تا 1403": pd.concat([sader1402, sader1403]), "دیتای مقایسه دو سال": matched}
    selected = st.radio("📂 دیتاست را انتخاب کنید", list(dataset_options.keys()), key="map_dataset")
    df = dataset_options[selected]

    if 'بازار ' not in df.columns:
        st.error("❌ ستون 'بازار ' یافت نشد.")
        return

    num_cols = df.select_dtypes(include='number').columns.tolist()
    value = st.selectbox("📌 متغیر کمی", num_cols)

    df['بازار '] = df['بازار '].apply(translate_country_name)
    grouped = df.groupby('بازار ')[value].sum().reset_index()

    fig = px.choropleth(
        grouped, locations='بازار ', locationmode="country names", color=value,
        hover_name='بازار ', color_continuous_scale=px.colors.sequential.YlOrRd,
        title="نقشه جغرافیایی"
    )
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------------------
def show_divergence(sader1402, sader1403, matched):
    st.header("📉 نمودار تفاضلی صادرات")
    df = matched.copy()
    cat_cols = df.select_dtypes(include='object').columns.tolist()
    num_cols = df.select_dtypes(include='number').columns.tolist()

    category = st.selectbox("📌 متغیر کیفی", cat_cols)
    value = st.selectbox("📌 متغیر کمی", num_cols)

    if st.button("ایجاد نمودار", key="div_btn"):
        grouped = df.groupby(category)[value].sum().reset_index()
        colors = grouped[value].apply(lambda x: 'green' if x > 0 else 'red')

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(y=category, x=value, data=grouped, palette=colors)
        ax.axvline(x=0, color='black', linewidth=1)
        plt.xlabel((value))
        plt.ylabel((category))
        st.pyplot(fig)


# --------------------------------------------------------------------
def show_scatter(sader1402, sader1403, matched):
    st.header("💠 نمودار پراکندگی")
    dataset_options = {"دیتای 1402 تا 1403": pd.concat([sader1402, sader1403]), "دیتای مقایسه دو سال": matched}
    selected = st.radio("📂 دیتاست را انتخاب کنید", list(dataset_options.keys()), key="scatter_dataset")
    df = dataset_options[selected]

    num_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()

    category = st.selectbox("📌 متغیر کیفی", cat_cols)
    v1 = st.selectbox("📌 متغیر کمی اول", num_cols)
    v2 = st.selectbox("📌 متغیر کمی دوم", num_cols)
    v3 = st.selectbox("📌 متغیر کمی سوم", num_cols)
    subcats = df[category].unique()
    selected_subcats = st.multiselect("زیرشاخه‌ها", subcats)
    is_3d = st.checkbox("نمودار سه‌بعدی")

    if st.button("ایجاد نمودار", key="scatter_btn"):
        if selected_subcats:
            df = df[df[category].isin(selected_subcats)]
        grouped = df.groupby(category).agg({v1: 'sum', v2: 'sum', v3: 'sum'}).reset_index()

        if is_3d:
            fig = px.scatter_3d(grouped, x=v1, y=v2, z=v3, color=category, template='plotly_dark')
        else:
            fig = px.scatter(grouped, x=v1, y=v2, size=v3, color=category, template='plotly_dark')

        st.plotly_chart(fig, use_container_width=True)
        with st.spinner('Loading data...'):
            time.sleep(1)
        st.success('Data loaded successfully!')
