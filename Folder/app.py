import streamlit as st
import random
import time

# ===== CONFIGURACIÓN DEL JUEGO =====
# NUM_PREGUNTAS = 10 # Al cambiar este número, se puede aumentar la cantidad de preguntas para jugar, no puede ser mayor a 20
PUNTOS_POR_PREGUNTA = 2 # Se usa para ajustar cuanto puntos vale cada pregunta
# PUNTUACION_MAXIMA = NUM_PREGUNTAS * PUNTOS_POR_PREGUNTA # Resultado que da el valor total de la puntuacion maxima y se puede comparar con la cantidad de puntos recolectadas
TIEMPO_ESPERA_CORRECTO = 2 # Configuracion de tiempo para que el audio se pueda reproducir completo de respuesta correcta
TIEMPO_ESPERA_INCORRECTO = 6  # Configuracion de tiempo para que el audio se pueda reproducir completo de respuesta incorrecta
REPRODUCIR_AUDIO_PREGUNTA = True # Activa o desactiva la pista de audio

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Trivia Ultra-Master IUT", page_icon="💰")

# Ocultar TODOS los reproductores de audio
st.markdown("""
<style>
audio, .stAudio {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    width: 0 !important;
    opacity: 0 !important;
}
</style>
""", unsafe_allow_html=True)


# --- 1. BASE DE DATOS (20 preguntas) ---
if 'pool_preguntas' not in st.session_state:
    st.session_state.pool_preguntas = [
{"p": "¿Cuál es la capital de Venezuela?", "o": ["Maracaibo", "Caracas", "Valencia", "Coro"], "c": "Caracas"},                 #01
        {"p": "¿Qué planeta es conocido como el Planeta Rojo?", "o": ["Venus", "Marte", "Júpiter", "Saturno"], "c": "Marte"},  #02
        {"p": "¿Cuántos bits tiene un byte?", "o": ["4", "16", "32", "8"], "c": "8"},                                          #03
        {"p": "¿Quién pintó la Mona Lisa?", "o": ["Dali", "Picasso", "Da Vinci", "Van Gogh"], "c": "Da Vinci"},                #04
        {"p": "¿Cuál es el metal más caro del mundo?", "o": ["Oro", "Platino", "Rodio", "Cobre"], "c": "Rodio"},               #05
        {"p": "¿Qué animal es la mascota de Linux?", "o": ["Gato", "Pingüino", "Perro", "Elefante"], "c": "Pingüino"},         #06
        {"p": "¿En qué año llegó el hombre a la Luna?", "o": ["1965", "1972", "1969", "1980"], "c": "1969"},                   #07
        {"p": "¿Cuál es el río más largo del mundo?", "o": ["Amazonas", "Nilo", "Orinoco", "Misisipi"], "c": "Amazonas"},      #08
        {"p": "¿Qué elemento químico tiene el símbolo 'O'?", "o": ["Oro", "Osmio", "Oxígeno", "Hierro"], "c": "Oxígeno"},      #09
        {"p": "¿Cuál es el lenguaje de programación de esta App?", "o": ["Java", "C++", "Python", "PHP"], "c": "Python"},      #10
        #------Preguntas Nuevas-----
        {"p": "¿Donde se usa un Power MOSFET?", "o": ["Sistemas de alimentación", "Procesadores", "Memorias RAM", "Para reproducir las canciones de Chayanne"], "c": "Sistemas de alimentación"},  #11
        {"p": "¿Un filtro de segundo orden se realiza con:?", "o": ["Profesores dificiles", "Amplificadores Operacionales", "Condensadores", "Bobinas"], "c": "Amplificadores Operacionales"},     #12
        {"p": "¿Qué componente almacena energía en un campo eléctrico?", "o": ["Bobina", "Resistencia", "Condensador", "Tobo de agua"], "c": "Condensador"},  #13
        {"p": "¿Qué componente almacena energía en un campo magnético?", "o": ["Bobina", "Condensador", "Alambre pua", "Circuito integrado"], "c": "Bobina"}, #14
        {"p": "¿Cuál es la ley que relaciona voltaje, corriente y resistencia?", "o": ["Ley de Faraday", "Ley de Ohm", "Ley del hielo ", "Ley de Watt"], "c": "Ley de Ohm"}, #15
        {"p": "¿Qué hace un diodo?", "o": ["Amplifica señales", "Es un componente racista", "Permite corriente en un solo sentido", "Genera oscilaciones"], "c": "Permite corriente en un solo sentido"}, #16
        {"p": "¿Qué unidad mide la resistencia?", "o": ["Voltios", "Amperios", "Watts", "Ohmios"], "c": "Ohmios"},      #17
        {"p": "¿Qué unidad mide la capacitancia?", "o": ["Henrios", "Faradios", "Ohmios", "Siemens"], "c": "Faradios"}, #18
        {"p": "¿Qué componente se usa para amplificar señales?", "o": ["Resistencia", "Condensador", "Transistor", "Bobina"], "c": "Transistor"},  #19
        {"p": "¿Cuál es el símbolo del transistor NPN?", "o": ["🙂", "🔌", "⚡", "quede minimo común multiplo"], "c": "quede minimo común multiplo"}, #20
    ]
    random.shuffle(st.session_state.pool_preguntas)

