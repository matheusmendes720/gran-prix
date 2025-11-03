# 🧠 BREAKDOWN COMPLETO: LSTM
## Análise Profunda Passo a Passo - Long Short-Term Memory

---

**Data:** Novembro 2025  
**Versão:** LSTM Breakdown v1.0  
**Status:** ✅ Breakdown Completo Expandido

---

## 📋 ÍNDICE EXPANDIDO

### Parte I: Fundamentos de LSTM
1. [O que é LSTM?](#1-o-que-é-lstm)
2. [Por que LSTM?](#2-por-que-lstm)
3. [Arquitetura da Célula LSTM](#3-arquitetura-célula)
4. [Comparação com RNN](#4-comparação-rnn)
5. [Problema do Vanishing Gradient](#5-vanishing-gradient)

### Parte II: Matemática Profunda
6. [Equações dos Gates](#6-equações-gates)
7. [Derivação do Forget Gate](#7-derivação-forget-gate)
8. [Derivação do Input Gate](#8-derivação-input-gate)
9. [Derivação do Output Gate](#9-derivação-output-gate)
10. [Cell State Update](#10-cell-state-update)

### Parte III: Backpropagation
11. [Backpropagation Through Time (BPTT)](#11-bptt)
12. [Gradientes dos Gates](#12-gradientes-gates)
13. [Derivação Completa BPTT](#13-derivação-bptt)
14. [Vanishing/Exploding Gradient](#14-gradient-problems)
15. [Solução: Gradient Clipping](#15-gradient-clipping)

### Parte IV: Implementação
16. [Forward Pass Completo](#16-forward-pass)
17. [Backward Pass Completo](#17-backward-pass)
18. [Otimização (Adam)](#18-otimização)
19. [Regularização](#19-regularização)
20. [Aplicações Nova Corrente](#20-aplicações)

---

# 1. O QUE É LSTM?

## 1.1 Definição

**LSTM (Long Short-Term Memory)** é uma arquitetura de rede neural recorrente (RNN) projetada para resolver o problema do **vanishing gradient**.

**Inovação:** Adiciona um **"memory cell"** que pode armazenar informação por longos períodos.

## 1.2 Componentes Principais

Uma célula LSTM tem **4 componentes**:

1. **Forget Gate** ($f_t$): Decide o que esquecer
2. **Input Gate** ($i_t$): Decide o que armazenar
3. **Cell State** ($C_t$): Memória de longo prazo
4. **Output Gate** ($o_t$): Decide o que produzir

---

# 2. POR QUE LSTM?

## 2.1 Problemas do RNN Simples

**RNN Padrão:**
$$h_t = \tanh(W_{hh} h_{t-1} + W_{xh} x_t + b_h)$$

**Problemas:**
- ❌ Vanishing gradient (gradientes desaparecem)
- ❌ Exploding gradient (gradientes explodem)
- ❌ Não lembra informações de longo prazo

## 2.2 Vantagens do LSTM

- ✅ **Lembra longo prazo:** Cell state mantém informação
- ✅ **Esquece seletivamente:** Forget gate remove informação irrelevante
- ✅ **Gradientes estáveis:** Cell state facilita backpropagation
- ✅ **Modela dependências longas:** Eficaz para séries temporais

---

# 3. ARQUITETURA DA CÉLULA LSTM

## 3.1 Diagrama Completo

```
Input: x_t (features at time t)
Hidden: h_{t-1} (previous hidden state)
Cell: C_{t-1} (previous cell state)
│
├─→ Forget Gate (f_t)
│   └─→ Multiplica C_{t-1} (decide o que esquecer)
│
├─→ Input Gate (i_t)
│   ├─→ C̃_t (candidate values)
│   └─→ Multiplica C̃_t (decide o que armazenar)
│
├─→ Cell State Update
│   └─→ C_t = f_t ⊙ C_{t-1} + i_t ⊙ C̃_t
│
├─→ Output Gate (o_t)
│   └─→ Multiplica tanh(C_t) (decide o que produzir)
│
└─→ Hidden State: h_t = o_t ⊙ tanh(C_t)
```

## 3.2 Fluxo de Dados

1. **Forget Gate** → Remove informação antiga
2. **Input Gate** → Adiciona informação nova
3. **Cell State** → Atualiza memória
4. **Output Gate** → Produz output

---

# 4. COMPARAÇÃO COM RNN

## 4.1 RNN Simples

**Equação:**
$$h_t = \tanh(W_h h_{t-1} + W_x x_t + b)$$

**Limitações:**
- Memória: apenas $h_t$
- Gradiente: desaparece rapidamente
- Capacidade: limitada para dependências curtas

## 4.2 LSTM

**Equações (ver seção 6):**
- Múltiplos gates
- Cell state separado
- Gradiente preservado através de cell state

**Vantagens:**
- Memória: cell state + hidden state
- Gradiente: mais estável
- Capacidade: dependências muito longas

---

# 5. PROBLEMA DO VANISHING GRADIENT

## 5.1 O Problema

**Em RNN simples:**
$$\frac{\partial L}{\partial W} = \sum_{t=1}^{T} \frac{\partial L}{\partial h_T} \prod_{k=t+1}^{T} \frac{\partial h_k}{\partial h_{k-1}}$$

**Produto de derivadas:**
$$\prod_{k=t+1}^{T} \frac{\partial h_k}{\partial h_{k-1}} = \prod_{k=t+1}^{T} \tanh'(W_h h_{k-1} + ...) W_h$$

**Se $|\tanh'(.)| < 1$ e $|W_h| < 1$:**
$$\lim_{T-t \to \infty} \prod_{k=t+1}^{T} (...) \to 0$$

**Gradiente desaparece!** ❌

## 5.2 Solução LSTM

**Cell state permite "escalas" diretas:**

$$\frac{\partial C_t}{\partial C_{t-1}} = f_t + \text{termos controlados por gates}$$

**Forget gate** pode ser próximo de 1 → gradiente preservado!

---

# 6. EQUAÇÕES DOS GATES

## 6.1 Forget Gate

**Função:**
$$f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)$$

**Interpretação:**
- $f_t \approx 1$: Mantém informação
- $f_t \approx 0$: Esquece informação

**Aplicado ao cell state anterior:**
$$f_t \odot C_{t-1}$$

onde $\odot$ é produto elemento a elemento (Hadamard).

## 6.2 Input Gate

**Gate de input:**
$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$

**Valores candidatos:**
$$\tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C)$$

**Aplicado:**
$$i_t \odot \tilde{C}_t$$

## 6.3 Cell State Update

**Atualização:**
$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$$

**Forma completa:**
$$C_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) \odot C_{t-1} + \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) \odot \tanh(W_C \cdot [h_{t-1}, x_t] + b_C)$$

## 6.4 Output Gate

**Gate de output:**
$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$

**Hidden state:**
$$h_t = o_t \odot \tanh(C_t)$$

---

# 7. DERIVAÇÃO DO FORGET GATE

## 7.1 Objetivo

**Forget gate decide:** Quanto da informação antiga ($C_{t-1}$) manter.

## 7.2 Cálculo

**Input:**
$$\mathbf{z}_f = W_f \cdot \mathbf{concat}(h_{t-1}, x_t) + b_f$$

**Sigmoid:**
$$f_t = \sigma(\mathbf{z}_f) = \frac{1}{1 + e^{-\mathbf{z}_f}}$$

**Aplicação:**
$$f_t \odot C_{t-1}$$

**Element-wise:**
$$f_{t,i} \times C_{t-1,i}$$

## 7.3 Propriedades

- $f_t \in [0, 1]$ (sigmoid output)
- Se $f_{t,i} = 0$: esquece completamente valor $i$ de $C_{t-1}$
- Se $f_{t,i} = 1$: mantém valor $i$ completamente

---

# 8. DERIVAÇÃO DO INPUT GATE

## 8.1 Objetivo

**Input gate decide:** Quanto da nova informação ($\tilde{C}_t$) armazenar.

## 8.2 Cálculo

**Step 1: Gate de input**
$$i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i)$$

**Step 2: Valores candidatos**
$$\tilde{C}_t = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C)$$

**Step 3: Combinação**
$$i_t \odot \tilde{C}_t$$

**Interpretação:**
- $i_t$: quanto armazenar (0-1)
- $\tilde{C}_t$: valores novos candidatos (-1 a 1)

---

# 9. DERIVAÇÃO DO OUTPUT GATE

## 9.1 Objetivo

**Output gate decide:** Quanto da informação do cell state usar no output.

## 9.2 Cálculo

**Step 1: Gate de output**
$$o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o)$$

**Step 2: Cell state processado**
$$\tanh(C_t)$$

**Step 3: Hidden state**
$$h_t = o_t \odot \tanh(C_t)$$

**Interpretação:**
- $o_t$: quanto expor do cell state
- $\tanh(C_t)$: cell state normalizado para [-1, 1]
- $h_t$: informação exposta para próxima camada/timestep

---

# 10. CELL STATE UPDATE

## 10.1 Equação Completa

$$C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$$

**Expandindo todos os termos:**

$$C_t = \sigma(W_f [h_{t-1}, x_t] + b_f) \odot C_{t-1} + \sigma(W_i [h_{t-1}, x_t] + b_i) \odot \tanh(W_C [h_{t-1}, x_t] + b_C)$$

## 10.2 Interpretação

**Parte 1:** $f_t \odot C_{t-1}$
- **Esquece** informação antiga proporcionalmente a $f_t$

**Parte 2:** $i_t \odot \tilde{C}_t$
- **Adiciona** informação nova proporcionalmente a $i_t$

**Soma:** Combinação de informação antiga (esquece seletivamente) + informação nova (armazena seletivamente)

## 10.3 Propriedades

**Conservação de informação:**
- Se $f_t \approx 1$ e $i_t \approx 0$: mantém informação antiga
- Se $f_t \approx 0$ e $i_t \approx 1$: substitui por informação nova
- Se ambos ≈ 0: cell state próximo de zero

---

# 11. BACKPROPAGATION THROUGH TIME (BPTT)

## 11.1 Objetivo

**Calcular gradientes** retrocedendo no tempo.

## 11.2 Loss Function

**Para sequência de comprimento T:**

$$L = \sum_{t=1}^{T} L_t$$

onde $L_t$ é loss no timestep $t$ (ex: MSE).

## 11.3 Gradiente w.r.t. Parâmetros

**Gradiente total:**
$$\frac{\partial L}{\partial W} = \sum_{t=1}^{T} \frac{\partial L_t}{\partial W}$$

**Para LSTM, precisamos:**
$$\frac{\partial L}{\partial W_f}, \frac{\partial L}{\partial W_i}, \frac{\partial L}{\partial W_C}, \frac{\partial L}{\partial W_o}$$

---

# 12. GRADIENTES DOS GATES

## 12.1 Gradiente do Cell State

**Gradiente w.r.t. $C_t$:**

$$\frac{\partial L}{\partial C_t} = \frac{\partial L}{\partial h_t} \frac{\partial h_t}{\partial C_t} + \frac{\partial L}{\partial C_{t+1}} \frac{\partial C_{t+1}}{\partial C_t}$$

**Onde:**
$$\frac{\partial h_t}{\partial C_t} = o_t \odot (1 - \tanh^2(C_t))$$

$$\frac{\partial C_{t+1}}{\partial C_t} = f_{t+1}$$

**Resultado:**
$$\frac{\partial L}{\partial C_t} = \frac{\partial L}{\partial h_t} o_t \odot (1 - \tanh^2(C_t)) + \frac{\partial L}{\partial C_{t+1}} f_{t+1}$$

**Importante:** Gradiente flui através de $f_{t+1}$, que pode ser ≈ 1 → gradiente preservado!

## 12.2 Gradientes dos Gates

### Forget Gate
$$\frac{\partial L}{\partial W_f} = \sum_{t=1}^{T} \frac{\partial L}{\partial C_t} \frac{\partial C_t}{\partial f_t} \frac{\partial f_t}{\partial W_f}$$

$$\frac{\partial C_t}{\partial f_t} = C_{t-1}$$

$$\frac{\partial f_t}{\partial W_f} = f_t(1-f_t) [h_{t-1}, x_t]$$

### Input Gate
$$\frac{\partial L}{\partial W_i} = \sum_{t=1}^{T} \frac{\partial L}{\partial C_t} \tilde{C}_t \cdot i_t(1-i_t) [h_{t-1}, x_t]$$

### Candidate Values
$$\frac{\partial L}{\partial W_C} = \sum_{t=1}^{T} \frac{\partial L}{\partial C_t} i_t \cdot (1-\tilde{C}_t^2) [h_{t-1}, x_t]$$

### Output Gate
$$\frac{\partial L}{\partial W_o} = \sum_{t=1}^{T} \frac{\partial L}{\partial h_t} \tanh(C_t) \cdot o_t(1-o_t) [h_{t-1}, x_t]$$

---

# 13. DERIVAÇÃO COMPLETA BPTT

## 13.1 Algoritmo Completo

### Forward Pass
```
Para t = 1 até T:
    f_t = σ(W_f [h_{t-1}, x_t] + b_f)
    i_t = σ(W_i [h_{t-1}, x_t] + b_i)
    C̃_t = tanh(W_C [h_{t-1}, x_t] + b_C)
    C_t = f_t ⊙ C_{t-1} + i_t ⊙ C̃_t
    o_t = σ(W_o [h_{t-1}, x_t] + b_o)
    h_t = o_t ⊙ tanh(C_t)
    ŷ_t = W_y h_t + b_y
    L_t = loss(y_t, ŷ_t)
```

### Backward Pass
```
∂L/∂h_T = ∂L_T/∂h_T (último timestep)
∂L/∂C_T = ∂L/∂h_T · o_T ⊙ (1 - tanh²(C_T))

Para t = T até 1:
    # Gradiente do output gate
    ∂L/∂W_o += ∂L/∂h_t · tanh(C_t) · o_t(1-o_t) [h_{t-1}, x_t]
    
    # Gradiente do cell state
    ∂L/∂C_t = ∂L/∂h_t · o_t ⊙ (1 - tanh²(C_t)) + ∂L/∂C_{t+1} · f_{t+1}
    
    # Gradiente do forget gate
    ∂L/∂W_f += ∂L/∂C_t · C_{t-1} · f_t(1-f_t) [h_{t-1}, x_t]
    
    # Gradiente do input gate
    ∂L/∂W_i += ∂L/∂C_t · C̃_t · i_t(1-i_t) [h_{t-1}, x_t]
    
    # Gradiente dos valores candidatos
    ∂L/∂W_C += ∂L/∂C_t · i_t · (1-C̃_t²) [h_{t-1}, x_t]
    
    # Gradiente para timestep anterior
    ∂L/∂h_{t-1} = ∂L/∂h_t · ∂h_t/∂h_{t-1} + ∂L/∂C_t · ∂C_t/∂h_{t-1}
```

---

# 14. VANISHING/EXPLODING GRADIENT

## 14.1 Análise do Gradiente

**Gradiente através do tempo:**
$$\frac{\partial L}{\partial C_1} = \frac{\partial L}{\partial C_T} \prod_{t=2}^{T} \frac{\partial C_t}{\partial C_{t-1}}$$

**Onde:**
$$\frac{\partial C_t}{\partial C_{t-1}} = f_t + \text{termos adicionais}$$

### Se Forget Gate ≈ 1
**Gradiente preservado:** $\prod_{t=2}^{T} f_t \approx 1$

### Se Forget Gate ≈ 0
**Gradiente desaparece:** $\prod_{t=2}^{T} f_t \approx 0$

## 14.2 Exploding Gradient

**Se valores dos gates grandes:**
- Gradientes podem explodir
- Solução: **Gradient Clipping**

---

# 15. GRADIENT CLIPPING

## 15.1 Método

**Clipping por valor:**
```python
if grad_norm > max_norm:
    grad = grad * (max_norm / grad_norm)
```

**Clipping por norma:**
```python
grad_norm = torch.norm(gradients)
if grad_norm > max_norm:
    gradients = gradients * (max_norm / grad_norm)
```

## 15.2 Implementação

```python
def clip_gradients(model, max_norm=1.0):
    """
    Clips gradients to prevent exploding.
    """
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm)
```

---

# 16. FORWARD PASS COMPLETO

## 16.1 Implementação Python

```python
import numpy as np
import torch
import torch.nn as nn

class LSTMCell(nn.Module):
    """
    Implementação completa célula LSTM.
    """
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        
        # Forget gate
        self.W_f = nn.Linear(input_size + hidden_size, hidden_size)
        # Input gate
        self.W_i = nn.Linear(input_size + hidden_size, hidden_size)
        # Candidate values
        self.W_C = nn.Linear(input_size + hidden_size, hidden_size)
        # Output gate
        self.W_o = nn.Linear(input_size + hidden_size, hidden_size)
    
    def forward(self, x_t, h_t_prev, C_t_prev):
        """
        Forward pass de uma célula LSTM.
        """
        # Concatenar input e hidden state anterior
        concat = torch.cat([h_t_prev, x_t], dim=1)
        
        # Forget gate
        f_t = torch.sigmoid(self.W_f(concat))
        
        # Input gate
        i_t = torch.sigmoid(self.W_i(concat))
        
        # Candidate cell state
        C_tilde = torch.tanh(self.W_C(concat))
        
        # Update cell state
        C_t = f_t * C_t_prev + i_t * C_tilde
        
        # Output gate
        o_t = torch.sigmoid(self.W_o(concat))
        
        # Hidden state
        h_t = o_t * torch.tanh(C_t)
        
        return h_t, C_t
```

## 16.2 Sequência Completa

```python
def lstm_forward(X, model):
    """
    Forward pass para sequência completa.
    
    X: (seq_length, batch_size, input_size)
    """
    h_t = torch.zeros(batch_size, hidden_size)
    C_t = torch.zeros(batch_size, hidden_size)
    
    outputs = []
    
    for t in range(seq_length):
        x_t = X[t]  # (batch_size, input_size)
        h_t, C_t = lstm_cell(x_t, h_t, C_t)
        outputs.append(h_t)
    
    return torch.stack(outputs), h_t, C_t
```

---

# 17. BACKWARD PASS COMPLETO

## 17.1 Implementação

**PyTorch faz automaticamente** via autograd, mas aqui a forma manual:

```python
def lstm_backward(dL_dh, dL_dC, X, h_prev, C_prev, h_curr, C_curr, gates):
    """
    Backward pass manual.
    """
    # Gradiente do output gate
    dL_do = dL_dh * torch.tanh(C_curr)
    dL_dW_o = dL_do * o * (1 - o) * concat
    
    # Gradiente do cell state
    dL_dC_curr = dL_dh * o * (1 - torch.tanh(C_curr)**2) + dL_dC_next * f_next
    
    # Gradiente do forget gate
    dL_df = dL_dC_curr * C_prev
    dL_dW_f = dL_df * f * (1 - f) * concat
    
    # Gradiente do input gate
    dL_di = dL_dC_curr * C_tilde
    dL_dW_i = dL_di * i * (1 - i) * concat
    
    # Gradiente dos valores candidatos
    dL_dC_tilde = dL_dC_curr * i
    dL_dW_C = dL_dC_tilde * (1 - C_tilde**2) * concat
    
    # Gradiente para timestep anterior
    dL_dh_prev = dL_dh @ W_o[:, :hidden_size] + dL_dC_curr @ W_f[:, :hidden_size] + ...
    dL_dC_prev = dL_dC_curr * f
    
    return dL_dh_prev, dL_dC_prev, dL_dW_f, dL_dW_i, dL_dW_C, dL_dW_o
```

---

# 18. OTIMIZAÇÃO (ADAM)

## 18.1 Adam Optimizer

**Atualização:**

$$m_t = \beta_1 m_{t-1} + (1-\beta_1) g_t$$
$$v_t = \beta_2 v_{t-1} + (1-\beta_2) g_t^2$$
$$\hat{m}_t = \frac{m_t}{1-\beta_1^t}$$
$$\hat{v}_t = \frac{v_t}{1-\beta_2^t}$$
$$\theta_{t+1} = \theta_t - \frac{\alpha}{\sqrt{\hat{v}_t} + \epsilon} \hat{m}_t$$

**Hiperparâmetros:**
- $\alpha = 0.001$ (learning rate)
- $\beta_1 = 0.9$ (momentum decay)
- $\beta_2 = 0.999$ (squared gradient decay)
- $\epsilon = 10^{-8}$ (numérico)

---

# 19. REGULARIZAÇÃO

## 19.1 Dropout

**Aplica dropout no hidden state:**
$$h_t = \text{dropout}(h_t, p)$$

**Dropout rate:** $p = 0.2-0.5$ comum.

## 19.2 L2 Regularization

**Adiciona ao loss:**
$$L_{total} = L + \lambda \sum_{W} \|W\|_2^2$$

**$\lambda$:** weight decay (ex: 0.0001).

---

# 20. APLICAÇÕES NOVA CORRENTE

## 20.1 Previsão de Demanda com LSTM

**Arquitetura:**
- Input: 30 dias históricos
- LSTM: 2 camadas, 50 unidades cada
- Output: 30 dias de previsão

**Features:**
- Consumo histórico
- Temperatura
- Feriados
- Sazonalidade

### Implementação

```python
import torch
import torch.nn as nn

class DemandLSTM(nn.Module):
    def __init__(self, input_size=10, hidden_size=50, num_layers=2, output_size=30):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        # x: (batch, seq_len, features)
        lstm_out, (h_n, c_n) = self.lstm(x)
        # Usar última saída
        last_hidden = lstm_out[:, -1, :]
        forecast = self.fc(last_hidden)
        return forecast
```

## 20.2 Treinamento

```python
model = DemandLSTM(input_size=10, hidden_size=50, num_layers=2)
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

for epoch in range(100):
    for batch_x, batch_y in dataloader:
        # Forward
        forecast = model(batch_x)
        loss = criterion(forecast, batch_y)
        
        # Backward
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
```

---

# RESUMO FINAL

## Equações Principais LSTM

| Gate/Estado | Fórmula |
|-------------|---------|
| **Forget Gate** | $f_t = \sigma(W_f [h_{t-1}, x_t] + b_f)$ |
| **Input Gate** | $i_t = \sigma(W_i [h_{t-1}, x_t] + b_i)$ |
| **Candidate** | $\tilde{C}_t = \tanh(W_C [h_{t-1}, x_t] + b_C)$ |
| **Cell State** | $C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t$ |
| **Output Gate** | $o_t = \sigma(W_o [h_{t-1}, x_t] + b_o)$ |
| **Hidden State** | $h_t = o_t \odot \tanh(C_t)$ |

---

**Nova Corrente Grand Prix SENAI**

**LSTM COMPLETE BREAKDOWN - Version 1.0**

*Novembro 2025*

