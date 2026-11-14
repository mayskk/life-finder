
import streamlit as st
import pandas as pd

# Настройки страницы
st.set_page_config(
    page_title="LIFE FINDER",
    page_icon="🪐",
    layout="wide"
)

# Параметры оценки
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

# Загрузка базы NASA
@st.cache_data
def load_data():
    planets = pd.read_csv(
        DATA_FILE,
        comment="#",
        skipinitialspace=True
    )

    return planets[
        ["pl_name", "pl_rade", "pl_eqt",
         "pl_orbsmax", "pl_bmasse"]
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

# Главная страница
st.title("🪐 LIFE FINDER")

st.markdown(
    "<h3 style='text-align:center;'>"
    "Поиск потенциально пригодных для жизни экзопланет"
    "</h3>",
    unsafe_allow_html=True
)

st.markdown("---")

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

# Поиск планеты
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

st.markdown("---")

st.markdown(
    "<p style='text-align:center;'>"
    "LIFE FINDER | Исследуем космос вместе"
    "</p>",
    unsafe_allow_html=True
)

with st.expander("О программе LIFE FINDER"):
    st.write(
        "LIFE FINDER — учебный проект для поиска экзопланет "
        "и предварительной оценки их потенциальной пригодности "
        "для жизни по радиусу, температуре и массе. "
        "Данные берутся из каталога NASA Exoplanet Archive."
    )
