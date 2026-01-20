/**
 * 0x_SYSTEMS Master Control
 * Logic: Universal Header, Footer, and Theme Persistence
 */

const initSystem = () => {
    // 1. Define Universal Header
    const headerHTML = `
    <header class="max-w-6xl mx-auto flex justify-between items-center p-6 mb-10">
        <div onclick="window.location.href='/'" style="cursor:pointer">
            <h1 class="text-2xl font-extrabold tracking-tighter">0X_<span class="text-blue-500">SYSTEMS</span></h1>
            <p class="text-[10px] uppercase tracking-[0.3em] opacity-50">Operational Protocol 2.6</p>
        </div>
        
        <nav class="hidden md:flex space-x-8 text-[11px] font-bold uppercase tracking-widest opacity-70">
            <a href="/" class="hover:text-blue-500 transition">Command_Center</a>
            <a href="/tools.html" class="hover:text-blue-500 transition">Utilities</a>
            <a href="/shop/" class="hover:text-blue-500 transition">Vault</a>
        </nav>

        <div class="flex items-center space-x-6">
            <div class="theme-switch" id="themeBtn" title="Toggle System Mode">
                <div class="switch-circle" id="circle"></div>
            </div>
            <a href="/shop/" class="hidden sm:block bg-blue-600 text-white px-5 py-2 rounded-full text-xs font-bold hover:bg-blue-700 transition shadow-lg shadow-blue-900/20">Access_Vault</a>
        </div>
    </header>`;

    // 2. Define Universal Footer
    const footerHTML = `
    <footer class="max-w-6xl mx-auto mt-20 py-10 border-t border-slate-800/50 flex flex-col md:flex-row justify-between items-center px-6 gap-6">
        <p class="text-[10px] opacity-30 font-mono tracking-widest uppercase">&copy; 2026 0X_ROOT_SX INTERNAL OPERATIONS</p>
        <div class="flex space-x-8 text-[10px] font-bold opacity-50 uppercase tracking-widest">
            <a href="/status" class="hover:text-blue-500 transition">System_Status</a>
            <a href="/docs" class="hover:text-blue-500 transition">Security_Logs</a>
            <a href="/contact" class="hover:text-blue-500 transition">Secure_Line</a>
        </div>
    </footer>`;

    // Injecting Elements
    document.body.insertAdjacentHTML('afterbegin', headerHTML);
    document.body.insertAdjacentHTML('beforeend', footerHTML);

    // 3. Advanced Theme Logic (Persistence)
    const themeBtn = document.getElementById('themeBtn');
    
    const applyTheme = (theme) => {
        if (theme === 'light') {
            document.body.classList.add('light-theme');
        } else {
            document.body.classList.remove('light-theme');
        }
    };

    // Load from LocalStorage
    const savedTheme = localStorage.getItem('0x_theme_config') || 'dark';
    applyTheme(savedTheme);

    themeBtn.addEventListener('click', () => {
        const isLight = document.body.classList.toggle('light-theme');
        localStorage.setItem('0x_theme_config', isLight ? 'light' : 'dark');
    });
};

// Initialize on Load
window.addEventListener('DOMContentLoaded', initSystem);
