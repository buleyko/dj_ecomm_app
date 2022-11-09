function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

class Logger {
    constructor(options) {
        this.infoMsgPrefix = options.infPref;
        this.errorMsgPrefix = options.errPref;
        this.off = options.off;
    }
    info(msg='') {
        if (!this.off) {
            console.log(`${this.infoMsgPrefix}: ${this.name}: ${msg}`);
        }
    }
    error(msg='') {
        if (!this.off) {
            console.log(`${this.errorMsgPrefix}: ${this.name}: ${msg}`);
        }
    }
}

const logger = new Logger({
    infPref: 'INFO',
    errPref: 'ERROR',
    off: false,
})

const isExist = (obj) => {
    return (obj != null && obj !== undefined || (Array.isArray(obj) && obj.length != 0))
}

const parseIntOrZero = (val) => {
    const parsed = parseInt(val);
    return (isNaN(parsed))? 0 : parsed; 
}

const inputDefault = (defVal) => {
    return function() {
        event.target.value = (event.target.value.length == 0)? defVal : event.target.value;
    };
};
const inputDefaultOne = inputDefault(1);

const onlyOneToNine = (evt) => {
    var ASCIICode = (evt.which) ? evt.which : evt.keyCode
    if (ASCIICode > 31 && (ASCIICode < 49 || ASCIICode > 57)) {
        return false;
    }
    return true;
} // <input type="text" onkeypress="return onlyOneToNine(event);">

const getBySelector = (selector, single=true) => {
    let res = null;
    if (single) {
        try {
            res = document.querySelector(selector);
        } catch(e) {
            if (e instanceof SyntaxError) {
                logger.info.call(this, `selector syntax ${selector}`);
            } else {
                logger.info.call(this, `querySelector by:${selector}`);
            }
        }
        if (res == null) {
            logger.info.call(this, `element(s) with selector ${selector} undefined`); 
        }
        return res;
    } else {
        try {
            res = document.querySelectorAll(selector);
        } catch(e) {
            if (e instanceof SyntaxError) {
                logger.info.call(this, `selector syntax ${selector}`);
            } else {
                logger.info.call(this, `querySelectorAll by:${selector}`);
            }
        }
        if (res.length == 0) {
            logger.info.call(this, `element(s) with selector ${selector} undefined`);
            return [];
        }
        return [...res];
    }
}

const getInnerHtml = (selector) => {
    let res = getBySelector(selector);
    if (isExist(res)) { 
        return res.innerHTML;
    }
}
const setInnerHtml = (selector, innerData) => {
    let res = getBySelector(selector);
    if (isExist(res)) { 
        res.innerHTML = innerData;
    }
}

Array.prototype.findElementIndex = function(el) {
    const index = this.indexOf(el);
    return (index != -1) ? index : null;
}

Element.prototype.hiddenParentByСondition = function(condition) {
    if (condition) {
        if (this.parentElement.classList.contains('hidden')) {
            this.parentElement.classList.remove('hidden');
        }
    } else {
        if (!this.parentElement.classList.contains('hidden')) {
            this.parentElement.classList.add('hidden');
        }
    }
}

class FetchDataException extends Error {
    constructor(message, options=null) {
        super(message, options);
    }
}

async function fetchAsync(method, url, data) {

    const requestOptions = {
        method: method,
        headers: { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data)
    };
    try {
        const response = await fetch(url, requestOptions);
        const res = await response.json();
        return res;
    } catch (e) {
        throw new FetchDataException(`ERROR: fetch data by URL: ${url}: ${e}`);
    }
}


class CssClassManager {
    
