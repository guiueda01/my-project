import cv2
import numpy as np
import streamlit as st

def simular_detector_cachorro(imagem_bytes):
    # 1. Converter os bytes do upload do Streamlit para o formato OpenCV
    file_bytes = np.asarray(bytearray(imagem_bytes.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if img is None:
        return None, False
    
    img_saida = img.copy()
    h, w, _ = img.shape
    detectado = False
    
    # 2. Pré-processamento clássico (Cinza + Blur)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    
    # 3. Detecção de Bordas (Canny)
    edges = cv2.Canny(blurred, 30, 150)
    
    # 4. Operação Morfológica para unificar a silhueta
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    dilated = cv2.dilate(edges, kernel, iterations=2)
    closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    
    # 5. Encontrar Contornos
    contornos, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 6. Aplicação das Regras Heurísticas
    for cnt in contornos:
        area = cv2.contourArea(cnt)
        x, y, box_w, box_h = cv2.boundingRect(cnt)
        aspect_ratio = float(box_w) / box_h
        
        # Regra 1: Tamanho proporcional na tela
        area_proporcional = area / (h * w)
        if 0.10 < area_proporcional < 0.85:
            
            # Regra 2: Proporção de aspecto (evita linhas puras ou faixas)
            if 0.4 < aspect_ratio < 2.5:
                
                # Regra 3: Densidade de textura interna (pelos)
                roi_edges = edges[y:y+box_h, x:x+box_w]
                densidade_bordas = np.sum(roi_edges == 255) / (box_w * box_h)
                
                if densidade_bordas > 0.05:
                    detectado = True
                    # Bounding box verde para a detecção suspeita
                    cv2.rectangle(img_saida, (x, y), (x + box_w, y + box_h), (0, 255, 0), 4)
                    cv2.putText(img_saida, "Alvo Detectado", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Converter de BGR (OpenCV) para RGB (Streamlit) antes de retornar
    img_saida_rgb = cv2.cvtColor(img_saida, cv2.COLOR_BGR2RGB)
    return img_saida_rgb, detectado

# ────────────────────────────────────────────────────────
# INTERFACE STREAMLIT
# ────────────────────────────────────────────────────────
st.set_page_config(page_title="PoC: Detector Baseado em Regras", layout="centered")

st.title("🦮 Simulador de Visão Computacional")
st.subheader("Detecção de alvos sem Deep Learning (Baseado em Heurísticas)")
st.write("Suba uma imagem para testar o comportamento do pipeline de contornos e densidade.")

# Componente de Upload de arquivo
arquivo_imagem = st.file_uploader("Escolha uma imagem (JPG, JPEG, PNG)", type=["jpg", "jpeg", "png"])

if arquivo_imagem is not None:
    # Executa o processamento
    with st.spinner("Processando imagem através do pipeline de regras..."):
        imagem_processada, resultado_bool = simular_detector_cachorro(arquivo_imagem)
    
    if imagem_processada is not None:
        # Exibe os cards de status com base na resposta do algoritmo
        st.write("---")
        if resultado_bool:
            st.success("### ✅ Resultado: CACHORRO DETECTADO (Critérios Satisfeitos)")
        else:
            st.error("### ❌ Resultado: NÃO DETECTADO (Fora dos padrões das regras)")
        
        # Exibe a imagem final com as marcações na tela
        st.image(imagem_processada, caption="Resultado do Processamento", use_column_width=True)
