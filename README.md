# Sistema de Calendário

Este projeto é um sistema de calendário desenvolvido em Django, que permite gerenciar eventos com funcionalidades de CRUD (Criar, Ler, Atualizar e Deletar). O sistema é ideal para controle de tarefas e eventos, com funcionalidades específicas para administradores e usuários comuns.

## Funcionalidades

- **Cadastro de Usuários**: Permite o registro de novos usuários.
- **Calendário**: Exibição de eventos com cores diferenciadas conforme o status (pendente, concluído, atrasado e próximo ( 3 dias úteis) ).
- **Calendário Pessoal**: Exibição apenas dos eventos relacionados ao usuário logado.
- **Detalhes do Evento**: Visualização detalhada dos eventos.
- **Adicionar Novo Evento**: Permite a criação de novos eventos.
- **Editar Evento**: Possibilita a edição de eventos existentes.
- **Adicionar observação**: Adicina uma observação no evento que é destacada com tooltip.
- **Concluir Evento**: Marca um evento como concluído.
- **Excluir Evento**: Remove um evento do calendário.

## Instalação

1. **Clone o Repositório**

    ```bash
    git clone https://github.com/seu_usuario/sistemaCalendario.git
    ```

2. **Instale as Dependências**

    Navegue até o diretório do projeto e instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure o Banco de Dados**

    Execute as migrações para configurar o banco de dados:

    ```bash
    python manage.py migrate
    ```

4. **Crie um Superusuário**

    Para acessar o painel de administração, crie um superusuário:

    ```bash
    python manage.py createsuperuser
    ```

5. **Inicie o Servidor**

    Execute o servidor de desenvolvimento:

    ```bash
    python manage.py runserver
    ```


### CalendarioEvento

- **titulo**: Título do evento.
- **descricao**: Descrição do evento.
- **data_limite**: Data limite do evento.
- **responsavelEvento**: Usuário responsável pelo evento.
- **concluido**: Status de conclusão do evento.
- **dataConclusao**: Data em que o evento foi concluído.
- **observacao**: Observações adicionais sobre o evento.
- **recorrencia**: Tipo de recorrência do evento.

## Visão Geral das Views

- **register**: Página de registro de novos usuários.
- **calendario**: Exibe o calendário com eventos.
- **calendario_detalhes**: Exibe os detalhes de um evento específico.
- **CalenadarioNovo_evento**: Permite adicionar um novo evento.
- **CalendarioEdit**: Permite editar um evento existente.
- **CalendarioConcluido**: Marca um evento como concluído.
- **CalendarioDelete**: Exclui um evento.

## Dependências

- Django
- workalendar
- python-dateutil

---

Desenvolvido por [Pedro Ferraiuoli](https://github.com/pedroferraiuoli).