    add(selector, className, single=true) {
        let res = getBySelector(selector, single);
        if (isExist(res)) { 
            if (Array.isArray(res)) {
                res.forEach(el => {
                    if(!el.classList.contains(className)) {
                        el.classList.add(className)
                    }
                })
            } else {
                if(!res.classList.contains(className)) {
                    res.classList.add(className)
                }
            }
        }
    }
    remove(selector, className, single=true) {
        let res = getBySelector(selector, single);
        if (isExist(res)) { 
            if (Array.isArray(res)) {
                res.forEach(el => {
                    if(el.classList.contains(className)) {
                        el.classList.remove(className)
                    }
                })
            } else {
                if(res.classList.contains(className)) {
                    res.classList.remove(className)
                }
            }
        }
    }
    toggle(selector, className, single=true) {
        let res = getBySelector(selector, single);
        if (isExist(res)) { 
            if (Array.isArray(res)) {
                res.forEach(el => {
                    el.classList.toggle(className)
                })
            } else {
                res.classList.toggle(className)
            }
        }
    }
    changeOrAddAt(selector, from, to, single=true) {
        let res = getBySelector(selector, single);
        if (isExist(res)) { 
            if (Array.isArray(res)) {
                res.forEach(el => {
                    if(!el.classList.contains(from)) {
                        el.classList.add(from)
                    } else {
                        el.classList.toggle(from)
                        el.classList.toggle(to)
                    }
                })
            } else {
                if(!res.classList.contains(from)) {
                    res.classList.add(from)
                } else {
                    res.classList.toggle(from)
                    res.classList.toggle(to)
                }
            }
        }
        
    }
    changeByPref(classes, single=true) {
        /* Change each class that start with prefix(until '-'), remove old valua and add new */
        classes.split(' ').forEach(className => {
            const namePref = className.split('-')[0];
            let res = getBySelector(`[class*="${namePref}"]`, single);
            if (isExist(res)) { 
                if (Array.isArray(res)) {
                    res.forEach(el => {
                        el.classList.forEach(name => {
                            if(name.startsWith(namePref) && name != className) { 
                                el.classList.toggle(name)
                                el.classList.toggle(className)
                            }
                        })
                    })
                } else {
                    res.classList.forEach(name => {
                        if(name.startsWith(namePref) && name != className) {
                            res.classList.toggle(name)
                            res.classList.toggle(className)
                        }
                    })
                }
            }
            
        })
    }
}

const cssClass = new CssClassManager()

const settingsObj = {
    theme: setups.defaultTheme,
    content_layout: setups.defaultContentLayout,
}

const settings = new Proxy(settingsObj, {
    get(target, prop) {
        return target[prop];
    },
    set(target, prop, value) {
        if (prop in target) {
            target[prop] = value;

            const data = {
                settings: [
                    { key: prop, val: value },
                ]
            }
            fetchAsync('POST', '/options/', data)
                .then(res => {
                    logger.info.call(this, 'Theme changed');
                    if (prop == 'theme') {
                        theme.change(value);
                    }
                    if (prop == 'content_layout') {
                        cssClass.changeByPref(value);
                    }
                });

        } else { 
            throw new Error(`No ${prop} in settings object`);
        }
    },
    has(target, prop) {
        return Object.keys(target).includes(prop);
    },
})


