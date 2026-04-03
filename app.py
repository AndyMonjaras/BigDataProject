import streamlit as st
import requests
import pandas as pd
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Cyber-Sentinel SOC", page_icon="🛡️", layout="wide")
API_KEY = "d8ee8dd40924941ddbc76899606041ca9b23aed7ac6c1f04ea01a64fb7aa58dfef22fb4d9b7b01c1"

st.title("🛡️ Cyber-Sentinel: Centro de Operaciones Automatizado")
st.markdown("Este panel lee los ataques detectados por PySpark/Random Forest y cruza las IPs de origen con la Inteligencia de Amenazas Global.")
st.write("---")

# --- 1. SIMULACIÓN DE LECTURA DE RESULTADOS DE LA IA ---
# En la vida real esto leería pd.read_csv('resultados_ia.csv')
# Aquí creamos un Top 5 de atacantes detectados por tu modelo para la automatización
st.subheader("📊 Top 5 Atacantes Detectados por la IA hoy")
datos_ia = pd.DataFrame({
    "Source IP (Atacante)": ["118.25.6.39", "176.111.173.242", "5.188.10.179", "185.222.209.14", "8.8.8.8"],
    "Ataque Detectado": ["DDoS Hulk", "SSH Brute Force", "PortScan", "Web Attack", "Posible Falso Positivo"],
    "Paquetes Maliciosos": [25461, 15177, 8500, 4200, 150],
    "Servidor Afectado": ["Servidor Web Principal (80)", "Servidor Backup (22)", "Servidor API (443)", "Servidor ERP (443)", "Servidor DNS (53)"]
})

st.dataframe(datos_ia, use_container_width=True)

# --- 2. AUTOMATIZACIÓN DE LA API ---
st.write("---")
st.subheader("🌐 Validación Global Automatizada (AbuseIPDB)")
st.write("Verificando si estas IPs ya tienen antecedentes penales cibernéticos...")

if st.button("🚀 Iniciar Escaneo Automatizado del Top 5"):
    
    # Creamos un espacio vacío para mostrar el progreso
    progreso = st.progress(0)
    resultados_api = []
    
    # Bucle de automatización: Leemos cada IP de nuestra tabla y consultamos la API
    for i, ip in enumerate(datos_ia["Source IP (Atacante)"]):
        with st.spinner(f"Investigando IP: {ip}..."):
            
            url = 'https://api.abuseipdb.com/api/v2/check'
            params = {'ipAddress': ip, 'maxAgeInDays': '90'}
            headers = {'Accept': 'application/json', 'Key': API_KEY}
            
            try:
                res = requests.get(url, headers=headers, params=params)
                if res.status_code == 200:
                    data = res.json().get('data', {})
                    
                    # Guardamos el resultado en nuestra lista
                    resultados_api.append({
                        "IP Atacante": ip,
                        "País": data.get('countryName', 'Desconocido'),
                        "Puntaje de Abuso": f"{data.get('abuseConfidenceScore', 0)}%",
                        "ISP": data.get('isp', 'Desconocido')
                    })
                else:
                    resultados_api.append({"IP Atacante": ip, "País": "Error API", "Puntaje de Abuso": "N/A", "ISP": "N/A"})
                    
            except Exception as e:
                resultados_api.append({"IP Atacante": ip, "País": "Fallo conexión", "Puntaje de Abuso": "N/A", "ISP": "N/A"})
            
            # Pausa de 1 segundo para no saturar la API
            time.sleep(1)
            # Actualizamos la barra de progreso
            progreso.progress((i + 1) / len(datos_ia))
            
    # Mostrar resultados finales combinados
    st.success("Escaneo automático completado.")
    df_resultados = pd.DataFrame(resultados_api)
    
    # Damos formato visual a la tabla de resultados
    st.dataframe(
        df_resultados.style.applymap(
            lambda x: 'background-color: #ff4b4b; color: white' if x == '100%' else '', 
            subset=['Puntaje de Abuso']
        ),
        use_container_width=True
    )

st.write("---")
st.caption("Proyecto Final - Big Data - TecNM Celaya 2026")