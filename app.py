import streamlit as st
import random

# Configuración de la página
st.set_page_config(page_title="Buscaminas", layout="wide")
st.markdown("""
<style>
/* Estilos personalizados para botones */
div.stButton > button {
    padding: 0.4rem;
    min-width: 2.5rem;
    min-height: 2.5rem;
    font-size: 1.2rem;
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

# Inicialización del estado de la sesión
def init_state():
    if 'board' not in st.session_state:
        st.session_state.rows = 10
        st.session_state.cols = 10
        st.session_state.mines = 15
        st.session_state.board = []
        st.session_state.revealed = []
        st.session_state.flagged = []
        st.session_state.game_over = False
        st.session_state.win = False
        generate_board()

# Generación del tablero con minas y conteos
def generate_board():
    rows, cols, mines = st.session_state.rows, st.session_state.cols, st.session_state.mines
    # Crear lista de celdas vacías
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    # Posiciones de minas aleatorias
    mine_positions = random.sample(range(rows * cols), mines)
    for pos in mine_positions:
        r, c = divmod(pos, cols)
        board[r][c] = 'M'
    # Contar minas alrededor
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == 'M': continue
            count = 0
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    nr, nc = r + i, c + j
                    if 0 <= nr < rows and 0 <= nc < cols and board[nr][nc] == 'M':
                        count += 1
            board[r][c] = count
    st.session_state.board = board
    st.session_state.revealed = [[False] * cols for _ in range(rows)]
    st.session_state.flagged = [[False] * cols for _ in range(rows)]
    st.session_state.game_over = False
    st.session_state.win = False

# Revelar celdas recursivamente
from collections import deque
def reveal_cell(r, c):
    if st.session_state.game_over or st.session_state.revealed[r][c] or st.session_state.flagged[r][c]:
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
    # Si es 0, expansión BFS
    if st.session_state.board[r][c] == 0:
        queue = deque([(r, c)])
        while queue:
            x, y = queue.popleft()
            for i in (-1, 0, 1):
                for j in (-1, 0, 1):
                    nx, ny = x + i, y + j
                    if 0 <= nx < st.session_state.rows and 0 <= ny < st.session_state.cols:
                        if not st.session_state.revealed[nx][ny] and not st.session_state.flagged[nx][ny]:
                            st.session_state.revealed[nx][ny] = True
                            if st.session_state.board[nx][ny] == 0:
                                queue.append((nx, ny))

# Comprobar si se ha ganado
def check_win():
    for r in range(st.session_state.rows):
        for c in range(st.session_state.cols):
            if st.session_state.board[r][c] != 'M' and not st.session_state.revealed[r][c]:
                return False
    return True

# Interfaz de usuario
init_state()
with st.sidebar:
    st.title("Buscaminas")
    st.sidebar.markdown("Selecciona parámetros:")
    rows = st.slider("Filas", 5, 20, st.session_state.rows)
    cols = st.slider("Columnas", 5, 20, st.session_state.cols)
    mines = st.slider("Minas", 5, min(rows * cols - 1, 50), st.session_state.mines)
    flag_mode = st.checkbox("Modo bandera", value=st.session_state.get('flag_mode', False))
    st.session_state.flag_mode = flag_mode
    if (rows, cols, mines) != (st.session_state.rows, st.session_state.cols, st.session_state.mines):
        st.session_state.rows, st.session_state.cols, st.session_state.mines = rows, cols, mines
        generate_board()
    if st.button("Reiniciar"):
        generate_board()

# Mostrar el tablero
if st.session_state.game_over:
    st.error("¡Has perdido! 💥")
elif check_win():
    st.success("¡Felicidades, has ganado! 🎉")
    st.session_state.win = True
# Layout principal
container = st.container()
for r in range(st.session_state.rows):
    cols_ui = container.columns(st.session_state.cols)
    for c in range(st.session_state.cols):
        cell_idx = f"cell-{r}-{c}"
        if st.session_state.revealed[r][c]:
            # Celda revelada
            value = st.session_state.board[r][c]
            if value == 'M':
                cols_ui[c].markdown("💣", unsafe_allow_html=True)
            elif value == 0:
                cols_ui[c].markdown("", unsafe_allow_html=True)
            else:
                cols_ui[c].markdown(f"**{value}**", unsafe_allow_html=True)
        else:
            # Celda oculta
            label = "🚩" if st.session_state.flagged[r][c] else ""
            if cols_ui[c].button(label, key=cell_idx):
                if st.session_state.flag_mode:
                    st.session_state.flagged[r][c] = not st.session_state.flagged[r][c]
                else:
                    reveal_cell(r, c)

# Revisar victoria tras movimientos
if not st.session_state.game_over and not st.session_state.win:
    if check_win():
        st.success("¡Felicidades, has ganado! 🎉")
        st.session_state.win = True
