import os
import random
from datetime import datetime
from PIL import Image, PngImagePlugin

def embaralhar_e_destacar(uids_list):
    output_dir = '0-outputs'
    images_dir_rws = 'img-rws'
    images_dir_tdm = 'img-tdm'
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(images_dir_rws, exist_ok=True)
    os.makedirs(images_dir_tdm, exist_ok=True)
    
    # Determinar quantas cartas serão invertidas (% do total)
    num_invertidas = int(0.01* len(uids_list))
    
    # Selecionar aleatoriamente os índices das cartas a serem invertidas
    indices_invertidos = random.sample(range(len(uids_list)), num_invertidas)
    
    # Adicionar o prefixo "inv" às cartas selecionadas
    for i in indices_invertidos:
        if not uids_list[i].startswith("inv"):
            uids_list[i] = "inv" + uids_list[i]
    
    # Embaralhar a lista
    random.shuffle(uids_list)
    
    # Mostrar o resultado do sorteio no terminal
    print("Resultado do sorteio:")
    for i, uid in enumerate(uids_list, start=1):
        print(f"    {i}. {uid}")
    
    # Perguntar pelo layout das cartas
    layout_input = input("\nDigite o layout das cartas (ex.: '1 2 3. 4 5 6'):\n\t ")
    layout = [linha.strip().split() for linha in layout_input.split(".")]

    # Traduzir números no layout para UIDs
    selecionadas = []
    for linha in layout:
        for i, item in enumerate(linha):
            if item.isdigit():  # É um número
                num = int(item)
                if 1 <= num <= len(uids_list):
                    carta = uids_list[num - 1]
                    linha[i] = carta  # Traduzir para o UID correspondente
                    selecionadas.append(carta)

    # Exibir as cartas selecionadas no terminal
    print("\nCartas selecionadas para o layout:")
    for carta in selecionadas:
        print(f"    {carta}")

    # Gerar dois arquivos PNG: um para cada diretório de imagens
    gerar_png(layout, images_dir_rws, output_dir, "outputs-rws")
    gerar_png(layout, images_dir_tdm, output_dir, "outputs-tdm")

def gerar_png(layout, images_dir, output_dir, prefixo):
    imagens_cartas = []
    largura_padrao = 0  # Será calculado com base na primeira carta
    altura_padrao = 425  # Altura fixa para todas as cartas

    for linha in layout:
        linha_imagens = []
        for carta in linha:
            if carta == ",":  # Espaço vazio
                linha_imagens.append(None)
            else:
                invertida = carta.startswith("inv")
                if invertida:
                    carta = carta[3:]  # Remover o prefixo 'inv'
                
                caminho_imagem = os.path.join(images_dir, f"{carta}.jpg")
                if os.path.exists(caminho_imagem):
                    imagem = Image.open(caminho_imagem)
                    if invertida:
                        imagem = imagem.rotate(180)  # Rotacionar a imagem em 180 graus
                    proporcao = altura_padrao / float(imagem.height)
                    nova_largura = int(imagem.width * proporcao)
                    imagem_redimensionada = imagem.resize((nova_largura, altura_padrao), Image.Resampling.LANCZOS)
                    linha_imagens.append(imagem_redimensionada)

                    if largura_padrao == 0:  # Definir largura padrão com base na primeira carta
                        largura_padrao = imagem_redimensionada.width
                else:
                    print(f"Imagem não encontrada para: {carta}")
                    linha_imagens.append(None)
        imagens_cartas.append(linha_imagens)

    # Calcular largura máxima por linha e altura total
    larguras_por_linha = [
        sum(imagem.width if imagem else largura_padrao for imagem in linha) for linha in imagens_cartas
    ]
    largura_maxima = max(larguras_por_linha)
    altura_total = len(imagens_cartas) * altura_padrao

    # Criar a imagem final com fundo transparente
    imagem_final = Image.new("RGBA", (largura_maxima, altura_total), (255, 255, 255, 0))

    # Colocar as cartas centralizadas no layout
    y_offset = 0
    for linha, largura_linha in zip(imagens_cartas, larguras_por_linha):
        x_offset = (largura_maxima - largura_linha) // 2  # Centralizar a linha
        for imagem in linha:
            if imagem is not None:
                imagem_final.paste(imagem, (x_offset, y_offset), imagem.convert("RGBA"))
                x_offset += imagem.width
            else:
                x_offset += largura_padrao  # Espaço para cartas vazias agora tem largura de uma carta
        y_offset += altura_padrao

    # Função para encontrar um nome disponível para o arquivo PNG
    def proximo_nome_disponivel(prefixo="resultado", extensao="png"):
        numero = 1
        while True:
            nome_arquivo = f"{prefixo}-{numero:03d}.{extensao}"
            nome_arquivo_path = os.path.join(output_dir, nome_arquivo)
            if not os.path.exists(nome_arquivo_path):
                return nome_arquivo_path
            numero += 1

    # Gerar o arquivo PNG com as imagens das cartas destacadas
    nome_arquivo_png = proximo_nome_disponivel(prefixo)
    
    # Adicionar metadados personalizados
    metadata = PngImagePlugin.PngInfo()
    metadata.add_text("Origem", f"Imagens do diretório: {images_dir}")
    metadata.add_text("Título", "Layout de Cartas")
    metadata.add_text("Descrição", "Imagem gerada com o layout personalizado de cartas.")
    metadata.add_text("Autor", "Nome do Autor")
    metadata.add_text("Palavras-chave", "cartas, layout, embaralhamento, imagens")
    metadata.add_text("Data/Hora de Criação", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    # Salvar a imagem com os metadados
    imagem_final.save(nome_arquivo_png, pnginfo=metadata)

    print(f"\nArquivo PNG '{nome_arquivo_png}' gerado com sucesso.")


# Lista de UIDs
uids = [
    "Cups01", "Cups02", "Cups03", "Cups04", "Cups05", "Cups06", "Cups07", "Cups08", "Cups09", "Cups10", "Cups11", "Cups12", "Cups13", "Cups14", 
    "MA-01-Mago", "MA-02-Papisa", "MA-03-Imperatriz", "MA-04-Imperador", "MA-05-Papa", "MA-06-Amantes", "MA-07-Carruagem", "MA-08-Justica", 
    "MA-09-Eremita", "MA-10-Roda", "MA-11-Forca", "MA-12-Enforcado", "MA-13-Morte", "MA-14-Temperanca", "MA-15-Diabo", "MA-16-Torre", 
    "MA-17-Estrela", "MA-18-Lua", "MA-19-Sol", "MA-20-Julgamento", "MA-21-Mundo", "MA-22-Louco", "Pents01", "Pents02", "Pents03", "Pents04", 
    "Pents05", "Pents06", "Pents07", "Pents08", "Pents09", "Pents10", "Pents11", "Pents12", "Pents13", "Pents14", "Swords01", "Swords02", "Swords03", "Swords04", 
    "Swords05", "Swords06", "Swords07", "Swords08", "Swords09", "Swords10", "Swords11", "Swords12", "Swords13", "Swords14", 
    "Wands01", "Wands02", "Wands03", "Wands04", "Wands05", "Wands06", "Wands07", "Wands08", "Wands09", "Wands10", "Wands11", 
    "Wands12", "Wands13", "Wands14"
]

# Executar a função
embaralhar_e_destacar(uids)