class CartMamager {
    constructor(options) {
        this.addUrl = options.addUrl;
        this.updateUrl = options.updateUrl;
        this.deleteUrl = options.deleteUrl;
        this.deliveryUpdateUrl = options.deliveryUpdateUrl;
        this.cartCountSelector = document.querySelector(options.cartCountSelector);
        this.cartTotalSelector = document.querySelector(options.cartTotalSelector);
        this.boxElem = document.querySelector(options.boxSelector);
        this.boxCountElem = document.querySelector(options.boxCountSelector);
        this.boxCount = parseIntOrZero(getInnerHtml(options.boxCountSelector));
        this.deliveryElem = document.querySelector(options.deliverySelector);
        this.quantityKeySelector = options.quantityKeySelector;
        this.totalPriceProdKeySelector = options.totalPriceProdKeySelector;
        this.prodKeySelector = options.prodKeySelector;
        this.boxes = [];
        this.setup();
    }
    setup() {
        this.boxElem.addEventListener('animationend', (ev) => {
            if (ev.animationName == "box_scale") {
                this.boxElem.classList.remove('box_scale');
            }
        });
    }
    getProdId(el) {
        if (el.hasAttribute('data-prodid') && (parseIntOrZero(el.dataset.prodid) != 0)) {
            return el.dataset.prodid;
        }
        return null;
    }
    getProdCounter(el) {
        let prodId = this.getProdId(el);
        return document.querySelector(`#${this.quantityKeySelector}${prodId}`);
    }
    setPordQuantity(el, qty) {
        el.dataset.quantity = qty;
    }
    getPordQuantity(el) {
        return parseIntOrZero(el.dataset.quantity);
    }
    setProductBtnBgColor(el) {
        let qty = this.getPordQuantity(el);
        if (qty > 0) {
            el.classList.add('prod-selected');
        }
    }
    setBoxTotalCount(res) {
        let count = res['quantity'];
        this.boxCountElem.innerHTML = (count==0)? '' : count;
        this.boxCountElem.hiddenParentByСondition(count > 0);
    }
    setCartQuantity(res) {
        let qty = res['quantity'];
        this.cartCountSelector.innerHTML = (qty==0)? '0' : qty;
    }
    setCartTotal(res) {
        let price = res['total_price'];
        this.cartTotalSelector.innerHTML = (price==0)? '0' : price;
    }
    setCartProdTotal(res) {
        let prod_total_price = res['prod_total_price'];
        let prodId = res['id'];
        let prodTotal = document.querySelector(`#${this.totalPriceProdKeySelector}${prodId}`);
        prodTotal.innerHTML = (prod_total_price==0)? '0' : prod_total_price;
    }
    setBoxElemAnimation(res) {
        let count = res['quantity'];
        if(count > 0) {
            if (!this.boxElem.classList.contains('selected')) {
                this.boxElem.classList.add('selected');
                this.boxElem.classList.add('box_scale');
            } else {
                this.boxElem.classList.add('box_scale');
            }
        }
        if(count == 0 && this.boxElem.classList.contains('selected')) {
            this.boxElem.classList.remove('selected');
            this.boxElem.classList.add('box_scale');
        }
    }
    setProdBtnCount(el) {
        let qty = this.getPordQuantity(el);
        let itemProdCountElem = el.querySelector('small');
        if (isExist(itemProdCountElem)) {
            itemProdCountElem.innerHTML = (qty==0)? '' : qty;
            itemProdCountElem.hiddenParentByСondition(qty > 0);
        }
    }
    selectProduct(el, res) {
        this.setPordQuantity(el, 1);
        this.setProdBtnCount(el);
        this.setProductBtnBgColor(el);
        this.setBoxTotalCount(res);
        this.setBoxElemAnimation(res);
    }
    changeProdQuantityInCart(el, res) {
        this.setPordQuantity(el, res['prod_quantity']);
        this.setBoxTotalCount(res);
        this.setCartQuantity(res);
        this.setCartTotal(res);
        this.setCartProdTotal(res);
        this.setBoxElemAnimation(res);
        el.innerHTML = res['prod_quantity'];
    }
    deleteProdFromCart(res) {
        let prodId = res['id'];
        this.setBoxTotalCount(res);
        this.setCartQuantity(res);
        this.setCartTotal(res);
        this.setBoxElemAnimation(res);
        let prodDel = document.querySelector(`#${this.prodKeySelector}${prodId}`);
        prodDel.remove();
    }
    selectDelivery(res) {
        this.deliveryElem.innerHTML = res['delivery_price']
        this.setCartTotal(res);
    }
    select() {
        const el = event.target;
        let prodId = this.getProdId(el);
        let prodQty = this.getPordQuantity(el)
        if (prodId !== null) {
            if (prodQty == 0) {
                let prodQty = 1;
                this.add(el, prodId, prodQty);
            }
        }
    }
    increment() {
        const el = this.getProdCounter(event.target);
        let prodId = this.getProdId(el);
        let prodQty = this.getPordQuantity(el) + 1;
        if (prodId !== null) {
            this.update(el, prodId, prodQty);
        }
    }
    decrement() {
        const el = this.getProdCounter(event.target);
        let prodId = this.getProdId(el);
        let prodQty = this.getPordQuantity(el) - 1;
        if (prodId !== null && prodQty > 0) {
            this.update(el, prodId, prodQty);
        }
    }
    remove() {
        const el = event.target;
        let prodId = this.getProdId(el);
        if (prodId !== null) {
            this.delete(el, prodId);
        }
    }
    addDelivery() {
        const el = event.target;
        let deliveryId = parseIntOrZero(el.value);
        // if (deliveryId !== 0) {
        this.delivery(el, deliveryId);
        // }
    }
    add(el, prodId, prodQty) {
        const data = {
            id: prodId,
            quantity: prodQty,
        }
        fetchAsync('POST', this.addUrl, data)
            .then(res => {
                this.selectProduct(el, res);
            })
    }
    update(el, prodId, prodQty) {
        const data = {
            id: prodId,
            quantity: prodQty,
        }
        fetchAsync('POST', this.updateUrl, data)
            .then(res => {
                this.changeProdQuantityInCart(el, res);
            })
    }
    delete(el, prodId) {
        const data = {
            id: prodId,
        }
        fetchAsync('POST', this.deleteUrl, data)
            .then(res => {
                this.deleteProdFromCart(res);
            })
    }
    delivery(el, deliveryId) {
        const data = {
            id: deliveryId,
        }
        fetchAsync('POST', this.deliveryUpdateUrl, data)
            .then(res => {
                this.selectDelivery(res);
            })
    }
}

