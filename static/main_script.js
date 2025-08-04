// Script principal para controle das abas e inicialização

class TabManager {
    constructor() {
        this.currentTab = 'auto-prog';
        this.initializeEventListeners();
        this.initializeApp();
    }

    initializeEventListeners() {
        // Event listeners para as abas
        
        document.getElementById('tab-sankhya').addEventListener('click', () => this.switchTab('sankhya'));
    }

    switchTab(tabName) {
        // Remover classe active de todas as abas
        document.querySelectorAll('.tab-button').forEach(button => {
            button.classList.remove('active');
            button.classList.add('border-transparent', 'text-gray-400');
            button.classList.remove('border-purple-500', 'text-purple-400');
        });

        // Esconder todo o conteúdo das abas
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.add('hidden');
        });

        // Ativar a aba selecionada
        const selectedTab = document.getElementById(`tab-${tabName}`);
        selectedTab.classList.add('active');
        selectedTab.classList.remove('border-transparent', 'text-gray-400');
        selectedTab.classList.add('border-purple-500', 'text-purple-400');

        // Mostrar o conteúdo da aba selecionada
        const selectedContent = document.getElementById(`content-${tabName}`);
        selectedContent.classList.remove('hidden');

        this.currentTab = tabName;

        // Inicializar funcionalidades específicas da aba
        if (tabName === 'sankhya') {
            initializeSankhyaAutomation();
        }
    }

    initializeApp() {
        // Esconder loading layer após um breve delay
        setTimeout(() => {
            const loadingLayer = document.getElementById('loading-layer');
            if (loadingLayer) {
                loadingLayer.style.opacity = '0';
                setTimeout(() => {
                    loadingLayer.style.display = 'none';
                }, 300);
            }
        }, 1000);

        // Inicializar com a primeira aba ativa
        this.switchTab('auto-prog');
    }
}

// Função para mostrar notificações toast
function showToast(message, type = 'info') {
    // Criar elemento toast
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full`;
    
    // Definir cores baseadas no tipo
    const typeClasses = {
        'success': 'bg-green-600 text-white',
        'error': 'bg-red-600 text-white',
        'warning': 'bg-yellow-600 text-white',
        'info': 'bg-blue-600 text-white'
    };
    
    toast.className += ` ${typeClasses[type] || typeClasses.info}`;
    
    // Definir ícones baseados no tipo
    const typeIcons = {
        'success': 'fas fa-check-circle',
        'error': 'fas fa-exclamation-circle',
        'warning': 'fas fa-exclamation-triangle',
        'info': 'fas fa-info-circle'
    };
    
    toast.innerHTML = `
        <div class="flex items-center">
            <i class="${typeIcons[type] || typeIcons.info} mr-2"></i>
            <span>${message}</span>
            <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    // Adicionar ao DOM
    document.body.appendChild(toast);
    
    // Animar entrada
    setTimeout(() => {
        toast.classList.remove('translate-x-full');
    }, 100);
    
    // Remover automaticamente após 5 segundos
    setTimeout(() => {
        toast.classList.add('translate-x-full');
        setTimeout(() => {
            if (toast.parentElement) {
                toast.remove();
            }
        }, 300);
    }, 5000);
}

// Função para confirmar ações importantes
function confirmAction(message, callback) {
    const confirmed = confirm(message);
    if (confirmed && typeof callback === 'function') {
        callback();
    }
    return confirmed;
}

// Função para formatar data para exibição
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

// Função para formatar data e hora para exibição
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR');
}

// Função para validar formulários
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('border-red-500');
            isValid = false;
        } else {
            field.classList.remove('border-red-500');
        }
    });
    
    return isValid;
}

// Função para limpar formulários
function clearForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        form.reset();
        // Remover classes de erro
        form.querySelectorAll('.border-red-500').forEach(field => {
            field.classList.remove('border-red-500');
        });
    }
}

// Função para fazer download de arquivos
function downloadFile(url, filename) {
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Função para copiar texto para clipboard
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Texto copiado para a área de transferência', 'success');
    } catch (err) {
        console.error('Erro ao copiar texto: ', err);
        showToast('Erro ao copiar texto', 'error');
    }
}

// Inicializar aplicação quando DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar gerenciador de abas
    const tabManager = new TabManager();
    
    // Tornar funções globalmente acessíveis
    window.tabManager = tabManager;
    window.showToast = showToast;
    window.confirmAction = confirmAction;
    window.formatDate = formatDate;
    window.formatDateTime = formatDateTime;
    window.validateForm = validateForm;
    window.clearForm = clearForm;
    window.downloadFile = downloadFile;
    window.copyToClipboard = copyToClipboard;
    
    console.log('Sistema Unificado inicializado com sucesso!');
});

// Tratamento para finalizar a sessão da API ao sair da página
window.addEventListener('beforeunload', function(event) {
    // Verifica se a aba do Sankhya foi utilizada
    if (window.sankhyaAutomation && window.sankhyaAutomation.hasBeenUsed) {
        // Usa navigator.sendBeacon para enviar uma requisição final
        // que funciona mesmo quando a página está sendo descarregada.
        navigator.sendBeacon('/api/sankhya/finalizar_conexoes', new Blob());
        console.log("Enviando solicitação para finalizar conexões Sankhya.");
    }
});


// Tratamento de erros globais
window.addEventListener('error', function(event) {
    console.error('Erro global capturado:', event.error);
    showToast('Ocorreu um erro inesperado. Verifique o console para mais detalhes.', 'error');
});

// Tratamento de promessas rejeitadas
window.addEventListener('unhandledrejection', function(event) {
    console.error('Promise rejeitada:', event.reason);
    showToast('Erro de comunicação com o servidor.', 'error');
});

