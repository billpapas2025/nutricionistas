import streamlit as st
import pandas as pd
import os

# Archivos Excel
CLIENTES_FILE = "clientes.xlsx"
DIETAS_FILE = "dietas.xlsx"
PROGRESO_FILE = "progreso.xlsx"

# Función para cargar o crear DataFrames
def load_data(file, columns):
    if os.path.exists(file):
        return pd.read_excel(file)
    else:
        return pd.DataFrame(columns=columns)

# Cargar datos
clientes_df = load_data(CLIENTES_FILE, ["Nombre", "Edad", "Fecha de nacimiento", "Correo", "Dirección", "Ciudad"])
dietas_df = load_data(DIETAS_FILE, ["Cliente", "Desayuno", "Ejercicio", "Sueño", "Recomendaciones"])
progreso_df = load_data(PROGRESO_FILE, ["Cliente", "Peso", "Altura", "Grasa", "Músculo", "Agua", "Fecha"])

# Guardar datos
def save_data(df, file):
    df.to_excel(file, index=False)

# Menú principal
st.sidebar.title("Menú")
option = st.sidebar.radio("Selecciona una opción:", ["Inicio", "Clientes", "Dietas", "Progreso"])

if option == "Inicio":
    st.image("logo.png", width=200)  # Incluir un logotipo en la página principal
    st.title("Bienvenido al Software de Nutrición")
    st.write("Usa el menú de la izquierda para navegar.")

elif option == "Clientes":
    st.title("Gestión de Clientes")
    with st.form("Agregar Cliente"):
        nombre = st.text_input("Nombre")
        edad = st.number_input("Edad", min_value=1, max_value=120)
        fecha_nac = st.date_input("Fecha de nacimiento")
        correo = st.text_input("Correo")
        direccion = st.text_input("Dirección")
        ciudad = st.text_input("Ciudad")
        submitted = st.form_submit_button("Guardar Cliente")
        
        if submitted:
            nuevo_cliente = pd.DataFrame([{ "Nombre": nombre, "Edad": edad, "Fecha de nacimiento": fecha_nac,
                "Correo": correo, "Dirección": direccion, "Ciudad": ciudad }])
            clientes_df = pd.concat([clientes_df, nuevo_cliente], ignore_index=True)
            save_data(clientes_df, CLIENTES_FILE)
            st.success("Cliente guardado correctamente")

elif option == "Dietas":
    st.title("Gestión de Dietas")
    cliente = st.selectbox("Selecciona un cliente", clientes_df["Nombre"] if not clientes_df.empty else [])
    desayuno = st.radio("¿Desayunas cada día?", ["Sí", "No"])
    ejercicio = st.radio("¿Haces ejercicio?", ["Sí", "No"])
    sueno = st.radio("¿Duermes más de 6 horas cada noche?", ["Sí", "No"])
    
    if st.button("Guardar Dieta"):
        recomendaciones = "Revisar hábitos alimenticios." if desayuno == "No" else "Seguir con buenos hábitos."
        nueva_dieta = pd.DataFrame([{ "Cliente": cliente, "Desayuno": desayuno,
            "Ejercicio": ejercicio, "Sueño": sueno, "Recomendaciones": recomendaciones }])
        dietas_df = pd.concat([dietas_df, nueva_dieta], ignore_index=True)
        save_data(dietas_df, DIETAS_FILE)
        st.success("Dieta guardada correctamente")
    
    # Mostrar recomendaciones del cliente seleccionado
    if cliente in dietas_df["Cliente"].values:
        recomendacion_cliente = dietas_df[dietas_df["Cliente"] == cliente]["Recomendaciones"].iloc[-1]
        st.subheader("Recomendaciones para este cliente:")
        st.write(recomendacion_cliente)

elif option == "Progreso":
    st.title("Registro de Progreso")
    cliente = st.selectbox("Selecciona un cliente", clientes_df["Nombre"] if not clientes_df.empty else [])
    peso = st.number_input("Peso (kg)", min_value=1.0)
    altura = st.number_input("Altura (cm)", min_value=50.0)
    grasa = st.number_input("Grasa corporal (%)", min_value=0.0, max_value=100.0)
    musculo = st.number_input("Masa muscular (%)", min_value=0.0, max_value=100.0)
    agua = st.number_input("Porcentaje de agua (%)", min_value=0.0, max_value=100.0)
    fecha = st.date_input("Fecha de registro")
    
    if st.button("Guardar Progreso"):
        nuevo_progreso = pd.DataFrame([{ "Cliente": cliente, "Peso": peso, "Altura": altura,
            "Grasa": grasa, "Músculo": musculo, "Agua": agua, "Fecha": fecha }])
        progreso_df = pd.concat([progreso_df, nuevo_progreso], ignore_index=True)
        save_data(progreso_df, PROGRESO_FILE)
        st.success("Progreso guardado correctamente")