class WishMamager {
    constructor(options) {
        this.addUrl = options.addUrl;
        this.deleteUrl = options.deleteUrl;
        this.wishElem = document.querySelector(options.wishSelector);
        this.wishCountElem = document.querySelector(options.wishCountSelector);
        this.wishCount = parseIntOrZero(getInnerHtml(options.wishCountSelector));
        this.wishes = [];
        this.setup();
    }
    setup() {
        this.wishElem.addEventListener('animationend', (ev) => {
            if (ev.animationName == "wished_scale") {
                this.wishElem.classList.remove('wished_scale');
            }
        });
    }
    getProdId(el) {
        if (el.hasAttribute('data-prodid') && (parseIntOrZero(el.dataset.prodid) != 0)) {
            return el.dataset.prodid;
        }
        return null;
    }
    setWishCount(count) {
        this.wishCountElem.innerHTML = (count == 0 )? '' : count;
        this.wishCountElem.hiddenParentByСondition(count > 0);
    } 
    setWishElemColor(count) {
        if(count > 0) {
            if (!this.wishElem.classList.contains('wished')) {
                this.wishElem.classList.add('wished');
                this.wishElem.classList.add('wished_scale');
            } else {
                this.wishElem.classList.add('wished_scale');
            }
        }
        if(count == 0 && this.wishElem.classList.contains('wished')) {
            this.wishElem.classList.remove('wished');
            this.wishElem.classList.add('wished_scale');
        }
    }
    selectProduct(el, res) {
        let itemSvgElem = el.querySelector('svg');
        itemSvgElem.classList.remove('unwish');
        itemSvgElem.classList.add('wish');
        this.setWishCount(res['quantity']);
        this.setWishElemColor(res['quantity']);
    }
    deselectProduct(el, res) {
        let itemSvgElem = el.querySelector('svg');
        itemSvgElem.classList.remove('wished');
        itemSvgElem.classList.remove('wish');
        itemSvgElem.classList.add('unwish');
        this.setWishCount(res['quantity']);
        this.setWishElemColor(res['quantity']);
    }
    increment(el) {
        let prodId = this.getProdId(el);
        if (prodId !== null) {
            this.add(el, prodId);
        }
    }
    decrement(el) {
        let prodId = this.getProdId(el);
        if (prodId !== null) {
            this.delete(el, prodId);
        }
    }
    add(el, prodId) {
        const data = {
            id: prodId,
        }
        fetchAsync('POST', this.addUrl, data)
            .then(res => {
                this.selectProduct(el, res);
            })
    }
    delete(el, prodId) {
        const data = {
            id: prodId,
        }
        fetchAsync('POST', this.deleteUrl, data)
            .then(res => {
                this.deselectProduct(el, res);
            })
    }
    setWishBy(el) {
        let itemSvgElem = el.querySelector('svg');
        if(!itemSvgElem.classList.contains('wish') && !itemSvgElem.classList.contains('wished')) {
            this.increment(el);
        } else {
            this.decrement(el);
        }
    }
    toggle() {
        const el = event.target;
        this.setWishBy(el);
    }
}
class CompareMamager {
    constructor(options) {
        this.addUrl = options.addUrl;
        this.deleteUrl = options.deleteUrl;
        this.compareElem = document.querySelector(options.compareSelector);
        this.compareCountElem = document.querySelector(options.compareCountSelector);
        this.compareCount = parseIntOrZero(getInnerHtml(options.compareCountSelector));
        this.compares = [];
        this.setup();
    }
    setup() {
        this.compareElem.addEventListener('animationend', (ev) => {
            if (ev.animationName == "compared_scale") {
                this.compareElem.classList.remove('compared_scale');
            }
        });
    }
    getProdId(el) {
        if (el.hasAttribute('data-prodid') && (parseIntOrZero(el.dataset.prodid) != 0)) {
            return el.dataset.prodid;
        }
        return null;
    }
    setCompareCount(count) {
        this.compareCountElem.innerHTML = (count == 0)? '' : count;
        this.compareCountElem.hiddenParentByСondition(count > 0);
    }
    setCompareElemColor(count) {
        if(count > 0) {
            if (!this.compareElem.classList.contains('compared')) {
                this.compareElem.classList.add('compared');
                this.compareElem.classList.add('compared_scale');
            } else {
                this.compareElem.classList.add('compared_scale');
            }
        }
        if(count == 0 && this.compareElem.classList.contains('compared')) {
            this.compareElem.classList.remove('compared');
            this.compareElem.classList.add('compared_scale');
        }
    }
    selectProduct(el, res) {
        let itemSvgElem = el.querySelector('svg');
        itemSvgElem.classList.remove('uncompare');
        itemSvgElem.classList.add('compare');
        this.setCompareCount(res['quantity']);
        this.setCompareElemColor(res['quantity']);
    }
    deselectProduct(el, res) {
        let itemSvgElem = el.querySelector('svg');
        itemSvgElem.classList.remove('compared');
        itemSvgElem.classList.remove('compare');
        itemSvgElem.classList.add('uncompare');
        this.setCompareCount(res['quantity']);
        this.setCompareElemColor(res['quantity']);
    }
    increment(el) {
        let prodId = this.getProdId(el);
        if (prodId !== null) {
            this.add(el, prodId);
        }
    }
    decrement(el) {
        let prodId = this.getProdId(el);
        if (prodId !== null) {
            this.delete(el, prodId);
        }
    }
    add(el, prodId) {
        const data = {
            id: prodId,
        }
        fetchAsync('POST', this.addUrl, data)
            .then(res => {
                this.selectProduct(el, res);
            })
    }
    delete(el, prodId) {
        const data = {
            id: prodId,
        }
        fetchAsync('POST', this.deleteUrl, data)
            .then(res => {
                this.deselectProduct(el, res);
            })
    }
    setCompareBy(el) {
        let itemSvgElem = el.querySelector('svg');
        if(!itemSvgElem.classList.contains('compare') && !itemSvgElem.classList.contains('compared')) {
            this.increment(el);
        } else {
            this.decrement(el);
        }
    }
    toggle() {
        const el = event.target;
        this.setCompareBy(el);
    }
}

