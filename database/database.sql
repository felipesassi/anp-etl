CREATE TABLE IF NOT EXISTS ANP (
  "Regiao - Sigla" TEXT,
  "Estado - Sigla" TEXT,
  "Municipio" TEXT,
  "Revenda" TEXT,
  "CNPJ da Revenda" TEXT,
  "Nome da Rua" TEXT,
  "Numero Rua" TEXT,
  "Complemento" TEXT,
  "Bairro" TEXT,
  "Cep" TEXT,
  "Bandeira" TEXT,
  "Produto" TEXT,
  "Unidade de Medida" TEXT,
  "Data da Coleta" DATE,
  "Valor de Compra" DOUBLE PRECISION,
  "Valor de Venda" DOUBLE PRECISION,
  "Valor de Venda Anterior" DOUBLE PRECISION,
  "Data da Coleta Anterior" DATE,
  "Dias entre Coletas" INTEGER
);

CREATE TABLE IF NOT EXISTS GAS_STATIONS (
  "Regiao - Sigla" TEXT,
  "Estado - Sigla" TEXT,
  "Municipio" TEXT,
  "Revenda" TEXT,
  "CNPJ da Revenda" TEXT,
  "Nome da Rua" TEXT,
  "Numero Rua" TEXT,
  "Complemento" TEXT,
  "Bairro" TEXT,
  "Cep" TEXT,
  "Bandeira" TEXT
);
