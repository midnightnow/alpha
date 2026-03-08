// Mocking performance
global.performance = {
    now: jest.fn(() => Date.now())
};

// Mocking requestAnimationFrame
global.requestAnimationFrame = jest.fn(callback => setTimeout(callback, 0));

// Mocking devicePixelRatio
global.devicePixelRatio = 1;

// Mocking Image
global.Image = class {
    constructor() {
        setTimeout(() => {
            if (this.onload) this.onload();
        }, 0);
    }
};
