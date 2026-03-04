import streamlit as st
import random
import time

# ===== CONFIGURACIÓN DEL JUEGO =====
NUM_PREGUNTAS = 10  # Al cambiar este número, se puede aumentar la cantidad de preguntas para jugar, no puede ser mayor a 20
PUNTOS_POR_PREGUNTA = 2 #Se usa para ajustar cuanto puntos vale cada pregunta
PUNTUACION_MAXIMA = NUM_PREGUNTAS * PUNTOS_POR_PREGUNTA  #Resultado que da el valor total de la puntuacion maxima y se puede comparar con la cantidad de puntos recolectadas
TIEMPO_ESPERA_CORRECTO = 2  #Configuracion de tiempo para que el audio se pueda reproducir completo de respuesta correcta
TIEMPO_ESPERA_INCORRECTO = 6  #Configuracion de tiempo para que el audio se pueda reproducir completo de respuesta incorrecta

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Trivia Ultra-Master IUT", page_icon="💰")

# --- 1. BASE DE DATOS DE PRUEBA (El "Pool" de 20 preguntas) ---
# Instrucción para el alumno: "Aquí es donde añades tus preguntas de TDA"
if 'pool_preguntas' not in st.session_state:
    st.session_state.pool_preguntas = [
        {"p": "¿Cuál es la capital de Venezuela?", "o": ["Maracaibo", "Caracas", "Valencia", "Coro"], "c": "Caracas"},         #01
        {"p": "¿Qué planeta es conocido como el Planeta Rojo?", "o": ["Venus", "Marte", "Júpiter", "Saturno"], "c": "Marte"},  #02
        {"p": "¿Cuántos bits tiene un byte?", "o": ["4", "16", "32", "8"], "c": "8"},                                          #03
        {"p": "¿Quién pintó la Mona Lisa?", "o": ["Dali", "Picasso", "Da Vinci", "Van Gogh"], "c": "Da Vinci"},                #04
        {"p": "¿Cuál es el metal más caro del mundo?", "o": ["Oro", "Platino", "Rodio", "Cobre"], "c": "Rodio"},               #05
        {"p": "¿Qué animal es la mascota de Linux?", "o": ["Gato", "Pingüino", "Perro", "Elefante"], "c": "Pingüino"},         #06
        {"p": "¿En qué año llegó el hombre a la Luna?", "o": ["1965", "1972", "1969", "1980"], "c": "1969"},                   #07
        {"p": "¿Cuál es el río más largo del mundo?", "o": ["Amazonas", "Nilo", "Orinoco", "Misisipi"], "c": "Amazonas"},      #08
        {"p": "¿Qué elemento químico tiene el símbolo 'O'?", "o": ["Oro", "Osmio", "Oxígeno", "Hierro"], "c": "Oxígeno"},      #09
        {"p": "¿Cuál es el lenguaje de programación de esta App?", "o": ["Java", "C++", "Python", "PHP"], "c": "Python"},      #10

            # ----- Nuevas Preguntas de Electrónica (10 preguntas adicionales) ------
        
        {"p": "¿Donde se usa un Power MOSFET?", "o": ["Sistemas de alimentación", "Procesadores", "Memorias RAM", "Para reproducir las canciones de Chayanne"], "c": "Sistemas de alimentación"},  #11
        {"p": "¿Un filtro de segundo orden se realiza con:?", "o": ["Profesores dificiles", "Amplificadores Operacionales", "Condensadores", "Bobinas"], "c": "Amplificadores Operacionales"},     #12
        {"p": "¿Qué componente almacena energía en un campo eléctrico?", "o": ["Bobina", "Resistencia", "Condensador", "Tobo de agua"], "c": "Condensador"},              #13
        {"p": "¿Qué componente almacena energía en un campo magnético?", "o": ["Bobina", "Condensador", "Alambre pua", "Circuito integrado"], "c": "Bobina"},             #14
        {"p": "¿Cuál es la ley que relaciona voltaje, corriente y resistencia?", "o": ["Ley de Faraday", "Ley de Ohm", "Ley del hielo ", "Ley de Watt"], "c": "Ley de Ohm"},     #15
        {"p": "¿Qué hace un diodo?", "o": ["Amplifica señales", "Es un componente racista", "Permite corriente en un solo sentido", "Genera oscilaciones"], "c": "Permite corriente en un solo sentido"}, #16
        {"p": "¿Qué unidad mide la resistencia?", "o": ["Voltios", "Amperios", "Watts", "Ohmios"], "c": "Ohmios"},                                                                                 #17
        {"p": "¿Qué unidad mide la capacitancia?", "o": ["Henrios", "Faradios", "Ohmios", "Siemens"], "c": "Faradios"},                                                                            #18
        {"p": "¿Qué componente se usa para amplificar señales?", "o": ["Resistencia", "Condensador", "Transistor", "Bobina"], "c": "Transistor"},                                                  #19
        {"p": "¿Cuál es el símbolo del transistor NPN?", "o": ["🙂", "🔌", "⚡", "quede minimo común multiplo"], "c": "quede minimo común multiplo"},                                                           #20
    ]
    # Mezclamos el pool para que no siempre salgan igual
    random.shuffle(st.session_state.pool_preguntas)

