# API Documentation

API completa do AI Code Assistant.

## Base URL

```
http://localhost:8000/api/v1
```

## Autenticação

Atualmente a API não requer autenticação. Em versões futuras, será implementado um sistema de autenticação baseado em tokens JWT.

## Endpoints

### 1. Health Check

Verifica se a API está funcionando corretamente.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "service": "AI Code Assistant"
}
```

**Status Codes:**
- `200 OK` - Serviço funcionando

---

### 2. Geração de Código

Gera código a partir de uma descrição em linguagem natural.

**Endpoint:** `POST /generate`

**Request Body:**
```json
{
  "prompt": "Crie uma função para calcular números de Fibonacci",
  "language": "python",
  "context": "Use recursão com memoização para otimização"
}
```

**Parameters:**
- `prompt` (string, required) - Descrição do código desejado
- `language` (string, optional) - Linguagem de programação (default: "python")
- `context` (string, optional) - Contexto adicional

**Response:**
```json
{
  "success": true,
  "code": "def fibonacci(n, memo={}):\n    if n in memo:\n        return memo[n]\n    if n <= 1:\n        return n\n    memo[n] = fibonacci(n-1, memo) + fibonacci(n-2, memo)\n    return memo[n]",
  "explanation": "Generated a fibonacci function with memoization for optimization",
  "language": "python"
}
```

**Status Codes:**
- `200 OK` - Código gerado com sucesso
- `422 Unprocessable Entity` - Parâmetros inválidos
- `500 Internal Server Error` - Erro na geração

---

### 3. Explicação de Código

Explica o que um código faz de forma detalhada.

**Endpoint:** `POST /explain`

**Request Body:**
```json
{
  "code": "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)",
  "language": "python"
}
```

**Parameters:**
- `code` (string, required) - Código para explicar
- `language` (string, optional) - Linguagem de programação (default: "python")

**Response:**
```json
{
  "success": true,
  "code": "def quicksort(arr):\n    ...",
  "explanation": "This is an implementation of the QuickSort algorithm...\n\n1. Overall purpose: Sorts an array efficiently using divide-and-conquer\n2. Key components:\n   - Base case: Returns array if length <= 1\n   - Pivot selection: Uses middle element\n   - Partitioning: Divides into left, middle, right\n3. Flow: Recursively sorts left and right partitions\n4. Time complexity: O(n log n) average case",
  "language": "python"
}
```

**Status Codes:**
- `200 OK` - Explicação gerada com sucesso
- `422 Unprocessable Entity` - Parâmetros inválidos
- `500 Internal Server Error` - Erro na explicação

---

### 4. Detecção de Bugs

Analisa código em busca de bugs, vulnerabilidades e problemas.

**Endpoint:** `POST /detect-bugs`

**Request Body:**
```json
{
  "code": "def divide(a, b):\n    return a / b",
  "language": "python"
}
```

**Parameters:**
- `code` (string, required) - Código para analisar
- `language` (string, optional) - Linguagem de programação (default: "python")

**Response:**
```json
{
  "success": true,
  "code": "def divide(a, b):\n    return a / b",
  "explanation": "Found 2 potential issue(s)",
  "bugs": [
    {
      "line": 2,
      "severity": "high",
      "description": "Division by zero error - no check for b == 0",
      "suggestion": "Add validation: if b == 0: raise ValueError('Cannot divide by zero')"
    },
    {
      "line": 1,
      "severity": "medium",
      "description": "Missing type hints",
      "suggestion": "Add type hints: def divide(a: float, b: float) -> float:"
    }
  ],
  "language": "python"
}
```

**Bug Object:**
- `line` (integer|null) - Número da linha do bug
- `severity` (string) - Gravidade: "critical", "high", "medium", "low", "info"
- `description` (string) - Descrição do problema
- `suggestion` (string) - Sugestão de correção

**Status Codes:**
- `200 OK` - Análise concluída
- `422 Unprocessable Entity` - Parâmetros inválidos
- `500 Internal Server Error` - Erro na análise

---

### 5. Refatoração de Código

Refatora código para melhorar qualidade e manutenibilidade.

**Endpoint:** `POST /refactor`

**Request Body:**
```json
{
  "code": "def calc(x, y, z):\n    a = x + y\n    b = a * z\n    c = b / 2\n    return c",
  "language": "python",
  "instructions": "Use nomes descritivos e adicione documentação"
}
```

**Parameters:**
- `code` (string, required) - Código para refatorar
- `language` (string, optional) - Linguagem de programação (default: "python")
- `instructions` (string, optional) - Instruções específicas de refatoração

**Response:**
```json
{
  "success": true,
  "code": "def calculate_weighted_average(base_value: float, addend: float, multiplier: float) -> float:\n    \"\"\"\n    Calculate the weighted average of two values.\n    \n    Args:\n        base_value: The first value\n        addend: Value to add to base\n        multiplier: Weight multiplier\n        \n    Returns:\n        The weighted average result\n    \"\"\"\n    sum_values = base_value + addend\n    weighted_sum = sum_values * multiplier\n    average = weighted_sum / 2\n    return average",
  "explanation": "Code has been refactored to improve quality, readability, and maintainability.",
  "language": "python"
}
```

**Status Codes:**
- `200 OK` - Refatoração concluída
- `422 Unprocessable Entity` - Parâmetros inválidos
- `500 Internal Server Error` - Erro na refatoração

---

### 6. Documentação Automática

Adiciona documentação completa ao código.

**Endpoint:** `POST /document`

**Request Body:**
```json
{
  "code": "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1",
  "language": "python",
  "style": "google"
}
```

**Parameters:**
- `code` (string, required) - Código para documentar
- `language` (string, optional) - Linguagem de programação (default: "python")
- `style` (string, optional) - Estilo de documentação: "google", "numpy", "sphinx" (default: "google")

**Response:**
```json
{
  "success": true,
  "code": "def binary_search(arr: list, target: any) -> int:\n    \"\"\"\n    Perform binary search on a sorted array.\n    \n    Args:\n        arr (list): Sorted array to search in\n        target (any): Value to find\n        \n    Returns:\n        int: Index of target if found, -1 otherwise\n        \n    Example:\n        >>> binary_search([1, 2, 3, 4, 5], 3)\n        2\n        >>> binary_search([1, 2, 3, 4, 5], 6)\n        -1\n    \"\"\"\n    left, right = 0, len(arr) - 1\n    \n    while left <= right:\n        # Calculate middle index\n        mid = (left + right) // 2\n        \n        if arr[mid] == target:\n            return mid  # Target found\n        elif arr[mid] < target:\n            left = mid + 1  # Search right half\n        else:\n            right = mid - 1  # Search left half\n    \n    return -1  # Target not found",
  "explanation": "Documentation added using google style",
  "language": "python"
}
```

**Status Codes:**
- `200 OK` - Documentação adicionada
- `422 Unprocessable Entity` - Parâmetros inválidos
- `500 Internal Server Error` - Erro na documentação

---

## Linguagens Suportadas

A API suporta as seguintes linguagens de programação:

- Python
- JavaScript
- TypeScript
- Java
- Go
- Rust
- C++
- C#
- Ruby
- PHP
- Swift
- Kotlin
- E outras...

## Rate Limiting

Atualmente não há limite de requisições. Em produção, será implementado rate limiting para proteger a API.

## Error Handling

Todos os endpoints retornam erros no seguinte formato:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common Error Codes

- `400 Bad Request` - Requisição malformada
- `422 Unprocessable Entity` - Validação de parâmetros falhou
- `500 Internal Server Error` - Erro interno do servidor
- `503 Service Unavailable` - Serviço temporariamente indisponível

## Examples

### Exemplo com cURL

```bash
# Gerar código
curl -X POST http://localhost:8000/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a REST API endpoint",
    "language": "python"
  }'

# Detectar bugs
curl -X POST http://localhost:8000/api/v1/detect-bugs \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def unsafe_function(x): return eval(x)",
    "language": "python"
  }'
```

### Exemplo com Python

```python
import requests

API_URL = "http://localhost:8000/api/v1"

# Gerar código
response = requests.post(f"{API_URL}/generate", json={
    "prompt": "Create a function to validate email",
    "language": "python"
})
print(response.json())

# Explicar código
response = requests.post(f"{API_URL}/explain", json={
    "code": "lambda x: x**2",
    "language": "python"
})
print(response.json())
```

### Exemplo com JavaScript

```javascript
const API_URL = 'http://localhost:8000/api/v1';

// Detectar bugs
fetch(`${API_URL}/detect-bugs`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: 'function test() { var x = null; return x.value; }',
    language: 'javascript'
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## Interactive Documentation

A API possui documentação interativa Swagger disponível em:

```
http://localhost:8000/api/v1/docs
```

Você pode testar todos os endpoints diretamente no navegador.
