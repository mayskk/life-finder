
import streamlit as st
import pandas as pd
import html
from urllib.parse import quote
import math

# Настройки страницы
st.set_page_config(
    page_title="LIFE FINDER",
    page_icon="🪐",
    layout="wide"
)

# Параметры оценки — оставляем прежними
DATA_FILE = "PSCompPars_2026.11.13_09.22.26.csv"

MIN_TEMPERATURE = 200
MAX_TEMPERATURE = 300
MIN_RADIUS = 0.8
MAX_RADIUS = 1.5
MIN_MASS = 0.5
MAX_MASS = 5.0

# Космический дизайн
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #07182D, #102C4C, #07182D);
    color: white;
}

h1, h2, h3, p, label {
    color: white !important;
}

.stAlert p {
    color: #10243A !important;
}

.stTextInput input {
    background-color: white;
    color: #10243A;
    border-radius: 10px;
}

.stButton button {
    background-color: #1688D4;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 25px;
}

.stButton button:hover {
    background-color: #0869AD;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# Загрузка прежней базы NASA
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


# Заголовок сайта
st.title("🪐 LIFE FINDER")

st.markdown(
    "<h3 style='text-align:center;'>"
    "Поиск потенциально пригодных для жизни экзопланет"
    "</h3>",
    unsafe_allow_html=True
)

st.markdown("---")


# Три вкладки сайта
tab_check, tab_catalog, tab_about = st.tabs([
    "🔍 Проверка планеты",
    "🪐 Каталог экзопланет",
    "ℹ️ О программе"
])


# ВКЛАДКА 1. ПРОВЕРКА ПЛАНЕТЫ
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

                # Оценка пригодности
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
                        st.success("🟢 ПРИГОДНА ДЛЯ ЖИЗНИ")
                    else:
                        st.error("🔴 НЕПРИГОДНА ДЛЯ ЖИЗНИ")

                st.caption(
                    "Это предварительная оценка по выбранным "
                    "критериям, а не доказательство наличия жизни. "
                    "Равновесная температура не равна измеренной "
                    "температуре поверхности."
                )


# ВКЛАДКА 2. КАТАЛОГ ЭКЗОПЛАНЕТ
with tab_catalog:

    st.subheader("🪐 Каталог экзопланет")

    st.write(
        "Выбери название планеты, чтобы открыть информацию "
        "о ней в NASA Exoplanet Archive."
    )

    # Берём названия только из нашего прежнего CSV
    planet_names = sorted(
        {
            str(name).strip()
            for name in planets["pl_name"].dropna()
            if str(name).strip()
        },
        key=str.casefold
    )

    # Поиск по каталогу
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

    # Разбиваем большой каталог на страницы
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

    # Каждое название — отдельная ссылка на NASA
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
            f'style="color:#62C5FF; font-size:17px; '
            f'text-decoration:underline;">'
            f'{safe_name} ↗'
            f'</a></p>',
            unsafe_allow_html=True
        )

    if not filtered_names:
        st.info("Планета с таким названием не найдена.")


# ВКЛАДКА 3. О ПРОГРАММЕ
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


# Нижняя часть сайта
st.markdown("---")

st.markdown(
    "<p style='text-align:center;'>"
    "LIFE FINDER | Исследуем космос вместе"
    "</p>",
    unsafe_allow_html=True
)
