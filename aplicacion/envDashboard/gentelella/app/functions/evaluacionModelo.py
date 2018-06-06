#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import dill
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from collections import defaultdict
from time import time


def report2dict(cr):
    # Parse rows
    tmp = list()
    for row in cr.split("\n"):
        parsed_row = [x for x in row.split("  ") if len(x) > 0]
        if len(parsed_row) > 0:
            tmp.append(parsed_row)

    # Store in dictionary
    measures = tmp[0]

    D_class_data = defaultdict(dict)
    for row in tmp[1:]:
        class_label = row[0]
        for j, m in enumerate(measures):
            D_class_data[class_label][m.strip()] = float(row[j + 1].strip())
    return D_class_data


def entrenarClasificador():
    start_time = time()
    clasificadorSVM = dill.load(open("app/functions/modelos/clasificadorSVM.pkl"))
    data = pd.read_csv('app/functions/datos/nuevoEntrenamiento.csv')
    data = data.sample(frac=1)

    mensajeEntrenamiento, mensajePrueba, labelEntrenamiento, labelPrueba = \
        train_test_split(data['text'], data['label'], test_size=0.5)
    nuevoClasificadorSVM = clasificadorSVM.fit(mensajeEntrenamiento, labelEntrenamiento)

    labelPrediccion = nuevoClasificadorSVM.predict(mensajePrueba)
    tn, fp, fn, tp = confusion_matrix(y_true=labelPrueba, y_pred=labelPrediccion).ravel()
    # print (tn, fp, fn, tp)
    # print(accuracy_score(labelPrueba, labelPrediccion))
    accuracy = accuracy_score(labelPrueba, labelPrediccion)

    # print(classification_report(labelPrueba, labelPrediccion))

    target_names = ['nosiata', 'siata']
    reportClassification = report2dict(classification_report(labelPrueba, labelPrediccion, target_names=target_names))
    # print reportClassification
    # print reportClassification['siata']['recall']

    total = float(len(data.index))
    dataSiata = data[data['label'] == 'siata']
    totalSiata = float(len(dataSiata.index))
    dataNoSiata = data[data['label'] == 'nosiata']
    totalNoSiata = float(len(dataNoSiata.index))

    tiempoEjecucion = time() - start_time
    tiempoEjecucion = str(round(tiempoEjecucion, 2))

    resultado = {}
    resultado['tn'] = tn
    resultado['fp'] = fp
    resultado['fn'] = fn
    resultado['tp'] = tp
    resultado['total'] = total
    resultado['accuracy'] = accuracy
    resultado['totalSiata'] = totalSiata
    resultado['totalNoSiata'] = totalNoSiata
    resultado['tiempoEjecucion'] = tiempoEjecucion
    resultado['reportClassification'] = dict(reportClassification)
    resultado['porcentajeSiata'] = str((totalSiata / total) * 100) + '%'
    resultado['porcentajeNoSiata'] = str((totalNoSiata / total) * 100) + '%'
    resultado['status'] = 'ok'
    resultado['mensaje'] = 'Se realizo el entrenamiento con exito'

    return resultado
    # with open('app/functions/modelos/nuevoClasificadorSVM.pkl', "wb") as f:
    #     dill.dump(nuevoClasificadorSVM, f)

#
# if __name__ == "__main__":
#     entrenarClasificador()
