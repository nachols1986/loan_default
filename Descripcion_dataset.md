# Análisis y Predicción del Incumplimiento de Préstamos

## Introducción

El análisis y predicción del incumplimiento de préstamos es fundamental para las instituciones financieras en la gestión del riesgo crediticio. La capacidad de identificar con precisión los préstamos que tienen mayor probabilidad de incumplir permite a los prestamistas tomar decisiones más informadas y mitigar posibles pérdidas. En este contexto, el presente trabajo se enfoca en explorar un conjunto de datos relacionado con préstamos y construir un modelo de clasificación para predecir si un prestatario caerá en incumplimiento o no.

## Descripción del Problema

El incumplimiento de préstamos representa un riesgo significativo para las instituciones financieras, ya que puede resultar en pérdidas financieras y afectar su estabilidad y solidez. Identificar los factores que influyen en el incumplimiento de préstamos y desarrollar modelos predictivos precisos es crucial para tomar decisiones fundamentadas en la gestión del riesgo crediticio. En este sentido, el análisis de datos y la construcción de modelos de clasificación pueden proporcionar insights valiosos para mejorar la evaluación de riesgos y la toma de decisiones crediticias.

## Objetivo

El objetivo principal de este trabajo es construir un modelo de clasificación que pueda predecir si un prestatario caerá en incumplimiento o no. Para lograr este objetivo, se explorará un conjunto de datos relacionado con préstamos, se realizará un análisis exploratorio de los datos para comprender mejor las características y los patrones presentes en ellos, y se construirá y evaluará el rendimiento de varios modelos de clasificación.

## Fuente

Los datos utilizados en este trabajo fueron obtenidos de Kaggle y se encuentran disponibles en el siguiente enlace: [Loan Default Dataset](https://www.kaggle.com/datasets/yasserh/loan-default-dataset).

Este conjunto de datos proporciona información detallada sobre préstamos, incluidos atributos como límite de préstamo, género del prestatario, tipo de préstamo, propósito del préstamo, solvencia crediticia, entre otros. El uso de estos datos permitirá realizar un análisis exhaustivo y construir un modelo predictivo robusto para la predicción del incumplimiento de préstamos.

## Información del Dataset

El conjunto de datos contiene 148,670 entradas y 34 columnas. A continuación se detallan las columnas presentes en el dataset:

- **ID**: Identificador único del préstamo
- **year**: Año en el que se otorgó el préstamo
- **loan_limit**: Límite del préstamo
- **Gender**: Género del prestatario
- **approv_in_adv**: Aprobación previa del préstamo
- **loan_type**: Tipo de préstamo
- **loan_purpose**: Propósito del préstamo
- **Credit_Worthiness**: Solvencia crediticia del prestatario
- **open_credit**: Crédito abierto
- **business_or_commercial**: Uso comercial o de negocios
- **loan_amount**: Monto del préstamo
- **rate_of_interest**: Tasa de interés
- **Interest_rate_spread**: Diferencia de la tasa de interés
- **Upfront_charges**: Cargos iniciales
- **term**: Plazo del préstamo
- **Neg_ammortization**: Amortización negativa
- **interest_only**: Solo intereses
- **lump_sum_payment**: Pago único
- **property_value**: Valor de la propiedad
- **construction_type**: Tipo de construcción
- **occupancy_type**: Tipo de ocupación
- **Secured_by**: Garantizado por
- **total_units**: Unidades totales
- **income**: Ingresos del prestatario
- **credit_type**: Tipo de crédito
- **Credit_Score**: Puntuación de crédito
- **co-applicant_credit_type**: Tipo de crédito del co-aplicante
- **age**: Edad del prestatario
- **submission_of_application**: Presentación de la solicitud
- **LTV**: Loan-to-Value ratio (relación préstamo-valor)
- **Region**: Región del préstamo
- **Security_Type**: Tipo de garantía
- **Status**: Estado del préstamo (incumplimiento o no)
- **dtir1**: Ratio de deuda a ingresos

## Hipótesis Planteadas

- **Hipótesis 1**: Existe una diferencia entre el nivel de morosidad de hombres y mujeres.
- **Hipótesis 2**: La morosidad varía linealmente con el monto del préstamo.
- **Hipótesis 3**: La morosidad aumenta con la tasa de interés.
- **Hipótesis 4**: La morosidad disminuye con el nivel de ingresos del tomador del préstamo.
