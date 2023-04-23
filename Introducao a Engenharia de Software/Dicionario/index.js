const input_node = document.getElementById("input_field")
const result_node = document.getElementById("result")

const footer_node = document.getElementById("footer")

definitions = {
    "engenharia de software": {
        "definition": "É uma disciplina de engenharia que se preocupa com todos os aspectos de produção de software.",
        "source": "SOMMERVILLE, Engenharia de Software, Pearson, 2003."
    },

    "software": {
        "definition": "Softwares são programas de computador e documentação associada. Produtos de software podem ser desenvolvidos para um cliente específico ou para o mercado em geral.",
        "source": "SOMMERVILLE, Engenharia de Software, Pearson, 2003."
    },

    "software legado": {
        "definition": "Os sistemas legados são plataformas ou softwares que estão obsoletos, ou seja, estão dentro de uma companhia por muitos anos. ",
        "source": "https://arphoenix.com.br/sistemas-legados-o-que-sao-e-porque-devo-atualiza-los/"
    },

    "dominio de aplicacao": {
        "definition": "É definido por um conjunto de características que descrevem uma família de problemas para os quais uma determinada aplicação pretende dar solução.",
        "source": "https://fluxodeinformacao.com/biblioteca/artigo/read/97190-o-que-e-o-dominio-de-uma-aplicacao"
    },

    "metodo agil": {
        "definition": "Métodos ágeis ou metodologia ágil é um termo usado para descrever abordagens de desenvolvimento de software que enfatizam a entrega incremental, a colaboração da equipe, o planejamento contínuo e o aprendizado contínuo, em vez de tentar entregar tudo de uma vez perto do fim.",
        "source": "https://controlf5it.com.br/blog/o-que-sao-metodos-ageis-de-desenvolvimento-de-software/"
    },

    "aplicações stand-alone": {
        "definition": "Essas são as aplicações executadas em um computador local, como um PC. Elas contêm toda a funcionalidade necessária e não precisam estar conectadas a uma rede. Exemplos de tais aplicações são aplicativos de escritório em um PC, programas CAD, software de manipulação de fotos etc.",
        "source": "SOMMERVILLE, Engenharia de Software, Pearson, 2003."
    },

    "aplicações interativas baseadas em transações": {
        "definition": "São aplicações que executam em um computador remoto, acessadas pelos usuários a partir de seus computadores ou terminais. Certamente, aqui são incluídas aplicações Web como aplicações de comércio eletrônico em que você pode interagir com o sistema remoto para comprar produtos ou serviços. Essa classe de aplicações também inclui sistemas corporativos, em que uma empresa fornece acesso a seus sistemas através de um navegador Web ou um programa cliente especial e serviços baseados em nuvem, como é o caso de serviços de e-mail e compartilhamento de fotos. Aplicações interati- vas frequentemente incorporam um grande armazenamento de dados, que é acessado e atualizado em cada transação.",
        "source": "SOMMERVILLE, Engenharia de Software, Pearson, 2003."
    },
    
    "sistemas de controle embarcado": {
        "definition": "São sistemas de controle que controlam e gerenciam dispositivos de hardware. Numericamente, é provável que haja mais sistemas embutidos do que de qualquer outro tipo. Exemplos de sistemas embutidos incluem software em telefone celular, softwares que controlam antitravamento de freios em um carro e software em um micro-ondas para controlar o processo de cozimento.",
        "source": "SOMMERVILLE, Engenharia de Software, Pearson, 2003."
    },

    "sistemas de processamento em lotes (batch)": {
        "definition": "São sistemas corporativos projetados para processar dados em grandes lotes. Eles processam grande número de entradas individuais para criar as saídas correspondentes. Exemplos dsistemas de lotes incluem sistemas periódicos de cobrança, como sistemas de cobrança telefônica, e sistemade pagamentos de salário.",
        "source": "SOMMERVILLE, Engenharia de Software, Pearson, 2003."
    },

    "sistemas de entretenimento": {
        "definition": "São sistemas cuja utilização principal é pessoal e cujo objetivo é entreter o usuário. A maioria desses sistemas é de jogos de diferentes tipos. A qualidade de interação com o usuário é a característica particular mais importante dos sistemas de entretenimento.",
        "source": "SOMMERVILLE, Engenharia de Software, Pearson, 2003."
    },

    "sistemas para modelagem e simulação": {
        "definition": "São sistemas que incluem vários objetos separados que interagem entre si, desenvolvidos por cientistas e engenheiros para modelar processos ou situações físicas. Esses sistemas geralmente fazem uso intensivo de recursos computacionais e requerem sistemas paralelos de alto desempenho para executar.",
        "source": "SOMMERVILLE, Engenharia de Software, Pearson, 2003."
    },

    "sistemas de coleta de dados e análise": {
        "definition": "São sistemas que coletam dados de seu ambiente com um conjunto de sensores e enviam esses dados para outros sistemas para processamento. O software precisa interagir com sensores e frequentemente é instalado em um ambiente hostil, por exemplo, dentro de uma máquina ou em um lugar remoto.",
        "source": "SOMMERVILLE, Engenharia de Software, Pearson, 2003."
    },

    "sistemas de sistemas": {
        "definition": "São sistemas compostos de uma série de outros sistemas de software. Alguns deles podem ser produtos genéricos de software, como um programa de planilha eletrônica. Outros sistemas do conjunto podem ser escritos especialmente para esse ambiente.",
        "source": "SOMMERVILLE, Engenharia de Software, Pearson, 2003."
    },

    "estudo de viabilidade": {
        "definition": "Fase em que é feita uma estimativa acerca da possibilidade de se satisfazerem as necessidades do usuário identificado usando-se tecnologias atuais de software e hardware.",
        "source": "Slide"
    },

    "elicitação e análise de requisitos": {
        "definition": "É o processo de derivação dos requisitos do sistema por meio da observação dos sistemas existentes, além de discussões com os potenciais usuários.",
        "source": "Slide"
    },

    "especificação de requisitos": {
        "definition": "É a atividade de traduzir as informações obtidas durante a atividade de análise em um documento que defina um conjunto de requisitos.",
        "source": "Slide"
    },

    "validação de requisitos": {
        "definition": "Atividade que verifica os requisitos quanto a realismo, consistência e completude.",
        "source": "Slide"
    },

    "projeto de arquitetura": {
        "definition": "Projeto no qual deve-se identificar a estrutura geral do sistema, os componentes principais seus relacionamentos e como eles são distribuídos.",
        "source": "Slide"
    },

    "projeto de interface": {
        "definition": "Etapa no qual você define as interfaces entre os componentes do sistema.",
        "source": "Slide"
    },

    "projeto de componente": {
        "definition": "Projeto no qual você toma cada componente do sistema e projeta seu funcionamento.",
        "source": "Slide"
    },

    "projeto de banco de dados": {
        "definition": "Projeto no qual você projeta as estruturas de dados do sistema e como eles devem ser representados em um banco de dados.",
        "source": "Slide"
    },

    "testes de componente": {
        "definition": "Os componentes do sistema são testados pelas pessoas que o desenvolveram",
        "source": "Slide"
    },

    "testes de sistema": {
        "definition": "Componentes do sistema são integrados para criar um sistema completo.",
        "source": "Slide"
    },

    "testes de aceitação": {
        "definition": "Esse é o estágio final do processo de testes, antes que o sistema seja aceito para uso operacional.",
        "source": "Slide"
    },

    "": {
        "definition": "",
        "source": ""
    }
}