class InputWatcher {
    constructor(options) {
        this.obserEvent = options.obserEvent;
        this.obserElements = document.querySelectorAll(options.obserElementsSelector);
        this.handler = options.handler;
        this.setup();
    }
    setup() {
        this.obserElements.forEach((el) => {
            el.addEventListener(this.obserEvent, this.checkEvent);
        });
    }
    checkEvent = () => {
        let tmpCounter = 0;
        this.obserElements.forEach((el) => {
            let value = el.value.trim();
            if (value != '') {
                tmpCounter += 1;
            }
        });
        this.handler(this.obserElements.length == tmpCounter)
    }   
}

class FilterWatcher {
    constructor(options) {
        this.obserEvent = options.obserEvent;
        this.obserElements = document.querySelectorAll(options.obserElementsSelector);
        this.applySelector = document.querySelector(options.applySelector);
        this.filters = [];
        this.setup();
    }
    setup() {
        this.obserElements.forEach((el) => {
            el.addEventListener(this.obserEvent, this.checkEvent);
        });
    }
    checkEvent = () => {
        this.obserElements.forEach((el) => {
            const filter = this.getFilter(el);
            if (el.checked) {
                this.filters.push(filter);
            } else {
                this.filters = this.filters.filter((v)=>v!=filter);
            }
        });
        if (this.filters.length > 0) {
            this.applySelector.classList.remove('hidden');
        } else {
            this.applySelector.classList.add('hidden');
        }
    }
    getFilter(el) {
        return `${el.dataset.attr}=${el.dataset.val}`
    }
    apply(clear=false) {
        if (!clear && this.filters.length > 0) {
            const paramsStr = this.filters.join('&');
            let url = window.location.href.split('?')[0];
            window.location.href = url + '?' + paramsStr
        } else if (clear || this.filters.length == 0) {
            let url = window.location.href.split('?')[0];
            window.location.href = url
        } else {
            let url = window.location.href.split('?')[0];
            window.location.href = url
        }
    }
}

