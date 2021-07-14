# Bem vindo ao meu teste

Olá, meu nome é Hítallo William e esse é o meu projeto. Meu email pessoal é hitallo91@gmail.com

## Documentação da API

Para acessar a documentação clique [aqui](https://app.swaggerhub.com/apis/hitallow/crud-users/1.0)

A documentação foi feita utilizando o swagger

## Tecnologias utilizadas
  Para o desenvolvimento dessa aplicação foram usadas as seguintes tecnlogias:
  - Python
  - SQlite
  - SQLAlchemy
  - Flask

## Arquitetura
  Para o desenvolvimento foi utilizado uma arquitetura baseada no Hexagonal(ports and adapter).
  Utilizando a inversão de dependências para desaclopar o código principal da aplicação.
  No `core` da aplicação há apenas código python puro, tornando a aplicação maleável e independente de tecnologia ou framework.
  Os modulos são separados da seguinte maneira
  - domain: Entidades do core da aplicação
  - ports: Portas(ou adapters) cujos quais são responsáveis por conectar o código ao mundo externo, nessa pasta há apenas contratos de implementação.
  - usecase: Fluxo principal da aplicação, local onde há de fato a lógica de negócio da aplicação. Faz uso das portas para executar a lógica.

# Testes

Foi utilizado os testes providos pelo própio python, fazendo uso do pacote `unittest`.
#### Para rodar os teste, execute em seu terminal
```
  $ python -m unittest discover -s app/testing/ -p '*_test.py'
```
#### Cobertura de código
Cobertura de código gerado com [Coverage.py](https://coverage.readthedocs.io/en/coverage-5.5/). 
```
Name                                                     Stmts   Miss  Cover
----------------------------------------------------------------------------
app/__init__.py                                              5      2    60%
app/core/__init__.py                                         0      0   100%
app/core/domain/__init__.py                                  0      0   100%
app/core/domain/user.py                                     54      6    89%
app/core/ports/__init__.py                                   0      0   100%
app/core/ports/user.py                                      35      9    74%
app/core/usecase/__init__.py                                 0      0   100%
app/core/usecase/user.py                                    87      3    97%
app/database/__init__.py                                     0      0   100%
app/database/config/__init__.py                              0      0   100%
app/database/config/db_base.py                               2      0   100%
app/database/config/db_connection.py                        18      8    56%
app/database/config/init_database.py                         7      7     0%
app/database/repositories/__init__.py                        0      0   100%
app/database/repositories/user_repository.py                66     54    18%
app/database/tables/__init__.py                              0      0   100%
app/database/tables/user.py                                 17      2    88%
app/modules/__init__.py                                      0      0   100%
app/modules/users/__init__.py                               17      7    59%
app/modules/users/controllers/__init__.py                    0      0   100%
app/modules/users/controllers/get_user_profile.py           11      6    45%
app/modules/users/controllers/list_all_users.py             13      8    38%
app/modules/users/controllers/list_user_by_email.py         10      6    40%
app/modules/users/controllers/list_user_by_name.py          13      8    38%
app/modules/users/controllers/list_user_by_username.py      10      6    40%
app/modules/users/controllers/register_with_github.py       18     12    33%
app/modules/users/controllers/save_user.py                  18     13    28%
app/modules/users/controllers/update_user.py                 4      2    50%
app/modules/users/services/__init__.py                       0      0   100%
app/modules/users/services/github_api.py                    47     35    26%
app/testing/__init__.py                                      0      0   100%
app/testing/core/__init__.py                                 0      0   100%
app/testing/core/domain/__init__.py                          0      0   100%
app/testing/core/domain/user_test.py                        33      0   100%
app/testing/core/usecase/__init__.py                         0      0   100%
app/testing/core/usecase/user_usercase_test.py             158      0   100%
----------------------------------------------------------------------------
TOTAL                                                      643    194    70%
```
É possível verificar a veracidade instalando o coverage com o comando:
```
pip install coverage 
```
E executando os comandos, então será mostrado em seu terminal o mesmo output mostrado acima
```
  $ coverage run --source app -m unittest discover -s app/testing/ -p '*_test.py' && coverage report
```

## Executar localmente
Caso tenha curiosade e queira executar o código local, você pode sequir um dos dois passos.
Mas primeiro crie um arquivo `.env` com base no `.env.example` e preencha as informações, ao mudar a porta onde a aplicação será servida é preciso ter atenção na hora da execução.

Bem depois de configurado você pode utilizar uma `venv` ou o docker provido por mim.

### Utilizando venv

É preciso ter instalado o pip na sua máquina. Para instalar a virtualenv você pode usar este comando, caso você utilize uma versão diferente é preciso especificar.
```
  $ pip install virtualenv
```
Agora você pode criar sua virtualenv com o comando a seguir.
```
  $ virtualenv <nome_da_sua_venv> 
```
Após criar sua virtualenv ative ela executando.
```
  $ source <nome_da_sua_venv>/bin/activate
```
Utilize o arquivo `requirements.txt` para utilizar as memas dependencias que eu utilizei. Para isto rode:
```
  $ pip install requirements.txt
```
Rode a aplicação executando:
```
  $ python main.py
```

Após executar este comando basta acessar seu localhost na porta que você especificou no arquivo `.env`, mas caso não tenha alterado ou tenha deixado vazio a porta padrão é a porta 8081.


Para desativar a virtualenv utilize:
```
  $ deactivate
```


### Utilizando docker

Tenha o docker instalado na sua máquina.
Builde a imagem com o seguinte comando no meso nível do arquivo Dockerfile:
```
  $ docker build -t test-hitallo-backend-py:latest .
```
Para então executar o container, utilize: (altere a porta 8081 para a porta que você desejar)
```
  $ docker run -d --name test-hitallo-backend-py  -p 8081:8081 test-hitallo-backend-py
```

Levando em conta que nós deixamos a porta do `.env` como 8081 o código deverá funcionar como mágica ✨.

Caso você tenha escolhido uma porta diferente é preciso alterar o mapeamento para onde foi especifidado.
Neste caso siga este comando personalizado:
```
  $ docker run -d --name test-hitallo-backend-py  -p <host_port>:<container_port> test-hitallo-backend-py
```


### Porque utilizar SQlite?

Bem levando em conta a facilidade de lidar com o banco de dados sqlite e não precisar se configurações avançadas me pareceu mais convidativo, não é uma limitação.
