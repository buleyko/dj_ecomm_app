const themes = {
    light: {
        '--bg-html-color': '#FFFFFF',
        '--bg-body-color': '#FFFFFF',
        '--bg-content-color': '#F0F0F0',
        '--bg-nav-color': '#C0C0C0',
        '--bg-footer-color': '#C0C0C0',
        '--text-color': '#404040',
        '--border-color': '#404040',
        '--box-shadow-color': 'gray',
        '--wish-color': '#E498A5',
        '--compare-color': '#7CB9E8',
        '--box-color':  '#8FBC8F',
        '--bg-error-message-color': '#F08080',
        '--error-message-color': '#FFFFFF',
        '--bg-success-message-color': '#90ee90',
        '--success-message-color': '#FFFFFF',
        
    },
    dark: {
        '--bg-html-color': '#FFFFFF',
        '--bg-body-color': '#C0C0C0',
        '--bg-content-color': '#606060',
        '--bg-nav-color': '#404040',
        '--bg-footer-color': '#404040',
        '--text-color': '#F0F0F0',
        '--border-color': '#F0F0F0',
        '--box-shadow-color': '#f0f2f4',
        '--wish-color': '#E498A5',
        '--compare-color': '#7CB9E8',
        '--box-color':  '#8FBC8F',
        '--bg-error-message-color': '#F08080',
        '--error-message-color': '#FFFFFF',
        '--bg-success-message-color': '#90ee90',
        '--success-message-color': '#FFFFFF',
    }
}


class ThemeManager {
    constructor(options) {
        this.themeElem = document.querySelector(options.themeSelector);
        this.themes = options.themes;
        this.themesKeys = Object.keys(options.themes);
        this.defaultTheme = options.default;
        this.docStyle = document.documentElement.style;

        this.set();
    }
    getDefaultThemeIfNotExist(theme) {
        if (theme == null || theme == undefined || !this.themesKeys.includes(theme)) { 
            console.log('ERROR: Theme with this key doesn\'t exist. Set default theme.')
            return this.defaultTheme;
        }
        return theme;
    }
    set(theme=this.themeElem.dataset.theme) {
        theme = this.getDefaultThemeIfNotExist(theme);
        Object.entries(this.themes[theme]).forEach(([key, value]) => {
            this.docStyle.setProperty(key, value);
        });
    }
    next(theme) {
        /* If theme key is null - get next obj from themes obj */
        let currentThemeIndex = this.themesKeys.indexOf(theme);
        const nextIndex = (currentThemeIndex + 1) % this.themesKeys.length;
        return this.themesKeys[nextIndex];
    }
    change(theme=null) {
        const currentTheme = this.getDefaultThemeIfNotExist(this.themeElem.dataset.theme);
        if (currentTheme == theme) { return; }
        const newTheme = (theme == null)? this.next(currentTheme) : theme;
        this.set(newTheme);
        this.themeElem.setAttribute('data-theme', newTheme);
    }
}

const theme = new ThemeManager({
    themeSelector: setups.themeSelector, 
    themes: themes,
    default: setups.defaultTheme,
})