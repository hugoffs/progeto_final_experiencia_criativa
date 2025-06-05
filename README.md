# Componentes da equipe

Angelo Andrioli Netho
\
Eduardo Mendes Carbonera
\
Hugo Fagundes Faria Santos
\
Kaio Gonçalves Teles

# Aplicação deste repositório

Desenvolvido como parte de nosso trabalho de Extensão e disciplina de Experiência Criativa, este repositório apresenta a concepção e a solução para combater a ineficiência na irrigação dos campos agrícolas da universidade. Nosso objetivo é automatizar a irrigação, substituindo o processo manual pela utilização de irrigadores já instalados (e subutilizados) e integrando-os a sistemas de IoT para um gerenciamento de água mais preciso e sustentável.

# Estrutura de Pastas e Organização do Programa

controllers: Esta pasta é destinada a conter todos os arquivos que gerenciam a lógica de controle principal e dos sensores/atuadores. Isso inclui módulos como login, sensores, atuadores, entre outros.

models: Dedicada à organização e representação dos dados, como informações de sensores, atuadores e usuários.

static: Armazena todos os arquivos estáticos utilizados nas páginas, como CSS, JavaScript, imagens e fontes.

utils: Contém os módulos responsáveis por funcionalidades auxiliares, como a conexão com o banco de dados e outras utilidades gerais do sistema.

views: Onde se encontram todos os arquivos HTML, que correspondem às interfaces do usuário.

O arquivo principal da aplicação é o app.py. Ele será responsável por importar o appcontroller.py (localizado na pasta controllers), que gerencia o fluxo principal do programa. No futuro, as classes referentes aos sensores e atuadores deverão ser importadas para seus respectivos controladores.

# Cronograma
- [x] Inclusão do Banco de Dados
- [ ] Conclusão da estilização através de CSS
- [ ] Conclusão do esqueleto través de HTML
- [ ] Conclusão das funcionalidades através de Javascript
