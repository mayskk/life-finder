
import streamlit as st
import pandas as pd
import html
from urllib.parse import quote
import math

st.set_page_config(
    page_title="LIFE FINDER",
    page_icon="🪐",
    layout="wide"
)

DATA_FILE = "PSCompPars_2026.11.13_09.22.26.csv"

MIN_TEMPERATURE = 200
MAX_TEMPERATURE = 300
MIN_RADIUS = 0.8
MAX_RADIUS = 1.5
MIN_MASS = 0.5
MAX_MASS = 5.0

# ОФОРМЛЕНИЕ САЙТА
st.markdown("""
<style>
.stApp {
    background-image:
        linear-gradient(
            rgba(4, 8, 25, 0.55),
            rgba(4, 8, 25, 0.65)
        ),
        url("https://raw.githubusercontent.com/mayskk/life-finder/main/F246F421-584D-490A-9C23-A04F056FF6C9.PNG");

    background-size: cover;
    background-position: center center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: white;
}

/* Заголовки */
h1 {
    color: white !important;
    font-size: 46px !important;
    font-weight: 800 !important;
}

h2 {
    color: white !important;
    font-size: 34px !important;
    font-weight: 700 !important;
}

h3 {
    color: white !important;
    font-size: 27px !important;
    font-weight: 700 !important;
}

/* Основной текст */
p, label, .stMarkdown, .stCaption {
    color: white !important;
    font-size: 19px !important;
}

/* Поле поиска */
.stTextInput input {
    background-color: white;
    color: #172033;
    border-radius: 10px;
    font-size: 18px;
    padding: 12px;
}

/* ФИОЛЕТОВАЯ КНОПКА */
.stButton button {
    background: linear-gradient(135deg, #8B35D6, #6420A8);
    color: white !important;
    border-radius: 12px;
    border: 1px solid #B77AFF;
    padding: 12px 28px;
    font-size: 19px;
    font-weight: 700;
    transition: 0.2s;
}

.stButton button:hover {
    background: linear-gradient(135deg, #A64DFF, #792BD1);
    color: white !important;
    border: 1px solid #D8B5FF;
}

/* Вкладки */
.stTabs [data-baseweb="tab"] {
    font-size: 19px;
    font-weight: 700;
}

/* Карточки и уведомления */
.stMetric {
    background-color: rgba(20, 25, 55, 0.65);
    padding: 15px;
    border-radius: 12px;
}

.stAlert p {
    font-size: 18px !important;
    color: inherit !important;
}

/* Ссылки каталога */
a {
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    planets = pd.read_csv(
        DATA_FILE,
        comment="#",
        skipinitialspace=True
    )

    return planets[
        [
            "pl_name",
            "pl_rade",
            "pl_eqt",
            "pl_orbsmax",
            "pl_bmasse"
        ]
    ]


try:
    planets = load_data()
except Exception:
    st.error("Не удалось загрузить базу NASA.")
    st.write(
        "Проверь, что CSV-файл находится "
        "в одной папке с app.py."
    )
    st.stop()


st.title("🪐 LIFE FINDER")

st.markdown(
    "<h3 style='text-align:center;'>"
    "Поиск потенциально пригодных для жизни экзопланет"
    "</h3>",
    unsafe_allow_html=True
)

st.markdown("---")


tab_check, tab_catalog, tab_about = st.tabs([
    "🔍 Проверка планеты",
    "🪐 Каталог экзопланет",
    "ℹ️ О программе"
])


# ВКЛАДКА 1 — ПРОВЕРКА ПЛАНЕТЫ
with tab_check:

    st.markdown(
        "<h2 style='text-align:center;'>"
        "Есть ли жизнь за пределами Земли?"
        "</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "Исследуй далёкие миры вместе с LIFE FINDER"
        "</p>",
        unsafe_allow_html=True
    )

    st.write("")

    planet_name = st.text_input(
        "Введите название экзопланеты:",
        placeholder="Например, TRAPPIST-1 e"
    )

    if st.button("🔍 Найти экзопланету"):

        if not planet_name.strip():
            st.warning("Сначала введите название планеты.")

        else:
            result = planets[
                planets["pl_name"].str.strip().str.lower()
                == planet_name.strip().lower()
            ]

            if result.empty:
                st.error(
                    "Эта экзопланета не найдена в базе NASA."
                )

            else:
                planet = result.iloc[0]

                radius = planet["pl_rade"]
                temperature = planet["pl_eqt"]
                distance = planet["pl_orbsmax"]
                mass = planet["pl_bmasse"]

                st.markdown("---")
                st.subheader(f"🪐 {planet['pl_name']}")
                st.markdown("### Характеристики планеты")

                col1, col2 = st.columns(2)

                with col1:
                    st.metric(
                        "Радиус",
                        f"{radius} радиуса Земли"
                        if pd.notna(radius) else "Нет данных"
                    )

                    st.metric(
                        "Температура",
                        f"{temperature} K"
                        if pd.notna(temperature) else "Нет данных"
                    )

                with col2:
                    st.metric(
                        "Масса",
                        f"{mass} массы Земли"
                        if pd.notna(mass) else "Нет данных"
                    )

                    st.metric(
                        "Расстояние до звезды",
                        f"{distance} а.е."
                        if pd.notna(distance) else "Нет данных"
                    )

                st.markdown("---")
                st.subheader("Результат анализа")

                if (
                    pd.isna(radius)
                    or pd.isna(temperature)
                    or pd.isna(mass)
                ):
                    st.warning(
                        "Недостаточно данных для оценки."
                    )

                else:
                    suitable = (
                        MIN_TEMPERATURE <= temperature <= MAX_TEMPERATURE
                        and MIN_RADIUS <= radius <= MAX_RADIUS
                        and MIN_MASS <= mass <= MAX_MASS
                    )

                    if suitable:
                        st.success(
                            "🟢 ПРИГОДНА ДЛЯ ЖИЗНИ"
                        )
                    else:
                        st.error(
                            "🔴 НЕПРИГОДНА ДЛЯ ЖИЗНИ"
                        )

                st.caption(
                    "Это предварительная оценка по выбранным "
                    "критериям, а не доказательство наличия жизни. "
                    "Равновесная температура не равна измеренной "
                    "температуре поверхности."
                )


# ВКЛАДКА 2 — КАТАЛОГ
with tab_catalog:

    st.subheader("🪐 Каталог экзопланет")

    st.write(
        "Выбери название планеты, чтобы открыть информацию "
        "о ней в NASA Exoplanet Archive."
    )

    planet_names = sorted(
        {
            str(name).strip()
            for name in planets["pl_name"].dropna()
            if str(name).strip()
        },
        key=str.casefold
    )

    search_name = st.text_input(
        "Найти планету в каталоге:",
        placeholder="Начни вводить название..."
    )

    if search_name.strip():
        filtered_names = [
            name for name in planet_names
            if search_name.strip().casefold() in name.casefold()
        ]
    else:
        filtered_names = planet_names

    st.write(f"Найдено планет: {len(filtered_names)}")

    PAGE_SIZE = 50

    total_pages = max(
        1,
        math.ceil(len(filtered_names) / PAGE_SIZE)
    )

    if total_pages > 1:
        page = st.selectbox(
            "Страница каталога:",
            options=list(range(1, total_pages + 1)),
            format_func=lambda number: f"{number} из {total_pages}"
        )
    else:
        page = 1

    start_index = (page - 1) * PAGE_SIZE
    end_index = start_index + PAGE_SIZE

    visible_names = filtered_names[start_index:end_index]

    for name in visible_names:

        encoded_name = quote(name, safe="")

        nasa_url = (
            "https://exoplanetarchive.ipac.caltech.edu/overview/"
            + encoded_name
        )

        safe_name = html.escape(name)

        st.markdown(
            f'<p style="margin: 8px 0;">'
            f'<a href="{nasa_url}" target="_blank" '
            f'style="color:#C99AFF; font-size:19px; '
            f'text-decoration:underline;">'
            f'{safe_name} ↗'
            f'</a></p>',
            unsafe_allow_html=True
        )

    if not filtered_names:
        st.info(
            "Планета с таким названием не найдена."
        )


# ВКЛАДКА 3 — О ПРОГРАММЕ
with tab_about:

    st.subheader("ℹ️ О программе LIFE FINDER")

    st.write(
        "LIFE FINDER — учебный проект для поиска экзопланет "
        "и предварительной оценки их потенциальной пригодности "
        "для жизни по радиусу, температуре и массе."
    )

    st.write(
        "Данные для поиска берутся из NASA Exoplanet Archive."
    )

    st.write(
        "Каталог содержит названия планет из той же базы данных, "
        "которая используется для проверки экзопланет."
    )

    st.write(
        "Нажав на название планеты в каталоге, "
        "можно перейти на её страницу в NASA Exoplanet Archive."
    )

    st.markdown("---")

    st.caption(
        "Важно: предварительная оценка LIFE FINDER "
        "не доказывает существование жизни на планете."
    )


# НИЖНЯЯ ЧАСТЬ САЙТА
st.markdown("---")

st.markdown(
    "<p style='text-align:center;'>"
    "LIFE FINDER | Исследуем космос вместе"
    "</p>",
    unsafe_allow_html=True
)
