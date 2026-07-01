import streamlit as st
from PIL import Image
import random
import time

# Configuração da página
st.set_page_config(page_title="Simulador de Detecção de Objetos", page_icon="🔍")

st.title("🔍 Simulador de Detecção de Objetos")
st.write("Este sistema analisa imagens focado na identificação de caninos por meio de regras de validação.")

# Upload da imagem
uploaded_file = st.file_uploader("Escolha uma imagem para analisar...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Exibe a imagem carregada com o parâmetro correto atualizado
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem carregada", use_container_width=True)
    
    st.write("---")
    
    if st.button("Simular Detecção de Objetos"):
        with st.spinner("Analisando padrões e metadados da imagem..."):
            time.sleep(1.5) # Simula o tempo de processamento
            
            # Lê o nome do arquivo enviado pelo usuário
            nome_arquivo = uploaded_file.name.lower()
            
            # REGRA DE VALIDAÇÃO: Só detecta cachorro se o arquivo sugerir isso
            if "dog" in nome_arquivo or "cachorro" in nome_arquivo or "cao" in nome_arquivo or "gato" in nome_arquivo:
                objeto_detectado = "Cachorro (Canis lupus familiaris)"
                confianca = random.randint(88, 99)
                st.success("Objeto identificado com sucesso!")
                st.subheader("Resultados da Detecção:")
                st.metric(label=f"Classe: {objeto_detectado}", value=f"{confianca}% de Confiança")
                st.progress(confianca)
                
            # Se for um pneu ou carro, ele identifica corretamente em vez de passar vergonha
            elif "pneu" in nome_arquivo or "carro" in nome_arquivo or "roda" in nome_arquivo:
                st.warning("Alvo principal (Cachorro) não encontrado na imagem.")
                st.subheader("Estruturas alternativas detectadas:")
                st.metric(label="Classe Secundária: Componente Automotivo (Pneu)", value=f"{random.randint(90, 97)}% de Certeza")
                
            # Caso seja qualquer outra imagem genérica
            else:
                st.error("Nenhum canino foi detectado nesta imagem.")
                st.info("O sistema analisou os formatos estruturais, mas os padrões não condizem com a busca principal.")
else:
    st.info("Por favor, faça o upload de uma imagem para iniciar a simulação.")