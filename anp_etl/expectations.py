from great_expectations.core.expectation_configuration import ExpectationConfiguration


def expectation_to_check_categorical_cols_values(suite):

    cols_and_checks = {
        "Produto": ["DIESEL S10", "DIESEL", "ETANOL", "GNV", "GASOLINA", "GASOLINA ADITIVADA"],
        "Regiao - Sigla": ["NE", "N", "S", "SE", "CO"],
        "Estado - Sigla": [
            "SC",
            "RO",
            "PI",
            "AM",
            "RR",
            "GO",
            "TO",
            "MT",
            "SP",
            "ES",
            "PB",
            "RS",
            "MS",
            "AL",
            "MG",
            "PA",
            "BA",
            "SE",
            "PE",
            "CE",
            "RN",
            "RJ",
            "MA",
            "AC",
            "DF",
            "PR",
            "AP",
        ],
    }

    for col in cols_and_checks:

        expectation_configuration = ExpectationConfiguration(
            expectation_type="expect_column_distinct_values_to_be_in_set",
            kwargs={"column": col, "value_set": cols_and_checks[col]},
        )

        suite.add_expectation(expectation_configuration=expectation_configuration)


def expectation_to_check_null_values(suite):

    for col in [
        "Valor de Venda",
        "Data da Coleta",
        "Revenda",
        "Municipio",
        "CNPJ da Revenda",
        "Cep",
        "Data da Coleta",
        "Estado - Sigla",
        "Regiao - Sigla",
        "Produto",
        "Bandeira",
    ]:

        expectation_configuration = ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": col},
        )

        suite.add_expectation(expectation_configuration=expectation_configuration)


def expectation_to_check_table_rows(suite):

    expectation_configuration = ExpectationConfiguration(
        expectation_type="expect_table_row_count_to_be_between",
        kwargs={"min_value": 100e3, "max_value": 1e6},
    )

    suite.add_expectation(expectation_configuration=expectation_configuration)


def expectation_to_check_columns_order(suite):

    expectation_configuration = ExpectationConfiguration(
        expectation_type="expect_table_columns_to_match_ordered_list",
        kwargs={
            "column_list": [
                "Regiao - Sigla",
                "Estado - Sigla",
                "Municipio",
                "Revenda",
                "CNPJ da Revenda",
                "Nome da Rua",
                "Numero Rua",
                "Complemento",
                "Bairro",
                "Cep",
                "Produto",
                "Data da Coleta",
                "Valor de Venda",
                "Valor de Compra",
                "Unidade de Medida",
                "Bandeira",
            ]
        },
    )

    suite.add_expectation(expectation_configuration=expectation_configuration)