# --- 2. GESTIÓN DEL ESTADO ---
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.puntos = 0
    st.session_state.juego_terminado = False
    st.session_state.num_preguntas = None
    st.session_state.respuesta_confirmada = False
    st.session_state.audio_pregunta_actual = -1
    
# --- 2.1. Control de interfaces ---
if 'pantalla_actual' not in st.session_state:
    st.session_state.pantalla_actual = "menu"   # menu | participar | ranking | juego

# --- 2.2. Datos del jugador ---
if 'nombre_jugador' not in st.session_state:
    st.session_state.nombre_jugador = ""

if 'configuracion_completa' not in st.session_state:
    st.session_state.configuracion_completa = False


# --- 3. FUNCIONES DE AUDIO ----
# --- 3.1. Audios de reproduccion mientras se juega ---
URL_AUDIO_PREGUNTA = "https://github.com/alexandervaleny32-sketch/TDA_Alex_Val/raw/main/Folder/Pregunta%20(Qui%C3%A9n%20quiere%20ser%20millonario).mp3" #Audio de pregunta
URL_CORRECTO = "https://github.com/alexandervaleny32-sketch/TDA_Alex_Val/raw/main/Folder/Respuesta%20correcta_(PAPI%20CACHAME).mp3" #Audio de correcto
URL_INCORRECTO = "https://github.com/alexandervaleny32-sketch/TDA_Alex_Val/raw/main/Folder/Incorrecto%20(Sonido%20de%20decepci%C3%B3n).mp3" #Audio de incorrecto

# --- 3.2. Audios de reproduccion final --- 
URL_PUNTUACION_PATETICA = "https://github.com/alexandervaleny32-sketch/TDA_Alex_Val/raw/main/Folder/Puntuacion%20patetica.mp3"
URL_PUNTUACION_BAJA = "https://github.com/alexandervaleny32-sketch/TDA_Alex_Val/raw/main/Folder/Puntuacion%20Baja.mp3"
URL_PUNTUACION_ALTA = "https://github.com/alexandervaleny32-sketch/TDA_Alex_Val/raw/main/Folder/Puntuacion%20alta.mp3"
URL_PUNTUACION_SUPREMA = "https://github.com/alexandervaleny32-sketch/TDA_Alex_Val/raw/main/Folder/Puntuacion%20Suprema.mp3"

# --- 3.4. Audio de fondo del menú ---
URL_AUDIO_FONDO = "https://github.com/alexandervaleny32-sketch/TDA_Alex_Val/raw/main/Folder/Tema%20de%20fondo%20(Quien%20Quiere%20Ser%20Millonario).mp3"



# Funciones para reproduccion de audios en el transcurso del juego
def reproducir_sonido_correcto():
    try:
        st.audio(URL_CORRECTO, format="audio/mp3", autoplay=True)  # hace la llamada del audio correto cuando la respuesta es correcta
    except:
        pass

def reproducir_sonido_incorrecto():
    try:
        st.audio(URL_INCORRECTO, format="audio/mp3", autoplay=True)  # hace la llamada del audio incorreto cuando la respuesta es incorrecta
    except:
        pass

def reproducir_audio_pregunta():
    if REPRODUCIR_AUDIO_PREGUNTA:
        if st.session_state.audio_pregunta_actual != st.session_state.indice:    # Compara si el audio de la pregunta actual ya se reprodujo
            try:
                st.audio(URL_AUDIO_PREGUNTA, format="audio/mp3", autoplay=True)  # hace la llamada del audio pregunta cuando sale una nueva pregunta
                st.session_state.audio_pregunta_actual = st.session_state.indice # Actualiza el estado para marcar que ya sonó en este índice   
            except:
                pass