class Search {
    constructor(options) {
        this.searchInputElement = document.querySelector(options.searchInputElementSelector);
    }
    getSearchParam() {
        return this.searchInputElement.value.trim();
    }
    apply() {
        const searchParamStr = this.getSearchParam()
        let url = window.location.href.split('?');
        if (url.length > 1) {
            url = window.location.href + '&search-name=' + searchParamStr
        } else {
            url = window.location.href + '?search-name=' + searchParamStr 
        }
        window.location.href = url
    }
}

const search = new Search({
    searchInputElementSelector: '#search-name',
})

const cart = new CartMamager({
    addUrl: '/cart/add/',
    updateUrl: '/cart/update/',
    deleteUrl: '/cart/delete/',
    deliveryUpdateUrl: '/checkout/update-delivery/',
    boxSelector: '#box-fix svg',
    boxCountSelector: '#cart-counter span',
    cartCountSelector: '#cart-quantity',
    cartTotalSelector: '#cart-total',
    deliverySelector: '#cart-delivery',
    totalPriceProdKeySelector: 'prod-total-',
    quantityKeySelector: 'prod-quantity-',
    prodKeySelector: 'cart-prod-',
})
const wish = new WishMamager({
    addUrl: '/wish/add/',
    deleteUrl: '/wish/delete/',
    wishSelector: '#wish-total svg',
    wishCountSelector: '#wish-counter span',
})
const compare = new CompareMamager({
    addUrl: '/comparison/add/',
    deleteUrl: '/comparison/delete/',
    compareSelector: '#compare-total svg',
    compareCountSelector: '#compare-counter span',
})

/* -------------------- Storage ----------------- */
class LocalStorageManager {
    set(key, value) {
        localStorage.setItem(key, value);
    }
    get(key) {
        return localStorage.getItem(key);
    }
    delete(key) {
        localStorage.removeItem(key);
    }
    clear() {
        localStorage.clear();
    }
}
const storage = new LocalStorageManager()

/* ------------------- Observable --------------- */
// class Observable {
//     constructor() {
//         this.observers = [];
//     }
//     subscribe(func) {
//         this.observers.push(func);
//     }
//     unsubscribe(func) {
//         this.observers = this.observers.filter(subscriber => subscriber !== func);
//     }
//     signal(data) {
//         this.observers.forEach(observer => observer(data));
//     }
// }
// const wishObs = new Observable();
// const compareObs = new Observable();
// const cartObs = new Observable();
/* --------------------------------------- */

// class ElementWatcher {
//     constructor(options) {
//         this.obserEvent = options.obserEvent;
//         this.obserElements = document.querySelectorAll(options.obserElementsSelector);
//         this.eventler = options.eventler;
//         this.handler = options.handler;
//         this.setup();
//     }
//     setup() {
//         this.obserElements.forEach((el) => {
//             el.addEventListener(this.obserEvent, this.checkEvent);
//         });
//     }
//     checkEvent = () => {
//         this.eventler();
//         this.handler();
//     }   
// }
