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
El conjunto de datos, conocido como "The Berka Dataset", es una colección de información financiera de un banco checo. Incluye información sobre más de 5,300 clientes bancarios con aproximadamente 1,000,000 de transacciones. Además, el banco representado en el conjunto de datos ha extendido cerca de 700 préstamos y emitido casi 900 tarjetas de crédito, todos los cuales están representados en los datos.

### Descripción de Entidades-Relaciones
- Cada cuenta tiene características estáticas (por ejemplo, fecha de creación, dirección de la sucursal) dadas en la relación "account" y características dinámicas (por ejemplo, pagos debitados o acreditados, saldos) dadas en las relaciones "permanent order" y "transaction".
- La relación "client" describe las características de las personas que pueden manipular las cuentas. Un cliente puede tener varias cuentas y viceversa; los clientes y las cuentas están relacionados en la relación "disposition".
- Las relaciones "loan" y "credit card" describen algunos servicios que el banco ofrece a sus clientes. Se pueden emitir varias tarjetas de crédito para una cuenta, pero a lo sumo se puede otorgar un préstamo para una cuenta.
- La relación "demographic data" proporciona información pública sobre los distritos (por ejemplo, la tasa de desempleo); información adicional sobre los clientes se puede deducir a partir de esto.

### Descripciones de Tablas
- **ACCOUNTS**: Cada registro describe características estáticas de una cuenta.
  - Tamaño: 4500 objetos en el archivo.
- **CLIENTS**: Cada registro describe características de un cliente.
  - Tamaño: 5369 objetos en el archivo.
- **DISPOSITION (DISP)**: Cada registro relaciona a un cliente con una cuenta, es decir, describe los derechos de los clientes para operar cuentas.
  - Tamaño: 5369 objetos en el archivo.
- **PERMANENT ORDERS (ORDER)**: Cada registro describe características de una orden de pago.
  - Tamaño: 6471 objetos en el archivo.
- **TRANSACTIONS (TRANS)**: Cada registro describe una transacción en una cuenta.
  - Tamaño: 1056320 objetos en el archivo.
- **LOANS**: Cada registro describe un préstamo otorgado para una cuenta.
  - Tamaño: 682 objetos en el archivo.
- **CREDIT CARDS (CARD)**: Cada registro describe una tarjeta de crédito emitida para una cuenta.
  - Tamaño: 892 objetos en el archivo.
- **DEMOGRAPHIC DATA (DISTRICT)**: Cada registro describe características demográficas de un distrito.
  - Tamaño: 77 objetos en el archivo.

## Hipótesis Planteadas
1. Existe una relación entre el historial de transacciones y el incumplimiento de préstamos.
2. Los clientes con un mayor número de préstamos tienen una mayor probabilidad de incumplir.
3. La ubicación geográfica de los clientes influye en su probabilidad de incumplimiento.
4. Los clientes con tarjetas de crédito activas tienen menos probabilidades de incumplir.
5. La tasa de desempleo en el distrito del cliente está relacionada con su historial crediticio.