# Funciones para reproduccion de audios al finalizar el juego
def reproducir_audio_final(puntos, maximo):
    porcentaje = (puntos / maximo) * 100

    if porcentaje <= 25:
        st.audio(URL_PUNTUACION_PATETICA, format="audio/mp3", autoplay=True)
        return "😢 Puntuación Patética: Puedes ser tiktoker mi amig@"
    
    elif porcentaje < 50:
        st.audio(URL_PUNTUACION_BAJA, format="audio/mp3", autoplay=True)
        return "😐 Puntuación Baja: Puedes esforzarte mas, si lo deseas claro esta"
    
    elif porcentaje < 95:
        st.audio(URL_PUNTUACION_ALTA, format="audio/mp3", autoplay=True)
        return "🔥 Puntuación Alta: Vas por buen camino mi amigo"
    
    else:
        st.audio(URL_PUNTUACION_SUPREMA, format="audio/mp3", autoplay=True)
        return "👑 Puntuación Suprema: Nada que decir Master"

# --- 3.3. FUNCIONES PARA RANKING ---
import json
import os
import socket

RANKING_FILE = "ranking.json"

def obtener_ip():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip
    except:
        return "0.0.0.0"

def cargar_ranking():
    if not os.path.exists(RANKING_FILE):
        return []
    try:
        with open(RANKING_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def guardar_ranking(data):
    with open(RANKING_FILE, "w") as f:
        json.dump(data, f, indent=4)

def registrar_jugador(nombre, ip, puntos, preguntas_totales, preguntas_correctas):
    ranking = cargar_ranking()

    # Buscar si ya existe un registro con ese nombre + IP
    existente = next((r for r in ranking if r["nombre"] == nombre and r["ip"] == ip), None)

    if existente:
        # Actualizar si el nuevo puntaje es mayor
        if puntos > existente["puntos"]:
            existente["puntos"] = puntos
            existente["preguntas_totales"] = preguntas_totales
            existente["preguntas_correctas"] = preguntas_correctas
    else:
        ranking.append({
            "nombre": nombre,
            "ip": ip,
            "puntos": puntos,
            "preguntas_totales": preguntas_totales,
            "preguntas_correctas": preguntas_correctas
        })

    guardar_ranking(ranking)

# --- 4. INTERFAZ VISUAL ---
st.title("💰 ¿Quién quiere ser Ingeniero en TDA y Electrónica?")
st.divider()

if st.session_state.num_preguntas:
    st.progress(st.session_state.indice / st.session_state.num_preguntas)
else:
    st.progress(0)

st.caption(f"Pregunta {st.session_state.indice + 1} de {st.session_state.num_preguntas} • Puntos: {st.session_state.puntos}")


# ============================
#       MENÚ PRINCIPAL
# ============================
if st.session_state.pantalla_actual == "menu":

    st.audio(URL_AUDIO_FONDO, format="audio/mp3", autoplay=True)

    st.header("🎉 Bienvenido a Trivia Ultra-Master IUT")
    st.write("Selecciona una opción para continuar:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🎮 Participar"):
            st.session_state.pantalla_actual = "participar"
            st.rerun()

    with col2:
        if st.button("📊 Ver Ranking"):
            st.session_state.pantalla_actual = "ranking"
            st.rerun()

    st.stop()



# ============================
#   PANTALLA DE PARTICIPACIÓN
# ============================
if st.session_state.pantalla_actual == "participar":

    st.audio(URL_AUDIO_FONDO, format="audio/mp3", autoplay=True)
    
    st.header("📝 Configuración del Jugador")

    st.session_state.nombre_jugador = st.text_input("Ingresa tu nombre:")

    num = st.number_input("Número de preguntas (1 a 20):", min_value=1, max_value=20, step=1)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⬅️ Volver al menú"):
            st.session_state.pantalla_actual = "menu"
            st.rerun()

    with col2:
        if st.button("Aceptar"):
            if st.session_state.nombre_jugador.strip() == "":
                st.error("Debes ingresar un nombre válido.")
            else:
                st.session_state.num_preguntas = num
                st.session_state.puntuacion_maxima_real = num * PUNTOS_POR_PREGUNTA
    
                # Ir a pantalla de pre-juego
                st.session_state.pantalla_actual = "pre_juego"
                st.session_state.pre_juego_inicio = time.time()
                st.rerun()


    st.stop()


# ============================
#      PANTALLA DE RANKING
# ============================
if st.session_state.pantalla_actual == "ranking":

    st.audio(URL_AUDIO_FONDO, format="audio/mp3", autoplay=True)
    
    st.header("📊 Ranking de Jugadores")

    ranking = cargar_ranking()

    if ranking:
        # Ordenar por puntaje de mayor a menor
        ranking = sorted(ranking, key=lambda x: x["puntos"], reverse=True)

        st.write("### Tabla de posiciones:")

        for r in ranking:
            st.write(
                f"**{r['nombre']}** — {r['puntos']} pts — "
                f"{r['preguntas_correctas']}/{r['preguntas_totales']} correctas"
            )
    else:
        st.info("Aún no hay jugadores registrados.")

    if st.button("⬅️ Volver al menú"):
        st.session_state.pantalla_actual = "menu"
        st.rerun()

    st.stop()

# ============================
#      PANTALLA PRE-JUEGO
# ============================
if st.session_state.pantalla_actual == "pre_juego":

    # Tiempo transcurrido desde que entró a esta pantalla
    transcurrido = int(time.time() - st.session_state.pre_juego_inicio)
    restante = 5 - transcurrido

    # Reproducir audio de fondo (oculto por CSS)
    st.audio(URL_AUDIO_FONDO, format="audio/mp3", autoplay=True)

    st.header("⏳ Preparando el juego...")
    st.subheader(f"Comenzamos en: **{restante}** segundos")

    # Si ya terminó el conteo → entrar al juego
    if restante <= 0:
        st.session_state.pantalla_actual = "juego"
        st.rerun()

    # Esperar 1 segundo y refrescar pantalla
    time.sleep(1)
    st.experimental_rerun()

    st.stop()   # ← ESTE ERA EL QUE FALTABA



# ============================
#           JUEGO
# ============================
if st.session_state.pantalla_actual == "juego" and not st.session_state.juego_terminado:



    reproducir_audio_pregunta()

    pregunta_actual = st.session_state.pool_preguntas[st.session_state.indice]

    st.subheader(f"Pregunta {st.session_state.indice + 1}:")
    st.write(f"### {pregunta_actual['p']}")

    opciones = pregunta_actual['o']

    col1, col2 = st.columns(2)
    with col1:
        btn_a = st.button(f"A) {opciones[0]}", use_container_width=True, disabled=st.session_state.respuesta_confirmada)
        btn_b = st.button(f"B) {opciones[1]}", use_container_width=True, disabled=st.session_state.respuesta_confirmada)
    with col2:
        btn_c = st.button(f"C) {opciones[2]}", use_container_width=True, disabled=st.session_state.respuesta_confirmada)
        btn_d = st.button(f"D) {opciones[3]}", use_container_width=True, disabled=st.session_state.respuesta_confirmada)

    seleccion = None
    if not st.session_state.respuesta_confirmada:
        if btn_a: seleccion = opciones[0]
        if btn_b: seleccion = opciones[1]
        if btn_c: seleccion = opciones[2]
        if btn_d: seleccion = opciones[3]

    if seleccion and not st.session_state.respuesta_confirmada:
        st.session_state.respuesta_confirmada = True

        if seleccion == pregunta_actual['c']:
            st.success("¡CORRECTO! 🌟")
            reproducir_sonido_correcto()
            st.session_state.puntos += 2
            time.sleep(TIEMPO_ESPERA_CORRECTO)
        else:
            st.error(f"INCORRECTO. La respuesta era: {pregunta_actual['c']} ❌")
            reproducir_sonido_incorrecto()
            time.sleep(TIEMPO_ESPERA_INCORRECTO)

        st.rerun()

    if st.session_state.respuesta_confirmada:
        st.info("⏳ Respuesta registrada. Prepárate para la siguiente pregunta....")
        if st.button("Continuar ▶️"):
            if st.session_state.indice < st.session_state.num_preguntas - 1:
                st.session_state.indice += 1
                st.session_state.respuesta_confirmada = False
                st.rerun()
            else:
                st.session_state.juego_terminado = True
                st.rerun()


# ============================
#        PANTALLA FINAL
# ============================
if st.session_state.pantalla_actual == "juego" and st.session_state.juego_terminado:



    st.header("🏁 ¡Fin del Juego!")
    st.write(f"👤 Jugador: **{st.session_state.nombre_jugador}**")
    st.metric("PUNTUACIÓN FINAL", f"{st.session_state.puntos} / {st.session_state.puntuacion_maxima_real}")

    resultado_audio = reproducir_audio_final(st.session_state.puntos, st.session_state.puntuacion_maxima_real)
    st.subheader(resultado_audio)

    # Registrar jugador en ranking
    ip = obtener_ip()
    registrar_jugador(
        nombre=st.session_state.nombre_jugador,
        ip=ip,
        puntos=st.session_state.puntos,
        preguntas_totales=st.session_state.num_preguntas,
        preguntas_correctas=st.session_state.puntos // 2
    )


    if st.button("🔄 Ir al menú principal"):
        st.session_state.indice = 0
        st.session_state.puntos = 0
        st.session_state.juego_terminado = False
        st.session_state.respuesta_confirmada = False
        st.session_state.audio_pregunta_actual = -1
        st.session_state.pantalla_actual = "menu"
        st.session_state.nombre_jugador = ""
        random.shuffle(st.session_state.pool_preguntas)
        st.rerun()

