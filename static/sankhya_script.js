// Script para funcionalidade do Sankhya Automation

class SankhyaAutomation {
    constructor() {
        this.isProcessing = false;
        this.hasBeenUsed = false; // <-- Adicione esta flag
        this.currentRodada = 0;
        this.totalRodadas = 0;
        this.totalPlanejamentos = 0;
        this.opsProcessadas = 0;
        this.initializeEventListeners();
    }


    initializeEventListeners() {
        document.getElementById('verificar-conexoes-btn').addEventListener('click', () => this.verificarConexoes());
        document.getElementById('buscar-planejamentos-btn').addEventListener('click', () => this.buscarPlanejamentos());
        document.getElementById('processar-automacao-btn').addEventListener('click', () => this.iniciarAutomacao());
    }

    addLogMessage(message, type = 'info') {
        const logContainer = document.getElementById('sankhya-log');
        const timestamp = new Date().toLocaleTimeString();
        const typeClass = `status-${type}`;
        
        const logEntry = document.createElement('div');
        logEntry.className = `mb-1 ${typeClass}`;
        logEntry.innerHTML = `<span class="text-gray-500">[${timestamp}]</span> ${message}`;
        
        logContainer.appendChild(logEntry);
        logContainer.scrollTop = logContainer.scrollHeight;
    }

    clearLog() {
        const logContainer = document.getElementById('sankhya-log');
        logContainer.innerHTML = '<p class="text-gray-400">Log limpo...</p>';
    }

    showButton(buttonId) {
        document.getElementById(buttonId).classList.remove('hidden');
    }

    hideButton(buttonId) {
        document.getElementById(buttonId).classList.add('hidden');
    }

    showSection(sectionId) {
        document.getElementById(sectionId).classList.remove('hidden');
    }

    hideSection(sectionId) {
        document.getElementById(sectionId).classList.add('hidden');
    }

    updateProgress(current, total) {
        const percentage = total > 0 ? Math.round((current / total) * 100) : 0;
        document.getElementById('progress-bar').style.width = `${percentage}%`;
        document.getElementById('progress-text').textContent = `${percentage}%`;
    }

    updateCounters(opsCreated, failures, currentRodada) {
        document.getElementById('ops-criadas').textContent = opsCreated;
        document.getElementById('ops-falhas').textContent = failures;
        document.getElementById('rodada-atual').textContent = currentRodada;
    }

    async verificarConexoes() {
        this.addLogMessage('Iniciando verificação de conexões...', 'info');
        
        try {
            const response = await fetch('/api/sankhya/verificar_conexoes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });

            const result = await response.json();

            if (result.sucesso) {
                this.addLogMessage('✅ ' + result.mensagem, 'success');
                this.showButton('buscar-planejamentos-btn');
            } else {
                this.addLogMessage('❌ ' + result.erro, 'error');
                this.hideButton('buscar-planejamentos-btn');
                this.hideButton('processar-automacao-btn');
            }
        } catch (error) {
            this.addLogMessage('❌ Erro ao verificar conexões: ' + error.message, 'error');
        }
    }

    async buscarPlanejamentos() {
        const dataPlaneamento = document.getElementById('data-planejamento').value;
        const braco = parseInt(document.getElementById('braco-sankhya').value);
        const rodadaInicial = parseInt(document.getElementById('rodada-inicial').value);
        const rodadaFinal = parseInt(document.getElementById('rodada-final').value);

        if (!dataPlaneamento) {
            this.addLogMessage('❌ Por favor, informe a data do planejamento', 'error');
            return;
        }

        if (rodadaInicial > rodadaFinal) {
            this.addLogMessage('❌ Rodada inicial não pode ser maior que a rodada final', 'error');
            return;
        }

        this.addLogMessage(`Buscando planejamentos para ${dataPlaneamento}, braço ${braco}, rodadas ${rodadaInicial}-${rodadaFinal}...`, 'info');

        try {
            const response = await fetch('/api/sankhya/buscar_planejamentos', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    data_planejamento: dataPlaneamento,
                    braco: braco,
                    rodada_inicial: rodadaInicial,
                    rodada_final: rodadaFinal
                })
            });

