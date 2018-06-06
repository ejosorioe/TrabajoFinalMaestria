#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import matplotlib.pyplot as plt
# import os.path
# import pandas as pd
# from string import punctuation
# from re import sub, compile, UNICODE, escape
# from datetime import datetime
# from time import time
#
# import dill
# from nltk import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem.snowball import SnowballStemmer
# from pymongo import MongoClient
# from wordcloud import WordCloud


def prepararTweetStemmer(mensaje):
    from unidecode import unidecode
    from string import punctuation
    from re import sub, compile, UNICODE, escape
    from nltk import word_tokenize
    from nltk.stem.snowball import SnowballStemmer

    emoji_pattern = compile("["
                               u"\U0001F600-\U0001F64F"  # emoticones
                            u"\U0001F300-\U0001F5FF"  # símbolos y pictografías
                            u"\U0001F680-\U0001F6FF"  # símbolos de transporte y mapa
                            u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                            u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=UNICODE)

    emoji_pattern2 = compile(u"[^\U00000000-\U0000d7ff\U0000e000-\U0000ffff]", flags=UNICODE)
    emoji_pattern3 = compile(u"\u2026", flags=UNICODE)  # caracter tres puntos
    stemmer = SnowballStemmer("spanish")

    mensaje = sub(r"http\S+", "", mensaje)
    mensaje = sub(r"[0-9]\S+", "", mensaje)
    mensaje = sub(emoji_pattern, "", mensaje)
    mensaje = sub(emoji_pattern2, "", mensaje)
    mensaje = sub(emoji_pattern3, "", mensaje)
    mensaje = sub('[%s]' % escape(punctuation), "", mensaje)
    mensaje = sub(r"¡|¿+", "", mensaje)
    try:
        mensaje = unicode(mensaje, 'utf8').lower()
    except:
        mensaje = unidecode(mensaje)
        mensaje = mensaje.lower()
    word_tokens = word_tokenize(mensaje)

    filtered_sentence = [unidecode(stemmer.stem(w)) for w in word_tokens]
    return filtered_sentence


def prepararTweet(mensaje):

    from unidecode import unidecode
    from string import punctuation
    from re import sub, compile, UNICODE, escape
    from nltk import word_tokenize

    emoji_pattern = compile("["
                               u"\U0001F600-\U0001F64F"  # emoticones
                            u"\U0001F300-\U0001F5FF"  # símbolos y pictografías
                            u"\U0001F680-\U0001F6FF"  # símbolos de transporte y mapa
                            u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                            u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=UNICODE)

    emoji_pattern2 = compile(u"[^\U00000000-\U0000d7ff\U0000e000-\U0000ffff]", flags=UNICODE)
    emoji_pattern3 = compile(u"\u2026", flags=UNICODE)  # caracter tres puntos


    mensaje = sub(r"http\S+", "", mensaje)
    mensaje = sub(r"[0-9]\S+", "", mensaje)
    mensaje = sub(emoji_pattern, "", mensaje)
    mensaje = sub(emoji_pattern2, "", mensaje)
    mensaje = sub(emoji_pattern3, "", mensaje)
    mensaje = sub('[%s]' % escape(punctuation), "", mensaje)
    mensaje = sub(r"¡|¿+", "", mensaje)
    try:
        mensaje = unicode(mensaje, 'utf8').lower()
    except:
        mensaje = unidecode(mensaje)
        mensaje = mensaje.lower()
    word_tokens = word_tokenize(mensaje)
    filtered_sentence = word_tokens

    return filtered_sentence

