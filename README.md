# Buscaminas en Streamlit

¡Bienvenido al proyecto **Buscaminas** implementado con Streamlit! Este clásico juego de descubrimiento de minas ha sido recreado con una interfaz moderna y totalmente funcional.

---

## 🚀 Características

* **Tablero personalizable**: Ajusta filas, columnas y número de minas desde la barra lateral.
* **Modo bandera**: Marca celdas sospechosas antes de despejar.
* **Detección de victoria y derrota**: Mensajes automáticos al ganar o detonar una mina.
* **Diseño responsive**: Las celdas ocupan todo el espacio, sin separaciones ni márgenes.
* **Expansión automática**: Al descubrir una celda vacía (0 minas adyacentes), se revelan sus vecinas.
* **Reinicio rápido**: Botón para reiniciar partida en cualquier momento.

---

## 📦 Instalación

1. **Clona este repositorio**

   ```bash
   git clone https://github.com/nicolauroca/minesweeper.git
   ```
2. **Crea y activa un entorno virtual** (recomendado)

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```
3. **Instala dependencias**

   ```bash
   pip install streamlit
   ```

---

## ▶️ Uso

Ejecuta la aplicación con Streamlit:

```bash
streamlit run buscaminas_streamlit.py
```

Al abrirse en tu navegador, configura el tamaño del tablero y la cantidad de minas; luego, haz clic en las celdas para descubrirlas o marca con banderas.

---

## ⚙️ Personalización

* **Filas y columnas**: Modifica los valores por defecto en `init_state()` si quieres otro tamaño inicial.
* **Estilos**: El bloque CSS en la parte superior del script permite ajustar colores, tamaños y eliminar espacios.
* **Lógica de minas**: El método `create_board()` define cómo se distribuyen y cuentan las minas.

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar estilos, añadir funcionalidad (puntuaciones, temporizador, historiales) o reportar bugs, abre un *issue* o un *pull request*.

---

## 📄 Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).
