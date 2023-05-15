# MultiBlogs - Plataforma de Blogs Multiusuários!

MultiBlogs é uma plataforma de blogs multiusuários desenvolvida em Django, que permite que vários usuários criem e gerenciem seus próprios blogs. A plataforma também inclui recursos como comentários, categorias, tags e páginas estáticas.

# Requisitos do sistema

Python 3.x

Django 3.x

PostgreSQL (ou outro banco de dados compatível com Django)


# Libs utilizadas

Django 4x

DRF 3x

Bootstrap 5x

Django Lifecycle Hooks
 
Python Decouple 

Django filters

DRF Camel case

Anymail  

Sentry

Django Storages

Django Bdbackup 4x

DRF Yasg

Django Import Export  

Django admin interface

Django TinyMCE 3x


#  Templates utilizados
Temas do **Start Bootstrap:**
https://startbootstrap.com

**Clean Blog**
https://startbootstrap.com/theme/clean-blog

**Tema Resume**
https://startbootstrap.com/theme/resume


# Instalação

Clone este repositório em sua máquina local:
  

    git clone https://github.com/seu-usuario/multiblogs.git
    
Crie um ambiente virtual para isolar as dependências do projeto:  

    python -m venv env

Ative o ambiente virtual:

    source env/bin/activate (no Linux ou macOS)
    env\Scripts\activate (no Windows)

Instale as dependências do projeto:

    pip install -r requirements.txt

Configure as variáveis de ambiente no arquivo .env. Exemplo:

    DEBUG=True
    SECRET_KEY=sua_chave_secreta
    DATABASE_URL=postgres://user:password@localhost/multiblogs

Execute as migrações do banco de dados:

    python manage.py migrate

Crie um superusuário para acessar o painel de administração:

    python manage.py createsuperuser

Execute o servidor de desenvolvimento:

    python manage.py runserver

# Uso
  
Acesse a plataforma no seu navegador em http://localhost:8000/.

Os usuários podem se registrar e criar seus próprios blogs a partir da página inicial. Cada blog criado terá uma URL própria e poderá ser personalizado pelo seu proprietário.  

O painel de administração está disponível em http://localhost:8000/admin/ e permite que o superusuário gerencie os usuários, blogs, posts, comentários, categorias e tags.

# Contribuindo
  
Para contribuir com o projeto, siga as instruções abaixo:
Faça um fork deste repositório e clone-o em sua máquina local.
Crie um branch para suas alterações:

    git checkout -b feature/nova-funcionalidade

Faça suas alterações e teste-as localmente.
Faça commit das suas alterações:

    git commit -m "Adiciona nova funcionalidade"

Faça push das suas alterações para o seu fork:

    git push origin feature/nova-funcionalidade

Crie um pull request para a branch main deste repositório.