def generarWordcloud(mensajes, nombreArchivo):
    from unidecode import unidecode
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    from string import punctuation
    from re import sub, compile, UNICODE, escape

    from nltk import word_tokenize
    from nltk.corpus import stopwords
    from nltk.stem.snowball import SnowballStemmer
    from wordcloud import WordCloud

    emoji_pattern = compile("["
                            u"\U0001F600-\U0001F64F"  # emoticones
                            u"\U0001F300-\U0001F5FF"  # símbolos y pictografías
                            u"\U0001F680-\U0001F6FF"  # símbolos de transporte y mapa
                            u"\U0001F1E0-\U0001F1FF"  # banderas (iOS)
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=UNICODE)

    emoji_pattern2 = compile(u"[^\U00000000-\U0000d7ff\U0000e000-\U0000ffff]", flags=UNICODE)
    emoji_pattern3 = compile(u"\u2026", flags=UNICODE)  # caracter tres puntos

    stemmer = SnowballStemmer("spanish")
    stop_words = set(stopwords.words('spanish'))


    file = open("app/functions/datos/"+nombreArchivo + '.txt', 'w')
    #file = open(os.path.join(BASE, "graficas/"+nombreArchivo + '.txt'), 'w')
    for mensaje in mensajes:
        mensaje = sub(r"http\S+", "", mensaje)
        mensaje = sub(r"[0-9]\S+", "", mensaje)
        mensaje = sub(r"@\S+", "", mensaje)
        mensaje = sub(r"#\S+", "", mensaje)
        mensaje = sub(emoji_pattern, "", mensaje)
        mensaje = sub(emoji_pattern2, "", mensaje)
        mensaje = sub(emoji_pattern3, "", mensaje)
        mensaje = sub('[%s]' % escape(punctuation), "", mensaje)
        mensaje = sub(r"¡|¿+", "", mensaje)
        mensaje = mensaje.lower()
        mensaje = unidecode(mensaje)
        wordTokens = word_tokenize(mensaje)
        palabrasFiltradas = [w for w in wordTokens if w not in stop_words]
        sentenciaFiltrada = ' '.join(palabrasFiltradas)
        file.write(sentenciaFiltrada.encode('utf-8') + " ")
    file.close()

    # text = open(os.path.join(BASE,nombreArchivo + '.txt')).read()
    text = open("app/functions/datos/"+nombreArchivo + '.txt').read()

    # wordcloud = WordCloud(background_color= "rgb(29,49,70)", mode="RGB", max_font_size=80,collocations=False, max_words=1000).generate(str(text))
   # wordcloud = WordCloud(background_color="white", mode="RGB", max_font_size=80, collocations=False,max_words=1000).generate(str(text))
    wordcloud = WordCloud(max_font_size=60, collocations=False, max_words=2000).generate(str(text))

    plt.figure(figsize=(8,4))
    plt.imshow(wordcloud, cmap=plt.cm.gray, interpolation="bilinear")
    plt.axis("off")
    plt.savefig("app/static/graficas/"+nombreArchivo + '.png', bbox_inches='tight', pad_inches = 0)
    plt.close()
    rutaImagen = "/static/graficas/"+nombreArchivo + '.png'
    return rutaImagen


def clasificarTweets(fechaInicio, fechaFin):
    import pandas as pd
    import dill
    from pymongo import MongoClient

    client = MongoClient('localhost', 27017)
    db = client.twitter
    tweets = db.tweets_valle_aburra

    tweetsDB = list(tweets.find({"fecha_guardado": {"$gte": fechaInicio, "$lt": fechaFin}}))
    dfTweets = pd.DataFrame(tweetsDB)
    if not dfTweets.empty:
        # clasificadorSVM = dill.load(open(os.path.join(BASE, "modelos/clasificadorSVM.pkl")))
        clasificadorSVM = dill.load(open("app/functions/modelos/clasificadorSVM.pkl"))
        dfTweets['categoria'] = clasificadorSVM.predict(dfTweets.text)

    return dfTweets


