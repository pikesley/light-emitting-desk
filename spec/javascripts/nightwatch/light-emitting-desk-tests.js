const timeout = 10

module.exports = {
    'Test setting mode': function (browser) {
        browser
            .url('http://light-emitting-desk-server:5050')
            .waitForElementVisible('body', timeout)

            .click('#mode-modal-toggle')

            .click('#sweep-select')
            .assert.cssClassPresent('#sweep-select', 'active')
            .assert.not.cssClassPresent('#sector-diverge-select', 'active')
            .assert.not.cssClassPresent('#converge-select', 'active')
            .assert.not.cssClassPresent('#spot-fill-select', 'active')
            .assert.not.cssClassPresent('#direct-switch-select', 'active')

            .click('#spot-fill-select')
            .assert.cssClassPresent('#spot-fill-select', 'active')
            .assert.not.cssClassPresent('#sector-diverge-select', 'active')
            .assert.not.cssClassPresent('#converge-select', 'active')
            .assert.not.cssClassPresent('#sweep-select', 'active')
            .assert.not.cssClassPresent('#direct-switch-select', 'active')

            .end();
    }
}
