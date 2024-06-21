# Descripción del Dataset Financiero Checo de 1999

## Introducción
Este conjunto de datos contiene información de un banco checo real correspondiente al período de 1993 a 1998. Proporciona una visión detallada de las relaciones entre los clientes y sus cuentas, así como de otros aspectos financieros y demográficos relevantes.

## Descripción del Problema
El análisis de datos financieros es esencial para comprender el comportamiento de los clientes y tomar decisiones informadas en el sector bancario. En este caso, nos centraremos en la predicción del incumplimiento de préstamos, un problema crucial que enfrentan las instituciones financieras.

## Objetivo
El objetivo principal de este análisis es desarrollar un modelo predictivo para clasificar a los clientes según su probabilidad de incumplimiento de préstamos. Esto ayudará a las instituciones financieras a identificar y gestionar eficazmente los riesgos crediticios.

## Fuente de los Datos
Los datos fueron obtenidos de [Kaggle](https://www.kaggle.com/datasets/mariammariamr/1999-czech-financial-dataset) y corresponden a un banco checo real. Fueron preparados por Petr Berka y Marta Sochorova.


## Información del Dataset
El dataset consiste en varios archivos CSV que contienen información sobre diferentes relaciones:
- `ACCOUNT.CSV`: características estáticas de una cuenta.
- `CLIENT.CSV`: características de un cliente.
- `DISP.CSV`: relación entre clientes y cuentas.
- `ORDER.CSV`: características de una orden de pago.
- `TRANS.CSV`: transacciones en una cuenta.
- `LOAN.CSV`: préstamos otorgados para una cuenta.
- `CARD.CSV`: tarjetas de crédito emitidas para una cuenta.
- `DISTRICT.CSV`: características demográficas de un distrito.

## Hipótesis Planteadas
1. Existe una relación entre el historial de transacciones y el incumplimiento de préstamos.
2. Los clientes con un mayor número de préstamos tienen una mayor probabilidad de incumplir.
3. La ubicación geográfica de los clientes influye en su probabilidad de incumplimiento.
4. Los clientes con tarjetas de crédito activas tienen menos probabilidades de incumplir.
5. La tasa de desempleo en el distrito del cliente está relacionada con su historial crediticio.