            const result = await response.json();

            if (result.sucesso) {
                this.totalPlanejamentos = result.total;
                this.totalRodadas = rodadaFinal - rodadaInicial + 1;
                
                if (this.totalPlanejamentos > 0) {
                    this.addLogMessage(`✅ Encontrados ${this.totalPlanejamentos} planejamentos pendentes`, 'success');
                    this.showButton('processar-automacao-btn');
                } else {
                    this.addLogMessage('⚠️ Nenhum planejamento pendente encontrado', 'warning');
                    this.hideButton('processar-automacao-btn');
                }
            } else {
                this.addLogMessage('❌ ' + result.erro, 'error');
                this.hideButton('processar-automacao-btn');
            }
        } catch (error) {
            this.addLogMessage('❌ Erro ao buscar planejamentos: ' + error.message, 'error');
        }
    }

    async iniciarAutomacao() {
        if (this.isProcessing) {
            this.addLogMessage('⚠️ Automação já está em andamento', 'warning');
            return;
        }

        const dataPlaneamento = document.getElementById('data-planejamento').value;
        const braco = parseInt(document.getElementById('braco-sankhya').value);
        const rodadaInicial = parseInt(document.getElementById('rodada-inicial').value);
        const rodadaFinal = parseInt(document.getElementById('rodada-final').value);

        this.isProcessing = true;
        this.hideButton('processar-automacao-btn');
        this.showSection('sankhya-progress-section');
        
        this.addLogMessage('🚀 Iniciando automação de criação de OPs...', 'info');

        let totalOpsCreated = 0;
        let totalFailures = 0;

        try {
            for (let rodada = rodadaInicial; rodada <= rodadaFinal; rodada++) {
                this.currentRodada = rodada;
                this.updateCounters(totalOpsCreated, totalFailures, rodada);
                
                this.addLogMessage(`--- Processando Rodada ${rodada} ---`, 'info');
                
                const response = await fetch('/api/sankhya/processar_rodada', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        data_planejamento: dataPlaneamento,
                        braco: braco,
                        rodada: rodada
                    })
                });

                const result = await response.json();

                if (result.sucesso) {
                    if (result.ops_criadas > 0) {
                        totalOpsCreated += result.ops_criadas;
                        this.addLogMessage(`✅ Rodada ${rodada}: ${result.ops_criadas} OPs criadas com sucesso`, 'success');
                    } else {
                        this.addLogMessage(`⚠️ Rodada ${rodada}: Nenhuma OP criada`, 'warning');
                    }
                    
                    if (result.mensagem) {
                        this.addLogMessage(result.mensagem, 'info');
                    }
                } else {
                    totalFailures++;
                    this.addLogMessage(`❌ Rodada ${rodada}: ${result.erro}`, 'error');
                }

                this.updateCounters(totalOpsCreated, totalFailures, rodada);
                this.updateProgress(rodada - rodadaInicial + 1, this.totalRodadas);

                // Pequena pausa entre rodadas
                await new Promise(resolve => setTimeout(resolve, 1000));
            }

            this.addLogMessage('🎉 Automação concluída!', 'success');
            await this.exibirResumoFinal();

        } catch (error) {
            this.addLogMessage('❌ Erro durante a automação: ' + error.message, 'error');
        } finally {
            this.isProcessing = false;
            this.showButton('processar-automacao-btn');
            
            // Finalizar conexões
            try {
                await fetch('/api/sankhya/finalizar_conexoes', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                this.addLogMessage('🔌 Conexões finalizadas', 'info');
            } catch (error) {
                this.addLogMessage('⚠️ Erro ao finalizar conexões: ' + error.message, 'warning');
            }
        }
    }

    async exibirResumoFinal() {
        try {
            const response = await fetch('/api/sankhya/resumo');
            const resumo = await response.json();

            this.showSection('sankhya-resumo-section');
            
            const resumoContent = document.getElementById('resumo-content');
            resumoContent.innerHTML = `
                <div class="grid md:grid-cols-2 gap-6">
                    <div class="bg-gray-700 p-4 rounded-lg">
                        <h3 class="text-lg font-semibold text-green-400 mb-3">
                            <i class="fas fa-check-circle mr-2"></i>
                            OPs Criadas com Sucesso (${resumo.total_ops_criadas})
                        </h3>
                        <div class="max-h-40 overflow-y-auto">
                            ${resumo.ops_criadas_sucesso.length > 0 ? 
                                resumo.ops_criadas_sucesso.map(op => 
                                    `<div class="text-sm text-gray-300 mb-1">
                                        NUPLAN: ${op.nuplan} → OP: ${op.idiproc}
                                    </div>`
                                ).join('') : 
                                '<div class="text-sm text-gray-400">Nenhuma OP criada</div>'
                            }
                        </div>
                    </div>
                    
                    <div class="bg-gray-700 p-4 rounded-lg">
                        <h3 class="text-lg font-semibold text-red-400 mb-3">
                            <i class="fas fa-exclamation-triangle mr-2"></i>
                            Falhas no Processamento (${resumo.total_falhas})
                        </h3>
                        <div class="max-h-40 overflow-y-auto">
                            ${resumo.detalhes_falhas.length > 0 ? 
                                resumo.detalhes_falhas.map(falha => 
                                    `<div class="text-sm text-gray-300 mb-2">
                                        <div class="font-medium">NUPLAN: ${falha.nuplan}</div>
                                        <div class="text-red-300 text-xs">${falha.erro}</div>
                                    </div>`
                                ).join('') : 
                                '<div class="text-sm text-gray-400">Nenhuma falha registrada</div>'
                            }
                        </div>
                    </div>
                </div>
                
                <div class="mt-6 p-4 bg-gray-700 rounded-lg text-center">
                    <div class="text-2xl font-bold text-purple-400">
                        ${resumo.total_ops_criadas + resumo.total_falhas} 
                        <span class="text-lg text-gray-300">registros processados</span>
                    </div>
                    <div class="text-sm text-gray-400 mt-2">
                        Taxa de sucesso: ${resumo.total_ops_criadas + resumo.total_falhas > 0 ? 
                            Math.round((resumo.total_ops_criadas / (resumo.total_ops_criadas + resumo.total_falhas)) * 100) : 0}%
                    </div>
                </div>
            `;

            this.addLogMessage(`📊 Resumo: ${resumo.total_ops_criadas} sucessos, ${resumo.total_falhas} falhas`, 'info');

        } catch (error) {
            this.addLogMessage('❌ Erro ao carregar resumo: ' + error.message, 'error');
        }
    }
}

// Inicializar quando a aba do Sankhya estiver ativa
let sankhyaAutomation = null;

function initializeSankhyaAutomation() {
    if (!sankhyaAutomation) {
        sankhyaAutomation = new SankhyaAutomation();
        window.sankhyaAutomation = sankhyaAutomation; // <-- Exponha a instância globalmente

        // Definir data padrão como hoje
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('data-planejamento').value = today;
    }
}


document.addEventListener('DOMContentLoaded', () => {
    // Inicializa a automação Sankhya assim que a página carrega
    const sankhyaApp = new SankhyaAutomation();
    
    // Define a data padrão para o campo de data como hoje
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('data-planejamento').value = today;

    // Adiciona uma flag para indicar que a automação foi usada
    window.addEventListener('beforeunload', function(event) {
        if (sankhyaApp.hasBeenUsed) {
            navigator.sendBeacon('/api/sankhya/finalizar_conexoes', new Blob());
            console.log("Enviando solicitação para finalizar conexões Sankhya.");
        }
    });
});