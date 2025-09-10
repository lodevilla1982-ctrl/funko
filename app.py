import streamlit as st
import zipfile
import io
import trimesh
import numpy as np

st.title("Generador de figuras tipo Funko para impresión FDM")

# Parámetros de entrada
tolerancia = st.selectbox("Tolerancia de encastre", ["-0.1 mm", "-0.05 mm"])
escala_cm = st.slider("Altura total del modelo (cm)", min_value=5, max_value=20, value=10)

# Botón para generar modelo
if st.button("Generar modelo y descargar ZIP"):
    stl_files = {}

    def crear_parte(nombre, posicion):
        size = 10.0
        mesh = trimesh.creation.box(extents=[size, size, size])
        mesh.apply_translation(posicion)
        factor = escala_cm / 10.0
        mesh.apply_scale(factor)
        tol_valor = -0.1 if tolerancia == "-0.1 mm" else -0.05
        mesh.apply_scale([1 + tol_valor / 10.0, 1, 1])
        stl_data = mesh.export(file_type='stl')
        stl_files[f"{nombre}.stl"] = stl_data

    crear_parte("cabeza", [0, 0, 0])
    crear_parte("pelo", [0, 0, 12])
    crear_parte("gorro", [0, 0, 18])
    crear_parte("cuerpo", [0, 0, -12])
    crear_parte("brazo_izquierdo", [-12, 0, -12])
    crear_parte("brazo_derecho", [12, 0, -12])
    crear_parte("pierna_izquierda", [-4, 0, -24])
    crear_parte("pierna_derecha", [4, 0, -24])
    crear_parte("zapato_izquierdo", [-4, 0, -30])
    crear_parte("zapato_derecho", [4, 0, -30])
    crear_parte("ojos_blancos", [0, 4, 4])
    crear_parte("pupilas", [0, 4, 5])
    crear_parte("detalles_blancos_torso", [0, 0, -10])
    crear_parte("orejas_gorro", [6, 0, 20])
    crear_parte("lunares_integrados", [0, 0, 18])
    crear_parte("lunares_encastrables", [0, 0, 19])

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for filename, data in stl_files.items():
            zip_file.writestr(filename, data)

    st.download_button(
        label="Descargar STL ZIP",
        data=zip_buffer.getvalue(),
        file_name="funko_parts.zip",
        mime="application/zip"
    )
