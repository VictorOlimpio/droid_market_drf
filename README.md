# DROID-MARKET-API

Esta API é destinada a realização de cotação de peças específicas de droids, atendendo asssim, as necessidades da Federação de Comércio.

## ARQUITETURA

Como foi definido pela Federação de Comercio, existem 3 entidades definidas na API: 

* User
* Piece
* Demand

Um Usuário além de ser responsável pela autenticação na API, possui as seguintes informações:

* nome
* telefone
* email

Por padrão, se um tipo não for definido ao Usuário, ele será criado como do tipo Anunciante. Um Usuário pode possuir muitas Demandas.

Uma Peça é definida da seguinte forma:

* tipo
* descrição
* valor

Uma Peça pode possuir muitas Demandas.

Uma Demanda possui as seguintes informações:

* rua
* bairro
* cidade
* uf
* numero
* cep
* situação (Aberta, Finalizada)

Os campos (rua, bairro, cidade, uf, numero, cep, complemento) formam a informação de endereço de entrega. A descrição da Peça é obtida através da relação de Demanda com peça, bem como as informações de contato do Usuário. Dessa forma uma Demanda pertence à um Usuário e à uma Peça.

## CONFIGURAÇÃO

A API foi desenvolvida em Django com o framework Django Rest Framework. O banco de dados utilizado é o MySQL.

A API atende aos padrões do JSON API, implementa autenticação, o padrão cliente-servidor, possui paginação e possibilita cacheamento, atendendo as CONSTRAINTS de APIs RESTFUL.

A aplicação será executada em um container Docker. Os arquivos Dockerfile e doker-compose encontram-se dentro da pasta doker-rails.

Para preparar o ambiente, execute os comandos a seguir:

```
docker-compose build
docker-compose up
```

## EXECUTANDO

Com a API executando, é possível realizar as requisições necessárias para a aplicação.
Os endpoints foram gerados e exportados em uma Collection Postman (https://www.getpostman.com/). Os endpoints se encontram dentro da pasta postman. Em seguida importe os endpoints no Postman.

Vale lembrar que os endpoints estão nomeados para melhor compreensão do que realizam.

Primeiramente é necessário se cadastrar utilizando a requisição registration.

Em seguida para se autenticar na API é necessário utilizar s requisição login.

A API utiliza autenticação via token, todas as demais requisições necessitam de autenticação, envie no header da requisição no campo Authorization o access token que é retornado na requisição login.

Todas as requisições para GET, POST, PATCH, DELETE das entidades da API estão listadas na collection do Postman.

