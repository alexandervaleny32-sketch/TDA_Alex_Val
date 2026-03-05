import streamlit as st
import random
import time

# ===== CONFIGURACIÓN DEL JUEGO =====
NUM_PREGUNTAS = 10 # Al cambiar este número, se puede aumentar la cantidad de preguntas para jugar, no puede ser mayor a 20
PUNTOS_POR_PREGUNTA = 2 # Se usa para ajustar cuanto puntos vale cada pregunta
PUNTUACION_MAXIMA = NUM_PREGUNTAS * PUNTOS_POR_PREGUNTA # Resultado que da el valor total de la puntuacion maxima y se puede comparar con la cantidad de puntos recolectadas
TIEMPO_ESPERA_CORRECTO = 2 # Configuracion de tiempo para que el audio se pueda reproducir completo de respuesta correcta
TIEMPO_ESPERA_INCORRECTO = 6  # Configuracion de tiempo para que el audio se pueda reproducir completo de respuesta incorrecta
REPRODUCIR_AUDIO_PREGUNTA = True # Activa o desactiva la pista de audio

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Trivia Ultra-Master IUT", page_icon="💰")

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
    st.session_state.num_preguntas = NUM_PREGUNTAS
    st.session_state.respuesta_confirmada = False
    st.session_state.audio_pregunta_actual = -1

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
# Parte de codigo para ocultar barra de reproductor de audios 
st.markdown("""
<style>
.stAudio, audio { display: none; }
</style>
""", unsafe_allow_html=True)
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
        return "😢 Puntuación Patética"
    
    elif porcentaje < 50:
        st.audio(URL_PUNTUACION_BAJA, format="audio/mp3", autoplay=True)
        return "😐 Puntuación Baja"
    
    elif porcentaje < 95:
        st.audio(URL_PUNTUACION_ALTA, format="audio/mp3", autoplay=True)
        return "🔥 Puntuación Alta"
    
    else:
        st.audio(URL_PUNTUACION_SUPREMA, format="audio/mp3", autoplay=True)
        return "👑 Puntuación Suprema"


# --- 4. INTERFAZ VISUAL ---
st.title("💰 ¿Quién quiere ser Ingeniero en TDA y Electrónica?")
st.divider()
st.progress(st.session_state.indice / st.session_state.num_preguntas)
st.caption(f"Pregunta {st.session_state.indice + 1} de {st.session_state.num_preguntas} • Puntos: {st.session_state.puntos}")

if not st.session_state.juego_terminado:
    # Reproducir audio de pregunta
    reproducir_audio_pregunta()
    
    pregunta_actual = st.session_state.pool_preguntas[st.session_state.indice]
    
    st.subheader(f"Pregunta {st.session_state.indice + 1}:")
    st.write(f"### {pregunta_actual['p']}")
    
    # --- BOTONES DE RESPUESTA ---
    opciones = pregunta_actual['o']    # Extrae de la pregunta la lista de opciones (A, B, C, D)
    
    col1, col2 = st.columns(2)         # Divide la pantalla en dos columnas iguales
    with col1:
        btn_a = st.button(f"A) {opciones[0]}", use_container_width=True, disabled=st.session_state.respuesta_confirmada)  # Si el usuario respondio, todo los botones se inhabilitan para que no puedan cambiar su respuestas y aumentar la cantidad de puntos 
        btn_b = st.button(f"B) {opciones[1]}", use_container_width=True, disabled=st.session_state.respuesta_confirmada)
    with col2:
        btn_c = st.button(f"C) {opciones[2]}", use_container_width=True, disabled=st.session_state.respuesta_confirmada)
        btn_d = st.button(f"D) {opciones[3]}", use_container_width=True, disabled=st.session_state.respuesta_confirmada)

    # Detectar qué botón presionó el usuario
    seleccion = None
    if not st.session_state.respuesta_confirmada: 
        if btn_a: seleccion = opciones[0]
        if btn_b: seleccion = opciones[1]
        if btn_c: seleccion = opciones[2]
        if btn_d: seleccion = opciones[3]

    # Se evalua la respuesta
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
    
    # Mensaje de espera ya cuando el usuario respondio y decide continuar a la siguiente pregunta
    if st.session_state.respuesta_confirmada:
        st.info("⏳ Respuesta registrada. Prepárate para la siguiente pregunta....")
        if st.button("Continuar ▶️"):
            if st.session_state.indice < st.session_state.num_preguntas - 1: # Verifica si quedan preguntas de la lista
                st.session_state.indice += 1  # Avanza a la siguiente pregunta
                st.session_state.respuesta_confirmada = False # "Limpia" la interfaz para la nueva pregunta
                st.rerun()
            else:
                st.session_state.juego_terminado = True # Finaliza el juego
                st.rerun()

else:
    # PANTALLA FINAL
    st.header("🏁 ¡Fin del Juego!")
    st.metric("PUNTUACIÓN FINAL", f"{st.session_state.puntos} / {PUNTUACION_MAXIMA}")
    resultado_audio = reproducir_audio_final(st.session_state.puntos, PUNTUACION_MAXIMA)
    st.subheader(resultado_audio)

    
    if st.session_state.puntos >= PUNTUACION_MAXIMA * 0.8:
        st.balloons()
        st.success("¡Eres un experto! Ya puedes trabajar en la cabecera de la TDA y eres conocedor de la Electrónica.")
    else:
        st.warning("Sigue estudiando, la norma ISDB-Tb y ley de Ohm te espera.")
    
    if st.button("🔄 Reintentar"):
        st.session_state.indice = 0
        st.session_state.puntos = 0
        st.session_state.juego_terminado = False
        st.session_state.respuesta_confirmada = False
        st.session_state.audio_pregunta_actual = -1
        random.shuffle(st.session_state.pool_preguntas)
        st.rerun()
