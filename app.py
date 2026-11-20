import random

from flask import Flask, redirect, render_template, request
 
app = Flask(__name__)

cartas = {
    "Jotaro" : {
                    "nome" : "Jotaro Kujo",
                    "img" : "jotaro.jpg",
                    "raridade" : "epica",
                    "força" : 90,
                    "habilidades_poderes" : 85,
                    "defesa_vida": 80,
                    "velocidade": 40,
                },
    "Dio" : {
                    "nome" : "Dio Brando",
                    "img" : "dio.jpeg",
                    "raridade" : "lendaria",
                    "força" : 60,
                    "habilidades_poderes" : 95,
                    "defesa_vida": 60,
                    "velocidade": 80,
                },

    "Joseph" : {
                    "nome" : "Joseph Joestar",
                    "img" : "joseph.jpeg",
                    "raridade" : "rara",
                    "força" : 65,
                    "habilidades_poderes" : 95,
                    "defesa_vida": 80,
                    "velocidade": 60,
                },

}



@app.route("/")
def index():
    return render_template("index.html")


@app.route("/regras")
def regras():
    return render_template("regras.html")


# Pacotinho: sorteia uma carta e vai direto para o duelo
@app.route("/pacotinho")
def pacotinho():
    carta = random.choice(list(cartas))
    return redirect("/duelo/" + carta)


# Duelo, passo 1: escolher o atributo
@app.route("/duelo/<carta>")
def escolher_atributo(carta):
    if carta not in cartas:          # apelido errado? volta para a coleção
        return redirect("/")
    return render_template("atributo.html", carta=carta, minha=cartas[carta])


# Duelo, passo 2: comparar com uma carta sorteada
@app.route("/duelo/<carta>/<atributo>")
def resultado(carta, atributo):
    if carta not in cartas:
        return redirect("/")
    minha = cartas[carta]
    if atributo not in minha:        # atributo errado? volta para a escolha
        return redirect("/duelo/" + carta)

    outras = [c for c in cartas if c != carta]
    if len(outras) == 0:             # só tem uma carta? duela com ela mesma
        outras = [carta]
    adversaria = cartas[random.choice(outras)]

    if minha[atributo] > adversaria[atributo]:
        resultado = "Você venceu!"
    elif minha[atributo] < adversaria[atributo]:
        resultado = "Você perdeu!"
    else:
        resultado = "Empate!"

    poder_total = minha["força"] + minha["habilidades_poderes"] + minha["defesa_vida"] + minha["velocidade"]

    return render_template("resultado.html",
                           atributo=atributo,
                           minha=minha,
                           adversaria=adversaria,
                           resultado=resultado,
                           poder_total=poder_total)

@app.route("/criar")
def criar():
    return render_template("criar.html")

@app.route("/carta_criada", methods=["POST"])
def carta_criada():
    nome = request.form["nome"]
    imagem = request.form["imagem"]
    raridade = request.form["raridade"]
    força = int(request.form["força"])
    habilidades_poderes = int(request.form["habilidades_poderes"])
    defesa_vida = int(request.form["defesa_vida"])
    velocidade = int(request.form["velocidade"])

    # A carta nova também entra no duelo (até o servidor reiniciar!)
    chave = nome.lower().replace(" ", "-")
    cartas[chave] = {"nome": nome, "imagem": imagem, "raridade": raridade,
                     "força": força, "habilidades_poderes": habilidades_poderes, "defesa_vida": defesa_vida, "velocidade": velocidade}

    poder_total = força + habilidades_poderes + defesa_vida + velocidade
    return render_template("carta_criada.html",
                           chave=chave, nome=nome, imagem=imagem, raridade=raridade,
                           força=força, habilidades_poderes=habilidades_poderes, defesa_vida=defesa_vida, velocidade=velocidade,
                           poder_total=poder_total)

app.run(debug=True)
