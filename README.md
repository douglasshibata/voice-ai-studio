# 🎙️ Voice AI Studio - Estúdio Local de Inteligência Artificial de Voz

Plataforma profissional e soberana de geração, clonagem, conversão, transcrição e dublagem de voz baseada em arquitetura modular de engines de IA com execução 100% local, foco absoluto em privacidade, aceleração GPU e integrações MCP/OpenAI.

---

## 🏛️ Arquitetura do Sistema

```
                        ┌────────────────────────┐
                        │   Tauri / React Web    │
                        └───────────┬────────────┘
                                    │ HTTP / WebSocket
                        ┌───────────▼────────────┐
                        │      FastAPI Core      │
                        └─────┬────────────┬─────┘
                              │            │
          ┌───────────────────▼──┐      ┌──▼───────────────────┐
          │  OpenAI API / MCP    │      │  Async Job Worker    │
          └──────────────────────┘      └──────────┬───────────┘
                                                   │
                                        ┌──────────▼───────────┐
                                        │   Engine Registry    │
                                        └─────┬────────────┬───┘
                                              │            │
                        ┌─────────────────────▼──┐      ┌──▼───────────────────┐
                        │ Piper / Whisper Engines│      │  Demucs / FFmpeg     │
                        └────────────────────────┘      └──────────────────────┘
```

### Componentes Principais
1. **Engine Registry & Adapters:** Camada de abstração que unifica engines de TTS (Piper, XTTS/Coqui), ASR (Faster-Whisper), Voice Conversion e Áudio/Separador de Stems (FFmpeg, Demucs).
2. **Model Catalog & Memory Manager:** Gestão inteligente do ciclo de vida de modelos em memória (VRAM/RAM), suporte a lazy loading e flush automatizado para prevenção de estouro de GPU.
3. **Voice Cloning & Design Engine:** Algoritmos de análise de qualidade acústica (SNR, clipping, silêncio), vinculação de consentimento explícito e marca d'água sintética.
4. **Studio Workflows:** Pipelines integrados para Text-to-Speech, Speech-to-Text com diarização, dublagem automatizada de vídeo e processador de áudiobooks multi-personagem.
5. **OpenAI-Compatible & MCP Server:** Servidor local que responde na especificação `/v1/audio/speech` e expõe ferramentas de voz nativas para agentes MCP.

---

## 💻 Requisitos do Sistema & Hardware

- **Sistemas Operacionais:** Linux (Ubuntu 22.04+), Windows 11, macOS (Apple Silicon M1/M2/M3).
- **Linguagens e Runtime:** Python 3.11+, Node.js 20+, FFmpeg.
- **Aceleração Hardware (Opcional, mas recomendado):**
  - NVIDIA GPU com suporte a CUDA 12.x e pelo menos 4GB VRAM.
  - Apple Silicon com aceleração Metal Performance Shaders (MPS).

---

## 🚀 Instalação & Configuração

### 1. Clonar o Repositório e Preparar o Ambiente Backend

```bash
cd voice-ai-studio
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
```

### 2. Configurar o Frontend Web Studio

```bash
cd voice-ai-studio/frontend
npm install
npm run build
```

---

## ⚡ Execução do Sistema

### Executar o Backend FastAPI

```bash
cd voice-ai-studio
PYTHONPATH=backend python3 -m uvicorn app.main:app --host 127.0.0.1 --port 3900 --reload
```

Acesse a documentação interativa Swagger/OpenAPI em: `http://127.0.0.1:3900/docs`.

### Executar via Docker Compose

```bash
cd voice-ai-studio/docker
docker compose up -d
```

---

## 🧪 Suíte de Testes Automatizados

Para executar todos os testes automatizados de backend, motores, trabalhadores e integração de APIs:

```bash
cd voice-ai-studio
PYTHONPATH=backend python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 🛡️ Segurança e Licenciamento

- **Privacidade Soberana:** Por padrão, nenhum arquivo de áudio ou texto sintetizado é enviado para servidores externos.
- **Matriz de Licenças:** Documentação completa das licenças de software e pesos dos modelos (MIT, Apache 2.0, MPL 2.0) disponível em `docs/licenses.md`.
- **Consentimento em Clonagem de Voz:** Exige confirmação explícita de autorização registrada no banco de dados local (`UserConsent`).
# voice-ai-studio
