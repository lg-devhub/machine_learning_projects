import cv2
import easyocr
import requests

# 📸 CAMINHO DA IMAGEM
imagem_path = "books.jpg"

# 🔍 CARREGAR IMAGEM
imagem = cv2.imread(imagem_path)

if imagem is None:
    print("❌ Erro ao carregar a imagem.")
    exit()

# 🧠 INICIALIZAR OCR
reader = easyocr.Reader(['en'])  # pode adicionar 'pt' também

# 🔎 EXTRAIR TEXTO
resultados = reader.readtext(imagem_path)

print("\n📄 TEXTO EXTRAÍDO:\n")

livros = []

for (bbox, texto, prob) in resultados:
    print(f"{texto} (confiança: {round(prob, 2)})")
    
    # filtrar textos muito pequenos ou irrelevantes
    if len(texto) > 3:
        livros.append(texto)

# remover duplicados
livros = list(set(livros))

print("\n📚 POSSÍVEIS LIVROS ENCONTRADOS:\n")
for livro in livros:
    print("-", livro)


# 🌐 FUNÇÃO PARA BUSCAR LIVRO
def buscar_livro(nome):
    url = f"https://www.googleapis.com/books/v1/volumes?q={nome}"
    response = requests.get(url)

    if response.status_code != 200:
        return None

    data = response.json()

    if "items" in data:
        info = data["items"][0]["volumeInfo"]
        return {
            "titulo": info.get("title", "N/A"),
            "autor": ", ".join(info.get("authors", ["Desconhecido"])),
            "descricao": info.get("description", "Sem descrição")
        }

    return None


# 🔗 BUSCAR INFORMAÇÕES
print("\n🔎 RESULTADOS DA BUSCA:\n")

for livro in livros:
    resultado = buscar_livro(livro)

    if resultado:
        print(f"📖 Título: {resultado['titulo']}")
        print(f"✍️ Autor: {resultado['autor']}")
        print("-" * 40)


# 🖥️ MOSTRAR IMAGEM
cv2.imshow("Imagem", imagem)
cv2.waitKey(0)
cv2.destroyAllWindows()