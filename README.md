# Desafio Back End - APIs REST

## Descrição do Desafio

O desafio consiste em criar três APIs REST para a empresa Khanto. As APIs serão responsáveis por gerenciar três entidades: Imóveis, Anúncios e Reservas. 

### Tecnologias Utilizadas

- Python
- Django e Django Rest Framework
- Banco de dados SQL

### Contexto

A empresa Khanto está desenvolvendo um novo sistema e precisa criar um banco de dados com as seguintes entidades:

1. Imóveis: Representa os imóveis disponíveis para locação. Cada imóvel possui um código, limite de hóspedes, quantidade de banheiros, se aceita animais de estimação, valor de limpeza, data de ativação e data e horário de criação/atualização.

2. Anúncios: Representa os anúncios dos imóveis publicados em plataformas como Airbnb, Booking.com e Skyscanner. Cada anúncio está associado a um único imóvel e possui informações como plataforma, taxa da plataforma, data e horário de criação/atualização.

3. Reservas: Representa as reservas feitas pelos usuários para os imóveis anunciados. Cada reserva possui um código, data de check-in, data de check-out, preço total, comentário, número de hóspedes e data e horário de criação/atualização. Uma reserva está associada a um único anúncio.

### Requisitos

API 1 - Imóveis:
- [x] Buscar uma lista de imóveis
- [x] Buscar um imóvel individual
- [x] Criar um imóvel
- [x] Alterar um imóvel
- [x] Deletar um imóvel
- [x] Criar uma fixture (seeder) com pelo menos 5 imóveis

API 2 - Anúncios:
- [x] Buscar uma lista de anúncios
- [x] Buscar um anúncio individual
- [x] Criar um anúncio
- [x] Alterar um anúncio
- [ ] Apagar um anúncio (não implementado)
- [x] Criar uma fixture (seeder) com pelo menos 3 anúncios

API 3 - Reservas:
- [x] Buscar uma lista de reservas
- [x] Buscar uma reserva individual
- [x] Criar uma reserva
- [x] Deletar uma reserva
- [ ] Alterar uma reserva (não implementado)
- [x] Validar que não é possível criar uma reserva com data de check-in posterior à data de check-out
- [x] Criar uma fixture (seeder) com pelo menos 8 reservas

### Observações importantes

- A qualidade do Readme e a organização do repositório serão avaliadas.
- Todos os campos de cada tabela devem aparecer em cada API de busca.
- Para fazer uma busca individual, é necessário passar um parâmetro na URL contendo o ID da entidade. Caso o parâmetro não seja passado, a lista completa será retornada.
- As tabelas e códigos relacionados ao banco de dados devem ser construídos utilizando o ORM nativo do Django.
- Devem ser criados testes unitários relevantes.

## Modelos de Dados

### Imóveis

O modelo de dados para a entidade Imóveis é representado pela classe `Property`:

```python
class AvailableManager(models.Manager):
    """Classe de gerenciamento de modelos.
    
    Neste projeto, está sendo utilizada para retornar nas consultas apenas
    objetos com a condição is_available=True, o que facilita o manuseio de
    Imóveis 'disponíveis' ou em 'operação' no gerenciamento de dados."""
    def get_queryset(self):
        return super().get_queryset().filter(is_available=True)

class Property(TimeStampedModel):
    property_code = models.CharField(max_length=30, unique=True)
    guest_limit = models.PositiveIntegerField()
    number_of_bathrooms = models.PositiveIntegerField()
    accepts_animals = models.BooleanField()
    cleaning_fee = models.DecimalField(max_digits=6, decimal_places=2)
    activation_date = models.DateField()
    is_available = models.BooleanField(default=True)
    
    objects = models.Manager()
    available = AvailableManager()
    
    class Meta():
        verbose_name = 'Imóvel'
        verbose_name_plural = 'Imóveis'
```

### Anúncios

O modelo de dados para a entidade Anúncios é representado pela classe `Advertisement`:

```python
from model_utils.models import TimeStampedModel
from django.db import models

PLATFORMS = (('Ab', 'AirBnb'), ('Bk', 'Booking.com'), ('Ss', 'Skyscanner'))

class Advertisement(TimeStampedModel):
    platform = models.CharField(max_length=100, choices=PLATFORMS)
    platform_fee = models.DecimalField(max_digits=8, decimal_places=2)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    
    class Meta():
        ordering = ('platform',)
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        
    def __str__(self):
        return self.platform
```

### Reservas

O modelo de dados para a entidade Reservas é representado pela classe `Reservation`:

