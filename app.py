import streamlit as st
import random
from collections import deque

# Configuración de la página
st.set_page_config(page_title="Buscaminas", layout="wide")

# Estilos personalizados
st.markdown("""
<style>
/* Eliminar espacio entre columnas */
div[data-testid="column"] {
    padding: 0 !important;
    margin: 0 !important;
}
/* Estilos de botones */
div.stButton > button {
    width:100%;
    padding: 0.4rem;
    min-width: 2.5rem;
    min-height: 2.5rem;
    font-size: 1.2rem;
    margin: 0 !important;
}
/* Celdas ocultas */
.hidden > button {
    background-color: #9e9e9e;
}
/* Celdas reveladas */
.revealed {
    background-color: #e0e0e0;
}
/* Banderas */
.flagged {
    color: red;
}
</style>
""", unsafe_allow_html=True)

# -- Estado de la sesión y generación de tablero --
def init_state():
    if 'board' not in st.session_state:
        st.session_state.rows = 10
        st.session_state.cols = 10
        st.session_state.mines = 15
        st.session_state.flag_mode = False
        generate_board()

@st.cache_data(show_spinner=False)
def create_board(rows, cols, mines):
    # Crear tablero con minas y conteo de adyacentes
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    for pos in random.sample(range(rows * cols), mines):
        r, c = divmod(pos, cols)
        board[r][c] = 'M'
    for r in range(rows):
        for c in range(cols):
            if board[r][c] != 'M':
                count = sum(
                    1
                    for i in (-1, 0, 1)
                    for j in (-1, 0, 1)
                    if 0 <= r + i < rows and 0 <= c + j < cols and board[r + i][c + j] == 'M'
                )
                board[r][c] = count
    return board


def generate_board():
    st.session_state.board = create_board(
        st.session_state.rows, st.session_state.cols, st.session_state.mines
    )
    st.session_state.revealed = [[False] * st.session_state.cols for _ in range(st.session_state.rows)]
    st.session_state.flagged = [[False] * st.session_state.cols for _ in range(st.session_state.rows)]
    st.session_state.game_over = False
    st.session_state.win = False
    # Invalidar caché de create_board si cambian parámetros
    create_board.clear()

# Revelar celdas recursivamente

def reveal_cell(r, c):
    if st.session_state.revealed[r][c] or st.session_state.flagged[r][c] or st.session_state.game_over:
        return
    st.session_state.revealed[r][c] = True
    if st.session_state.board[r][c] == 'M':
        st.session_state.game_over = True
        # Revelar todas las minas
        for i in range(st.session_state.rows):
            for j in range(st.session_state.cols):
                if st.session_state.board[i][j] == 'M':
                    st.session_state.revealed[i][j] = True
        return
    # Expansión para celdas vacías
    if st.session_state.board[r][c] == 0:
        queue = deque([(r, c)])
        while queue:
            x, y = queue.popleft()
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    nx, ny = x + i, y + j
                    if (0 <= nx < st.session_state.rows and 0 <= ny < st.session_state.cols
                            and not st.session_state.revealed[nx][ny]
                            and not st.session_state.flagged[nx][ny]):
                        st.session_state.revealed[nx][ny] = True
                        if st.session_state.board[nx][ny] == 0:
                            queue.append((nx, ny))

# Acción de clic en celda (revelar o marcar bandera)

def click_action(r, c):
    if st.session_state.flag_mode:
        st.session_state.flagged[r][c] = not st.session_state.flagged[r][c]
    else:
        reveal_cell(r, c)

# Comprobar victoria
def check_win():
    return all(
        st.session_state.revealed[r][c] or st.session_state.board[r][c] == 'M'
        for r in range(st.session_state.rows)
        for c in range(st.session_state.cols)
    )

# -- Interfaz de usuario --
init_state()

with st.sidebar:
    st.title("Buscaminas")
    rows = st.slider("Filas", 5, 20, st.session_state.rows)
    cols = st.slider("Columnas", 5, 20, st.session_state.cols)
    mines = st.slider("Minas", 5, min(rows * cols - 1, 50), st.session_state.mines)
    flag_mode = st.checkbox("Modo bandera", value=st.session_state.flag_mode)
    if (rows, cols, mines) != (st.session_state.rows, st.session_state.cols, st.session_state.mines):
        st.session_state.rows, st.session_state.cols, st.session_state.mines = rows, cols, mines
        generate_board()
    st.session_state.flag_mode = flag_mode
    if st.button("Reiniciar"):
        generate_board()

# Mensajes de estado
if st.session_state.game_over:
    st.error("¡Has perdido! 💥")
elif check_win():
    st.success("¡Felicidades, has ganado! 🎉")
    st.session_state.win = True

# Dibujar tablero
container = st.container()
for r in range(st.session_state.rows):
    cols_ui = container.columns(st.session_state.cols)
    for c in range(st.session_state.cols):
        key = f"cell-{r}-{c}"
        if st.session_state.revealed[r][c]:
            value = st.session_state.board[r][c]
            if value == 'M':
                cols_ui[c].markdown("💣")
            elif value == 0:
                cols_ui[c].markdown(" ")
            else:
                cols_ui[c].markdown(f"**{value}**")
        else:
            label = "🚩" if st.session_state.flagged[r][c] else ""
            cols_ui[c].button(
                label,
                key=key,
                on_click=click_action,
                args=(r, c),
            )

# Comprobar victoria tras último clic
if not st.session_state.game_over and not st.session_state.win and check_win():
    st.success("¡Felicidades, has ganado! 🎉")
    st.session_state.win = True