def correrClasificador(fechaInicio, fechaFin):
    from datetime import datetime
    from time import time
    import pandas as pd

    start_time = time()
    fechaInicio = datetime.strptime(fechaInicio, '%m/%d/%Y')
    fechaFin = datetime.strptime(fechaFin, '%m/%d/%Y')

    tweetsClasificador = clasificarTweets(fechaInicio, fechaFin)
    if tweetsClasificador.empty:
        data = {'status': 'error', 'mensaje': 'No se encontraron datos dentro de las fechas seleccionadas'}
        return data
    else:
        totalTweets = len(tweetsClasificador.index)

        tweetsSIATA = tweetsClasificador[tweetsClasificador['categoria'] == 'siata']
        cantidadTweetsSIATA = len(tweetsSIATA.index)

        tweetsNoSIATA = tweetsClasificador[tweetsClasificador['categoria'] == 'nosiata']
        cantidadTweetsNoSIATA = len(tweetsNoSIATA.index)

        rutaWordcloudNoSIATA = generarWordcloud(tweetsNoSIATA.text, "prueba_tweetsNoSIATA")
        rutaWordcloudSIATA = generarWordcloud(tweetsSIATA.text, "prueba_tweetsSIATA")

        diferencia = fechaFin - fechaInicio
        diasAbarcados = diferencia.days

        tiempoEjecucion = time() - start_time
        tiempoEjecucion = str(round(tiempoEjecucion, 2))

        usuarios = tweetsSIATA['user']
        usuarios =list(usuarios)
        usuariospd = pd.DataFrame.from_dict(usuarios)
        # print(usuariospd.screen_name.unique())
        # print(len(usuariospd.screen_name.unique()))
        cantidadInvitaciones = len(usuariospd.screen_name.unique())

        resultado = {}
        resultado['cantidadTweetsSIATA'] = cantidadTweetsSIATA
        resultado['cantidadTweetsNoSIATA'] = cantidadTweetsNoSIATA
        resultado['totalTweets'] = totalTweets
        resultado['cantidadInvitaciones'] = cantidadInvitaciones
        resultado['diasAbarcados'] = diasAbarcados
        resultado['tiempoEjecucion'] = tiempoEjecucion
        resultado['rutaWordcloudSIATA'] = rutaWordcloudSIATA
        resultado['rutaWordcloudNoSIATA'] = rutaWordcloudNoSIATA
        resultado['status'] = 'ok'
        resultado['mensaje'] = 'Se realizo la clasificación con éxito'

        return resultado

# if __name__ == "__main__":
#     print correrClasificador("05/20/2018", "05/21/2018")

# # print correrClasificador("05/20/2018", "05/21/2018")
# if __name__ == "__main__":
#
#     data = pd.read_csv('datos/entrenamiento.csv')
#     data = data.sample(frac=1)
#
#     vectorConteo = CountVectorizer(analyzer = prepararTweetStemmer).fit(data['text'])
#     matrizTerminos = vectorConteo.transform(data['text'])
#
#     tfidfTransformer = TfidfTransformer().fit(matrizTerminos)
#     mensajesTfidf = tfidfTransformer.transform(matrizTerminos)
#
#     mensajeEntrenamiento, mensajePrueba, labelEntrenamiento, labelPrueba = \
#         train_test_split(data['text'], data['label'], test_size=0.5)
#
#
#     pipelineSVM = Pipeline([
#                             ('bow', CountVectorizer(analyzer=prepararTweetStemmer)),  # strings to token integer counts
#                             ('tfidf', TfidfTransformer()),  # integer counts to weighted TF-IDF scores
#                             ('classifier', SVC()),  # train on TF-IDF vectors w/ Naive Bayes classifier
#                         ])
#
#     paramSVM = [
#                   {'classifier__C': [0.1, 1, 10], 'classifier__kernel': ['linear']},
#                   {'classifier__C': [0.1, 1, 10], 'classifier__kernel': ['poly']},
#                   {'classifier__C': [0.1, 1, 10], 'classifier__kernel': ['rbf']},
#                   {'tfidf__use_idf': (True, False) },
#                   { 'bow__analyzer': (prepararTweetStemmer, prepararTweet)},
#                 ]
#
#     gridSVM = GridSearchCV(
#             pipelineSVM,
#             paramSVM,
#             refit = True,
#             n_jobs = -1,
#             scoring = 'accuracy',
#         )
#
#     clasificadorSVM = gridSVM.fit(mensajeEntrenamiento, labelEntrenamiento)
#
#     with open('modelos/clasificadorSVM.pkl', "wb") as f:
#         dill.dump(clasificadorSVM, f)


#https://stackoverflow.com/questions/26696695/store-object-using-python-pickle-and-load-it-into-different-namespace