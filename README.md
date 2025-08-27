# 🌍 GeoIP ACL Networks Downloader

[![Versão Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://python.org)
[![Licença: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Estilo de Código: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Uma ferramenta Python poderosa que baixa e processa faixas de redes IP para qualquer país a partir de múltiplas fontes GeoIP. Perfeita para regras de firewall, análise de rede, bloqueio geográfico de IP e aplicações de cibersegurança.

## ✨ Funcionalidades

- 🌎 **Suporte Multi-País**: Baixe faixas de IP para qualquer país usando códigos de país de 2 letras
- 🚀 **Downloads Paralelos**: Download simultâneo de múltiplas fontes para processamento mais rápido
- 🔧 **Filtragem Inteligente**: Remove automaticamente sub-redes redundantes e redes sobrepostas
- 📊 **Dual Stack**: Separa redes IPv4 e IPv6 em arquivos diferentes
- 🛡️ **Tratamento Robusto de Erros**: Tratamento abrangente de erros com logging detalhado
- ⚙️ **Altamente Configurável**: URLs personalizadas, timeouts, arquivos de saída e opções de logging
- 📝 **Logging Detalhado**: Rastreamento de progresso e logs detalhados para debug

## 🚀 Início Rápido

```bash
# Baixar redes IP brasileiras
python geoip_acl_downloader.py --acl BR

# Baixar redes BR com logging verbose
python geoip_acl_downloader.py --acl BR --verbose

# Baixar redes BR com nomes de arquivo personalizados
python geoip_acl_downloader.py --acl DE --ipv4 brasil_v4.txt --ipv6 brasil_v6.txt

# Teste simples
python geoip_acl_downloader.py --help
```

## 📋 Requisitos

- Python 3.7+
- Biblioteca `requests`

## 🔧 Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/AlanMartines/geoip-acl-downloader.git
   cd geoip-acl-downloader
   ```

2. **Instale as dependências:**
   ```bash
   pip install requests
   ```
   
   Ou usando um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install requests
   ```

3. **Execute o script:**
   ```bash
   python geoip_acl_downloader.py --acl BR
   ```

## 📖 Uso

### Uso Básico

```bash
python geoip_acl_downloader.py --acl <CODIGO_PAIS>
```

### Argumentos da Linha de Comando

| Argumento | Abrev. | Obrigatório | Descrição | Padrão |
|-----------|--------|-------------|-----------|---------|
| `--acl` | `-a` | ✅ | Código de país de duas letras (ex: BR, US, CN) | - |
| `--ipv4` | - | ❌ | Nome do arquivo para redes IPv4 | `{pais}_ipv4.txt` |
| `--ipv6` | - | ❌ | Nome do arquivo para redes IPv6 | `{pais}_ipv6.txt` |
| `--urls` | - | ❌ | URLs personalizadas para download (separadas por espaço) | Fontes GeoIP padrão |
| `--timeout` | - | ❌ | Timeout da requisição em segundos | `30` |
| `--verbose` | `-v` | ❌ | Habilitar logging verbose | `False` |
| `--log-file` | - | ❌ | Caminho do arquivo de log personalizado | `geoip_acl_downloader.log` |

### Exemplos

#### Exemplos Básicos
```bash
# Baixar redes brasileiras
python geoip_acl_downloader.py --acl BR

# Baixar redes americanas
python geoip_acl_downloader.py --acl US

# Baixar redes chinesas
python geoip_acl_downloader.py --acl CN
```

#### Exemplos Avançados
```bash
# Timeout personalizado e logging verbose
python geoip_acl_downloader.py --acl DE --timeout 60 --verbose

# Nomes de arquivo personalizados
python geoip_acl_downloader.py --acl JP --ipv4 japao_ipv4.txt --ipv6 japao_ipv6.txt

# Fontes GeoIP personalizadas
python geoip_acl_downloader.py --acl FR --urls https://exemplo.com/custom1.acl https://exemplo.com/custom2.acl

# Arquivo de log personalizado
python geoip_acl_downloader.py --acl IN --log-file india_download.log

# Todas as opções combinadas
python geoip_acl_downloader.py --acl RU --ipv4 russia_v4.txt --ipv6 russia_v6.txt --timeout 45 --verbose --log-file russia.log
```

## 🌍 Países Suportados

A ferramenta suporta qualquer país com código ISO de 2 letras. Aqui estão alguns exemplos comuns:

| Código | País | Código | País | Código | País |
|--------|------|--------|------|--------|------|
| 🇧🇷 BR | Brasil | 🇺🇸 US | Estados Unidos | 🇨🇳 CN | China |
| 🇩🇪 DE | Alemanha | 🇫🇷 FR | França | 🇬🇧 UK | Reino Unido |
| 🇯🇵 JP | Japão | 🇮🇳 IN | Índia | 🇷🇺 RU | Rússia |
| 🇨🇦 CA | Canadá | 🇦🇺 AU | Austrália | 🇰🇷 KR | Coreia do Sul |
| 🇮🇹 IT | Itália | 🇪🇸 ES | Espanha | 🇳🇱 NL | Holanda |
| 🇸🇪 SE | Suécia | 🇳🇴 NO | Noruega | 🇨🇭 CH | Suíça |
| 🇦🇷 AR | Argentina | 🇲🇽 MX | México | 🇨🇱 CL | Chile |

> **Nota**: A disponibilidade de redes depende das fontes GeoIP. Alguns países podem ter faixas de IP limitadas ou indisponíveis.

## 📁 Arquivos de Saída

A ferramenta gera dois arquivos por país:

- **`{pais}_ipv4.txt`**: Faixas de rede IPv4 em notação CIDR
- **`{pais}_ipv6.txt`**: Faixas de rede IPv6 em notação CIDR

### Exemplo de Formato de Saída
```
# br_ipv4.txt
177.32.0.0/12
186.192.0.0/12
191.240.0.0/12

# br_ipv6.txt
2001:12f0::/32
2804:0::/16
2804:14c::/32
```

## 🔍 Fontes de Dados

Por padrão, a ferramenta baixa destas fontes GeoIP confiáveis:

1. **MaxMind GeoIP**: `https://geoip.site/download/MaxMind/GeoIP.acl`
2. **IP2Location**: `https://geoip.site/download/IP2Location/GeoIP.acl`
3. **DB-IP**: `https://geoip.site/download/DB-IP/GeoIP.acl`

Você pode especificar fontes personalizadas usando o parâmetro `--urls`.

## 💻 Uso Programático

Você também pode usar a ferramenta como módulo Python:

```python
from geoip_acl_downloader import GeoIPACLDownloader

# Uso básico
downloader = GeoIPACLDownloader('BR')
downloader.process()

# Uso avançado com configurações personalizadas
downloader = GeoIPACLDownloader(
    country_code='US',
    timeout=60,
    urls=['https://exemplo.com/custom.acl']
)
downloader.process('us_ipv4_personalizado.txt', 'us_ipv6_personalizado.txt')
```

## 📊 Performance

- **Downloads Paralelos**: Baixa de múltiplas fontes simultaneamente
- **Filtragem Inteligente**: Remove sub-redes redundantes eficientemente
- **Eficiente em Memória**: Processa grandes conjuntos de dados sem uso excessivo de memória
- **Processamento Rápido**: Tempo típico de 10-30 segundos dependendo da rede e tamanho dos dados

### Exemplo de Métricas de Performance
```
2024-08-27 10:30:15 - INFO - Iniciando GeoIP ACL downloader para país: BR
2024-08-27 10:30:18 - INFO - Total de redes encontradas: 2847 (IPv4: 2654, IPv6: 193) para BR
2024-08-27 10:30:19 - INFO - Filtradas 234 sub-redes redundantes. 2613 redes restantes.
2024-08-27 10:30:19 - INFO - Processamento concluído com sucesso em 4.23 segundos
2024-08-27 10:30:19 - INFO - Resultados finais para BR: 2420 redes IPv4, 193 redes IPv6
```

## 🛠️ Casos de Uso

- **🔥 Regras de Firewall**: Gerar regras de firewall específicas por país
- **🛡️ Bloqueio Geográfico**: Bloquear ou permitir tráfego de países específicos
- **📊 Análise de Rede**: Analisar distribuição de IP e faixas de rede
- **🔒 Cibersegurança**: Inteligência de ameaças e reputação de IP
- **📈 Analytics**: Análise geográfica de tráfego web
- **🚫 Restrição de Conteúdo**: Implementar restrições geográficas de conteúdo
- **🔍 Pesquisa**: Topologia de rede e pesquisa de infraestrutura da internet

## 🐛 Solução de Problemas

### Problemas Comuns

1. **Nenhuma rede encontrada**
   ```bash
   # Verifique se o código do país é válido (2 letras)
   python geoip_acl_downloader.py --acl INVALIDO  # ❌ Inválido
   python geoip_acl_downloader.py --acl BR        # ✅ Válido
   ```

2. **Erros de timeout**
   ```bash
   # Aumentar timeout para conexões lentas
   python geoip_acl_downloader.py --acl US --timeout 120
   ```

3. **Erros de permissão**
   ```bash
   # Certifique-se de ter permissões de escrita no diretório atual
   ls -la
   chmod +w .
   ```

4. **Conectividade de rede**
   ```bash
   # Teste com logging verbose para ver mensagens de erro detalhadas
   python geoip_acl_downloader.py --acl BR --verbose
   ```

### Modo Debug

Habilite o logging verbose para solução detalhada de problemas:

```bash
python geoip_acl_downloader.py --acl BR --verbose
```

Isso mostrará:
- Progresso do download para cada URL
- Detalhes do parsing de rede
- Estatísticas de filtragem
- Mensagens de erro detalhadas

## 📝 Logging

A ferramenta cria logs detalhados em `geoip_acl_downloader.log` (ou caminho personalizado com `--log-file`):

```
2024-08-27 10:30:15,123 - INFO - Iniciando GeoIP ACL downloader para país: BR
2024-08-27 10:30:15,124 - INFO - Baixando de: https://geoip.site/download/MaxMind/GeoIP.acl
2024-08-27 10:30:16,456 - INFO - Baixados com sucesso 1.234.567 caracteres do MaxMind
2024-08-27 10:30:16,789 - INFO - Extraídas 1.245 redes do MaxMind
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja como você pode ajudar:

1. **Faça um fork do repositório**
2. **Crie uma branch de feature**: `git checkout -b feature/funcionalidade-incrivel`
3. **Faça suas alterações**
4. **Adicione testes** se aplicável
5. **Commit suas alterações**: `git commit -m 'Adiciona funcionalidade incrível'`
6. **Push para a branch**: `git push origin feature/funcionalidade-incrivel`
7. **Abra um Pull Request**

### Setup de Desenvolvimento

```bash
# Clone seu fork
git clone https://github.com/AlanMartines/geoip-acl-downloader.git
cd geoip-acl-downloader

# Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale dependências
pip install requests

# Execute testes
python -m pytest tests/  # Se testes estiverem disponíveis

# Formatação de código (opcional)
pip install black
black geoip_acl_downloader.py
```

### Diretrizes de Contribuição

- Siga as diretrizes de estilo PEP 8
- Adicione docstrings para novas funções
- Inclua tratamento de erros para novas funcionalidades
- Atualize o README se adicionar nova funcionalidade
- Teste com múltiplos códigos de país

## 📄 Licença

Este projeto é licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ⭐ Suporte

Se você achar esta ferramenta útil, considere:

- ⭐ **Dar uma estrela ao repositório**
- 🐛 **Relatar problemas** que encontrar
- 💡 **Sugerir novas funcionalidades**
- 🤝 **Contribuir** para o código
- 📢 **Compartilhar** com outros que possam achar útil

## 🔗 Projetos Relacionados

- [MaxMind GeoIP](https://www.maxmind.com/) - Banco de dados GeoIP comercial
- [IP2Location](https://www.ip2location.com/) - Banco de dados de geolocalização IP
- [DB-IP](https://db-ip.com/) - Banco de dados de geolocalização IP gratuito
