# Guia de Contribuição

Obrigado por considerar contribuir para o AI Code Assistant! Este documento fornece diretrizes para contribuições.

## Como Contribuir

### Reportando Bugs

Se você encontrou um bug, por favor crie uma issue com:

1. Título descritivo e claro
2. Descrição detalhada do problema
3. Passos para reproduzir
4. Comportamento esperado vs. atual
5. Screenshots (se aplicável)
6. Informações do ambiente (OS, versões, etc.)

### Sugerindo Features

Para sugerir uma nova funcionalidade:

1. Verifique se já não existe uma issue similar
2. Crie uma nova issue com label "enhancement"
3. Descreva claramente a funcionalidade
4. Explique por que seria útil
5. Forneça exemplos de uso

### Pull Requests

1. **Fork o repositório**
   ```bash
   git clone https://github.com/seu-usuario/ai-code-assistant.git
   ```

2. **Crie uma branch**
   ```bash
   git checkout -b feature/MinhaNovaFuncionalidade
   ```

3. **Faça suas alterações**
   - Siga os padrões de código do projeto
   - Adicione testes para novas funcionalidades
   - Atualize a documentação

4. **Execute os testes**
   ```bash
   # Backend
   cd backend
   pytest --cov=app

   # Frontend
   cd frontend
   npm test
   ```

5. **Commit suas mudanças**
   ```bash
   git commit -m "feat: adiciona nova funcionalidade X"
   ```

   Use commits semânticos:
   - `feat:` - Nova funcionalidade
   - `fix:` - Correção de bug
   - `docs:` - Documentação
   - `style:` - Formatação
   - `refactor:` - Refatoração
   - `test:` - Testes
   - `chore:` - Manutenção

6. **Push para seu fork**
   ```bash
   git push origin feature/MinhaNovaFuncionalidade
   ```

7. **Abra um Pull Request**
   - Título descritivo
   - Descrição detalhada das mudanças
   - Referencie issues relacionadas
   - Adicione screenshots se aplicável

## Padrões de Código

### Python (Backend)

- Siga a PEP 8
- Use type hints
- Docstrings em todas as funções
- Máximo de 88 caracteres por linha (Black)
- Use f-strings para formatação

Exemplo:
```python
def calculate_sum(numbers: list[int]) -> int:
    """
    Calculate the sum of a list of numbers.

    Args:
        numbers: List of integers to sum

    Returns:
        The sum of all numbers
    """
    return sum(numbers)
```

### TypeScript (Frontend)

- Use TypeScript estrito
- Componentes funcionais com hooks
- Props tipadas com interfaces
- CSS modules ou styled-components
- Nomes descritivos

Exemplo:
```typescript
interface ButtonProps {
  label: string;
  onClick: () => void;
  disabled?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  label,
  onClick,
  disabled = false
}) => {
  return (
    <button onClick={onClick} disabled={disabled}>
      {label}
    </button>
  );
};
```

## Testes

### Backend

- Use pytest
- Cobertura mínima de 80%
- Testes unitários e de integração
- Mock de chamadas externas (OpenAI)

```python
def test_generate_code_success(mock_openai):
    """Test successful code generation."""
    mock_openai.return_value = {"code": "print('hello')"}
    result = generate_code("print hello")
    assert result["success"] is True
```

### Frontend

- Use Vitest e Testing Library
- Testes de componentes
- Testes de hooks
- Testes de integração

```typescript
describe('CodeEditor', () => {
  it('renders correctly', () => {
    render(<CodeEditor value="" onChange={() => {}} />);
    expect(screen.getByPlaceholderText(/Enter your code/)).toBeInTheDocument();
  });
});
```

## Estrutura de Commits

Use commits semânticos:

```
<type>(<scope>): <subject>

<body>

<footer>
```

Exemplo:
```
feat(backend): add support for Rust language

- Add Rust to supported languages
- Update schemas and tests
- Add documentation

Closes #123
```

## Code Review

Todos os PRs passarão por code review. Espere:

1. Feedback construtivo
2. Possíveis solicitações de mudanças
3. Aprovação antes do merge

## Configuração do Ambiente

### Requisitos

- Python 3.11+
- Node.js 20+
- Docker e Docker Compose
- Git

### Setup Inicial

1. Clone o repositório
2. Configure as variáveis de ambiente
3. Instale as dependências
4. Execute os testes

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest

# Frontend
cd frontend
npm install
npm test
```

## Ferramentas Recomendadas

### IDE/Editor

- VSCode com extensões:
  - Python
  - ESLint
  - Prettier
  - Docker

### Linters

```bash
# Backend
black backend/
flake8 backend/
mypy backend/

# Frontend
npm run lint
npm run format
```

## Versionamento

Seguimos [Semantic Versioning](https://semver.org/):

- MAJOR: Mudanças incompatíveis
- MINOR: Novas funcionalidades compatíveis
- PATCH: Correções de bugs

## Processo de Release

1. Atualizar versão em:
   - `backend/app/core/config.py`
   - `frontend/package.json`
   - `README.md`

2. Atualizar CHANGELOG.md

3. Criar tag de versão:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

## Comunicação

- Issues: Para bugs e features
- Discussions: Para perguntas e ideias
- Pull Requests: Para código

## Código de Conduta

### Nossa Promessa

- Ambiente acolhedor e inclusivo
- Respeito a diferentes pontos de vista
- Feedback construtivo
- Foco no que é melhor para a comunidade

### Comportamentos Esperados

- Linguagem acolhedora e inclusiva
- Respeito por diferentes opiniões
- Críticas construtivas
- Foco no que é melhor para o projeto

### Comportamentos Inaceitáveis

- Assédio ou discriminação
- Linguagem ofensiva
- Ataques pessoais ou políticos
- Publicação de informações privadas

## Dúvidas?

Sinta-se à vontade para:

- Abrir uma issue com a tag "question"
- Iniciar uma discussion
- Entrar em contato com os mantenedores

## Reconhecimento

Todos os contribuidores serão listados no README.md e terão nosso reconhecimento!

Obrigado por contribuir! 🎉
