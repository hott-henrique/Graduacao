# Sistema de transporte

## Organização dos arquivos

O programa deve estar organizado em 3 arquivos:
- tpmain.c - Deve conter a função main a a lógica do sistema.
- tp.h - Deve conter as assinaturas das funções que executa as operações especificadas.
- tp.c - Deve implementar as funções necessárias para executar as operações.

## Especificação

Elabore um programa em Linguagem C que faça reservas de passagens de ônibus de determinada empresa.

O programa deve ler o número dos ônibus e o número de lugares disponíveis em cada um.

Utilize um vetor de 4 posições, em que cada posição representa um ônibus.

O programa deve ter o seguinte menu de opções:

0. **Sair:** Deve finalizar a execução.
1. **Cadastrar o número dos ônibus:** Deve solicitar ao usuário o número dos quatro ônibus disponíveis.
2. **Cadastrar o quantidade de vagas:** Deve solicitar ao usuário a quantidade de vagas em cada um dos quatro ônibus disponíveis.
3. **Reservar passagem:** Deve solicitar o ônibus e o nome do passageiro, salvar passagem, e mostrar a mensagem de sucesso ou falha.
4. **Consultar por ônibus:** Deve solicitar o ônibus, mostrar todos os seus ocupantes ou acusar erro se teve algum.
5. **Consultar por passageiro:** Deve solicitar o nome do passageiro, mostrar todos as suas reservas ou acusar erro se teve algum.