# --- 2. GESTIÓN DEL ESTADO DEL JUEGO ---
# Usamos session_state para que la App "recuerde" en qué pregunta vamos
if 'indice' not in st.session_state:
    st.session_state.indice = 0
    st.session_state.puntos = 0
    st.session_state.juego_terminado = False
    st.session_state.num_preguntas = NUM_PREGUNTAS  # Guardamos la configuración
    
# --- 3. FUNCIONES DE AUDIO ---
# Nota para el alumno: Streamlit puede reproducir audio desde una URL
def reproducir_sonido_correcto():
    """Reproduce sonido de respuesta correcta"""
    try:
        st.audio("Folder/Respuesta correcta_(PAPI CACHAME).mp3", format="audio/mp3", autoplay=True)
    except:
        pass  # Si falla, que no rompa la app

def reproducir_sonido_incorrecto():
    """Reproduce sonido de respuesta incorrecta"""
    try:
        st.audio("Folder/Incorrecto (Sonido de decepción).mp3", format="audio/mp3", autoplay=True)
    except:
        pass  # Si falla, que no rompa la app

# --- 4. INTERFAZ VISUAL ---
st.title("💰 ¿Quién quiere ser Ingeniero en TDA y Electrónica?")
st.divider()
st.progress(st.session_state.indice / st.session_state.num_preguntas)
st.caption(f"Pregunta {st.session_state.indice + 1} de {st.session_state.num_preguntas} • Puntos: {st.session_state.puntos}")

if not st.session_state.juego_terminado:
    # Obtenemos la pregunta actual del pool
    pregunta_actual = st.session_state.pool_preguntas[st.session_state.indice]
    
    st.subheader(f"Pregunta {st.session_state.indice + 1}:")
    st.write(f"### {pregunta_actual['p']}")
    
    # Creamos los botones para las opciones
    # El alumno puede cambiar el diseño de estos botones
    opciones = pregunta_actual['o']
    
    # Usamos columnas para que parezca el tablero del programa de TV
    col1, col2 = st.columns(2)
    
    with col1:
        btn_a = st.button(f"A) {opciones[0]}", use_container_width=True)
        btn_b = st.button(f"B) {opciones[1]}", use_container_width=True)
    with col2:
        btn_c = st.button(f"C) {opciones[2]}", use_container_width=True)
        btn_d = st.button(f"D) {opciones[3]}", use_container_width=True)

    # Lógica de respuesta
    seleccion = None
    if btn_a: seleccion = opciones[0]
    if btn_b: seleccion = opciones[1]
    if btn_c: seleccion = opciones[2]
    if btn_d: seleccion = opciones[3]

    if seleccion:
        if seleccion == pregunta_actual['c']:
            st.success("¡CORRECTO! 🌟")
            reproducir_sonido_correcto()   #Audio de correcto
            st.session_state.puntos += 2
            time.sleep(TIEMPO_ESPERA_CORRECTO) # Pausa para la reproduccion de audio de repuesta correcta
        else:
            st.error(f"INCORRECTO. La respuesta era: {pregunta_actual['c']} ❌")
            reproducir_sonido_incorrecto()  #Audio de incorrecto
            time.sleep(TIEMPO_ESPERA_INCORRECTO) # Pausa para la reproduccion de audio de repuesta incorrecta

        # Verificamos si aún quedan preguntas por jugar
        if st.session_state.indice < st.session_state.num_preguntas - 1:
            st.session_state.indice += 1
            st.rerun()
        else:
            st.session_state.juego_terminado = True
            st.rerun()

else:
    # PANTALLA FINAL
    st.header("🏁 ¡Fin del Juego!")
    st.metric("PUNTUACIÓN FINAL", f"{st.session_state.puntos} / {PUNTUACION_MAXIMA}")
    
    # Calculamos el porcentaje de aciertos (80% para ser experto)
    if st.session_state.puntos >= PUNTUACION_MAXIMA * 0.8:
        st.balloons()
        st.success("¡Eres un experto! Ya puedes trabajar en la cabecera de la TDA y eres conocedor de la Electrónica.")
    else:
        st.warning("Sigue estudiando, la norma ISDB-Tb y ley de Ohm te espera.")
    
    if st.button("Reintentar"):
        # Limpiamos todo para empezar de nuevo
        st.session_state.indice = 0
        st.session_state.puntos = 0
        st.session_state.juego_terminado = False
        random.shuffle(st.session_state.pool_preguntas)
        st.rerun()