show_strings(Object.keys(definitions))

function levenshtein(a, b) {
    // Source: https://gist.github.com/andrei-m/982927

    /**
     * Copyright (c) 2011 Andrei Mackenzie
     * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
     * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
     * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    **/

    if (a.length == 0) return b.length;
    if (b.length == 0) return a.length;

    var matrix = [];

    // Increment along the first column of each row.
    var i;
    for (i = 0; i <= b.length; i++) {
        matrix[i] = [i];
    }

    // Increment each column in the first row.
    var j;
    for (j = 0; j <= a.length; j++) {
        matrix[0][j] = j;
    }

    // Fill in the rest of the matrix.
    for (i = 1; i <= b.length; i++) {
        for (j = 1; j <= a.length; j++) {
            if (b.charAt(i - 1) == a.charAt(j - 1)) {
                matrix[i][j] = matrix[i - 1][j - 1];
            } else {
                matrix[i][j] = Math.min(
                    matrix[i - 1][j - 1] + 1, // Substitution
                    Math.min(
                        matrix[i][j - 1] + 1, // Insertion
                        matrix[i - 1][j] + 1 // Deletion
                    )
                );
            }
        }
    }

    return matrix[b.length][a.length];
};

function search_definition(string_to_search) {
    let possibilities = { }

    for (const [key, value] of Object.entries(definitions)) {
        dist = Number(levenshtein(key, string_to_search))

        if (dist <= 5) {
            return value["definition"]
        } else if (dist <= 35) {
            possibilities[key] = dist
        }
    }

    let possible_strings = Object.keys(possibilities);

    possible_strings.sort(function(a, b) { return possibilities[a] - possibilities[b] });

    return possible_strings
}

function show_strings(list_of_strings) {
    clear_node(result_node)

    let lst = document.createElement("ul")

    list_of_strings.forEach(string => {
        let nn = document.createElement("li")
        nn.textContent = string
        nn.onclick = function () {
            input_node.value = string
            input_node.dispatchEvent(new KeyboardEvent('keyup', { 'key': 'enter' }))
        }

        lst.appendChild(nn)
    });

    result_node.appendChild(lst)
}

function clear_node(node) {
    while (node.firstChild) {
        node.removeChild(node.firstChild);
    }
}

input_node.addEventListener("keyup", function (event) {
    footer_node.style.removeProperty("position")
    footer_node.style.removeProperty("bottom")
    footer_node.style.removeProperty("width")

    string_to_search = input_node.value

    if (string_to_search === "") {
        show_strings(Object.keys(definitions))
        return;
    }

    result = search_definition(string_to_search.toLowerCase())

    if (Array.isArray(result)) {
        if (result.length === 0) {
            clear_node(result_node)
        } else {
            show_strings(result)
            return
        }
    } else {
        clear_node(result_node)
        result_node.textContent = result

        footer_node.style.position = "fixed"
        footer_node.style.bottom = 0
        footer_node.style.width = "100%"
    }
})