```python
from model_utils.models import TimeStampedModel
from django.db import models
from django.core.exceptions import ValidationError

class Reservation(TimeStampedModel):
    reservation_code = models.CharField(max_length=100, unique=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    comment = models.TextField(blank=True)
    guest_count = models.PositiveIntegerField()
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE)
    
    class Meta():
        verbose_name = 'Reserva'

    def clean(self):
        if self.check_in_date >= self.check_out_date:
            raise ValidationError("A data de check-in deve ser anterior à data de check-out")
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
```

### Informações adicionais
- Classe de modelo utilizada: `TimeStampedModel` É uma classe que fornece e atualiza os campos `created_at` e `updated_at` - requisitos do projeto - sem a necessidade de lidar diretamente com estas funcionalidades.
- A classe `AvailableManager` gerencia os objetos do modelo `Property` que estão disponíveis, filtrando apenas aqueles com a propriedade `is_available=True`.
- A variável `objects` é o gerenciador padrão do Django para o modelo `Property`, enquanto a variável `available` é um gerenciador personalizado que permite acessar apenas os imóveis disponíveis.
- A classe `Meta` define os nomes que serão exibidos para o modelo, "Imóvel" no singular e "Imóveis" no plural. Essas definições melhoram a legibilidade e usabilidade do sistema.
- A definição das variáveis `verbose_name` e `verbose_name_plural` nas classes `Meta` dos modelos é uma forma de especificar como o nome do modelo deve ser exibido em interfaces e mensagens.
- A função `clean` da classe `Reservation` valida se a data de check-in é anterior à data de check-out. Se a validação falhar, é lançada uma exceção `ValidationError`. A função `save` chama `clean` antes de salvar os dados, garantindo a integridade das reservas no sistema.

## APIs
Neste projeto, as três APIs (Imóveis, Anúncios e Reservas) foram agrupadas em um único aplicativo Django. Essa escolha traz vantagens específicas para projetos de menor escala, priorizando a simplicidade e agilidade. Porém, em projetos maiores e mais complexos, é recomendável separar as APIs em aplicativos individuais, visando a escalabilidade, modularidade e organização do sistema.
### Classe `PropertyRetrieveAPIView`
É uma modificação da classe `RetrieveAPIView` e tem a função de buscar um imóvel específico pelo seu ID. Ela permite a busca apenas de imóveis disponíveis para visualização na API.

Essa peculiaridade é alcançada através das seguintes modificações:

1. Método `get_queryset()`:
   - Retorna apenas os imóveis disponíveis utilizando o gerenciador de modelos `Property.available.all()`.
   
2. Método `retrieve()`:
   - Verifica se o imóvel buscado está disponível.
   - Retorna os dados do imóvel caso esteja disponível.
   - Caso o imóvel não esteja disponível, retorna uma mensagem informando que as informações do imóvel estão indisponíveis no momento.

## Executando o Projeto

Siga as instruções abaixo para executar o projeto:

1. Clone o repositório do projeto:

```shell
git clone https://github.com/gssartori/khanto-api.git
```

2. Navegue até o diretório do projeto:

```shell
cd khanto_project
```

3. Instale as dependências:

```shell
pip install -r requirements.txt
```

4. Execute as migrations para criar as tabelas no banco de dados:

```shell
python manage.py migrate
```

5. Execute a fixture (seeder) para popular o banco de dados com dados iniciais:

```shell
python manage.py loaddata fixtures/new-ads.json
python manage.py loaddata fixtures/new-properties.json
python manage.py loaddata fixtures/new-reservations.json
```

6. Inicie o servidor:

```shell
python manage.py runserver
```

7. Acesse as APIs através das seguintes URLs:

- Imóveis: `http://localhost:8000/imoveis/`
- Anúncios: `http://localhost:8000/anuncios/`
- Reservas: `http://localhost:8000/reservas/`

## Testes

A implementação de testes unitários relevantes infelizmente ainda não foi iniciada. No entanto, alguns exemplos de testes básicos e relevantes podem ser aplicados são:

1. Testes de busca:
   - Verificar se é possível buscar uma lista de entidades (imóveis, anúncios, reservas).
   - Verificar se os campos esperados estão presentes em cada entidade retornada.
   - Verificar se a busca por uma entidade individual retorna os detalhes corretos quando fornecido o ID.

2. Testes de criação:
   - Enviar uma requisição para criar uma nova entidade (imóvel, anúncio, reserva) e verificar se a resposta é bem-sucedida.
   - Verificar se a entidade é adicionada corretamente ao banco de dados.

3. Testes de atualização:
   - Enviar uma requisição para alterar os detalhes de uma entidade existente e verificar se a resposta é bem-sucedida.
   - Verificar se as alterações são refletidas corretamente no banco de dados.

4. Testes de exclusão:
   - Enviar uma requisição para deletar uma entidade existente e verificar se a resposta é bem-sucedida.
   - Verificar se a entidade é removida corretamente do banco de dados.

## Autor: Gabriel Sartori
